import time
from typing import Iterator
import logging
from torch.utils.data import IterableDataset
from typing import Dict
import pickle
from invertedai_simulate.dataset.db import CacheDataDB
from invertedai_simulate.dataset.models import DataLoader
from invertedai_simulate.interface import IAIEnv, ServerTimeoutError
import argparse
import gym

logger = logging.getLogger(__name__)


class IAIEnvDataset(IterableDataset):

    def __init__(self, config, scenario_name, world_parameters=None, vehicle_physics=None, scenario_parameters=None,
                 sensors=None, env: IAIEnv = None):
        """
        A iterable dataset that either takes or constructs an IAIEnv and output the information from each step from the
        IAIEnv environment
        """
        self.config = config
        self.load_cache_from = config.load_cache_from
        self.save_cache_to = config.save_cache_to
        self.cache_in_memory = config.cache_in_memory
        if self.load_cache_from:
            self.cache_loading_db = CacheDataDB(self.load_cache_from)
            self.starting_index_offset = self.cache_loading_db.count_all()
        else:
            self.cache_loading_db = None
            self.starting_index_offset = 0
        if self.load_cache_from == self.save_cache_to:
            self.cache_saving_db = self.cache_loading_db
        else:
            if self.save_cache_to:
                self.cache_saving_db = CacheDataDB(self.save_cache_to)
            else:
                self.cache_saving_db = None
        self.save_to_disk_interval = config.save_to_disk_interval
        self.saved_data = []
        self.last_saved_at = time.time()
        self._env: IAIEnv = gym.make(config.env_name, config=config) if env is None else env
        self.set_env_scenario(scenario_name, world_parameters, vehicle_physics, scenario_parameters, sensors)

        super(IAIEnvDataset).__init__()

    def set_env_scenario(self, scenario_name, world_parameters=None, vehicle_physics=None, scenario_parameters=None,
                         sensors=None):
        return self._env.set_scenario(scenario_name, world_parameters, vehicle_physics, scenario_parameters, sensors)

    def __iter__(self) -> Iterator[Dict]:
        done = False
        if self.config.enable_rendering:
            self._render_env()
        obs = self._reset_env()
        action = obs['prev_action']
        while not done:
            obs, rewards, done, info = self._step_env(action)
            action = self.get_next_action(info)
            if self.config.obs_only:
                data = dict(obs=obs, rewards=None, info=None)
            else:
                data = dict(obs=obs)
            if self.cache_in_memory:
                self.saved_data.append(data)
            if self.cache_saving_db:
                if (time.time() - self.last_saved_at) % 60 >= self.save_to_disk_interval:
                    pickled_obs, pickled_reward, pickled_info = pickle.dumps(obs), pickle.dumps(rewards), pickle.dumps(
                        info)
                    self.cache_saving_db.insert_cached_object([(pickled_obs, pickled_reward, pickled_info)])
                    self.last_saved_at = time.time()
            yield data

    def __getitem__(self, index) -> Dict:
        if self.cache_in_memory:
            if self.load_cache_from:
                if index >= self.starting_index_offset:
                    return self.saved_data[index - self.starting_index_offset]
                else:
                    return self.build_data_from_queried_result(self.cache_loading_db.load_data_by_idx(index + 1))
            else:
                return self.saved_data[index]
        else:
            return self.build_data_from_queried_result(self.cache_loading_db.load_data_by_idx(index + 1))

    def __exit__(self):
        self.close()

    @staticmethod
    def build_data_from_queried_result(result: DataLoader) -> Dict:
        obs, rewards, info = result.OBS, result.REWARDS, result.INFO
        return dict(obs=pickle.loads(obs),
                    info=pickle.loads(obs),
                    rewards=pickle.loads(rewards))

    def close(self):
        self._close_env()

    @staticmethod
    def get_next_action(info):
        return info['expert_action']

    def _step_env(self, action):
        return self._env.step(action)

    def _reset_env(self):
        return self._env.reset()

    def _close_env(self):
        self._env.close()

    def _render_env(self):
        self._env.render()

    def _seed_env(self, seed=None):
        self._env.seed(seed)

    def pre_load_data(self, limit=None):
        for i, _ in enumerate(self):
            if limit and i + 1 == limit:
                break

    @staticmethod
    def add_config(parser: argparse.ArgumentParser) -> None:
        IAIEnv.add_config(parser)
        parser.add_argument('--enable_rendering', type=int, default=0)
        parser.add_argument('--obs_only', type=int, default=0)
        parser.add_argument('--cache_in_memory', type=int, default=1)
        parser.add_argument('--load_cache_from', type=str, default='')
        parser.add_argument('--save_cache_to', type=str, default='')
        parser.add_argument('--save_to_disk_interval', type=int, default=15, help='The frequency we save to disk in'
                                                                                  'minute')
        parser.add_argument('--env_name', type=str, default='iai/GenericEnv-v0', help='The gym environment name to '
                                                                                      'build if env is not provided'
                                                                                      'in __init__')
