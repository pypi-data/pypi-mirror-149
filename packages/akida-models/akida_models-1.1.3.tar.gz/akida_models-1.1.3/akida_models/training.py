#!/usr/bin/env python
# ******************************************************************************
# Copyright 2021 Brainchip Holdings Ltd.
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
Common utility methods used by the training scripts.
"""

import argparse
import numpy as np

from keras.preprocessing.image import DirectoryIterator
from keras.optimizer_v2.adam import Adam
from keras.layers import Activation


def compile_model(model,
                  learning_rate=1e-3,
                  loss='categorical_crossentropy',
                  metrics=None):
    """ Compiles the model using Adam optimizer.

    Args:
        model (keras.Model): the model to compile
        learning_rate (float, optional): the learning rate. Defaults to 1e-3.
        loss (str or function, optional): the loss function. Defaults to
            'categorical_crossentropy'.
        metrics (list, optional): list of metrics to be evaluated during
            training and testing. Defaults to None.
    """
    if metrics is None:
        metrics = ['accuracy']

    model.compile(optimizer=Adam(learning_rate=learning_rate),
                  loss=loss,
                  metrics=metrics)


def freeze_model_before(model, freeze_before):
    """ Freezes the model before the given layer name.

    Args:
        model (keras.Model): the model to freeze
        freeze_before (str): name of the layer from which the model will not be
            frozen

    Raises:
        ValueError: if the provided layer name was not found in the model
    """
    if freeze_before is not None:
        trainable = False
        for layer in model.layers:
            if layer.name == freeze_before:
                trainable = True
            layer.trainable = trainable
        if not trainable:
            raise ValueError(f"No such layer {freeze_before} in model.")


def evaluate_model(model,
                   x,
                   y=None,
                   batch_size=None,
                   steps=None,
                   print_history=False):
    """ Evaluates model performances.

    Args:
        model (keras.Model): the model to evaluate
        x (tf.Dataset, np.array or generator): evaluation input data
        y (tf.Dataset, np.array or generator, optional): evaluation target
            data. Defaults to None.
        batch_size (int, optional): the batch size. Defaults to None.
        steps (int, optional): total number of steps before declaring the
            evaluation round finished. Defaults to None.
        print_history (bool, optional): either to print all history or just
            accuracy. Defaults to False.
    """
    history = model.evaluate(x=x,
                             y=y,
                             batch_size=batch_size,
                             steps=steps,
                             verbose=0)

    if print_history:
        print('Validation history: ', history)
    else:
        print('Validation accuracy: ', history[1])


def evaluate_akida_model(model, x, activation):
    """ Evaluates Akida model and return predictions and labels to compute
    accuracy.

    Args:
        model (akida.Model): the model to evaluate
        x (tf.Dataset, np.array or generator): evaluation input data
        activation (str): activation function to apply to potentials

    Returns:
        np.array, np.array: predictions and labels
    """

    # Initialize to None to allow different shapes depending on the caller
    labels = None
    pots = None

    # Datasets created as ImageDataGenerator will be looped over indefinitely,
    # they thus need a special treatment
    steps = None
    if isinstance(x, DirectoryIterator):
        steps = np.math.ceil(x.samples / x.batch_size)

    for batch, label_batch in x:
        if not isinstance(batch, np.ndarray):
            batch = batch.numpy()

        pots_batch = model.predict(batch.astype('uint8'))

        if labels is None:
            labels = label_batch
            pots = pots_batch.squeeze(axis=(1, 2))
        else:
            labels = np.concatenate((labels, label_batch))
            pots = np.concatenate((pots, pots_batch.squeeze(axis=(1, 2))))

        # End the for loop if the number of batches has reached the number of
        # steps
        if steps is not None and x.total_batches_seen == steps:
            break

    return Activation(activation)(pots), labels


def get_training_parser(batch_size,
                        tune=False,
                        freeze_before=False,
                        global_batch_size=True,
                        global_parser=None):
    """ Instantiates a base arguments parser for training scripts.

    The returned parser comes with train, tune and eval actions as subparsers
    (with default parameters) for which one can add arguments if required.

    Args:
        batch_size (int): batch size default value
        tune (bool, optional): either to add a tune action or not. Default to
            False.
        freeze_before (bool, optional): either to add a "--freeze_before"
            parameter in train and tune actions or not. Default to False.
        global_batch_size (bool, optional): either to add batch size as a
            global parser parameter or for train/tune actions only. Default to
            True.
        global_parser (argparse.ArgumentParser, optional): global parser with
            custom parameters. Defaults to None.

    Returns:
        argparse.ArgumentParser, argparse.ArgumentParser,
        argparse.ArgumentParser, argparse.ArgumentParser,
        argparse._SubParsersAction: main parser and train, tune and eval actions
            subparsers and the subparser object.
    """

    # Define a strictly positive int type for parameters
    def positive_int(value):
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(
                "%s is an invalid value, must be >0." % value)
        return ivalue

    parser = argparse.ArgumentParser()

    # Base arguments
    if global_parser is None:
        global_parser = argparse.ArgumentParser(add_help=False)

    global_parser.add_argument("-m",
                               "--model",
                               type=str,
                               required=True,
                               help="Model to load")
    if global_batch_size:
        global_parser.add_argument("-b",
                                   "--batch_size",
                                   type=positive_int,
                                   default=batch_size,
                                   help="The batch size")

    # Create an action subparser
    subparsers = parser.add_subparsers(help="Desired action to perform",
                                       dest="action")

    # Create parent subparser for arguments shared between train and tune
    # actions
    parent_parser = argparse.ArgumentParser(add_help=False,
                                            parents=[global_parser])
    parent_parser.add_argument("-s",
                               "--savemodel",
                               type=str,
                               default=None,
                               help="Save model with the specified name")
    parent_parser.add_argument("-e",
                               "--epochs",
                               type=positive_int,
                               required=True,
                               help="The number of training epochs")
    if not global_batch_size:
        parent_parser.add_argument("-b",
                                   "--batch_size",
                                   type=positive_int,
                                   default=batch_size,
                                   help="The batch size")
    if freeze_before:
        parent_parser.add_argument(
            "-fb",
            "--freeze_before",
            type=str,
            default=None,
            help="Freeze the layers of the model before this \
                                layer")

    # Subparsers based on parent
    train_parser = subparsers.add_parser("train",
                                         parents=[parent_parser],
                                         help="Train a Keras model")
    tune_parser = None
    if tune:
        tune_parser = subparsers.add_parser("tune",
                                            parents=[parent_parser],
                                            help="Tune a Keras model")

    # Other subparsers
    eval_parser = subparsers.add_parser("eval",
                                        help="Evaluate a model",
                                        parents=[global_parser])

    eval_parser.add_argument("-ak",
                             "--akida",
                             action='store_true',
                             help="Converts to an Akida model and evaluate")

    return parser, train_parser, tune_parser, eval_parser, subparsers
