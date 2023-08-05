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
Preprocessing tools for CSE-CIC-IDS-2018 data handling.
"""

import os
import pickle
import tensorflow as tf

from keras.utils.data_utils import get_file


def load_labels_mapping():
    """ Loads labels mapping from Brainchip data server.

    Returns:
        dict: the dictionnary of labels mapping
    """
    labels_mapping_path = get_file(
        "labels_mapping.pkl",
        "http://data.brainchip.com/dataset-mirror/cse_cic_ids_2018/labels_mapping.pkl",
        cache_subdir='datasets/cse_2018/')

    with open(labels_mapping_path, 'rb') as handle:
        labels_mapping = pickle.load(handle)
    return labels_mapping


def load_columns_type():
    """ Loads columns types from Brainchip data server.

    Returns:
        list, dict: the list of numerical columns and the dictionary of
        categorical columns with their vocabulary
    """
    columns_types_path = get_file(
        "columns_types.pkl",
        "http://data.brainchip.com/dataset-mirror/cse_cic_ids_2018/columns_types.pkl",
        cache_subdir='datasets/cse_2018/')

    with open(columns_types_path, 'rb') as handle:
        numerical_columns, categorical_columns = pickle.load(handle)
    return numerical_columns, categorical_columns


def load_data(batch_size=65536, load_train=True, load_test=True):
    """ Loads the dataset from Brainchip data server.

    Args:
        batch_size (int): number of records to combine in a single batch
        load_train (bool): flag to enable train set loading
        load_test (bool): flag to enable test set loading

    Returns:
        tf.dataset, tf.dataset: the train and test sets

    """
    LABEL_COLUMN = 'label'

    x_train = None
    x_test = None

    if load_train:
        train_file_path = get_file(
            "train_set.zip",
            "http://data.brainchip.com/dataset-mirror/cse_cic_ids_2018/train_set.zip",
            cache_subdir='datasets/cse_2018/',
            extract=True)
        train_file_path = os.path.join(os.path.dirname(train_file_path),
                                       "train_set.csv")
        x_train = tf.data.experimental.make_csv_dataset(train_file_path,
                                                        batch_size=batch_size,
                                                        label_name=LABEL_COLUMN,
                                                        num_epochs=1,
                                                        ignore_errors=True)

    if load_test:
        test_file_path = get_file(
            "test_set.zip",
            "http://data.brainchip.com/dataset-mirror/cse_cic_ids_2018/test_set.zip",
            cache_subdir='datasets/cse_2018/',
            extract=True)
        test_file_path = os.path.join(os.path.dirname(test_file_path),
                                      "test_set.csv")
        x_test = tf.data.experimental.make_csv_dataset(test_file_path,
                                                       batch_size=batch_size,
                                                       label_name=LABEL_COLUMN,
                                                       num_epochs=1,
                                                       ignore_errors=True)

    return x_train, x_test
