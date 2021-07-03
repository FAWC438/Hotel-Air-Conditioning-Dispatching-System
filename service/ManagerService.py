from datetime import datetime

from common import Tool
from entity.AirCondition import AirCondition
from entity.Server import Server
import pandas as pd
import math


def getManagerDailySheet() -> dict:
    """
    经理获得日报表，并利用pandas进行数据持久化

    :return:
    """
    sheet_dict = {}
    for room in Server.instance().airCondition_list:
        assert isinstance(room, AirCondition)
        # room_usage_count向上取整，即如果还有空调正在使用，则也计入使用空调的次数
        room_dict = {'room_id': room.roomId,
                     'room_usage_count': math.ceil(len(room.using_info) / 2),
                     'reach_target_temp_num': room.reach_target_temp_num,
                     'scheduling_num': room.scheduling_num,
                     'specifications_num': room.specifications_num,
                     'total_price': room.total_price}

        most_common_temp = Server.instance().default_temp
        tmp_counter = 0
        for temp, counter in room.most_common_target_temp.items():
            if tmp_counter <= counter != 0:
                most_common_temp = temp
                tmp_counter = counter
        room_dict['most_common_temp'] = most_common_temp

        most_common_wind = Server.instance().default_wind_level
        tmp_counter = 0
        for wind, counter in room.most_common_target_wind.items():
            if tmp_counter <= counter != 0:
                most_common_wind = wind
                tmp_counter = counter
        room_dict['most_common_wind'] = most_common_wind
        sheet_dict[room.roomId] = room_dict

    csv_path = Tool.PersistencePath + '/DailySheet/' + datetime.now().strftime('%Y-%m-%d,%H-%M-%S') + '.csv'
    pd.DataFrame(sheet_dict).to_csv(csv_path)
    return sheet_dict
