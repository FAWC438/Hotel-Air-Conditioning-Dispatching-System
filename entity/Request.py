"""
用户请求类

"""
from datetime import datetime

from entity.AirCondition import AirCondition
from entity.Server import Server, WindLevel, Mode


class Request:
    def __init__(self, arrive_time: datetime, target_air_condition: AirCondition, target_temp: int = -1,
                 target_wind: int = -1,
                 target_mode: int = -1):
        # -1代表没有相关请求

        self.arrive_time = arrive_time
        self.target_air_condition = target_air_condition
        self.priority = int((arrive_time - Server.instance().SystemTimer).seconds)  # 请求的优先级为请求发出时间减去服务器开启时间，即该数字小优先级越高

        if Server.instance().default_lowest_temp <= target_temp <= Server.instance().default_highest_temp:
            self.target_temp = target_temp
        else:
            self.target_temp = -1

        if WindLevel.NoWind <= target_wind <= WindLevel.Level_3:
            self.target_wind = target_wind
        else:
            self.target_wind = -1

        if target_mode == Mode.Cold or target_mode == Mode.Hot:
            self.target_mode = target_mode
        else:
            self.target_mode = -1

    def __str__(self):
        return str({'arrive_time': self.arrive_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'room_id': self.target_air_condition.roomId, 'priority': self.priority,
                    'target_temp': self.target_temp, 'target_wind': self.target_wind, 'target_mode': self.target_mode})

    def requestIsFinish(self):
        if self.target_air_condition.cur_temp == self.target_temp or self.target_temp == -1:
            return True
        return False

    def updatePriority(self):
        self.priority = int((self.arrive_time - Server.instance().SystemTimer).seconds)
