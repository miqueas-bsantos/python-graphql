# flask_sqlalchemy/models.py
from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship, backref)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
# We will need this for querying
Base.query = db_session.query_property()

class User(Base):
    __tablename__ = 'TB_USER'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    profession = Column(String(100))
    age = Column(Integer)
    hobbies = relationship("Hobby", cascade="delete,all")    
    posts = relationship("Post", cascade="delete,all")    

class Hobby(Base):
    __tablename__ = 'TB_HOBBY'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    description = Column(String(100))
    user_id = Column(Integer, ForeignKey('TB_USER.id'))

class Post(Base):
    __tablename__ = 'TB_POST'
    id = Column(Integer, primary_key=True,  autoincrement=True)
    comment = Column(String(255))
    user_id = Column(Integer, ForeignKey('TB_USER.id'))

Base.metadata.create_all(bind=engine)