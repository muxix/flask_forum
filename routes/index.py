import os
import uuid

from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    send_from_directory
)

from models.user import User
from models.topic import Topic
from models.reply import Reply
from routes import current_user

# from werkzeug.utils import secure_filename

# import json
# import redis
# cache = redis.StrictRedis()

main = Blueprint('index', __name__)

"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 论坛首页
"""


@main.route("/")
def index():
    u = current_user()
    return render_template("index.html", user=u)


@main.route("/register", methods=['POST'])
def register():
    # form = request.args
    form = request.form
    # 用类函数来判断
    User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.index'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        # 转到 topic.index 页面
        return redirect(url_for('sim_bp_topic.index'))


def created_topic(user_id):
    # O(n)
    ts = Topic.all(user_id=user_id)
    return ts

    # k = 'created_topic_{}'.format(user_id)
    # if cache.exists(k):
    #     v = cache.get(k)
    #     ts = json.loads(v)
    #     return ts
    # else:
    #     ts = Topic.all(user_id=user_id)
    #     v = json.dumps([t.json() for t in ts])
    #     cache.set(k, v)
    #     return ts


def replied_topic(user_id):
    # O(m*n)
    rs = Reply.all(user_id=user_id)
    ts = []
    for r in rs:
        t = Topic.one(id=r.topic_id)
        ts.append(t)
    return ts

    # k = 'replied_topic_{}'.format(user_id)
    # if cache.exists(k):
    #     v = cache.get(k)
    #     ts = json.loads(v)
    #     return ts
    # else:
    #     rs = Reply.all(user_id=user_id)
    #     ts = []
    #     for r in rs:
    #         t = Topic.one(id=r.topic_id)
    #         ts.append(t)
    #
    #     v = json.dumps([t.json() for t in ts])
    #     cache.set(k, v)
    #
    #     return ts


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        ts_created = created_topic(u.id)
        ts_created.reverse()
        ts_replied = replied_topic(u.id)
        ts_replied.reverse()
        return render_template(
            'profile.html',
            user=u,
            ts_created=ts_created,
            ts_replied=ts_replied
        )


@main.route('/user/<int:id>')
def user_detail(id):
    u = User.one(id=id)
    if u is None:
        abort(404)
    else:
        ts_created = created_topic(u.id)
        ts_created.reverse()
        ts_replied = replied_topic(u.id)
        ts_replied.reverse()
        return render_template(
            'profile.html',
            user=u,
            ts_created=ts_created,
            ts_replied=ts_replied
        )


@main.route('/setting')
def setting():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('setting.html', user=u)


@main.route('/user/update', methods=['POST'])
def user_update():
    form = request.form.to_dict()
    u = current_user()
    if 'new_pass' in form:
        result = (User.salted_password(form['old_pass']) == u.password)
        if not result:
            return render_template('setting.html', user=u, stat='error', password_error='密码错误')
        form['password'] = User.salted_password(form['new_pass'])
        del form['old_pass']
        del form['new_pass']
    u.update(u.id, **form)
    return render_template('setting.html', user=u, stat='pass', message='修改成功')


@main.route('/image/add', methods=['POST'])
def avatar_add():
    file = request.files['avatar']

    # 不要直接拼接路由，不安全
    # ../../root/.ssh/authorized_keys
    # 处理方式一：secure_filename()
    # filename = secure_filename(file.filename)
    # 处理方式二：文件名存成随机数
    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)

    u = current_user()
    User.update(u.id, image='/images/{}'.format(filename))

    return redirect(url_for('.profile'))


@main.route('/images/<filename>')
def image(filename):
    # 不要如下直接拼接路由，不安全
    # path = os.path.join('images', filename)
    # return open(path, 'rb').read()
    return send_from_directory('images', filename)


def not_found(e):
    return render_template('404.html')


# def blueprint():
#     main = Blueprint('index', __name__)
#     main.route("/")(index)
#     main.route("/register", methods=['POST'])(register)
#     main.route("/login", methods=['POST'])(login)
#     main.route('/profile')(profile)
#     main.route('/user/<int:id>')(user_detail)
#
#     return main
