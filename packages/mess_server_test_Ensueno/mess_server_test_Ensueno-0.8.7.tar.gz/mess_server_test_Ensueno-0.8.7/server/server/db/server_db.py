import os
import traceback
from datetime import datetime

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, ForeignKey, \
    Boolean, Text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql import default_comparator


class Storage:
    class Users:

        def __init__(self, username, passwd_hash):
            self.login = username
            self.last_login = datetime.now()
            self.passwd_hash = passwd_hash
            self.pubkey = None
            self.id = None

        def __repr__(self):
            return "<User('%s', '%s', '%s')>" % (self.id, self.login, self.last_login)

    class LoginHistory:

        def __init__(self, user_id, ip_addr, port, start_time):
            self.user_id = user_id
            self.ip_addr = ip_addr
            self.port = port
            self.start_time = start_time
            self.end_time = None
            self.id = None

        def __repr__(self):
            return "<LoginHistory('%s', '%s', '%s', '%s', '%s')>" % (self.user_id, self.ip_addr, self.port,
                                                                     self.start_time, self.end_time)

    class Contacts:

        def __init__(self, owner_id, buddy_id):
            self.id = None
            self.owner_id = owner_id
            self.buddy_id = buddy_id

        def __repr__(self):
            return "<Contact('%s', '%s')>" % (self.owner_id, self.buddy_id)

    class UsersHistory:
        def __init__(self, user):
            self.id = None
            self.user = user
            self.sent = 0
            self.accepted = 0

    def __init__(self, path=None):
        if not path:
            path = os.getcwd()
            filename = f'server_db.db3'
            self.database_engine = create_engine(
                f'sqlite:///{os.path.join(path, filename)}',
                echo=False,
                pool_recycle=7200,
                connect_args={
                    'check_same_thread': False})
        else:
            self.database_engine = create_engine(
                f'sqlite:///{path}',
                echo=False,
                pool_recycle=7200,
                connect_args={
                    'check_same_thread': False})

        self.metadata = MetaData()

        users_table = Table('users', self.metadata,
                            Column('id', Integer, primary_key=True),
                            Column('login', String(100), unique=True, nullable=False),
                            Column('last_login', DateTime, default=datetime.now),
                            Column('is_active', Boolean, default=False),
                            Column('ip_addr', String, default='111'),
                            Column('port', Integer, default=111),
                            Column('passwd_hash', String),
                            Column('pubkey', Text)
                            )

        user_login_history = Table('login_history', self.metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('user_id', ForeignKey('users.id')),
                                   Column('start_time', DateTime, default=datetime.now),
                                   Column('end_time', DateTime, default=datetime.now),
                                   Column('ip_addr', String(100), nullable=False),
                                   Column('port', String(100), nullable=False)
                                   )

        user_contacts = Table('contacts', self.metadata,
                              Column('id', Integer, primary_key=True),
                              Column('owner_id', ForeignKey('users.id')),
                              Column('buddy_id', ForeignKey('users.id')),
                              )

        users_history_table = Table('users_history', self.metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('user', ForeignKey('users.id')),
                                    Column('sent', Integer),
                                    Column('accepted', Integer)
                                    )

        self.metadata.create_all(self.database_engine)

        mapper(self.Users, users_table)
        mapper(self.LoginHistory, user_login_history)
        mapper(self.Contacts, user_contacts)
        mapper(self.UsersHistory, users_history_table)

        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()
        self.safe_commit()

    def safe_commit(self):
        if self.session:
            try:
                self.session.commit()
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
                self.session.rollback()

    def register_user(self, name, passwd_hash):
        user = self.Users(name, passwd_hash)
        user.ip_addr = None
        user.port = None
        self.session.add(user)
        self.safe_commit()
        start_history = self.UsersHistory(user.id)
        self.session.add(start_history)
        self.safe_commit()

    def remove_user(self, name):
        user = self.session.query(self.Users).filter_by(login=name).first()
        self.session.query(self.LoginHistory).filter_by(user_id=user.id).delete()
        self.session.query(self.Contacts).filter_by(owner_id=user.id).delete()
        self.session.query(self.Contacts).filter_by(buddy_id=user.id).delete()
        self.session.query(self.UsersHistory).filter_by(user=user.id).delete()
        self.session.query(self.Users).filter_by(login=name).delete()
        self.safe_commit()

    def login_user(self, username, ip_address, port, key):
        user = self.session.query(self.Users).filter_by(login=username).scalar()
        if user:
            user.last_login = datetime.now()
            user.is_active = True
            if user.pubkey != key:
                user.pubkey = key
            user.ip_addr = ip_address
            user.port = port
        else:
            raise ValueError('Пользователь не зарегистрирован.')
        history = self.LoginHistory(user_id=user.id, ip_addr=ip_address, port=port, start_time=user.last_login)
        self.session.add(history)
        self.safe_commit()

    def logout_user(self, username):
        user = self.session.query(self.Users).filter_by(login=username).scalar()
        user.is_active = False
        history = self.session.query(self.LoginHistory).filter_by(
            user_id=user.id,
            start_time=user.last_login
        ).scalar()
        history.end_time = datetime.now()
        self.safe_commit()

    def get_hash(self, name):
        user = self.session.query(self.Users).filter_by(login=name).first()
        return user.passwd_hash

    def get_pubkey(self, name):
        user = self.session.query(self.Users).filter_by(login=name).first()
        return user.pubkey

    def check_user(self, name):
        return True if self.session.query(self.Users).filter_by(login=name).count() else False

    def counting_messages(self, author, to_whom):
        author = self.session.query(self.Users).filter_by(login=author).scalar()
        to_whom = self.session.query(self.Users).filter_by(login=to_whom).scalar()
        author_sent = self.session.query(self.UsersHistory).filter_by(user=author.id).first()
        to_whom_accepted = self.session.query(self.UsersHistory).filter_by(user=to_whom.id).first()
        author_sent.sent += 1
        to_whom_accepted.accepted += 1
        self.safe_commit()

    def add_contacts(self, owner_name, buddy_name):
        owner = self.session.query(self.Users).filter_by(login=owner_name).scalar()
        buddy = self.session.query(self.Users).filter_by(login=buddy_name).scalar()
        contact = self.session.query(self.Contacts).filter(self.Contacts.owner_id == owner.id,
                                                           self.Contacts.buddy_id == buddy.id).scalar()
        if not contact:
            contact = self.Contacts(owner.id, buddy.id)
            self.session.add(contact)
            self.safe_commit()

    def remove_contacts(self, owner_name, buddy_name):
        owner = self.session.query(self.Users).filter_by(login=owner_name).scalar()
        buddy = self.session.query(self.Users).filter_by(login=buddy_name).scalar()
        try:
            self.session.query(self.Contacts).filter_by(owner_id=owner.id,
                                                        buddy_id=buddy.id).delete()
            self.safe_commit()
        except Exception:
            print(traceback.format_exc())

    def show_contacts(self, username):
        user = self.session.query(self.Users).filter_by(login=username).scalar()
        contacts_owner = self.session.query(self.Contacts.buddy_id).filter_by(owner_id=user.id)
        contacts_id = list(map(lambda x: x[0], contacts_owner))
        usernames = self.session.query(self.Users.login).filter(self.Users.id.in_(contacts_id))
        return usernames.all()

    def show_active_users(self):
        query = self.session.query(self.Users.login,
                                   self.Users.ip_addr,
                                   self.Users.port,
                                   self.Users.last_login
                                   ).filter_by(is_active=True).all()
        return query

    def login_history(self, username=None):
        query = self.session.query(self.Users.login,
                                   self.LoginHistory.start_time,
                                   self.LoginHistory.end_time,
                                   self.LoginHistory.ip_addr,
                                   self.LoginHistory.port
                                   ).join(self.Users)
        if username:
            query = query.filter(self.Users.login == username)
        return query.all()

    def show_users_list(self):
        query = self.session.query(
            self.Users.login,
            self.Users.last_login,
        )
        return query.all()

    def message_history(self, username=None):
        query = self.session.query(
            self.Users.login,
            self.Users.last_login,
            self.UsersHistory.sent,
            self.UsersHistory.accepted
        ).join(self.Users)
        if username:
            query = query.filter(self.Users.login == username)

        return query.all()


if __name__ == '__main__':
    test_db = Storage()

    print('В мессенджер заходят три участника: client_1, client_2, client_3')
    test_db.login_user('client_1', '192.168.1.4', 8888)
    test_db.login_user('client_2', '192.168.1.5', 7777)
    test_db.login_user('client_3', '192.168.1.5', 7778)

    print(f'Все участники: {test_db.show_users_list()}')
    print(f'Все активные участники: {test_db.show_active_users()}')
    test_db.logout_user('client_1')
    print('Участник client_1 вышел.')
    print(f'Все активные участники: {test_db.show_active_users()}')

    print(f'Участника no_one не было и истории его посещений не существует: {test_db.login_history("no_one")}')
    print(f'История посещений client_1: {test_db.login_history("client_1")}')
    test_db.add_contacts('client_1', 'client_2')
    test_db.add_contacts('client_3', 'client_1')

    print('Добавим контакт для client_1 - client_2 и для client_3 - client_1')
    print(f'Все контакты client_1: {test_db.show_contacts("client_1")}')

    print('Удалим контакт для client_3 - client_1')
    test_db.remove_contacts('client_3', 'client_1')
    print(f'Все контакты client_1: {test_db.show_contacts("client_1")}')

    print('Тест подсчета сообщений: client_3 отправил по 1 сообщению для client_1 и client_2')
    test_db.counting_messages("client_3", "client_1")
    test_db.counting_messages("client_3", "client_2")
    print(f'История сообщений client_1: {test_db.message_history("client_1")}')
    print(f'Общая история сообщений: {test_db.message_history()}')
