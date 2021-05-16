from flask import (
    render_template,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.message import Messages

# from flask_mail import Message, Mail
# from config import admin_mail

main = Blueprint('message', __name__)
# mail = Mail()


@main.route("/add", methods=["POST"])
def add():
    form = request.form.to_dict()
    receiver = User.one(username=form['receiver'])
    form['receiver_id'] = receiver.id
    u = current_user()
    form['sender_id'] = u.id

    # 发邮件
    # r = User.one(id=form['receiver_id'])
    # m = Message(
    #     subject=form['title'],
    #     body=form['content'],
    #     sender=admin_mail,
    #     recipients=[r.email]
    # )
    # mail.send(m)

    Messages.new(form)
    return redirect(url_for('.index'))


@main.route('/')
def index():
    u = current_user()
    if u:
        sent_messages = Messages.all(sender_id=u.id)
        received_messages = Messages.all(receiver_id=u.id)

        t = render_template(
            'message/index.html',
            send=sent_messages,
            received=received_messages,
        )
        return t
    else:
        return redirect(url_for('index.index'))


@main.route('/view/<int:id>')
def view(id):
    message = Messages.one(id=id)
    u = current_user()
    # if u.id == message.receiver_id or u.id == message.sender_id:
    if u.id in [message.receiver_id, message.sender_id]:
        s = User.one(id=message.sender_id)
        sender = s.username
        r = User.one(id=message.receiver_id)
        receiver = r.username
        return render_template('message/detail.html', message=message, sender=sender, receiver=receiver)
    else:
        return redirect(url_for('.index'))
