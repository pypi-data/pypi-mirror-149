import logging
from log_profile.logger_server import SERVER
from ipaddress import ip_address

logger = logging.getLogger(SERVER)


class Port:
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            print('Так нельзя!')
            sys.exit(1)
            logger.critical(
                        f'Попытка запуска сервера с указанием неподходящего порта '
                        f'{value}. Допустимые адреса с 1024 до 65535.')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


# class Address:
#     def __set__(self, instance, value):
#         print(value)
#         try:
#             ip_address(value)
#             instance.__dict__[self.name] = value
#         except:
#             print('так тоже нельзя')
#
#     def __set_name__(self, owner, name):
#         self.name = name
