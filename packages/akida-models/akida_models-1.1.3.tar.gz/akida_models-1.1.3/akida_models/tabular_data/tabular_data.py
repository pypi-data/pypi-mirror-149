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
TSE and MLP model definitions.
"""

import numpy as np
import tensorflow as tf

from keras.layers import Input, Activation, Reshape, Flatten
from keras.feature_column.dense_features_v2 import DenseFeatures

from ..layer_blocks import dense_block


def create_tse(numerical_columns, categorical_columns, units):
    """
    Create a Trainable Spike Encoder (TSE) network.

    Since Akida cannot handle a flat Dense as input, a reshape layer is inserted
    as the last layer the TSE sub-model and the first layer of the MLP part is a
    Flatten layer.

    Note that the following rule is applied to choose the embedding size of
    categorical columns:

    'Inspired by Howard & Gugger (2020), a discrete feature with k unique
    categories observed in the training data is processed by an embedding layer
    of size: 1.6 * k^0.56 (up to threshold of size 100).'

    See:
        - Howard, J., & Gugger, S. (2020). Deep Learning for Coders with fastai
          and PyTorch: AI Applications Without a PhD. 1st Edition (in particular
          Chapter 9: `09_tabular.ipynb
          <https://github.com/fastai/fastbook/blob/master/09_tabular.ipynb>`_
        - Erickson, N., Mueller, J., Shirkov, A., Zhang, H., Larroy, P., Li, M.,
          & Smola, A. (2020). AutoGluon-Tabular: Robust and Accurate AutoML for
          Structured Data. arXiv preprint arXiv:2003.06505.

    Args:
        numerical_columns (list): list of numerical columns names
        categorical_columns (dict): dictionary of categorical column names
            indexing the list of vocabulary for the column
        units (int): dimensionality of the output space
        input_weight_quantization (int): sets weight quantization in the first
            layer.

            * '0' implements floating point 32-bit weights.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.
        activ_quantization (int): sets all activations in the model to have a
            particular activation quantization bitwidth.

            * '0' implements floating point 32-bit activations.
            * '1' through '8' implements n-bit weights where n is from 1-8 bits.

    Returns:
        dict, tf.Tensor: the dictionary of input layers to build the
        model and the TSE output that can be used as an input for the MLP


    """
    feature_columns = []
    feature_layer_inputs = {}

    for col in numerical_columns:
        feature_layer_inputs[col] = Input(shape=(1,), name=col)
        feature_columns.append(tf.feature_column.numeric_column(col))

    for col, vocab in categorical_columns.items():
        feature_layer_inputs[col] = Input(shape=(1,), name=col, dtype='string')
        cat_col = tf.feature_column.categorical_column_with_vocabulary_list(
            col, vocab, num_oov_buckets=1)
        embedding_size = min(int(np.round(1.6 * len(vocab)**0.56)), 100)
        embedding_col = tf.feature_column.embedding_column(
            cat_col, embedding_size)
        feature_columns.append(embedding_col)

    feature_layer = DenseFeatures(feature_columns)
    feature_layer_outputs = feature_layer(feature_layer_inputs)

    x = dense_block(feature_layer_outputs,
                    units=units,
                    name='dense_to_spike',
                    add_activation=True,
                    add_batchnorm=True)
    x = Reshape(target_shape=(1, 1, units), name='final_embedding_reshape')(x)

    return feature_layer_inputs, x


def create_mlp(inputs, units_list, n_classes):
    """
    Create a Multilayer Perceptron (MLP) network.

    Since Akida cannot handle a flat Dense as input, a reshape layer is inserted
    as the last layer the TSE sub-model and the first layer of the MLP part is a
    Flatten layer.

    Args:
        inputs (:obj:`tf.Tensor`): input tensor of shape (1, 1, N)
        units_list (list): list of units as integers. Units are the
            dimensionality of the output space. The length of the list defines
            the number of hidden layers
        n_classes (int): dimensionality of the last layer output space

    Returns:
        tf.Tensor: the MLP output that will be used to create the model

    """
    x = Flatten()(inputs)

    for i, _ in enumerate(units_list):
        x = dense_block(x,
                        units=units_list[i],
                        name='dense' + str(i + 1),
                        add_activation=True,
                        add_batchnorm=True)
    x = dense_block(x,
                    units=n_classes,
                    name='last_dense',
                    add_activation=False,
                    use_bias=False)
    activation_function = 'softmax' if n_classes > 1 else 'sigmoid'
    x = Activation(activation_function, name='activation')(x)
    return x
