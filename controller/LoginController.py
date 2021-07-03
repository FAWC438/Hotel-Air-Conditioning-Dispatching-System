import datetime

from flask import Blueprint, session, request, jsonify, render_template

from common import Tool
from entity.AirCondition import AirCondition
from entity.Roles import Role, User, Administrator, Waiter, Manager
from entity.Server import Server

login = Blueprint('login', __name__)


@login.route('/', methods=['Get'])
def index():
    return render_template('index.html')


@login.route("/login", methods=['Get'])
def loginFunction():
    role_num = int(request.args.get('role', -1))
    return_dict = {'message': '', 'redirect': '/'}
    # print(type(role_num))
    # print(Role.Administrator.value)
    # print(role_num == Role.Administrator.value)
    if role_num == Role.User:

        print(Server.instance())
        if not Server.instance().is_on:
            return_dict['message'] = 'Server has not been on yet. Please contact admin to turn it on'
            return return_dict

        for i in range(len(Server.instance().airCondition_list)):
            if not Server.instance().airCondition_list[i].is_open:
                room_num = i
                break
        else:
            room_num = -1

        if room_num == -1:
            return_dict['message'] = 'Sorry, there is no empty room.'
            return return_dict

        # 给客户分配房间
        target_air_condition = Server.instance().airCondition_list[room_num]
        assert isinstance(target_air_condition, AirCondition)
        new_user = User(Tool.uniqueNum(), target_air_condition)
        target_air_condition.user = new_user
        target_air_condition.is_open = True
        target_air_condition.using_info.append((datetime.datetime.now(), 0))

        return_dict['message'] = 'Welcome to the hotel!'
        return_dict['redirect'] = '/user?user_id=' + new_user.user_id

    elif role_num == Role.Administrator:
        # print('Administrator')
        admin_name = request.args.get('name', 'default admin')
        password = request.args.get('password', '123')
        for admin in Server.instance().administrator_list:
            if admin.name == admin_name:
                cur_admin = admin
                break
        else:
            cur_admin = Administrator(Tool.uniqueNum(), admin_name, password)
        return_dict['message'] = 'Welcome, Administrator: ' + admin_name
        return_dict['redirect'] = '/admin?admin_id=' + cur_admin.admin_id

    elif role_num == Role.Waiter:

        if not Server.instance().is_on:
            return_dict['message'] = 'Server has not been on yet. Please contact admin to turn it on'
            return return_dict

        waiter_name = request.args.get('name', 'default waiter')
        password = request.args.get('password', '123')
        for waiter in Server.instance().waiter_list:
            if waiter.name == waiter_name:
                cur_waiter = waiter
                break
        else:
            cur_waiter = Waiter(Tool.uniqueNum(), waiter_name, password)
        return_dict['message'] = 'Welcome, Waiter: ' + waiter_name
        return_dict['redirect'] = '/waiter?waiter_id=' + cur_waiter.waiter_id

    elif role_num == Role.Manager:

        if not Server.instance().is_on:
            return_dict['message'] = 'Server has not been on yet. Please contact admin to turn it on'
            return return_dict

        manager_name = request.args.get('name', 'default manager')
        password = request.args.get('password', '123')
        for manager in Server.instance().manager_list:
            if manager.name == manager_name:
                cur_manager = manager
                break
        else:
            cur_manager = Manager(Tool.uniqueNum(), manager_name, password)
        return_dict['message'] = 'Welcome, Manager: ' + manager_name
        return_dict['redirect'] = '/manager?manager_id=' + cur_manager.manager_id

    else:
        return_dict['message'] = 'Invalid role'
    return jsonify(return_dict)
