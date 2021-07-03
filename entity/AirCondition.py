from common import Tool
from entity.Server import Server, WindLevel, Mode


class AirCondition:
    def __init__(self, default_temp: int, default_mode: int, default_highest_temp: int,
                 default_lowest_temp: int, default_wind_level: int, user=None):
        """
                空调（房间）对象

        :param user:使用该空调的用户对象
        :param default_temp:默认温度
        :param default_mode:默认控温模式
        :param default_highest_temp:默认最高温度
        :param default_lowest_temp:默认最低温度
        :param default_wind_level:默认风速
        """
        self.roomId = Tool.uniqueNum()
        self.cur_temp = default_temp
        self.target_temp = default_temp
        self.cur_wind = default_wind_level
        # self.target_wind = default_wind_level
        self.is_open = False
        self.using_info = []
        # usingInfo是一个元素为二元组的列表，二元组的第一个元素为时间戳，第二个元素为整数，0代表开启，1代表关闭
        # 例如，usingInfo = [(datetime(2021-6-4 21:00:01),0),(datetime(2021-6-4 21:00:04),1),
        # (datetime(2021-6-4 21:00:07),0),(datetime(2021-6-4 21:00:10),1)]，
        # 这表示该空调在时间1被开启，时间4被关闭；时间7被重新开启，时间10被再次关闭
        self.mode = default_mode
        self.user = user  # 存储使用该空调的用户对象
        self.most_common_target_temp = dict(
            zip([i for i in range(default_lowest_temp, default_highest_temp + 1)],
                [0 for _ in range(default_lowest_temp, default_highest_temp + 1)]))  # 最常用目标温度，该值只会在执行请求的时候增长
        self.most_common_target_wind = dict(zip([i for i in range(4)], [0 for _ in range(4)]))  # 最常用目标风速，该值只会在执行请求的时候增长
        self.reach_target_temp_num = 0
        self.scheduling_num = 0
        self.specifications_num = 0
        self.cur_price = 0.0
        self.total_price = 0.0

    def __str__(self):
        return str(self.getDict())

    def getDict(self) -> dict:
        user_id = ''
        if self.user is not None:
            user_id = self.user.user_id
        return {'room_id': self.roomId, 'is_on': str(self.is_open), 'user_id': user_id, 'cur_temp': str(self.cur_temp),
                'target_temp': str(self.target_temp),
                'cur_wind': str(WindLevel(self.cur_wind).name),
                'mode': str(Mode(self.mode).name),
                'cur_price': "{:.2f}".format(self.cur_price)}

    def reSet(self):
        """
        重置空调，用于空调关闭时

        :return:
        """
        self.cur_temp = Server.instance().default_temp
        self.target_temp = Server.instance().default_temp
        self.cur_wind = Server.instance().default_wind_level
        # self.target_wind = Server.instance().default_wind_level
        self.mode = Server.instance().default_mode
        self.is_open = False
        self.cur_price = 0.0
        self.user = None
