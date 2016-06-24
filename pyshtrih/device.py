# -*- coding: utf-8 -*-


from protocol import Protocol
from handlers import COMMANDS
from commands import SupportedCommands


class Device(object):
    __metaclass__ = SupportedCommands

    SERIAL_TIMEOUT = 3
    WAIT_TIME = 0.01

    DEFAULT_CASHIER_PASSWORD = 1
    DEFAULT_ADMIN_PASSWORD = 30

    DEFAULT_MAX_LENGTH = 40

    CONTROL_TAPE = False
    CASH_TAPE = False

    # TODO: подумать можно ли избавиться от port и baudrate в пользу автоматического поиска устройства
    def __init__(self, port='/dev/ttyS0', baudrate=9600, timeout=None, password=None, admin_password=None):
        """
        :type port: str
        :param port: порт взаимодействия с устройством
        :type baudrate: int
        :param baudrate: скорость взаимодействия с устройством
        :type timeout: int
        :param timeout: время таймаута ответа устройства
        :type password: int
        :param password: пароль кассира
        :type admin_password: int
        :param admin_password: пароль администратора
        """

        self.protocol = Protocol(
            port,
            baudrate,
            timeout or self.SERIAL_TIMEOUT
        )

        self.password = password or self.DEFAULT_CASHIER_PASSWORD
        self.admin_password = admin_password or self.DEFAULT_ADMIN_PASSWORD

        self.connected = False

    def connect(self):
        """
        Подключиться к ККМ.
        """

        if self.connected:
            self.disconnect()
        self.protocol.connect()
        self.connected = True

    def disconnect(self):
        """
        Отключиться от ККМ.
        """

        if not self.connected:
            return
        self.protocol.disconnect()
        self.connected = False


class ShtrihFRK(Device):
    SUPPORTED_COMMANDS = (
        0x10, 0x11, 0x13, 0x15, 0x17, 0x19, 0x1A, 0x1B, 0x1E, 0x1F, 0x21, 0x22, 0x23, 0x25, 0x28, 0x29, 0x2B, 0x2D,
        0x2E, 0x40, 0x41, 0x50, 0x51, 0x80, 0x82, 0x85, 0x86, 0x87, 0x88, 0x8C, 0x8D, 0xB0, 0xC2, 0xFC
    )

    CONTROL_TAPE = True
    CASH_TAPE = True
    DEFAULT_MAX_LENGTH = 36


class ShtrihComboFRK(Device):
    SUPPORTED_COMMANDS = (
        0x10, 0x11, 0x13, 0x15, 0x17, 0x19, 0x1A, 0x1B, 0x1E, 0x1F, 0x21, 0x22, 0x23, 0x25, 0x28, 0x29, 0x2B, 0x2D,
        0x2E, 0x40, 0x41, 0x50, 0x51, 0x80, 0x82, 0x85, 0x86, 0x87, 0x88, 0x8C, 0x8D, 0xB0, 0xC2, 0xE0, 0xFC
    )

    CASH_TAPE = True
    DEFAULT_MAX_LENGTH = 48


ShtrihComboPTK = ShtrihComboFRK


class ShtrihAllCommands(Device):
    SUPPORTED_COMMANDS = COMMANDS.keys()