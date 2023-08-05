import logging
import sys


class Port:
    """Universal descriptor for checking the validity of the Client and Server ports"""
    def __set__(self, instance, value):
        listen_port = value

        logger = logging.getLogger('app.server_script') if instance.name == 'Server' \
            else logging.getLogger('app.client_script')

        if isinstance(listen_port, int):
            if listen_port < 1024 or listen_port > 65535:
                logger.critical(f'Ошибка валидации порта. Число для порта не может '
                                f'быть меньше 1024 или больше 65535. Завершение работы.')
                sys.exit(1)
            else:
                logger.debug(f'Успешная валидация порта {listen_port}')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
