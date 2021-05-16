from flask import (
    render_template,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.topic import Topic
from models.board import Board

main = Blueprint('sim_bp_topic', __name__)


@main.route("/")
def index():
    board_id = int(request.args.get('board_id', -1))
    bs = Board.all()
    if board_id == -1:
        ts = Topic.all()
    else:
        ts = Topic.all(board_id=board_id)
    # token = new_csrf_token()
    # return render_template("topic/index.html", ts=ts, token=token, bs=bs, bid=board_id)
    return render_template("topic/index.html", ts=ts, bs=bs, bid=board_id)


@main.route('/<int:id>')
# 动态路由
def detail(id):
    # 浏览次数计算，不应该放在路由里面，路由里只应该有数据传递
    # 应该放在 topic model 里封装成方法
    m = Topic.get(id)
    return render_template("topic/detail.html", topic=m)


@main.route("/new")
def new():
    board_id = int(request.args.get('board_id'))
    bs = Board.all()
    u = current_user()
    if u:
        # token = new_csrf_token()
        # return render_template("topic/new.html", bs=bs, token=token, bid=board_id)
        return render_template("topic/new.html", bs=bs, bid=board_id)
    else:
        return redirect(url_for('index.index'))


@main.route("/add", methods=["POST"])
# @csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    if u:
        m = Topic.add(form, user_id=u.id)
        return redirect(url_for('.detail', id=m.id))
    else:
        return redirect(url_for('index.index'))


@main.route("/delete")
# @csrf_required
def delete():
    id = int(request.args.get('id'))
    u = current_user()
    print('删除 topic 用户是', u, id)
    Topic.delete(id)
    return redirect(url_for('.index'))
