"""Файл дескрипторов"""
import ipaddress
import logging
import sys

# Инициализиция логера
# метод определения модуля, источника запуска.
if sys.argv[0].find('client') == -1:
    # если не клиент то сервер!
    logger = logging.getLogger('server')
else:
    # ну, раз не сервер, то клиент
    logger = logging.getLogger('client')


class Port:
    """
    Класс - Дескриптор для описания порта:
    """
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            logger.critical(
                f'Попытка запуска с указанием неподходящего порта {value}. '
                f'Допустимы адреса с 1024 до 65535.')
            sys.exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Ip:
    """
    Класс - верификации ip-адреса
    """
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if value == '':
            instance.__dict__[self.name] = value
            return

        # проверка ip-адреса
        try:
            ip = ipaddress.ip_address(value)
            instance.__dict__[self.name] = str(ip)
        except Exception:
            raise ValueError(f"IP address {value} is not valid")