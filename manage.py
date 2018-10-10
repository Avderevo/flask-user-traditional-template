#!/usr/bin/env python3.5
from flask_login import LoginManager
import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app.database import db
from flask_bcrypt import Bcrypt


app = create_app()

bcrypt = Bcrypt(app)

app.config.from_object(os.environ['APP_SETTINGS'])

login_manager = LoginManager()
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "user.login_handler"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return None

def _make_context():
    return dict(db=db)


manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=_make_context))


from app.users.models.user import User


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def root():
    return "learn-auth app, start at /users/"

if __name__ == '__main__':
    manager.run()
