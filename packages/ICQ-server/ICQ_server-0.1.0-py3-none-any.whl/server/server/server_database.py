import sys
import os

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sys.path.append(os.path.join(os.getcwd(), '../../../messenger'))
sys.path.append('../../../messenger/')
from server_dist.server.common.variables import *


class ServerStorage:
    """Класс для работы с базой данных"""
    Base = declarative_base()

    class AllUsers(Base):
        """Класс отображает таблицы всех пользователй"""

        __tablename__ = 'Users'
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)
        last_login = Column(DateTime)
        passwd_hash = Column('passwd_hash', String)
        pubkey = Column('pubkey', Text)

        def __init__(self, username, passwd_hash):
            self.name = username
            self.passwd_hash = passwd_hash
            self.last_login = datetime.now()
            self.pubkey = None

    class ActiveUsers(Base):
        """Класс отображает таблицы активных пользователей"""

        __tablename__ = 'Active_users'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('Users.id'), unique=True)
        ip = Column(String)
        port = Column(Integer)
        login_time = Column(DateTime)

        def __init__(self, user_id, ip, port, login_time):
            self.user = user_id
            self.ip = ip
            self.port = port
            self.login_time = login_time

    class LoginHistory(Base):
        """Класс отображает истории входов"""

        __tablename__ = 'Login_history'
        id = Column(Integer, primary_key=True)
        name = Column(String, ForeignKey('Users.id'))
        ip = Column(String)
        port = Column(Integer)
        last_conn = Column(DateTime)

        def __init__(self, name, last_conn, ip, port):
            self.name = name
            self.last_conn = last_conn
            self.ip = ip
            self.port = port

    class UsersContacts(Base):
        """Класс отображение таблицы контактов пользователей"""

        __tablename__ = 'User_contacts'
        id = Column(Integer, primary_key=True)
        user = Column(ForeignKey('Users.id'))
        contact = Column(ForeignKey('Users.id'))

        def __init__(self, user, contact):
            self.user = user
            self.contact = contact

    class UsersHistory(Base):
        """Класс отображение таблицы истории действий"""

        __tablename__ = 'Users_history'
        id = Column(Integer, primary_key=True)
        user = Column(ForeignKey('Users.id'))
        sent = Column(Integer)
        accepted = Column(Integer)

        def __init__(self, user):
            self.user = user
            self.sent = 0
            self.accepted = 0

    def __init__(self, path):
        self.database_engine = create_engine(f'sqlite:///{path}', echo=False, pool_recycle=7200,
                                             connect_args={'check_same_thread': False})
        self.Base.metadata.create_all(self.database_engine)
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        self.session.query(self.ActiveUsers).delete()
        self.session.commit()

    def user_login(self, username, ip, port, key):
        """Обрабатываем вход пользователя, записывая его в таблицу активных юзеров,
        и в историю входов"""

        rez = self.session.query(self.AllUsers).filter_by(name=username)
        if rez.count():
            user = rez.first()
            user.last_login = datetime.now()
            if user.pubkey != key:
                user.pubkey = key
        else:
            raise ValueError('Пользователь не зарегистрирован.')

        new_active_user = self.ActiveUsers(user.id, ip, port, datetime.now())
        self.session.add(new_active_user)
        history = self.LoginHistory(user.id, datetime.now(), ip, port)
        self.session.add(history)

        self.session.commit()

    def user_logout(self, username):
        """После выхода удаляем пользователя из активных"""

        user = self.session.query(self.AllUsers).filter_by(name=username).first()
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        self.session.commit()

    def users_list(self):
        """Возвращаем список всех зарегистрированных пользователей"""

        query = self.session.query(
            self.AllUsers.name,
            self.AllUsers.last_login
        )
        return query.all()

    def active_users_list(self):
        """Возвращаем список всех активных пользователей"""

        query = self.session.query(
            self.AllUsers.name,
            self.ActiveUsers.ip,
            self.ActiveUsers.port,
            self.ActiveUsers.login_time
        ).join(self.AllUsers)
        return query.all()

    def login_history(self, username=None):
        """Возвращаем историю последних входов пользователей
        username: фильтрует по имени пользователя"""
        query = self.session.query(self.AllUsers.name,
                                   self.LoginHistory.ip,
                                   self.LoginHistory.port,
                                   self.LoginHistory.last_conn
                                   ).join(self.AllUsers)
        if username:
            query = query.filter(self.AllUsers.name == username)
        return query.all()

    def process_message(self, sender, recipient):
        """Фиксируем передачу сообщения и отмечаем это в БД"""
        sender = self.session.query(self.AllUsers).filter_by(name=sender).first().id
        recipient = self.session.query(self.AllUsers).filter_by(name=recipient).first().id
        sender_row = self.session.query(self.UsersHistory).filter_by(user=sender).first()
        sender_row.sent += 1
        recipient_row = self.session.query(self.UsersHistory).filter_by(user=recipient).first()
        recipient_row.accepted += 1
        self.session.commit()

    def add_contact(self, user, contact):
        """Добавляем контакт для пользователя"""
        user = self.session.query(self.AllUsers).filter_by(name=user).first()
        contact = self.session.query(self.AllUsers).filter_by(name=contact).first()

        if not contact or self.session.query(self.UsersContacts).filter_by(user=user.id, contact=contact.id).count():
            return
        contact_row = self.UsersContacts(user.id, contact.id)
        self.session.add(contact_row)
        self.session.commit()

    def remove_contact(self, user, contact):
        """Удаляем контакт из базы данных"""
        user = self.session.query(self.AllUsers).filter_by(name=user).first()
        contact = self.session.query(self.AllUsers).filter_by(name=contact).first()

        if not contact:
            return

        print(self.session.query(self.UsersContacts).filter(
            self.UsersContacts.user == user.id,
            self.UsersContacts.contact == contact.id
        ).delete())
        self.session.commit()

    def get_contacts(self, username):
        """Функция возвращает список контактов пользователя."""

        user = self.session.query(self.AllUsers).filter_by(name=username).one()
        query = self.session.query(self.UsersContacts, self.AllUsers.name). \
            filter_by(user=user.id). \
            join(self.AllUsers, self.UsersContacts.contact == self.AllUsers.id)
        return [contact[1] for contact in query.all()]

    def message_history(self):
        """Возвращаем количество переданных и полученных сообщений"""
        query = self.session.query(
            self.AllUsers.name,
            self.AllUsers.last_login,
            self.UsersHistory.sent,
            self.UsersHistory.accepted
        ).join(self.AllUsers)
        return query.all()

    def add_user(self, name, passwd_hash):
        """Метод регистрации пользователя."""
        user_row = self.AllUsers(name, passwd_hash)
        self.session.add(user_row)
        self.session.commit()
        history_row = self.UsersHistory(user_row.id)
        self.session.add(history_row)
        self.session.commit()

    def remove_user(self, name):
        """Метод удаляющий пользователя из базы."""
        user = self.session.query(self.AllUsers).filter_by(name=name).first()
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        self.session.query(self.LoginHistory).filter_by(name=user.id).delete()
        self.session.query(self.UsersContacts).filter_by(user=user.id).delete()
        self.session.query(
            self.UsersContacts).filter_by(
            contact=user.id).delete()
        self.session.query(self.UsersHistory).filter_by(user=user.id).delete()
        self.session.query(self.AllUsers).filter_by(name=name).delete()
        self.session.commit()

    def get_hash(self, name):
        """Метод получения хэша пароля пользователя."""
        user = self.session.query(self.AllUsers).filter_by(name=name).first()
        return user.passwd_hash

    def get_pubkey(self, name):
        """Метод получения публичного ключа пользователя."""
        user = self.session.query(self.AllUsers).filter_by(name=name).first()
        return user.pubkey

    def check_user(self, name):
        """Метод проверяющий существование пользователя."""
        if self.session.query(self.AllUsers).filter_by(name=name).count():
            return True
        else:
            return False


if __name__ == '__main__':
    db = ServerStorage()
    db.user_login('client_1', '192.168.1.4', 8888)
    db.user_login('client_2', '192.168.1.5', 7777)

    print(' ---- Список пользователей ----')
    print(db.active_users_list())

    db.user_logout('client_1')
    print(' ---- Выполняем логаут client_1 ----')
    print(db.active_users_list())

    print(' ---- История входов пользователя client_1 ----')
    print(db.login_history('client_1'))

    print(' ---- Список всех зарегистрированных пользователей ----')
    print(db.users_list())
