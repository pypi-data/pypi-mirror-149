from invertedai_simulate.utils import Resolution, PyGameWindow
from invertedai_simulate.zmq_client import ApiMessagingClient
from typing import Dict, Tuple, Any
import argparse
import numpy as np
import matplotlib.pyplot as plt
import gym
import pygame
import cv2
try:
  import google.colab
  IN_COLAB = True
except:
  IN_COLAB = False
import __main__ as main
if IN_COLAB or hasattr(main, '__file__'):
    from halo import Halo
else:
    from halo import HaloNotebook as Halo


Action = Tuple[float, float]
Obs = Dict[str, np.ndarray]


class ClientHandshakeError(Exception):
    pass


class ServerTimeoutError(Exception):
    pass


class IAIEnv(gym.Env):
    """
    A gym environment that connects to the iai server application running the simulation
    """
    def __init__(self, config):
        self.zmq_server_address = f"tcp://{config.zmq_server_address}"
        self.client_id = config.client_id
        self.remote = ApiMessagingClient(self.zmq_server_address, self.client_id)
        self.enable_progress_spinner = config.enable_progress_spinner
        for i in range(config.num_handshake_tries):
            if self.remote.client_handshake():
                break
        else:
            raise ClientHandshakeError
        self.done = None
        self.info = None
        self.reward = None
        self.obs = None
        self.pygame_window = None
        self.sensors_dict = None
        self.scale = None
        self.renderer = None
        self.render_sensors = None
        self.display_handle = None
        self.notebook_image = None

    def set_scenario(self, scenario_name, world_parameters=None, vehicle_physics=None, scenario_parameters=None,
                     sensors=None):
        """

        :param scenario_name:
        :type scenario_name:
        :param world_parameters:
        :type world_parameters:
        :param vehicle_physics:
        :type vehicle_physics:
        :param scenario_parameters:
        :type scenario_parameters:
        :param sensors:
        :type sensors:
        :return:
        :rtype:
        """
        self.sensors_dict = sensors
        with Halo(text=f'Loading: {scenario_name} scenario', spinner='dots', enabled=self.enable_progress_spinner):
            self.remote.initialize(scenario_name, world_parameters, vehicle_physics, scenario_parameters, sensors)
            _, message = self.remote.get_reply()
        return message

    def get_map(self):
        """
        Returns the map of the scenario in OSM format
        """
        raise NotImplementedError

    def set_goal_location(self):
        """
        Returns the current location of all agents
        """
        pass

    def reset(self, rand_seed=None):
        """
        Restarts the scenario
        :param rand_seed
        """
        if rand_seed is None:
            rand_seed = 0
        self.remote.send_command("reset", {'tensor': np.array(rand_seed)})
        _, message = self.remote.get_reply()
        self.obs = message
        return message

    def visualize_fig(self, fig):
        ax1 = fig.add_subplot(1, 2, 1)
        ax1.imshow(self.obs['front_image'].squeeze().permute(1, 2, 0))
        ax1.axis('off')
        ax2 = fig.add_subplot(1, 2, 2)
        ax2.imshow(self.obs['birdview_image'].squeeze().permute(1, 2, 0))
        ax2.axis('off')
        plt.ion()
        plt.show()
        plt.pause(0.001)


    def render_init(self, sensors_dict, renderer='pygame', scale=1, notebook_display=None, notebook_image=None):
        self.scale = scale
        self.renderer = renderer
        self.render_sensors = sensors_dict
        if renderer == 'notebook':
            assert notebook_display is not None
            assert notebook_image is not None
            self.display_handle = notebook_display(None, display_id=True)
            self.notebook_image = notebook_image
        elif renderer == 'pygame':
            width = np.sum([sensors_dict[sns]['resolution'].width*scale for sns in sensors_dict if sensors_dict[sns]['sensor_type']=='camera'])
            height = np.max([sensors_dict[sns]['resolution'].height*scale for sns in sensors_dict if sensors_dict[sns]['sensor_type']=='camera'])
            full_res = Resolution(width, height)
            pygame.init()
            self.pygame_window = PyGameWindow(full_res)


    def render(self, show=True):
      """
      """
      sensors_dict = self.render_sensors
      disp_img = np.concatenate(list(cv2.resize(self.obs['sensor_data'][name]['image'], None, fx=self.scale, fy=self.scale, interpolation=cv2.INTER_AREA) for name in sensors_dict if 'image' in self.obs['sensor_data'][name].keys()), axis=1)
      if show:
          if self.renderer == 'notebook':
              _, frame = cv2.imencode('.jpeg', disp_img)
              self.display_handle.update(self.notebook_image(data=frame.tobytes()))
              # self.display_handle.update(disp_img)
          elif self.renderer == 'pygame':
              self.pygame_window.render(disp_img)
              pygame.display.update()
          else:
              frame = disp_img
              cv2.imshow('Sensors', frame)
              c = cv2.waitKey(1)
      return disp_img


    def step(self, action: Action) -> Tuple[object, float, bool, dict]:
        """
        Accepts the next action of the ego vehicle and generates the next state of all
        the agents in the world
        :param action:
        :type action:
        :return:
        :rtype:
        """
        self.remote.send_command("step", {'step': action})
        _, message = self.remote.get_reply()
        self.obs = message['obs']
        self.reward = message['reward']
        self.done = message['done']
        self.info = message['info']
        return self.obs, self.reward, self.done, self.info

    def close(self):
        self.remote.close()

    def end_simulation(self):
        self.remote.send_command("end")
        message = self.remote.listen()
        return message.decode()

    def get_actions(self):
        self.remote.send_command("serverdrive", {'tensor': np.array(0)})
        message = self.remote.listen()
        return message.decode()

    @staticmethod
    def add_config(parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--num_handshake_tries', type=int, default=10)
        parser.add_argument('--zmq_server_address', type=str, default='localhost:5555')
        parser.add_argument('--client_id', type=str, default='0')
        parser.add_argument('--enable_progress_spinner', type=int, default=1)


gym.register('iai/GenericEnv-v0', entry_point=IAIEnv)
