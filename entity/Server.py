import threading

from enum import IntEnum


class Mode(IntEnum):
    Cold = 0
    Hot = 1


class WindLevel(IntEnum):
    NoWind = 0
    Level_1 = 1
    Level_2 = 2
    Level_3 = 3


class Algorithm(IntEnum):
    Priority = 0
    RR = 1


class Server(object):
    """
    服务器，是单例模式
    """
    _instance_lock = threading.Lock()

    AirCondition_num = -1
    default_temp = -1
    default_mode = -1
    default_highest_temp = -1
    default_lowest_temp = -1
    default_wind_level = -1
    SystemTimer = None
    time_slot = -1
    scheduling_algorithm = -1
    tariff = -1

    airCondition_list = []
    user_list = []
    administrator_list = []
    waiter_list = []
    manager_list = []
    request_queue = []
    request_lock = threading.Lock()

    @classmethod
    def instance(cls, *args, **kwargs):
        with cls._instance_lock:
            if not hasattr(Server, '_instance'):
                Server._instance = Server()
                return Server._instance
            return Server._instance

    def __init__(self):
        self.is_on = False
