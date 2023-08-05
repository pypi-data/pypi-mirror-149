#!/usr/bin/env python
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
Layers blocks definitions.
"""

from keras.layers import (BatchNormalization, ReLU, Conv2D, SeparableConv2D,
                          Dense, MaxPool2D, AvgPool2D, GlobalAvgPool2D)


def _add_pooling_layer(x, pooling_type, pool_size, padding, layer_base_name):
    """Add a pooling layer in the graph.

    From an input tensor 'x', the function returns the output tensor after
    a pooling layer defined by 'pooling_type'.

    Args:
        x (tf.Tensor): the input tensor
        pooling_type (str): type of pooling among the following: 'max',
            'avg' or 'global_avg'.
        pool_size (int or tuple of 2 integers): factors by which to
            downscale (vertical, horizontal). (2, 2) will halve the input in
            both spatial dimension. If only one integer is specified, the same
            window length will be used for both dimensions.
        padding (str): one of "valid" or "same" (case-insensitive).
        layer_base_name (str): base name for the pooling layer.

    Returns:
        tf.Tensor: an output tensor after pooling
    """
    if pooling_type == 'max':
        return MaxPool2D(pool_size=pool_size,
                         padding=padding,
                         name=layer_base_name + '_maxpool')(x)
    if pooling_type == 'avg':
        return AvgPool2D(pool_size=pool_size,
                         padding=padding,
                         name=layer_base_name + '_avgpool')(x)
    if pooling_type == 'global_avg':
        return GlobalAvgPool2D(name=layer_base_name + '_global_avg')(x)
    raise ValueError("'pooling_type' argument must be 'max', "
                     "'avg' or 'global_avg'.")


def conv_block(inputs,
               filters,
               kernel_size,
               pooling=None,
               pool_size=(2, 2),
               add_batchnorm=False,
               add_activation=True,
               **kwargs):
    """Adds a convolutional layer with optional layers in the following order:
    max pooling, batch normalization, activation.

    Args:
        inputs (tf.Tensor): input tensor of shape `(rows, cols, channels)`
        filters (int): the dimensionality of the output space
            (i.e. the number of output filters in the convolution).
        kernel_size (int or tuple of 2 integers): specifying the
            height and width of the 2D convolution kernel.
            Can be a single integer to specify the same value for
            all spatial dimensions.
        pooling (str): add a pooling layer of type 'pooling' among the
            values 'max', 'avg', 'global_max' or 'global_avg', with pooling
            size set to pool_size. If 'None', no pooling will be added.
        pool_size (int or tuple of 2 integers): factors by which to
            downscale (vertical, horizontal). (2, 2) will halve the input in
            both spatial dimension. If only one integer is specified, the same
            window length will be used for both dimensions.
        add_batchnorm (bool): add a BatchNormalization layer
        add_activation (bool): add a ReLU layer
        **kwargs: arguments passed to the keras.Conv2D layer, such as
            strides, padding, use_bias, weight_regularizer, etc.

    Returns:
        tf.Tensor: output tensor of conv2D block.
    """
    if 'activation' in kwargs and kwargs['activation']:
        raise ValueError(
            "Keyword argument 'activation' in conv_block must be None.")
    if 'dilation_rate' in kwargs:
        if kwargs['dilation_rate'] != 1 and kwargs['dilation_rate'] != (1, 1):
            raise ValueError("Keyword argument 'dilation_rate' is not "
                             "supported in conv_block.")

    conv_layer = Conv2D(filters, kernel_size, **kwargs)
    x = conv_layer(inputs)

    if pooling:
        x = _add_pooling_layer(x, pooling, pool_size, conv_layer.padding,
                               conv_layer.name)

    if add_batchnorm:
        x = BatchNormalization(name=conv_layer.name + '_BN')(x)

    if add_activation:
        x = ReLU(6.0, name=conv_layer.name + '_relu')(x)

    return x


def separable_conv_block(inputs,
                         filters,
                         kernel_size,
                         pooling=None,
                         pool_size=(2, 2),
                         add_batchnorm=False,
                         add_activation=True,
                         **kwargs):
    """Adds a separable convolutional layer with optional layers in the
    following order: global average pooling, max pooling, batch normalization,
    activation.

    Args:
        inputs (tf.Tensor): input tensor of shape `(height, width, channels)`
        filters (int): the dimensionality of the output space
            (i.e. the number of output filters in the pointwise convolution).
        kernel_size (int or tuple of 2 integers): specifying the
            height and width of the 2D convolution window. Can be a single
            integer to specify the same value for all spatial dimensions.
        pooling (str): add a pooling layer of type 'pooling' among the
            values 'max', 'avg', 'global_max' or 'global_avg', with pooling
            size set to pool_size. If 'None', no pooling will be added.
        pool_size (int or tuple of 2 integers): factors by which to
            downscale (vertical, horizontal). (2, 2) will halve the input in
            both spatial dimension. If only one integer is specified, the same
            window length will be used for both dimensions.
        add_batchnorm (bool): add a BatchNormalization layer
        add_activation (bool): add a ReLU layer
        **kwargs: arguments passed to the keras.SeparableConv2D layer,
            such as strides, padding, use_bias, etc.

    Returns:
        tf.Tensor: output tensor of separable conv block.
    """
    if 'activation' in kwargs and kwargs['activation']:
        raise ValueError("Keyword argument 'activation' in separable_conv_block"
                         " must be None.")
    if 'dilation_rate' in kwargs:
        if kwargs['dilation_rate'] != 1 and kwargs['dilation_rate'] != (1, 1):
            raise ValueError("Keyword argument 'dilation_rate' is not "
                             "supported in separable_conv_block.")
    if 'depth_multiplier' in kwargs:
        if kwargs['depth_multiplier'] != 1:
            raise ValueError("Keyword argument 'depth_multiplier' is not "
                             "supported in separable_conv_block.")

    sep_conv_layer = SeparableConv2D(filters, kernel_size, **kwargs)
    x = sep_conv_layer(inputs)

    if pooling:
        x = _add_pooling_layer(x, pooling, pool_size, sep_conv_layer.padding,
                               sep_conv_layer.name)

    if add_batchnorm:
        x = BatchNormalization(name=sep_conv_layer.name + '_BN')(x)

    if add_activation:
        x = ReLU(6.0, name=sep_conv_layer.name + '_relu')(x)

    return x


def dense_block(inputs,
                units,
                add_batchnorm=False,
                add_activation=True,
                **kwargs):
    """Adds a dense layer with optional layers in the following order:
    batch normalization, activation.

    Args:
        inputs (tf.Tensor): Input tensor of shape `(rows, cols, channels)`
        units (int): dimensionality of the output space
        add_batchnorm (bool): add a BatchNormalization layer
        add_activation (bool): add a ReLU layer
        **kwargs: arguments passed to the Dense layer, such as
            use_bias, kernel_initializer, weight_regularizer, etc.

    Returns:
        tf.Tensor: output tensor of the dense block.
    """
    if 'activation' in kwargs and kwargs['activation']:
        raise ValueError("Keyword argument 'activation' in dense_block"
                         " must be None.")

    dense_layer = Dense(units, **kwargs)
    x = dense_layer(inputs)

    if add_batchnorm:
        x = BatchNormalization(name=dense_layer.name + '_BN')(x)

    if add_activation:
        x = ReLU(6.0, name=dense_layer.name + '_relu')(x)

    return x
