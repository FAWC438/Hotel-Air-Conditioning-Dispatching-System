from flask import Blueprint, session, request, jsonify, render_template, Response, abort, json

from common.Tool import getAdminById
from entity.Server import Server, Mode, WindLevel, Algorithm
from service.AdministratorService import initServer, getMonitor

admin = Blueprint('admin', __name__)


@admin.route('/', methods=['Get'])
def adminIndex():
    cur_id = request.args.get('admin_id', '???')
    print(cur_id)
    return render_template('admin.html')


@admin.route('/initServer', methods=['Get'])
def init():
    admin_id = request.args.get('admin_id', '???')
    target_user = getAdminById(admin_id)
    if target_user is None:
        abort(Response('Invalid admin id'))
    return_dict = {'message': '', 'redirect': '/admin?admin_id=' + admin_id}
    # if not Server.instance().is_on:
    AirCondition_num = int(request.args.get('AirCondition_num', 3))
    default_temp = request.args.get('default_temp', 26)
    default_mode = int(request.args.get('default_mode', Mode.Cold))
    default_highest_temp = int(request.args.get('default_highest_temp', 31))
    default_lowest_temp = int(request.args.get('default_lowest_temp', 18))
    default_wind_level = int(request.args.get('default_wind_level', WindLevel.NoWind))
    time_slot = int(request.args.get('time_slot', 2))
    scheduling_algorithm = int(request.args.get('scheduling_algorithm', Algorithm.Priority))
    tariff = float(request.args.get('tariff', 1.0))
    initServer(AirCondition_num, default_temp, default_mode, default_highest_temp, default_lowest_temp,
               default_wind_level, time_slot, scheduling_algorithm, tariff)

    return_dict['message'] = 'Server init OK!'
    print(Server.instance())
    return jsonify(return_dict)


@admin.route('/allRoomInfo', methods=['Get'])
def allRoomInfo():
    admin_id = request.args.get('admin_id', '???')
    target_admin = getAdminById(admin_id)
    if target_admin is None:
        abort(Response('Invalid admin id'))

    # 这里的json是狗屎
    monitor_json_list = []
    for room_id, room_info in getMonitor().items():
        monitor_json_list.append({'room_id': room_id, 'room_info': room_info})

    return jsonify({'message': monitor_json_list, 'redirect': '/admin?admin_id=' + admin_id})
