from flask import Flask
from flask_apscheduler import APScheduler
from flask_cors import CORS

from controller.AdministratorController import *
from controller.LoginController import *
from controller.ManagerController import *
from controller.UserController import *
from controller.WaiterController import *


class APSchedulerJobConfig(object):
    SCHEDULER_API_ENABLED = True
    JOBS = [
        {
            'id': Tool.uniqueNum(),  # 任务唯一ID
            'func': 'service.UserService:requestScheduling',
            # 执行任务的function名称，service.UserService 就是 service下面的`UserService.py` 文件，
            # `requestScheduling` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
            'args': '',  # 如果function需要参数，就在这里添加
            'trigger': {
                'type': 'cron',  # 类型
                # 'day_of_week': "0-6", # 可定义具体哪几天要执行
                # 'hour': '*', # 小时数
                # 'minute': '1',
                'second': '*/3'  # "*/3" 表示每3秒执行一次，单独一个"3" 表示每分钟的3秒。
            }
        }
    ]


# 标记网页页面返回位置templates文件夹, 静态文件访问母路径static
app = Flask(__name__, template_folder='templates', static_url_path='/', static_folder='static')
CORS(app, supports_credentials=True)

if __name__ == '__main__':
    app.config.from_object(APSchedulerJobConfig)

    app.register_blueprint(login, url_prefix='/')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(waiter, url_prefix='/waiter')
    app.register_blueprint(manager, url_prefix='/manager')
    # app.register_blueprint(server, url_prefix='/main_machine')

    # 初始化Flask-APScheduler，定时任务
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    app.run(host='0.0.0.0', debug=True, port=5438, threaded=True)
