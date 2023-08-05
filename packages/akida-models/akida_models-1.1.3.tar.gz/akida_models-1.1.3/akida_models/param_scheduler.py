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
Parameters scheduling policy module.

Originated from: https://github.com/fastai/fastai/blob/master/nbs/14_callback.schedule.ipynb
"""

import math

import numpy as np

from keras.callbacks import Callback


class _Annealer:
    def __init__(self, f, start, end):
        self.f = f
        self.start = start
        self.end = end

    def __call__(self, pos):
        return self.f(self.start, self.end, pos)


def SchedLin(start, end):
    """ Linear schedule function from `start` to `end`.

    Args:
        start (float): starting point
        end (float): ending point

    Returns:
        function: the scheduling function
    """

    def sched_lin(start, end, pos):
        return start + pos * (end - start)

    return _Annealer(sched_lin, start, end)


def SchedCos(start, end):
    """ Cosine schedule function from `start` to `end`.

    Args:
        start (float): starting point
        end (float): ending point

    Returns:
        function: the scheduling function
    """

    def sched_cos(start, end, pos):
        return start + (1 + math.cos(math.pi * (1 - pos))) * (end - start) / 2

    return _Annealer(sched_cos, start, end)


def SchedNo(start, end):
    """ Constant schedule function with `start` value.

    Args:
        start (float): starting point
        end (float): ending point

    Returns:
        function: the scheduling function
    """

    def sched_no(start, end, pos):
        return start

    return _Annealer(sched_no, start, end)


def SchedExp(start, end):
    """ Exponential schedule function from `start` to `end`.

    Args:
        start (float): starting point
        end (float): ending point

    Returns:
        function: the scheduling function
    """
    if start == 0:
        raise ValueError("Starting point cannot be 0 for SchedExp.")

    def sched_exp(start, end, pos):
        return start * (end / start)**pos

    return _Annealer(sched_exp, start, end)


def SchedPoly(start, end, power):
    """ Polynomial schedule (of `power`) function from `start` to `end`.

    Args:
        start (float): starting point
        end (float): ending point
        power (float): power of the polynomial

    Returns:
        function: the scheduling function
    """

    def _inner(pos):
        return start + (end - start) * pos**power

    return _inner


def combine_scheds(pcts, scheds):
    """ Combine `scheds` according to `pcts` in one function.

    The generated function will use scheds[0] from 0 to pcts[0]
    then scheds[1] from pcts[0] to pcts[0]+pcts[1] and so forth.

    example:
        all_pos = np.linspace(0., 1, 100)
        pcts = np.array([0.3, 0.7])
        scheds = [SchedCos(0.3, 0.6), SchedCos(0.6, 0.2)]
        sched_comb = combine_scheds(pcts, scheds)
        all_lrs = []
        for pos in all_pos:
            all_lrs.append(sched_comb(pos))
        plt.plot(all_pos, all_lrs)
        plt.show()

    example 2:
        p = np.linspace(0., 1, 100)
        f = combine_scheds([0.3, 0.2, 0.5], [SchedLin(0., 1.), SchedNo(1., 1.),
                SchedCos(1., 0.)])
        plt.plot(p, [f(o) for o in p])
        plt.show()

    Args:
        pcts (list): list of positive numbers that add up to 1 and is the same
            length as scheds.
        scheds (list): list of scheduling functions

    Returns:
        function: the combined scheduling function
    """
    assert sum(pcts) == 1.
    pcts = np.hstack((np.array(0,), pcts))

    assert np.all(pcts >= 0)
    pcts = np.cumsum(pcts, 0)

    def _inner(pos):
        if int(pos) == 1:
            return scheds[-1](1.)

        idx = np.max(np.where(pos >= pcts))
        actual_pos = (pos - pcts[idx]) / (pcts[idx + 1] - pcts[idx])
        return scheds[idx](actual_pos)

    return _inner


class ParamScheduler(Callback):
    """ Schedule hyper-parameters according to `scheds`.

    # example for linear scheduler for LR
        sched = {'lr': SchedLin(1e-3, 1e-2)}

    Args:
        scheds (dict): dictionary with one key for each hyper-parameter you want
            to schedule, with either a scheduler or a list of schedulers as
            values (in the second case, the list must have the same length as
            the number of parameters groups of the optimizer).
        total_num_iterations (int): number of iterations
    """

    def __init__(self, scheds, total_num_iterations):
        super().__init__()

        self.scheds = scheds
        # pct_train: from 0. to 1., the percentage of training iterations
        # completed
        self.pct_train = 0  # is rewritten at each batch
        self.history = {}

        if total_num_iterations <= 0:
            raise ValueError(f"total_num_iterations must be > 0 but received \
                {total_num_iterations}")

        self.total_num_iterations = total_num_iterations  # static
        self.cum_batch_num = 0  # keep adding 1 to this at every batch

    def _update_val(self, pct):
        # pct is the percent training done
        for n, f in self.scheds.items():
            self.model.optimizer._set_hyper(n, f(pct))

    def on_batch_begin(self, batch, logs=None):
        # before_batch: set the proper hyper-parameters in the optimizer
        self._update_val(self.pct_train)
        # update the tracking info
        self.cum_batch_num += 1
        self.pct_train = self.cum_batch_num / self.total_num_iterations

    def on_batch_end(self, batch, logs=None):
        # after_batch: record hyper-parameters of this batch
        logs = logs or {}
        # keep in memory the current values
        for p in self.scheds.keys():
            self.history.setdefault(p, []).append(
                self.model.optimizer.get_config()[p])
        # logs on batch end is a dict with aggregated metric results up until
        # this batch.
        for k, v in logs.items():
            self.history.setdefault(k, []).append(v)
