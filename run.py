#!/usr/bin/env python
import os
if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


from flask_migrate import MigrateCommand
from app import create_app
from flask_script import Manager, Command # deploy addon .1
from app import db
from app.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
print(os.getenv('FLASK_CONFIG'))
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    ''' Creates the database'''
    db.create_all()


@manager.command
def drop_tables():
    ''' Drop Tables for debugging only '''
    db.drop_all()


@manager.command
def add_user(email, username):
    ''' Creates a user for login access '''
    from getpass import getpass
    password = getpass()
    password2 = getpass(prompt='Confirm: ')

    if password != password2:
        import sys
        sys.exit('Error! Passwords do not match.\n' \
                 'Quiting...')
    db.create_all()
    user = User(email=email, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    print('Username: {}, Email: {} was successfully created!'.format(user.username, user.email))


# db.create_all()


if __name__ == '__main__':
    manager.run()
# app.run()
