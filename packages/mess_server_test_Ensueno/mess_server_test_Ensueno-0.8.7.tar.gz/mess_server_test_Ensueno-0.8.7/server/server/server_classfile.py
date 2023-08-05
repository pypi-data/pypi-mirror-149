import argparse
import binascii
import configparser
import hmac
import logging
import os
import sys
import threading
from select import select

from server.db.server_db import Storage
from common.decorators import Log
from common.descriptors import Port
from common.metaclasses import AppMaker
from common.parent_classfile import App
from common.vars import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DATA, MESSAGE_TEXT, MESSAGE, SENDER, DESTINATION, \
    EXIT, GET_CONTACTS, RESPONSE_202, RESPONSE_400, RESPONSE_511, RESPONSE_200, RESPONSE_205, RESPONSE_210,  \
    LIST_INFO, ADD_CONTACT, REMOVE_CONTACT, USERS_REQUEST, DEFAULT_PORT, PUBLIC_KEY, PUBLIC_KEY_REQUEST


@Log()
class Server(threading.Thread, App, metaclass=AppMaker):
    # """Child class for creating a server"""
    port = Port()

    def __init__(self):
        App.__init__(self)
        super().__init__()
        self.name = 'Server'
        self.address = None
        self.port = None
        self.logger = logging.getLogger('app.server_script')
        self.parser = argparse.ArgumentParser()
        self.messages_list = []
        self.client_list = []
        self.ready_to_input = []
        self.ready_to_output = []
        self.error_data = []
        self.client_names = dict()
        self.new_connection = False
        self.conflag_lock = threading.Lock()
        self.database = None
        self.config = None
        self.thread_run = True
        self.client_digest = {}

    def config_load(self):
        self.config = configparser.ConfigParser()
        dir_path = os.getcwd()
        self.config.read(f"{dir_path}/{'server.ini'}")

        if 'SETTINGS' not in self.config:
            self.config.add_section('SETTINGS')
            self.config.set('SETTINGS', 'Default_port', str(DEFAULT_PORT))
            self.config.set('SETTINGS', 'Listen_Address', '')
            self.config.set('SETTINGS', 'Database_path', '')
            self.config.set('SETTINGS', 'Database_file', 'server_database.db3')

    def server_parse_args(self):
        """Retrieves port and address from command line arguments"""
        self.parser.add_argument('-p', default=self.config['SETTINGS']['Default_port'], type=int, nargs='?')
        self.parser.add_argument('-a', default=self.config['SETTINGS']['Listen_Address'], nargs='?')
        namespace = self.parser.parse_args(sys.argv[1:])

        try:
            self.port = namespace.p
        except AttributeError:
            self.logger.critical(f'Ошибка валидации порта. Парсер аргументов командной'
                                 f'строки не обнаружил атрибута \'p\' '
                                 f'Завершение работы.')
            sys.exit(1)

        self.address = self.validate_address(namespace)
        self.logger.debug(f'Сервер распарсил адрес {self.address} и порт {self.port}')

    def validate_address(self, namespase_obj):
        """Port address validation"""

        try:
            listen_address = namespase_obj.a
            self.logger.debug(f'Успешная валидация адреса {listen_address}')
            return listen_address
        except AttributeError:
            self.logger.critical(f'Ошибка валидации адреса. Парсер аргументов командной'
                                 f'строки не обнаружил атрибута \'a\' '
                                 f'Завершение работы.')
            sys.exit(1)

    def database_load(self):

        self.database = Storage(os.path.join(self.config['SETTINGS']['Database_path'],
                                             self.config['SETTINGS']['Database_file']))
        print(f'Подключена база данных {self.config["SETTINGS"]["Database_file"]}')
        self.logger.debug(f'Подключена база данных {self.config["SETTINGS"]["Database_file"]}')

    def bind_and_listen(self):
        """Binding a socket to port and address and listening for a connection"""
        try:
            self.socket.bind((self.address, self.port))
            self.logger.debug(f'Привязан сокет к адресу {(self.address, self.port)}')
        except OSError as e:
            self.logger.critical(f'Произошла критическая ошибка: {e.strerror}. Сервер завершил работу.')
            sys.exit(1)

        self.socket.settimeout(0.5)
        self.socket.listen(MAX_CONNECTIONS)
        self.logger.debug('Сервер прослушивает соединение. Ожидание клиентов.')
        print(f'Сервер готов к работе. Настройки адреса: {self.address} и порта: {self.port}')

    def accept_and_exchange(self):
        """Accepts a connection request and initiates a message exchange"""
        while self.thread_run:
            try:
                client, client_address = self.socket.accept()
                self.logger.info(f'Успешное соединение с адресом {client_address}')
                self.client_list.append(client)
                print(f'В список клиентов добавлен клиент {client.getpeername()}')
            except OSError:
                pass

            try:
                if self.client_list:
                    self.ready_to_input, self.ready_to_output, self.error_data = select(self.client_list,
                                                                                        self.client_list, [], 0)
            except OSError as err:
                self.logger.error(f'Ошибка работы с сокетами: {err.errno}')

            # без этой проверки на то, что последний сокет закрыт,
            # при закрытии всех клиентских консолей сервер будет
            # висеть в бесконечной ошибке
            if self.ready_to_input:
                if len(self.ready_to_input) == 1 and self.ready_to_input[0].fileno() == -1:
                    self.ready_to_input.clear()
            self.receiving_msg_and_reply()

    def remove_client(self, client):
        try:
            for client_name in self.client_names:
                if self.client_names[client_name] == client:
                    self.database.logout_user(client_name)
                    del self.client_names[client_name]
                    break
            self.client_list.remove(client)
            client.close()
        except Exception:
            pass

    def receiving_msg_and_reply(self):
        """Receives messages from outgoing clients, sends a response"""

        if self.ready_to_input:
            for non_empty_client in self.ready_to_input:
                try:
                    msg_from_client = self.get_message(current_socket=non_empty_client)
                    self.logger.info(f'Принято сообщение от клиента {non_empty_client}')
                    self.send_reply(msg_from_client, non_empty_client)
                    self.logger.info(f'Отправлен ответ сервера клиенту {non_empty_client}')
                except Exception as e:
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(e).__name__, e.args)
                    print(message)
                    self.logger.error(message)
                    self.remove_client(non_empty_client)

            if self.messages_list:
                for msg in self.messages_list:
                    try:
                        self.mailing_messages(msg)
                    except Exception:
                        if msg[DESTINATION] in self.client_names:
                            self.logger.info(f'Отсутствует связь с клиентом {msg[DESTINATION]}')
                            self.client_list.remove(self.client_names[msg[DESTINATION]])
                            del self.client_names[msg[DESTINATION]]
                            self.database.logout_user(msg[DESTINATION])

                self.messages_list.clear()

    def mailing_messages(self, message):
        """Sends messages to clients who receive messages or sends a rejection to the client
         if the recipient does not exist"""

        if message[DESTINATION] in self.client_names and \
                self.client_names[message[DESTINATION]] in self.ready_to_output:
            try:
                self.send_msg(message, current_socket=self.client_names[message[DESTINATION]])
                self.logger.info(f'Пользователь {message[SENDER]} отправил сообщение для {message[DESTINATION]}.')
                return
            except OSError:
                self.remove_client(message[DESTINATION])
        return

    def send_reply(self, message, client, response=RESPONSE_200):
        """Accepts a client message and forms a response"""

        if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
                and USER in message:
            response, msg, digest = self.authorize_user(message, client)
            username = message[USER][ACCOUNT_NAME]
            self.client_digest[username] = digest

            self.logger.debug(msg)

        elif RESPONSE in message and message[RESPONSE] == 511:
            client_digest = binascii.a2b_base64(message[DATA])
            username = message[USER][ACCOUNT_NAME]
            digest = self.client_digest[username]
            if hmac.compare_digest(digest, client_digest):
                self.client_names[username] = client
                client_ip, client_port = client.getpeername()
                self.database.login_user(username, client_ip,
                                         client_port, message[USER][PUBLIC_KEY])
                del self.client_digest[username]
            else:
                response = RESPONSE_400
                response[ERROR] = 'Неверный пароль.'

        elif ACTION in message and message[ACTION] == MESSAGE and \
                DESTINATION in message and TIME in message \
                and SENDER in message and MESSAGE_TEXT in message:
            if message[DESTINATION] in self.client_names:
                if self.client_names[message[DESTINATION]] in self.ready_to_output:
                    self.messages_list.append(message)
                    self.database.counting_messages(message[SENDER], message[DESTINATION])
                elif self.client_names[message[DESTINATION]] not in self.ready_to_output:
                    self.logger.error(f'Связь с клиентом {message[DESTINATION]} была потеряна. '
                                      f'Соединение закрыто, доставка невозможна.')
                    self.remove_client(self.names[message[DESTINATION]])
                else:
                    self.logger.error(
                        f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
                        f'отправка сообщения невозможна.')
                return
            else:
                response = RESPONSE_400
                response[ERROR] = 'Пользователь не зарегистрирован на сервере.'

        elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message and \
                self.client_names[message[ACCOUNT_NAME]] == client:
            self.remove_client(client)
            with self.conflag_lock:
                self.new_connection = True
            return

        elif ACTION in message and message[ACTION] == GET_CONTACTS and USER in message and \
                self.client_names[message[USER]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = [user[0] for user in self.database.show_contacts(message[USER])]

        elif ACTION in message and message[ACTION] == ADD_CONTACT and ACCOUNT_NAME in message and USER in message \
                and self.client_names[message[USER]] == client:
            self.database.add_contacts(message[USER], message[ACCOUNT_NAME])
            response[LIST_INFO] = ['add_contact_reply']

        elif ACTION in message and message[ACTION] == REMOVE_CONTACT and ACCOUNT_NAME in message and USER in message \
                and self.client_names[message[USER]] == client:
            self.database.remove_contacts(message[USER], message[ACCOUNT_NAME])
            response[LIST_INFO] = ['remove_contact_reply']

        elif ACTION in message and message[ACTION] == USERS_REQUEST and ACCOUNT_NAME in message \
                and self.client_names[message[ACCOUNT_NAME]] == client:
            response = RESPONSE_202
            response[LIST_INFO] = [user[0]
                                   for user in self.database.show_users_list()]

        elif ACTION in message and message[ACTION] == PUBLIC_KEY_REQUEST and ACCOUNT_NAME in message:
            response = RESPONSE_511
            response[DATA] = self.database.get_pubkey(message[ACCOUNT_NAME])
            if not response[DATA]:
                response = RESPONSE_400
                response[ERROR] = 'Нет публичного ключа для данного пользователя'

        else:
            response = RESPONSE_400
            response[ERROR] = 'Bad Request'

        try:
            self.send_msg(response, current_socket=client)
            if message and ACTION in message:
                if message[ACTION] == PRESENCE:
                    with self.conflag_lock:
                        self.new_connection = True
        except OSError:
            self.logger.debug('OS Error')
            pass
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            msg = template.format(type(ex).__name__, ex.args)
            print(msg)

    def authorize_user(self, message, digest=None):
        response = RESPONSE_400
        self.logger.debug(f'Авторизация клиента {message[USER]}')
        if message[USER][ACCOUNT_NAME] in self.client_names.keys():
            response[ERROR] = 'Имя пользователя уже занято.'
            msg = f'Имя пользователя уже занято, отправка {response}'
        elif not self.database.check_user(message[USER][ACCOUNT_NAME]):
            response[ERROR] = 'Пользователь не зарегистрирован.'
            msg = f'Пользователь не зарегистрирован, отправка {response}'
        else:
            self.logger.debug('Пользователь определен, проверка пароля.')
            response = RESPONSE_511
            random_str = binascii.hexlify(os.urandom(64))
            response[DATA] = random_str.decode('ascii')
            hash = hmac.new(self.database.get_hash(message[USER][ACCOUNT_NAME]), random_str, 'MD5')
            digest = hash.digest()
            msg = f'Сообщение для авторизации - {response}'
        return response, msg, digest

    def service_update_lists(self):
        for client in self.client_names:
            try:
                self.send_msg(RESPONSE_205, current_socket=self.client_names[client])
            except OSError:
                self.remove_client(self.client_names[client])
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                msg = template.format(type(ex).__name__, ex.args)
                print(msg)

    def run(self):
        self.config_load()
        self.server_parse_args()
        self.database_load()
        self.bind_and_listen()
        self.accept_and_exchange()
