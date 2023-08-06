import zmq
import flatbuffers
import logging
from iai_common.communications.utils import (
    get_message_body,
    build_clienthandshake,
    build_command,
    build_initialize,
    build_step,
)


class ZMQClient:
    """
    This class provides methods for establishing connections with the client
    and exchanging data using flatbuffers for serialization of data
    """
    def __init__(self, server_address):
        self._server_address = server_address
        self._context = zmq.Context.instance()
        self._socket = self._context.socket(zmq.REQ)
        self._context.setsockopt(
            zmq.LINGER, 100
        )
        self._socket.connect(server_address)
        logging.info(
            f"isp (Python): zmq.REP socket connected to server {self._server_address}"
        )

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        if not self._context.closed:
            self._socket.close()
            self._context.term()
            print(
                f"isp (Python): zmq.REP socket disconnected from server {self._server_address}"
            )

    def send_request(self, reply):
        self._socket.send(reply)

    def receive_reply(self):
        return self._socket.recv()


class ApiMessagingClient(ZMQClient):
    """
    The concrete class that handles handshaking and other communications to the zmq server
    """
    def __init__(self, server_address, client_name):
        super().__init__(server_address)
        self.client_name = client_name

    def client_handshake(self):
        print("-" * 10 + " Connecting to server " + "-" * 10)
        builder = flatbuffers.Builder(64)
        # construct MessageBody
        message = build_clienthandshake(builder, self.client_name)
        # construct Message
        self.send_request(message)

        try:
            reply = self.receive_reply()
            _, (server_name, model_name) = get_message_body(reply)
            print(f"Connected to {server_name}, with {model_name}")
            return True
        except Exception as error:
            logging.error("isp (Python): Unexpected reply to handshake." + repr(error))
            return False

    def initialize(
        self,
        scenario,
        world_parameters=None,
        vehicle_physics=None,
        scenario_parameters=None,
        sensors=None,
    ):
        builder = flatbuffers.Builder(64)
        message = build_initialize(builder, scenario,
                                   scenario_parameters=scenario_parameters,
                                   world_parameters=world_parameters,
                                   sensors=sensors)
        self.send_request(message)

    def get_reply(self):
        req = self.receive_reply()
        try:
            message_type, message = get_message_body(req)
            return message_type, message
        except RuntimeError as error:
            print("isp (Python): Unrecognizable Reply." + repr(error))
            return False

    def send_command(self, command_text, data=None):
        if data is None:
            data = {}
        builder = flatbuffers.Builder(64)
        message = build_command(builder, command_text, data)
        self.send_request(message)

    def listen(self):
        req = self.receive_reply()
        return req

    def send(self, message):
        try:
            self.send_request(message)
        except Exception as error:
            logging.error("isp (Python): ZMQ Failed" + repr(error))
            return False
