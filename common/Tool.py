import random
from datetime import datetime
from typing import Optional

from entity.Roles import User, Administrator, Waiter, Manager
from entity.Server import Server

PersistencePath = 'D:/code/Software-Engineering/service/persistence'


def uniqueNum():
    """
    生成唯一的随机数用于ID号
    :return:随机数
    """
    for i in range(0, 10):
        nowTime = datetime.now().strftime("%M%S")  # 生成当前时间
        randomNum = random.randint(0, 99)  # 生成的随机整数
        if randomNum < 10:
            randomNum = str(0) + str(randomNum)
        return str(nowTime) + str(randomNum)


def getAirConditionByRoomId(roomId: str):
    for a in Server.instance().airCondition_list:
        if a.roomId == roomId:
            return a
    return None


def getUserById(user_id: str) -> Optional[User]:
    for i in Server.instance().user_list:
        if i.user_id == user_id:
            return i
    return None


def getAdminById(admin_id: str) -> Optional[Administrator]:
    for i in Server.instance().administrator_list:
        if i.admin_id == admin_id:
            return i
    return None


def getWaiterById(waiter_id: str) -> Optional[Waiter]:
    for i in Server.instance().waiter_list:
        if i.waiter_id == waiter_id:
            return i
    return None


def getManagerById(manager_id: str) -> Optional[Manager]:
    for i in Server.instance().manager_list:
        if i.manager_id == manager_id:
            return i
    return None
