from flask import Blueprint, session, request, jsonify, render_template, Response, abort, send_from_directory

from common.Tool import getUserById, getWaiterById
from service.UserService import checkOut
from service.WaiterService import persistenceSpecification

waiter = Blueprint('waiter', __name__)


@waiter.route('/', methods=['Get'])
def managerIndex():
    cur_id = request.args.get('waiter_id', '???')
    print(cur_id)
    return render_template('waiter.html')


@waiter.route('/specification', methods=['Get'])
def getSpecification():
    user_id = request.args.get('user_id', '???')
    target_user = getUserById(user_id)
    if target_user is None:
        abort(Response('Invalid user id'))

    waiter_id = request.args.get('waiter_id', '???')
    target_waiter = getWaiterById(waiter_id)
    if target_waiter is None:
        abort(Response('Invalid waiter id'))

    if target_user.specification is None:
        return jsonify({'message': 'User: ' + user_id + ' please check out your room',
                        'redirect': '/waiter?waiter_id=' + waiter_id})
    else:
        csv_path = persistenceSpecification(target_user.specification)
        target_waiter.user_spec_mapper[user_id] = csv_path
        return jsonify({'message': target_user.specification.getDict(),
                        'redirect': '/waiter?waiter_id=' + waiter_id})


@waiter.route('/checkOut', methods=['Get'])
def checkOutHandler():
    user_id = request.args.get('user_id', '???')
    target_user = getUserById(user_id)
    if target_user is None:
        abort(Response('Invalid user id'))

    waiter_id = request.args.get('waiter_id', '???')
    target_waiter = getWaiterById(waiter_id)
    if target_waiter is None:
        abort(Response('Invalid waiter id'))

    checkOut(user_id)
    return jsonify({'message': 'OK! Please use user\'s id to get Specification.',
                    'redirect': '/waiter?' + 'waiter_id=' + waiter_id + '&user_id=' + user_id})


@waiter.route('/specFile', methods=['Get'])
def getSpecFile():
    user_id = request.args.get('user_id', '???')
    target_user = getUserById(user_id)
    if target_user is None:
        abort(Response('Invalid user id'))

    waiter_id = request.args.get('waiter_id', '???')
    target_waiter = getWaiterById(waiter_id)
    if target_waiter is None:
        abort(Response('Invalid waiter id'))

    csv_path = target_waiter.user_spec_mapper.get(user_id, '')
    if csv_path == '':
        return jsonify({'message': 'No specification file! ',
                        'redirect': '/waiter?waiter_id=' + waiter_id})
    path_list = csv_path.strip().split('/')
    return send_from_directory(directory='/'.join(path_list[:-1]), filename=path_list[-1])
