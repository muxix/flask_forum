import time

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Query

db = SQLAlchemy()


class SQLMixin(object):
    query: Query
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_time = Column(Integer, default=int(time.time()))
    # updated_time = Column(Integer, default=int(time.time()))

    @classmethod
    def new(cls, form):
        m = cls()
        for name, value in form.items():
            setattr(m, name, value)

        # 原 m.save()
        db.session.add(m)
        db.session.commit()

        return m

    @classmethod
    def delete(cls, id):
        cls.query.filter_by(id=id).delete()
        db.session.commit()

    @classmethod
    def update(cls, id, **kwargs):
        m = cls.query.filter_by(id=id).first()
        for name, value in kwargs.items():
            setattr(m, name, value)

        # 原 m.save()
        db.session.add(m)
        db.session.commit()

    @classmethod
    def all(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).all()
        return ms

    @classmethod
    def one(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).first()
        return ms

    @classmethod
    def columns(cls):
        return cls.__mapper__.c.items()

    def __repr__(self):
        """
        魔法方法
        得到类的 字符串表达 形式
        用 self.columns() 改写
        """
        name = self.__class__.__name__
        s = ''
        for attr, column in self.columns():
            if hasattr(self, attr):
                v = getattr(self, attr)
                s += '{}: ({})\n'.format(attr, v)
        return '< {}\n{} >\n'.format(name, s)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        d = dict()
        for attr, column in self.columns():
            if hasattr(self, attr):
                v = getattr(self, attr)
                d[attr] = v
        return d


class TestUser(SQLMixin, db.Model):
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)


if __name__ == '__main__':
    db.create_all()
    form = dict(
        username='123',
        password='456',
    )
    u = TestUser.new(form)
    print(u)
    u = TestUser.one(username='123')
    print(u)
