from datetime import datetime

from common.Tool import getUserById
from entity.AirCondition import AirCondition
from entity.Request import Request
from entity.Server import Server, Algorithm, Mode, WindLevel
from entity.Specification import Specification


def userRequestHandler(request: Request):
    """
    将用户请求放入请求队列，之所以要独立出来一个函数，是为了线程同步

    :param request:请求对象
    :return:
    """
    with Server.instance().request_lock:
        # 由于request_queue定时调度，需要线程锁
        Server.instance().request_queue.append(request)


def requestScheduling():
    """
    请求调度与执行

    :return:
    """

    with Server.instance().request_lock:  # 由于request_queue定时调度，需要线程锁
        for s in Server.instance().request_queue:
            print(s)

        # if Server.instance().request_queue is not None:
        #     Server.instance().request_queue = list(
        #         filter(lambda x: x.target_air_condition.is_open and not x.requestIsFinish(),
        #                Server.instance().request_queue))

        if Server.instance().is_on and Server.instance().request_queue != []:

            for a in Server.instance().airCondition_list:
                print(a)

            if Server.instance().scheduling_algorithm == Algorithm.Priority:
                # 对于相同房间的请求进行合并，这样就确保队列中一个房间只有一个对应的请求
                Server.instance().request_queue = requestMerge(Server.instance().request_queue)

                # 利用过滤器删除执行完成或是执行完成前空调就关闭的请求
                Server.instance().request_queue = list(
                    filter(lambda x: x.target_air_condition.is_open and not x.requestIsFinish(),
                           Server.instance().request_queue))
                #
                # 利用remove删除执行完成或是执行完成前空调就关闭的请求
                # 列表删除多个元素必须倒序
                # for i in range(len(Server.instance().request_queue) - 1, -1, -1):
                #     if not Server.instance().request_queue[i].target_air_condition.is_open or \
                #             Server.instance().request_queue[i].requestIsFinish():
                #         Server.instance().request_queue.remove(Server.instance().request_queue[i])

                # 反馈优先级，即等待越久的请求，其优先级会随时间变高
                for r in Server.instance().request_queue:
                    if float((r.arrive_time - Server.instance().SystemTimer).seconds) > 10:
                        r.priority -= 1

                Server.instance().request_queue.sort(key=lambda x: x.priority)

                for r in Server.instance().request_queue:
                    assert isinstance(r, Request)

                    target_room = r.target_air_condition
                    print(target_room.roomId + '号房间被调度')
                    target_room.scheduling_num += 1  # 被调度一次

                    if r.target_mode != -1:
                        target_room.mode = r.target_mode  # 先设置模式

                    if r.target_wind != -1:
                        target_room.cur_wind = r.target_wind  # 还需要设置风速
                        target_room.most_common_target_wind[r.target_wind] += 1  # 最常用目标风速再此统计
                        # target_room.target_wind = r.target_wind

                    if r.target_temp != -1 and isinstance(r.target_temp, int):
                        target_room.cur_temp = int(target_room.cur_temp)  # 权宜之计
                        if (target_room.mode == Mode.Cold and r.target_temp >= target_room.cur_temp) or (
                                target_room.mode == Mode.Hot and r.target_temp <= target_room.cur_temp):
                            target_room.cur_wind = WindLevel.NoWind
                            # 制冷目标温度却大于当前温度/制热目标温度却小于当前温度的情况，强制风速为0

                        target_room.most_common_target_temp[r.target_temp] += 1
                        # target_room.target_temp = r.target_temp

                        if r.target_temp < target_room.cur_temp:
                            # 目标温度小于当前温度
                            target_room.cur_temp -= target_room.cur_wind
                            if r.target_temp >= target_room.cur_temp:
                                target_room.cur_temp = r.target_temp
                                # target_room.target_wind = WindLevel.NoWind
                                target_room.reach_target_temp_num += 1
                            print(
                                'tariff: ' + str(Server.instance().tariff) + ' cur_wind: ' + str(target_room.cur_wind))
                            target_room.cur_price += (Server.instance().tariff * target_room.cur_wind)
                            target_room.total_price += (Server.instance().tariff * target_room.cur_wind)
                        elif r.target_temp > target_room.cur_temp:
                            # 目标温度大于当前温度
                            target_room.cur_temp += target_room.cur_wind
                            if r.target_temp <= target_room.cur_temp:
                                target_room.cur_temp = r.target_temp
                                # target_room.target_wind = WindLevel.NoWind
                                target_room.reach_target_temp_num += 1
                            target_room.cur_price += (Server.instance().tariff * target_room.cur_wind)
                            target_room.total_price += (Server.instance().tariff * target_room.cur_wind)
                    if r.requestIsFinish():
                        # 完成请求后房间空调应该无风，这样省电且不会产生没有请求却扣费的情况
                        r.target_air_condition.cur_wind = WindLevel.NoWind
            else:
                # TODO:时间片调度
                pass


def requestMerge(request_list: list):
    """
    请求合并

    :param request_list:欲合并的请求队列
    :return:合并后的请求队列
    """
    merged_list = []
    merged_room_id = []
    for i in range(len(request_list)):

        req_room = request_list[i].target_air_condition
        assert isinstance(req_room, AirCondition)

        if req_room.roomId in merged_room_id:
            # 同一个房间的请求已经被合并，无需再处理
            continue

        merged_room_id.append(req_room.roomId)  # 第一次合并时，记录被和并请求的房间
        earliest_time = request_list[i].arrive_time

        for j in range(i + 1, len(request_list)):
            cmp_room = request_list[j].target_air_condition
            assert isinstance(cmp_room, AirCondition)

            if req_room.roomId == cmp_room.roomId:
                if request_list[j].arrive_time <= earliest_time:
                    earliest_time = request_list[j].arrive_time
                    # request_list[i].arrive_time = request_list[j].arrive_time
                if request_list[j].arrive_time > request_list[i].arrive_time:
                    if request_list[j].target_temp != -1:
                        request_list[i].target_temp = request_list[j].target_temp
                    if request_list[j].target_wind != -1:
                        request_list[i].target_wind = request_list[j].target_wind
                    if request_list[j].target_mode != -1:
                        request_list[i].target_mode = request_list[j].target_mode
        request_list[i].arrive_time = earliest_time
        request_list[i].updatePriority()

        merged_list.append(request_list[i])
    return merged_list


def checkOut(user_id: str):
    """
    用户结算，这个方法会关闭空调并生成报表和目标用户绑定

    :param user_id:目标用户id
    :return:
    """
    user = getUserById(user_id)
    if user is None:
        return None
    target_room = user.air_condition
    assert isinstance(target_room, AirCondition)
    target_room.using_info.append((datetime.now(), 1))
    target_room.specifications_num += 1
    specification_price = target_room.cur_price
    specification_start_time = target_room.using_info[-2][0]
    specification_end_time = target_room.using_info[-1][0]
    target_room.reSet()
    user.specification = Specification(user.user_id, target_room.roomId, specification_start_time,
                                       specification_end_time, target_room.cur_wind, target_room.mode,
                                       Server.instance().tariff,
                                       specification_price)
    return user.specification
