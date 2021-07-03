from enum import IntEnum

from entity.Server import Server


class Role(IntEnum):
    User = 0
    Administrator = 1
    Waiter = 2
    Manager = 3


class User:
    def __init__(self, user_id: str, room):
        self.user_id = user_id
        self.air_condition = room
        if self not in Server.instance().user_list:
            Server.instance().user_list.append(self)
        self.specification = None


class Administrator:
    def __init__(self, admin_id: str, name: str, password: str = '123'):
        self.admin_id = admin_id
        self.name = name
        self.password = password
        if self not in Server.instance().administrator_list:
            Server.instance().administrator_list.append(self)


class Waiter:
    def __init__(self, waiter_id: str, name: str, password: str = '123'):
        self.waiter_id = waiter_id
        self.name = name
        self.password = password
        self.user_spec_mapper = {}
        if self not in Server.instance().waiter_list:
            Server.instance().waiter_list.append(self)


class Manager:
    def __init__(self, manager_id: str, name: str, password: str = '123'):
        self.manager_id = manager_id
        self.name = name
        self.password = password
        if self not in Server.instance().manager_list:
            Server.instance().manager_list.append(self)
