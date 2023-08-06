"""Утилиты"""
import sys,os
sys.path.append(os.path.join(os.getcwd(), '..'))
# sys.path.append('../')
import json

from common.errors import IncorrectDataRecievedError, NonDictInputError
from common.variables import MAX_MESSAGE_SIZE, ENCODING
from common.decos import log


@log
def get_message(sock):
    """Утилита приёма и декодирования сообщения принимает байты выдаёт словарь,
    если приняточто-то другое отдаёт ошибку значения
    :param sock:
    :return:
    """

    encoded_response = sock.recv(MAX_MESSAGE_SIZE)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        else:
            raise IncorrectDataRecievedError
    else:
        raise IncorrectDataRecievedError

@log
def send_message(sock, message):
    '''Утилита кодирования и отправки сообщения
    принимает словарь и отправляет его на сервер
    '''
    if not isinstance(message, dict):
        raise NonDictInputError
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)