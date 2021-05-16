import secret

from sqlalchemy import create_engine

from app import configured_app
from models.base_model import db
from models.user import User
from routes.board import Board
from models.topic import Topic
from models.reply import Reply


def reset_database():
    url = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(
        secret.database_password
    )
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS forum_data')
        c.execute('CREATE DATABASE forum_data CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        c.execute('USE forum_data')

    db.metadata.create_all(bind=e)


def generate_fake_data():
    # 创建用户
    user1_form = dict(
        username='user1',
        password='123'
    )
    u1 = User.register(user1_form)
    user_form = dict(
        username='test',
        password='123'
    )
    User.register(user_form)

    # 创建板块
    board1_form = dict(
        title='交流'
    )
    b1 = Board.new(board1_form)
    board2_form = dict(
        title='灌水'
    )
    Board.new(board2_form)

    # 创建话题
    # 创建大规模文本假数据，将假数据放到单独文件里
    with open('markdown_demo.md', encoding='utf8') as f:
        content = f.read()
    topic_form = dict(
        title='markdown demo',
        content=content,
        board_id=b1.id
    )
    t = Topic.add(topic_form, u1.id)

    # 创建回复
    reply_form = dict(
        content='reply test',
        topic_id=t.id,
    )
    for j in range(3):
        Reply.add(reply_form, u1.id)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_data()
