import hashlib

from sqlalchemy import Column, String

# from models import Model
from models.base_model import SQLMixin, db


class User(SQLMixin, db.Model):
    """
    保存用户数据的 model
    """

    username = Column(String(50), nullable=False)
    password = Column(String(256), nullable=False)
    image = Column(String(100), nullable=False, default='/images/default.gif')
    signature = Column(String(256), nullable=False, default='TA的签名 —— 一个字都没找到呀 >_<')

    @classmethod
    def salted_password(cls, password, salt='$!@><?>HUI&DWQa`'):

        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def hashed_password(self, pwd):
        # 用 ascii 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # 返回摘要字符串
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form['username']
        if len(name) > 2 and User.one(username=name) is None:
            salted_password = User.salted_password(form['password'])
            register_form = dict(
                username=name,
                password=salted_password
            )
            u = User.new(register_form)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        user = User.one(username=form['username'])
        if user is not None and user.password == User.salted_password(form['password']):
            return user
        else:
            return None
