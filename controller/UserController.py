from flask import Blueprint, session, request, jsonify, render_template, abort, Response
from datetime import datetime

from common.Tool import getUserById
from entity.Request import Request
from entity.Server import Server
from service.UserService import userRequestHandler, checkOut

user = Blueprint('user', __name__)


@user.route('/', methods=['Get'])
def userIndex():
    user_id = request.args.get('user_id', '???')
    print(user_id)
    return render_template('user.html')


@user.route('/roomInfo', methods=['Get'])
def getRoomInfo():
    user_id = request.args.get('user_id', '???')
    target_user = getUserById(user_id)
    if target_user is None:
        abort(Response('Invalid user id'))
    return jsonify({'message': target_user.air_condition.getDict(), 'redirect': '/user?user_id=' + user_id})


@user.route('/request', methods=['Get'])
def requestHandler():
    user_id = request.args.get('user_id', '???')
    target_user = getUserById(user_id)
    if target_user is None:
        abort(Response('Invalid user id'))
    target_temp = int(request.args.get('temp', -1))
    if target_temp > Server.instance().default_highest_temp or target_temp < Server.instance().default_lowest_temp:
        target_temp = -1

    target_wind = int(request.args.get('wind', -1))
    if target_wind > 3 or target_wind < 0:
        target_wind = -1

    target_mode = int(request.args.get('mode', -1))
    if target_mode != 0 and target_mode != 1:
        target_mode = -1

    if target_temp != -1:
        target_user.air_condition.target_temp = target_temp
    # if target_wind != -1:
    #     target_user.air_condition.target_wind = target_wind

    req = Request(datetime.now(), target_user.air_condition, int(target_temp), int(target_wind), int(target_mode))
    userRequestHandler(req)
    return jsonify({'message': 'OK!', 'redirect': '/user?user_id=' + user_id})


@user.route('/checkOut', methods=['Get'])
def checkOutHandler():
    user_id = request.args.get('user_id', '???')
    target_user = getUserById(user_id)
    if target_user is None:
        abort(Response('Invalid user id'))
    checkOut(user_id)
    return jsonify({'message': 'OK! Please find the waiter and show your user id to get Specification.',
                    'redirect': '/user?user_id=' + user_id})
