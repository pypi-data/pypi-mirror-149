import os
import json
import datetime
from hashlib import md5

from contextlib import contextmanager

from sqlalchemy import DateTime
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Unicode, String, create_engine, func
from sqlalchemy.orm import sessionmaker

# ## SQL DB
Base = declarative_base()

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

# ## USERS


class User(Base):
    __tablename__ = 'users'
    id = Column(String(128), primary_key=True)
    provider_id = Column(String(128))
    username = Column(Unicode, unique=True, nullable=False)
    name = Column(Unicode)
    email = Column(Unicode)
    avatar_url = Column(String(512))
    join_date = Column(DateTime)


class Models():

    _sql_engine = None
    _sql_session = None

    FAKE_USER_RECORD = dict(
        provider_id='__FAKE_USER__',
        username='fakeuser',
        name='Fakey McFakerson',
        email='fakey@mcfakerson.com',
        avatar_url='https://www.gravatar.com/avatar/HASH',
        join_date=datetime.datetime.now()
    )

    def __init__(self, connection_string='sqlite://'):
        self._sql_engine = create_engine(connection_string)
        Base.metadata.create_all(self._sql_engine)
        self.FAKE_USER_ID = self.hash_email(self.FAKE_USER_RECORD['email'])

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        if self._sql_session is None:
            self._sql_session = sessionmaker(bind=self._sql_engine)
        session = self._sql_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.expunge_all()
            session.close()

    def get_user(self, id_):
        with self.session_scope() as session:
            ret = session.query(User).filter_by(id=id_).first()
            if ret is not None:
                return object_as_dict(ret)
        return None


    def delete_user(self, id_):
        with self.session_scope() as session:
            ret = session.query(User).filter_by(id=id_).first()
            if ret is not None:
                session.delete(ret)
                return True
        return False


    def get_users(self):
        with self.session_scope() as session:
            ret = session.query(User)
            return [object_as_dict(item) for item in ret]


    def get_user_by_username(self, username_):
        with self.session_scope() as session:
            ret = session.query(User).filter(func.lower(User.username) == func.lower(username_)).first()
            if ret is not None:
                return object_as_dict(ret)
        return None


    def hash_email(self, email):
        return md5(email.encode('utf8')).hexdigest()


    def save_user(self, user):
        with self.session_scope() as session:
            user = User(**user)
            session.add(user)


    def create_or_get_user(self, provider_id, name, username, email, avatar_url):
        id_ = self.hash_email(email)
        with self.session_scope() as session:
            user = session.query(User).filter_by(id=id_).first()
            if user is None:
                params = {
                    'id': id_,
                    'provider_id': provider_id,
                    'username': username.lower(),
                    'name': name,
                    'email': email,
                    'avatar_url': avatar_url,
                    'join_date': datetime.datetime.now()
                }
                user = User(**params)
                session.add(user)
                params['new'] = True
                return params
            else:
                params = {
                    'provider_id': provider_id,
                    'username': username.lower(),
                    'name': name,
                    'avatar_url': avatar_url,
                }
                for k, v in params.items():
                    setattr(user, k, v)
                return object_as_dict(user)
