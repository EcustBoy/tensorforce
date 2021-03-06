# Copyright 2018 Tensorforce Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import unittest

from test.unittest_base import UnittestBase


class TestRewardEstimation(UnittestBase, unittest.TestCase):

    agent = dict(
        policy=dict(network=dict(type='auto', size=8, depth=1, internal_rnn=2)),
        update=dict(unit='episodes', batch_size=1),
        objective='policy_gradient'
    )
    require_observe = True

    def test_no_horizon_estimate(self):
        self.start_tests(name='no horizon estimate')

        # zero horizon
        reward_estimation = dict(horizon=0, discount=0.99, estimate_horizon=False)
        self.unittest(reward_estimation=reward_estimation)

        # horizon longer than episode
        reward_estimation = dict(horizon=10, discount=0.99, estimate_horizon=False)
        self.unittest(reward_estimation=reward_estimation)

    def test_early_horizon_estimate(self):
        self.start_tests(name='early horizon estimate')

        reward_estimation = dict(horizon=2, estimate_horizon='early')
        self.unittest(reward_estimation=reward_estimation)

        reward_estimation = dict(horizon=2, estimate_horizon='early', estimate_actions=True)
        baseline_objective = 'policy_gradient'
        baseline_optimizer = 'adam'
        # TODO: action value doesn't exist for Beta
        self.unittest(
            exclude_bounded_action=True, reward_estimation=reward_estimation,
            baseline_objective=baseline_objective, baseline_optimizer=baseline_optimizer
        )

        reward_estimation = dict(horizon=2, estimate_horizon='early', estimate_terminal=True)
        # TODO: currently requires same internal RNN horizon
        baseline_policy = dict(network=dict(type='auto', size=7, depth=1, internal_rnn=2))
        baseline_objective = 'policy_gradient'
        self.unittest(
            reward_estimation=reward_estimation, baseline_policy=baseline_policy,
            baseline_objective=baseline_objective
        )

        reward_estimation = dict(
            horizon=2, estimate_horizon='early', estimate_actions=True, estimate_terminal=True
        )
        # TODO: action value doesn't exist for Beta
        baseline_policy = dict(
            network=dict(type='auto', size=7, depth=1, internal_rnn=1),
            distributions=dict(float='gaussian')
        )
        baseline_objective = 'policy_gradient'
        baseline_optimizer = 'adam'
        self.unittest(
            reward_estimation=reward_estimation, baseline_policy=baseline_policy,
            baseline_objective=baseline_objective, baseline_optimizer=baseline_optimizer
        )

    def test_late_horizon_estimate(self):
        self.start_tests(name='late horizon estimate')

        reward_estimation = dict(horizon=2, estimate_horizon='late')
        baseline_objective = 'policy_gradient'
        self.unittest(reward_estimation=reward_estimation, baseline_objective=baseline_objective)

        reward_estimation = dict(horizon=2, estimate_horizon='late', estimate_actions=True)
        baseline_objective = 'policy_gradient'
        baseline_optimizer = 'adam'
        # TODO: action value doesn't exist for Beta
        self.unittest(
            exclude_bounded_action=True, reward_estimation=reward_estimation,
            baseline_objective=baseline_objective, baseline_optimizer=baseline_optimizer
        )

        reward_estimation = dict(horizon=2, estimate_horizon='late', estimate_terminal=True)
        baseline_policy = dict(network=dict(type='auto', size=7, depth=1, internal_rnn=1))
        baseline_optimizer = 'adam'
        self.unittest(
            reward_estimation=reward_estimation, baseline_policy=baseline_policy,
            baseline_optimizer=baseline_optimizer
        )

        reward_estimation = dict(
            horizon=2, estimate_horizon='late', estimate_actions=True, estimate_terminal=True
        )
        # TODO: action value doesn't exist for Beta
        baseline_policy = dict(
            network=dict(type='auto', size=7, depth=1, internal_rnn=1),
            distributions=dict(float='gaussian')
        )
        baseline_objective = 'policy_gradient'
        baseline_optimizer = 'adam'
        self.unittest(
            reward_estimation=reward_estimation, baseline_policy=baseline_policy,
            baseline_objective=baseline_objective, baseline_optimizer=baseline_optimizer
        )

    def test_advantage_estimate(self):
        self.start_tests(name='advantage estimate')

        reward_estimation = dict(horizon=2, estimate_horizon=False, estimate_advantage=True)
        self.unittest(reward_estimation=reward_estimation)

        reward_estimation = dict(
            horizon=2, estimate_horizon='early', estimate_actions=True, estimate_advantage=True
        )
        # TODO: currently incompatible with internal RNN
        # TODO: action value doesn't exist for Beta
        baseline_policy = dict(
            network=dict(type='auto', size=7, depth=1, internal_rnn=False),
            distributions=dict(float='gaussian')
        )
        baseline_optimizer = 'adam'
        self.unittest(
            reward_estimation=reward_estimation, baseline_policy=baseline_policy,
            baseline_optimizer=baseline_optimizer
        )

        reward_estimation = dict(
            horizon=2, estimate_horizon='late', estimate_terminal=True, estimate_advantage=True
        )
        baseline_policy = dict(network=dict(type='auto', size=7, depth=1, internal_rnn=1))
        baseline_objective = 'policy_gradient'
        baseline_optimizer = 'adam'
        self.unittest(
            reward_estimation=reward_estimation, baseline_policy=baseline_policy,
            baseline_objective=baseline_objective, baseline_optimizer=baseline_optimizer
        )
