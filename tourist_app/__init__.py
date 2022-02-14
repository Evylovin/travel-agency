from flask import Flask
from tourist_app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Создание объекта приложения
app = Flask(__name__)
# Ввод конфиг файла для приложения
app.config.from_object(Config)

# Подключение готовой базы данных
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)

# Настройка пользовательского входа с помощь логин менеджера
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Пожалуйста, выполните вход для дальнейших действий'

# Подключени шифратора паролей
bcrypt = Bcrypt(app)

# Подключение узлов с методами к приложению
# from app.module import route
from tourist_app.home_page.home_page import home
from tourist_app.authentication.authentication import authentication
from tourist_app.turifirm_route_page.turifirm_route_page import turifirm
from tourist_app.profile_page.profile_page import profile
from tourist_app.manager_pages.manager_page import manager

# app.register_blueprint(route)
app.register_blueprint(home)
app.register_blueprint(authentication)
app.register_blueprint(turifirm)
app.register_blueprint(profile)
app.register_blueprint(manager)


