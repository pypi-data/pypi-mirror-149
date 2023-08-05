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
AkidaNet model definition for ImageNet classification.

AkidaNet is an NSoC optimized model inspired from VGG and MobileNet V1
architectures. It can be used for multiple use cases through transfer learning.

"""

import warnings

from keras import Model, regularizers
from keras.layers import (Input, Reshape, Dropout, Activation, Rescaling)
from keras.utils.data_utils import get_file

from cnn2snn import quantize, load_quantized_model

from ..layer_blocks import conv_block, separable_conv_block

BASE_WEIGHT_PATH = 'http://data.brainchip.com/models/akidanet/'


def _obtain_input_shape(input_shape, default_size, min_size, include_top):
    """Internal utility to compute/validate a model's input shape.

    Args:
        input_shape: either None (will return the default model input shape),
            or a user-provided shape to be validated.
        default_size: default input width/height for the model.
        min_size: minimum input width/height accepted by the model.
        include_top: whether the model is expected to
            be linked to a classifier via a Flatten layer.

    Returns:
        tuple of integers: input shape (may include None entries).

    Raises:
        ValueError: in case of invalid argument values.
    """
    if input_shape and len(input_shape) == 3:
        if input_shape[-1] not in {1, 3}:
            warnings.warn('This model usually expects 1 or 3 input channels. '
                          'However, it was passed an input_shape with ' +
                          str(input_shape[-1]) + ' input channels.')
        default_shape = (default_size, default_size, input_shape[-1])
    else:
        default_shape = (default_size, default_size, 3)

    if input_shape:
        if input_shape is not None:
            if len(input_shape) != 3:
                raise ValueError(
                    '`input_shape` must be a tuple of three integers.')
            if ((input_shape[0] is not None and input_shape[0] < min_size) or
                    (input_shape[1] is not None and input_shape[1] < min_size)):
                raise ValueError('Input size must be at least ' +
                                 str(min_size) + 'x' + str(min_size) +
                                 '; got `input_shape=' + str(input_shape) + '`')
    else:
        if include_top:
            input_shape = default_shape
        else:
            input_shape = (None, None, 3)
    if include_top:
        if None in input_shape:
            raise ValueError('If `include_top` is True, '
                             'you should specify a static `input_shape`. '
                             'Got `input_shape=' + str(input_shape) + '`')
    return input_shape


def akidanet_imagenet(input_shape=None,
                      alpha=1.0,
                      include_top=True,
                      pooling=None,
                      classes=1000,
                      weight_quantization=0,
                      activ_quantization=0,
                      input_weight_quantization=None,
                      input_scaling=(128, -1)):
    """Instantiates the AkidaNet architecture.

    Args:
        input_shape (tuple): optional shape tuple.
        alpha (float): controls the width of the model.

            * If `alpha` < 1.0, proportionally decreases the number of filters
              in each layer.
            * If `alpha` > 1.0, proportionally increases the number of filters
              in each layer.
            * If `alpha` = 1, default number of filters from the paper are used
              at each layer.
        include_top (bool): whether to include the fully-connected
            layer at the top of the model.
        pooling (str): optional pooling mode for feature extraction
            when `include_top` is `False`.

            * `None` means that the output of the model will be the 4D tensor
              output of the last convolutional block.
            * `avg` means that global average pooling will be applied to the
              output of the last convolutional block, and thus the output of the
              model will be a 2D tensor.
        classes (int): optional number of classes to classify images
            into, only to be specified if `include_top` is `True`.
        weight_quantization (int): sets all weights in the model to have
            a particular quantization bitwidth except for the weights in the
            first layer.

            * '0' implements floating point 32-bit weights.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.
        activ_quantization: sets all activations in the model to have a
            particular activation quantization bitwidth.

            * '0' implements floating point 32-bit activations.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.
        input_weight_quantization: sets weight quantization in the first layer.
            Defaults to weight_quantization value.

            * '0' implements floating point 32-bit weights.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.
        input_scaling (tuple, optional): scale factor and offset to apply to
            inputs. Defaults to (128, -1). Note that following Akida convention,
            the scale factor is an integer used as a divider.

    Returns:
        keras.Model: a Keras model for AkidaNet/ImageNet.

    Raises:
        ValueError: in case of invalid input shape.
    """
    # check if overrides have been provided and override
    if input_weight_quantization is None:
        input_weight_quantization = weight_quantization

    # Define weight regularization, will apply to the convolutional layers and
    # to all pointwise weights of separable convolutional layers.
    weight_regularizer = regularizers.l2(4e-5)

    # Determine proper input shape and default size.
    if input_shape is None:
        default_size = 224
    else:
        rows = input_shape[0]
        cols = input_shape[1]

        if rows == cols and rows in [128, 160, 192, 224]:
            default_size = rows
        else:
            default_size = 224

    input_shape = _obtain_input_shape(input_shape,
                                      default_size=default_size,
                                      min_size=32,
                                      include_top=include_top)

    img_input = Input(shape=input_shape)

    if input_scaling is None:
        x = img_input
    else:
        scale, offset = input_scaling
        x = Rescaling(1. / scale, offset)(img_input)

    x = conv_block(x,
                   filters=int(32 * alpha),
                   name='conv_0',
                   kernel_size=(3, 3),
                   padding='same',
                   use_bias=False,
                   strides=2,
                   add_batchnorm=True,
                   add_activation=True,
                   kernel_regularizer=weight_regularizer)

    x = conv_block(x,
                   filters=int(64 * alpha),
                   name='conv_1',
                   kernel_size=(3, 3),
                   padding='same',
                   use_bias=False,
                   add_batchnorm=True,
                   add_activation=True,
                   kernel_regularizer=weight_regularizer)

    x = conv_block(x,
                   filters=int(128 * alpha),
                   name='conv_2',
                   kernel_size=(3, 3),
                   padding='same',
                   strides=2,
                   use_bias=False,
                   add_batchnorm=True,
                   add_activation=True,
                   kernel_regularizer=weight_regularizer)

    x = conv_block(x,
                   filters=int(128 * alpha),
                   name='conv_3',
                   kernel_size=(3, 3),
                   padding='same',
                   use_bias=False,
                   add_batchnorm=True,
                   add_activation=True,
                   kernel_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(256 * alpha),
                             name='separable_4',
                             kernel_size=(3, 3),
                             padding='same',
                             strides=2,
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(256 * alpha),
                             name='separable_5',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(512 * alpha),
                             name='separable_6',
                             kernel_size=(3, 3),
                             padding='same',
                             strides=2,
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(512 * alpha),
                             name='separable_7',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(512 * alpha),
                             name='separable_8',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(512 * alpha),
                             name='separable_9',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(512 * alpha),
                             name='separable_10',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(512 * alpha),
                             name='separable_11',
                             kernel_size=(3, 3),
                             padding='same',
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True,
                             pointwise_regularizer=weight_regularizer)

    x = separable_conv_block(x,
                             filters=int(1024 * alpha),
                             name='separable_12',
                             kernel_size=(3, 3),
                             padding='same',
                             strides=2,
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True,
                             pointwise_regularizer=weight_regularizer)

    # Last separable layer with global pooling
    layer_pooling = 'global_avg' if include_top or pooling == 'avg' else None
    x = separable_conv_block(x,
                             filters=int(1024 * alpha),
                             name='separable_13',
                             kernel_size=(3, 3),
                             padding='same',
                             pooling=layer_pooling,
                             use_bias=False,
                             add_batchnorm=True,
                             add_activation=True,
                             pointwise_regularizer=weight_regularizer)

    if include_top:
        shape = (1, 1, int(1024 * alpha))

        x = Reshape(shape, name='reshape_1')(x)
        x = Dropout(1e-3, name='dropout')(x)

        x = separable_conv_block(x,
                                 filters=classes,
                                 name='separable_14',
                                 kernel_size=(3, 3),
                                 padding='same',
                                 use_bias=False,
                                 add_batchnorm=False,
                                 add_activation=False,
                                 pointwise_regularizer=weight_regularizer)
        act_function = 'softmax' if classes > 1 else 'sigmoid'
        x = Activation(act_function, name=f'act_{act_function}')(x)
        x = Reshape((classes,), name='reshape_2')(x)

    # Create model.
    model = Model(img_input,
                  x,
                  name='akidanet_%0.2f_%s_%s' %
                  (alpha, input_shape[0], classes))

    if ((weight_quantization != 0) or (activ_quantization != 0) or
            (input_weight_quantization != 0)):
        return quantize(model, weight_quantization, activ_quantization,
                        input_weight_quantization)
    return model


def akidanet_imagenet_pretrained(alpha=1.0):
    """
    Helper method to retrieve an `akidanet_imagenet` model that was trained on
    ImageNet dataset.

    Args:
        alpha (float, optional): width of the model, allowed values in [0.25,
            0.5, 1]. Defaults to 1.0.

    Returns:
        keras.Model: a Keras Model instance.

    """
    if alpha == 1.0:
        model_name = 'akidanet_imagenet_224_iq8_wq4_aq4.h5'
        file_hash = '1be87e301fe9280d137a821de23fe9ac47c4c7e9ec8405f2279fd0ea02a648c7'
    elif alpha == 0.5:
        model_name = 'akidanet_imagenet_224_alpha_50_iq8_wq4_aq4.h5'
        file_hash = 'bd9ff5d5944d25d220883d2feaff8d34a6cafd3d8a44d98a3307281410781b6e'
    elif alpha == 0.25:
        model_name = 'akidanet_imagenet_224_alpha_25_iq8_wq4_aq4.h5'
        file_hash = '6ee45047b9e283576946d2a65e15411bdc82f1e02faf1b684ed0730089aae69c'
    else:
        raise ValueError(
            f"Requested model with alpha={alpha} is not available.")

    model_path = get_file(fname=model_name,
                          origin=BASE_WEIGHT_PATH + model_name,
                          file_hash=file_hash,
                          cache_subdir='models')
    return load_quantized_model(model_path)


def akidanet_cats_vs_dogs_pretrained():
    """
    Helper method to retrieve an `akidanet_imagenet` model that was trained on
    Cats vs.Dogs dataset.

    Returns:
        keras.Model: a Keras Model instance.

    """
    model_name = 'akidanet_cats_vs_dogs_iq8_wq4_aq4_lwq_float.h5'
    file_hash = '7f5d71f828c379503ed9d1c1a37e13611369ee558655c6b3406186a05340d35a'
    model_path = get_file(fname=model_name,
                          origin=BASE_WEIGHT_PATH + model_name,
                          file_hash=file_hash,
                          cache_subdir='models')
    return load_quantized_model(model_path)


def akidanet_imagenette_pretrained(alpha=1.0):
    """
    Helper method to retrieve a `akidanet_imagenet` model that was trained on
    Imagenette dataset.

    Args:
        alpha (float, optional): width of the model, allowed values in [0.25,
            0.5, 1]. Defaults to 1.0.

    Returns:
        keras.Model: a Keras Model instance.
    """
    if alpha == 1.0:
        model_name = 'akidanet_imagenette_224_iq8_wq4_aq4.h5'
        file_hash = '7c29aa9362685643b782868c7f73a5f0f1ed64c38896d894b90d78fb83fecfa6'
    elif alpha == 0.5:
        model_name = 'akidanet_imagenette_224_alpha_50_iq8_wq4_aq4.h5'
        file_hash = '6729a203605f527fd0cff76d76275ef74be2f467cd5e3abc9df3d7df54c1c2c9'
    elif alpha == 0.25:
        model_name = 'akidanet_imagenette_224_alpha_25_iq8_wq4_aq4.h5'
        file_hash = 'c99e1249802bb5b6348ca6746416cc9e903ef5c43f52ea734caef15916494904'
    else:
        raise ValueError(
            f"Requested model with alpha={alpha} is not available.")

    model_path = get_file(fname=model_name,
                          origin=BASE_WEIGHT_PATH + model_name,
                          file_hash=file_hash,
                          cache_subdir='models')
    return load_quantized_model(model_path)


def akidanet_faceidentification_pretrained():
    """
    Helper method to retrieve an `akidanet_imagenet` model that was trained on
    CASIA Webface dataset and that performs face identification.

    Returns:
        keras.Model: a Keras Model instance.

    """
    model_name = 'akidanet_faceidentification_iq8_wq4_aq4.h5'
    file_hash = 'a50a89a5608c1f01bb9ab70ed214be3e249890bc6a41bc179c2a9427020a2c95'
    model_path = get_file(fname=model_name,
                          origin=BASE_WEIGHT_PATH + model_name,
                          file_hash=file_hash,
                          cache_subdir='models')
    return load_quantized_model(model_path)


def akidanet_faceverification_pretrained():
    """
    Helper method to retrieve an `akidanet_imagenet` model that was trained on
    CASIA Webface dataset and optimized with ArcFace that can perform face
    verification on LFW.

    Returns:
        keras.Model: a Keras Model instance.

    """
    model_name = 'akidanet_faceverification_iq8_wq4_aq4.h5'
    file_hash = '8e1c47013dc17745901041f2060aa1e2b5f7222749ec5068b3c9549a42eab070'
    model_path = get_file(fname=model_name,
                          origin=BASE_WEIGHT_PATH + model_name,
                          file_hash=file_hash,
                          cache_subdir='models')
    return load_quantized_model(model_path)


def akidanet_melanoma_pretrained():
    """
    Helper method to retrieve an `akidanet_imagenet` model that was trained on
    SIIM-ISIC Melanoma Classification dataset.

    Returns:
        keras.Model: a Keras Model instance.

    """
    model_name = 'akidanet_melanoma_iq8_wq4_aq4.h5'
    file_hash = '844e56a7f5c642504483a19d307a2524d127716bf1d5a6bd4ead389f23b1e99a'
    model_path = get_file(fname=model_name,
                          origin=BASE_WEIGHT_PATH + model_name,
                          file_hash=file_hash,
                          cache_subdir='models')
    return load_quantized_model(model_path)


def akidanet_odir5k_pretrained():
    """
    Helper method to retrieve an `akidanet_imagenet` model that was trained on
    ODIR-5K dataset.

    The model focuses on the following classes that are a part of the original
    dataset: normal, cataract, AMD (age related macular degeneration) and
    pathological myopia.

    Returns:
        keras.Model: a Keras Model instance.

    """
    model_name = 'akidanet_odir5k_iq8_wq4_aq4.h5'
    file_hash = 'f8af24f8443191b493c1d82eaf3d8377018d056a936c0e9aea0e4fb701328b09'
    model_path = get_file(fname=model_name,
                          origin=BASE_WEIGHT_PATH + model_name,
                          file_hash=file_hash,
                          cache_subdir='models')
    return load_quantized_model(model_path)


def akidanet_retinal_oct_pretrained():
    """
    Helper method to retrieve an `akidanet_imagenet` model that was trained on
    retinal OCT dataset.

    Returns:
        keras.Model: a Keras Model instance.

    """
    model_name = 'akidanet_retinal_oct_iq8_wq4_aq4.h5'
    file_hash = '4811d9ec9ba46434074d3edfae7733557d4f3cde473bb2d194d3c3200f060b64'
    model_path = get_file(fname=model_name,
                          origin=BASE_WEIGHT_PATH + model_name,
                          file_hash=file_hash,
                          cache_subdir='models')
    return load_quantized_model(model_path)


def akidanet_ecg_pretrained():
    """
    Helper method to retrieve an `akidanet_imagenet` model that was trained on
    ECG classification Physionet2017 dataset.

    Returns:
        keras.Model: a Keras Model instance.

    """
    model_name = 'akidanet_ecg_iq8_wq4_aq4.h5'
    file_hash = 'd3bf3b598e1e0175873e60f39cd5b6cefa874f4d351518f1a788e402d7bfaa6b'
    model_path = get_file(fname=model_name,
                          origin=BASE_WEIGHT_PATH + model_name,
                          file_hash=file_hash,
                          cache_subdir='models')
    return load_quantized_model(model_path)


def akidanet_plantvillage_pretrained():
    """
    Helper method to retrieve an `akidanet_imagenet` model that was trained on
    PlantVillage dataset.

    Returns:
        keras.Model: a Keras Model instance.

    """
    model_name = 'akidanet_plantvillage_iq8_wq4_aq4.h5'
    file_hash = 'beace6e5a23ee690826252124b1da1f523f120cca15b117858adb2ccfd75420d'
    model_path = get_file(fname=model_name,
                          origin=BASE_WEIGHT_PATH + model_name,
                          file_hash=file_hash,
                          cache_subdir='models')
    return load_quantized_model(model_path)


def akidanet_cifar10_pretrained():
    """
    Helper method to retrieve an `akidanet_imagenet` model that was trained on
    CIFAR-10 dataset. Since CIFAR-10 images have a 32x32 size, they need to be
    resized to match akidanet input layer. This can be done by calling the
    'resize_image' function available under akida_models.cifar10.preprocessing.

    Returns:
        keras.Model: a Keras Model instance.

    """
    model_name = 'akidanet_cifar10_iq8_wq4_aq4.h5'
    file_hash = 'c645cf132c9641e3d0b3611baf7c1cab143aa29d6289a976bd9064e533a6afa0'
    model_path = get_file(fname=model_name,
                          origin=BASE_WEIGHT_PATH + model_name,
                          file_hash=file_hash,
                          cache_subdir='models')
    return load_quantized_model(model_path)


def akidanet_vww_pretrained():
    """
    Helper method to retrieve an `akidanet_imagenet` model that was trained on
    VWW dataset.

    Returns:
        keras.Model: a Keras Model instance.

    """
    model_name = 'akidanet_vww_iq8_wq4_aq4.h5'
    file_hash = '3c1f842cae0cb65abcda1197e4451c6ed24eb0f7dbc74be5d96441e478b7c1a8'
    model_path = get_file(fname=model_name,
                          origin=BASE_WEIGHT_PATH + model_name,
                          file_hash=file_hash,
                          cache_subdir='models')
    return load_quantized_model(model_path)
