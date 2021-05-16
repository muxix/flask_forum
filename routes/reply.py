from flask import (
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import current_user

from models.user import User
from models.reply import Reply
from models.message import Messages

main = Blueprint('sim_bp_reply', __name__)


def users_from_content(content):
    # 内容 @用户 内容
    # 用户名本身不能含有空格
    parts = content.split()
    users = []

    for p in parts:
        if p.startswith('@'):
            username = p[1:]
            u = User.one(username=username)
            print('users_from_content <{}> <{}> <{}>'.format(username, p, parts))
            if u is not None:
                users.append(u)

    return users


def send_message(sender, receivers, reply_link, reply_content):
    print('send_message', sender, receivers, reply_content)
    content = '链接：{}\n内容：{}'.format(
        reply_link,
        reply_content
    )
    for r in receivers:
        form = dict(
            title='{} @ 了你'.format(sender.username),
            content=content,
            sender_id=sender.id,
            receiver_id=r.id
        )
        Messages.new(form)


@main.route("/add", methods=["POST"])
def add():
    form = request.form.to_dict()
    u = current_user()
    if u:
        content = form['content']
        users = users_from_content(content)
        send_message(u, users, request.referrer, content)

        m = Reply.add(form, user_id=u.id)
        return redirect(url_for('sim_bp_topic.detail', id=m.topic_id))
    else:
        return redirect(url_for('index.index'))
