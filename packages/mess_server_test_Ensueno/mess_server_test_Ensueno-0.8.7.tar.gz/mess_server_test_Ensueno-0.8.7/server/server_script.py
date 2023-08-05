import logging
from time import sleep

from server.gui.server_window import ServerWindow
from server.server_classfile import Server


def server_start():
    logger = logging.getLogger('app.server_script')
    server = Server()
    server.start()
    logger.info('Сервер создан и готов к работе.')
    sleep(2)
    win = ServerWindow(server)
    win.server_window()


if __name__ == '__main__':
    server_start()
