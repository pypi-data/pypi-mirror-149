#!/usr/bin/env python
# coding: utf-8
# ******************************************************************************
# Copyright 2020 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""
Training script for ImageNet models.
"""

import os
import time
import argparse

import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds

from keras.callbacks import (TensorBoard, ModelCheckpoint,
                             LearningRateScheduler)
from keras import Sequential
from keras.optimizer_v2.gradient_descent import SGD
from keras.layers import Input
from keras.models import clone_model

import akida
from cnn2snn import load_quantized_model, convert

from .preprocessing import preprocess_image
from ..training import get_training_parser, freeze_model_before


def get_imagenet_dataset(data_path, training, image_size, batch_size):
    """ Loads ImageNet 2012 dataset and builds a tf.dataset out of it.

    Args:
        data_path (str): path to the folder containing ImageNet tar files
        training (bool): True to retrieve training data, False for validation
        image_size (int): desired image size
        batch_size (int): the batch size

    Returns:
        tf.dataset, int: the requested dataset (train or validation) and the
        corresponding steps
    """
    # Build the dataset
    write_dir = os.path.join(data_path, 'tfds')

    download_and_prepare_kwargs = {
        'download_dir': os.path.join(write_dir, 'downloaded'),
        'download_config': tfds.download.DownloadConfig(manual_dir=data_path)
    }

    split = 'train' if training else 'validation'

    dataset, infos = tfds.load(
        'imagenet2012',
        data_dir=os.path.join(write_dir, 'data'),
        split=split,
        shuffle_files=training,
        download=True,
        as_supervised=True,
        download_and_prepare_kwargs=download_and_prepare_kwargs,
        with_info=True)

    if training:
        dataset = dataset.shuffle(10000, reshuffle_each_iteration=True).repeat()

    dataset = dataset.map(lambda image, label: (preprocess_image(
        image, image_size, training), label))

    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(1)

    # The following will silence a Tensorflow warning on auto shard policy
    options = tf.data.Options()
    options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.DATA
    dataset = dataset.with_options(options)

    return dataset, infos.splits[split].num_examples / batch_size


def compile_model(model):
    """ Compiles the model.

    Args:
        model (keras.Model): the model to compile
    """
    model.compile(optimizer=SGD(momentum=0.9, nesterov=False),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy', 'sparse_top_k_categorical_accuracy'])


def evaluate(model, val_dataset, batch_size, num_samples, val_steps):
    """ Evaluates model performances.

    Args:
        model (keras.Model or akida.Model): the model to compile evaluate
        val_dataset (tf.dataset): validation dataset
        batch_size (int): the batch size
        num_samples (int): number of samples to use for Akida
        val_steps (int): validation steps
    """
    if isinstance(model, akida.Model):
        correct_preds = 0
        cur_samples = 0
        total_samples = val_steps * batch_size
        if num_samples <= 0:
            num_samples = total_samples
        else:
            num_samples = min(num_samples, total_samples)
        it = val_dataset.as_numpy_iterator()

        print(f"Processing {num_samples} samples.")
        if num_samples > batch_size:
            n_batches = num_samples // batch_size
            if n_batches > 5:
                log_samples = (n_batches // 5) * batch_size
            else:
                log_samples = batch_size
            print(f"Logging every {log_samples} samples.")
        else:
            log_samples = num_samples
        while cur_samples < num_samples:
            x, y = next(it)
            y_ak = model.predict_classes(x.astype(np.uint8))
            correct_preds += np.sum(y_ak == y.flatten())
            cur_samples += y_ak.shape[0]
            if cur_samples % log_samples == 0 and cur_samples < num_samples:
                # Log current accuracy
                accuracy = correct_preds / cur_samples
                print(f"Accuracy after {cur_samples}: {accuracy}")
        accuracy = correct_preds / cur_samples
        print(f"Accuracy after {cur_samples}: {accuracy}")
    else:
        history = model.evaluate(val_dataset, steps=val_steps)
        print(history)


def rescale(base_model, input_size):
    """ Rescales the model by changing its input size.

    Args:
        base_model (keras.Model): the model to rescale
        input_size (int): desired model input size

    Returns:
        keras.Model: the rescaled model
    """
    # Create the desired input
    input_shape = (input_size, input_size, base_model.input.shape[-1])
    new_input = Input(input_shape)

    # Workaround to force the input shape update that is not working for
    # functional models: the input_tensors parameter is ignored as described in
    # https://github.com/tensorflow/tensorflow/issues/40617.
    if not isinstance(base_model, Sequential):
        base_model.layers[0]._batch_input_shape = (None, input_size, input_size,
                                                   base_model.input.shape[-1])
        new_input = None

    # Clone the model and replace input layer
    clone = clone_model(base_model, input_tensors=new_input)
    clone.set_weights(base_model.get_weights())
    return clone


def create_log_dir(out_dir):
    """ Creates a directory to store Tensorflow logs.

    Args:
        out_dir (str): parent directory of the folder to create

    Returns:
        str: full path of the created directory
    """
    base_name = 'imagenet_cnn' + '_' + time.strftime('%Y_%m_%d.%H_%M_%S',
                                                     time.localtime())
    log_dir = os.path.join(out_dir, base_name)

    print('saving tensorboard and checkpoint information to', log_dir)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print('directory', log_dir, 'created ...')
    else:
        print('directory', log_dir, 'already exists ...')
    return log_dir


def train(model,
          train_dataset,
          train_steps,
          val_dataset,
          val_steps,
          out_dir,
          num_epochs,
          tune=False,
          learning_rate=1e-1,
          initial_epoch=0):
    """ Trains the model

    Args:
        model (keras.Model): the model to train
        train_dataset (tf.dataset): training dataset
        train_steps (int): train steps
        val_dataset (tf.dataset): validation dataset
        val_steps (int): validation steps
        out_dir (str): parent directory for logs folder
        num_epochs (int): the number of epochs
        tune (bool, optional): enable tuning (lower learning rate). Defaults to
         False.
        learning_rate (float, optional): the learning rate. Defaults to 1e-1.
        initial_epoch (int, optional): epoch at which to start training.
         Defaults to 0.
    """
    # 1. Define training callbacks
    callbacks = []

    # 1.1 Learning rate scheduler
    LR_START = learning_rate
    LR_END = 1e-4
    # number of epochs you first keep the learning rate constant
    LR_EPOCH_CONSTANT = 10
    # Modify default values for fine-tuning
    if tune:
        LR_START = 1e-4
        LR_END = 1e-8
        LR_EPOCH_CONSTANT = 2

    if LR_EPOCH_CONSTANT >= num_epochs:
        lr_decay = LR_END / LR_START
    else:
        lr_decay = (LR_END / LR_START)**(1. / (num_epochs - LR_EPOCH_CONSTANT))

    # This function keeps the learning rate at LR_START for the first N epochs
    # and decreases it exponentially after that.
    def agg_lr_scheduler(epoch):
        if epoch < LR_EPOCH_CONSTANT:
            return LR_START
        return LR_START * lr_decay**(epoch - (LR_EPOCH_CONSTANT - 1))

    callbacks.append(LearningRateScheduler(agg_lr_scheduler))

    # 1.2 Model checkpoints (save best models after each epoch)
    log_dir = create_log_dir(out_dir)
    filepath = os.path.join(
        log_dir, 'weights_epoch_{epoch:02d}_val_acc_{val_accuracy:.2f}.h5')
    model_checkpoint = ModelCheckpoint(filepath=filepath,
                                       monitor='val_accuracy',
                                       verbose=1,
                                       save_best_only=True,
                                       mode='max')
    callbacks.append(model_checkpoint)

    # 1.3 Tensorboard logs
    file_writer = tf.summary.create_file_writer(log_dir + "/metrics")
    file_writer.set_as_default()
    tensorboard = TensorBoard(log_dir=log_dir,
                              histogram_freq=1,
                              update_freq='epoch',
                              write_graph=False,
                              profile_batch=0)
    callbacks.append(tensorboard)

    # 2. Train
    history = model.fit(train_dataset,
                        steps_per_epoch=train_steps,
                        epochs=num_epochs,
                        callbacks=callbacks,
                        validation_data=val_dataset,
                        validation_steps=val_steps,
                        initial_epoch=initial_epoch)
    print(history.history)


def main():
    """ Entry point for script and CLI usage.
    """
    global_parser = argparse.ArgumentParser(add_help=False)
    global_parser.add_argument(
        "-d",
        "--data_dir",
        type=str,
        default='/hdd/datasets/imagenet/',
        help="The directory containing the ImageNet data.")
    global_parser.add_argument("-o",
                               "--out_dir",
                               type=str,
                               default='./logs',
                               help="The output directory (logs, checkpoints).")

    parsers = get_training_parser(batch_size=128,
                                  freeze_before=True,
                                  tune=True,
                                  global_parser=global_parser)

    train_parser = parsers[1]
    train_parser.add_argument("-lr",
                              "--learning_rate",
                              type=float,
                              default=1e-1,
                              help="Learning rate start value.")
    train_parser.add_argument("-ie",
                              "--initial_epoch",
                              type=int,
                              default=0,
                              help="Epoch at which to start training.")

    tune_parser = parsers[2]
    tune_parser.add_argument("-ie",
                             "--initial_epoch",
                             type=int,
                             default=0,
                             help="Epoch at which to start training.")

    eval_parser = parsers[3]
    eval_parser.add_argument("-ns",
                             "--num_samples",
                             type=int,
                             default=-1,
                             help="Number of samples to use (for Akida)")

    subparsers = parsers[-1]
    rescale_parser = subparsers.add_parser("rescale",
                                           help="Rescale a model.",
                                           parents=[global_parser])
    rescale_parser.add_argument("-i",
                                "--input_size",
                                type=int,
                                required=True,
                                help="The square input image size")
    rescale_parser.add_argument("-s",
                                "--savemodel",
                                type=str,
                                default=None,
                                help="Save model with the specified name")

    args = parsers[0].parse_args()

    # Load the source model
    model = load_quantized_model(args.model)

    # Freeze the model
    if "freeze_before" in args:
        freeze_model_before(model, args.freeze_before)

    # Compile model
    compile_model(model)

    # Load validation data
    im_size = model.input_shape[1]
    val_ds, val_steps = get_imagenet_dataset(args.data_dir, False, im_size,
                                             args.batch_size)

    # Train model
    if args.action in ['train', 'tune']:
        # Load training data
        train_ds, train_steps = get_imagenet_dataset(args.data_dir, True,
                                                     im_size, args.batch_size)
        tune = args.action == 'tune'
        train(model,
              train_ds,
              train_steps,
              val_ds,
              val_steps,
              args.out_dir,
              args.epochs,
              tune=tune,
              learning_rate=args.learning_rate if not tune else 1e-1,
              initial_epoch=args.initial_epoch)

        # Save model in Keras format (h5)
        if args.savemodel:
            model.save(args.savemodel, include_optimizer=False)
            print(f"Trained model saved as {args.savemodel}")

    elif args.action == 'eval':
        # Evaluate model accuracy
        if args.akida:
            model = convert(model)
        evaluate(model, val_ds, args.batch_size, args.num_samples, val_steps)

    elif args.action == 'rescale':
        # Rescale model
        m = rescale(model, args.input_size)

        # Save model in Keras format (h5)
        if args.savemodel:
            m.save(args.savemodel, include_optimizer=False)
            print(f"Rescaled model saved as {args.savemodel}")


if __name__ == "__main__":
    main()
