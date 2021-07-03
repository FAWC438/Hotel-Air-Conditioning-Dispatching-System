from flask import Blueprint, session, request, jsonify, render_template, abort, Response

from common.Tool import getManagerById
from service.ManagerService import getManagerDailySheet

manager = Blueprint('manager', __name__)


@manager.route('/', methods=['Get'])
def managerIndex():
    cur_id = request.args.get('manager_id', '???')
    print(cur_id)
    return render_template('manager.html')


@manager.route('/dailySheet', methods=['Get'])
def getDailySheet():
    manager_id = request.args.get('manager_id', '???')
    target_manager = getManagerById(manager_id)
    if target_manager is None:
        abort(Response('Invalid manager id'))

    dailySheet_json_list = []
    for room_id, room_info in getManagerDailySheet().items():
        dailySheet_json_list.append(room_info)

    return jsonify({'message': dailySheet_json_list, 'redirect': '/manager?manager_id=' + manager_id})
