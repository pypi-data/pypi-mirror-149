#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy <wxnacy@gmail.com>
# Description: 数据库模型

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, DATETIME, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import uuid
from dler.constants import DB_PATH
from dler.enum import TaskStatus

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DB_PATH
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class BaseDB(object):

    """模型基类"""
    __tablename__ = ''
    id = Column(String(32), primary_key=True, default=uuid.uuid4)

    def save(self):
        """TODO: Docstring for save.
        :returns: TODO

        """
        if not self.id:
            self.id = str(uuid.uuid4())
        session.add(self)
        session.commit()
        return self

    @classmethod
    def find(cls, query):
        """TODO: Docstring for find.

        :**kwargs: TODO
        :returns: TODO

        """
        return session.query(cls).filter_by(**query).all()

    @classmethod
    def find_one(cls, query):
        """TODO: Docstring for find.

        :**kwargs: TODO
        :returns: TODO

        """
        return session.query(cls).filter_by(**query).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.find_one({"id": _id})

    @classmethod
    def insert_many(cls, items):
        """批量插入

        :items: TODO
        :returns: TODO

        """
        session.execute(cls.__table__.insert(), items)
        session.commit()

    @classmethod
    def update(cls, query, update_data):
        """修改数据

        :query: TODO
        :update_data: TODO
        :returns: TODO

        """
        for item in cls.find(query):
            for k, v in update_data.items():
                setattr(item, k, v)
            item.save()

    @classmethod
    def update_success(cls, _id):
        """修改数据

        :query: TODO
        :update_data: TODO
        :returns: TODO

        """
        cls.update({"id": _id}, { "status": TaskStatus.SUCCESS.value })

    def dict(self):
        return self.__dict__


def init_db():
    """创建数据库
    """
    print("init database")
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
    #  Task( url = 'test').save()
    #  for item in Task.find({ "url": 'test' }):
        #  print(item)
        #  print(item.id)
    #  SubTask.update({ "task_id": "1ba2807b-864f-4813-83ee-09ff0be5d7b6" }, {"status": "success"})
