import json
import os
import sys
from socket import socket, AF_INET, SOCK_STREAM

from PyQt5.QtCore import pyqtSignal
from common.vars import ENCODING, MAX_PACKAGE_LENGTH

sys.path.append(os.path.join(os.getcwd(), '..'))


class App:
    # """Parent app class"""
    send_new_message = pyqtSignal(dict)
    message_205 = pyqtSignal()

    def __init__(self, current_socket=None):
        self.socket = current_socket if current_socket else socket(AF_INET, SOCK_STREAM)

    def send_msg(self, message, current_socket=None):
        """Sends a message in bytes form using a socket"""

        current_socket = current_socket if current_socket else self.socket
        json_msg = json.dumps(message)
        encoded_msg = json_msg.encode(ENCODING)
        current_socket.send(encoded_msg)

    def get_message(self, current_socket=None):
        """Receives data byte and transforms it into a dictionary"""

        current_socket = current_socket if current_socket else self.socket
        try:
            encoded_response = current_socket.recv(MAX_PACKAGE_LENGTH)
            if isinstance(encoded_response, bytes):
                json_response = encoded_response.decode(ENCODING)
                response = json.loads(json_response)
                if isinstance(response, dict):
                    return response
                raise ValueError
            raise ValueError

        except json.JSONDecodeError:
            return 'close'

        except ConnectionResetError:
            return 'close'

        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            return 'close'
