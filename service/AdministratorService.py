from datetime import datetime

from entity.AirCondition import AirCondition
from entity.Server import Server


def initServer(AirCondition_num: int, default_temp: int, default_mode: int, default_highest_temp: int,
               default_lowest_temp: int, default_wind_level: int, time_slot: int, scheduling_algorithm: int,
               tariff: float):
    """
    初始化服务器

    :param tariff: 费率，是一个0至1的小数，乘以风速就是单位时间费用
    :param scheduling_algorithm: 请求调度算法
    :param time_slot: 时间片
    :param AirCondition_num:空调/房间数量，即服务对象数量
    :param default_temp:默认温度
    :param default_mode:默认温控模式
    :param default_highest_temp:最高温度
    :param default_lowest_temp:最低温度
    :param default_wind_level:默认风量
    :return:
    """
    Server.instance().AirCondition_num = AirCondition_num
    Server.instance().default_temp = default_temp
    Server.instance().default_mode = default_mode
    Server.instance().default_highest_temp = default_highest_temp
    Server.instance().default_lowest_temp = default_lowest_temp
    Server.instance().default_wind_level = default_wind_level
    Server.instance().is_on = True
    Server.instance().SystemTimer = datetime.now()
    Server.instance().time_slot = time_slot
    Server.instance().scheduling_algorithm = scheduling_algorithm
    if tariff > 1.0:
        Server.instance().tariff = 1.0
    elif tariff < 0.0:
        Server.instance().tariff = 0.0
    else:
        Server.instance().tariff = tariff

    print('init Server.instance().tariff: ' + str(Server.instance().tariff))

    Server.instance().airCondition_list = [
        AirCondition(default_temp, default_mode, default_highest_temp, default_lowest_temp, default_wind_level)
        for _ in range(AirCondition_num)]


def getMonitor() -> dict:
    """
    管理员获得监视报表

    :return:
    """
    monitor_dict = {}
    for room in Server.instance().airCondition_list:
        monitor_dict[room.roomId] = room.getDict()
    return monitor_dict
