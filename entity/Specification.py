"""
详单，一个用户一个，由服务员出示

"""
from datetime import datetime

from entity.Server import WindLevel, Mode


class Specification:
    def __init__(self, user_id: str, room_id: str, using_start_time: datetime, using_end_time: datetime,
                 wind_level: int, mode: int, tariff: float, price: float):
        """
        服务员详单

        :param user_id:用户id
        :param room_id:房间id
        :param using_start_time:开始使用时间
        :param using_end_time:使用结束时间
        :param wind_level:使用结束时风速
        :param mode:使用结束时控温模式
        :param tariff:使用结束时费率
        :param price:总花费
        """
        self.user_id = user_id
        self.room_id = room_id
        self.using_start_time = using_start_time.strftime('%Y-%m-%d %H:%M:%S')
        self.using_end_time = using_end_time.strftime('%Y-%m-%d %H:%M:%S')
        self.mode = Mode(mode).name
        self.tariff = "{:.2f}".format(tariff)
        self.price = "{:.2f}".format(price)

    def getDict(self):
        return {'user_id': self.user_id,
                'room_id': self.room_id,
                'using_start_time': self.using_start_time,
                'using_end_time': self.using_end_time,
                'mode': self.mode,
                'tariff': self.tariff,
                'price': self.price}
