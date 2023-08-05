import json
import sys
import os

sys.path.append('../../../messenger/')
from server_dist.server.common.errors import *
from server_dist.server.common.log_decor import log
from server_dist.server.common.variables import *


@log
def get_message(client):
    """Функция приема сообщений"""
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    json_response = encoded_response.decode(ENCODING)
    response = json.loads(json_response)
    if isinstance(response, dict):
        return response
    else:
        raise TypeError


@log
def send_message(sock, message):
    """Функция отправки сообщений"""
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
