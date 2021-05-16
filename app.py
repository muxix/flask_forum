import time

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import secret

from models.base_model import db
from models.user import User
from models.topic import Topic
from models.reply import Reply

from routes.index import main as index_routes
# from routes.board import main as board_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.message import main as message_routes
from routes.index import not_found


# @app.template_filter()
def count(input):
    return len(input)


def format_time(unix_timestamp):
    time_format = '%Y-%m-%d %H:%M:%S'
    localtime = time.localtime(unix_timestamp)
    formatted = time.strftime(time_format, localtime)
    return formatted


def register_routes(app):
    """
    注册蓝图
    """

    app.register_blueprint(index_routes)
    # app.register_blueprint(board_routes, url_prefix='/board')
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(message_routes, url_prefix='/message')


def configured_app():
    app = Flask(__name__)
    # 设置 secret_key 来使用 flask 自带的 session
    app.secret_key = secret.flask_session_secret_key

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@localhost/forum_data?charset=utf8mb4'.format(
        secret.database_password
    )
    # 新特性
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 与官方推荐初始化方式不同
    # 相当于延迟加载，避免循环引用
    db.init_app(app)
    # mail.init_app(app)
    register_routes(app)

    app.template_filter()(count)
    app.template_filter()(format_time)
    app.errorhandler(404)(not_found)

    # Add administrative views here
    admin = Admin(app, name='forum admin', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Topic, db.session))
    admin.add_view(ModelView(Reply, db.session))

    return app


# 运行代码
if __name__ == '__main__':
    # debug 模式可以自动加载代码的变动, 不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问本代码
    # 自动 reload jinja
    app = configured_app()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=2000,
        threaded=True,
    )
    app.run(**config)
