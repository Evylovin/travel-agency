from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, SelectField, IntegerField, \
    HiddenField
from wtforms.validators import ValidationError, Length, EqualTo, DataRequired
from tourist_app.models import AppUser


# Форма регистрации на сайте
class RegisterForm(FlaskForm):
    # Проверка наличия совпадений имён пользователей при создании нового пользователя
    def validate_login(self, login_to_check):
        user = AppUser.get_user_by_login(login_to_check.data)
        if user:
            raise ValidationError('Такое имя пользователя уже есть! Попробуйте придумать другое')

    # Проверка наличия совпадени ФИО при создании нового пользователя
    def validate_fio(self, fio_to_check):
        fio = AppUser.get_user_by_fio(fio_to_check.data)
        if fio:
            raise ValidationError('У такого человека уже существует аккаунт! '
                                  'Если пароль и логин забыты, то обратитесь к администратору')

    # Данные для создания нового пользователя с ограничениями, которые накладываются на таблицу в БД
    fio = TextAreaField(label='ФИО:', validators=[DataRequired()])
    phone_number = StringField(label='Номер телефона:', validators=[DataRequired()])
    address = TextAreaField(label='Адрес:', validators=[DataRequired()])
    birthday = DateField(label='Дата рождения:', validators=[DataRequired()])
    role = SelectField(label='Роль на сайте:', choices=[])
    user_photo = StringField(label='Ссылка на фото пользователя с размером близким к 300х300')
    login = StringField(label='Логин:', validators=[Length(min=6, max=20), DataRequired()])
    password1 = PasswordField(label='Пароль:', validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label='Подтвердить пароль:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Создать аккаунт')


# Форма регистрации на сайте
class UpdateUser(FlaskForm):
    # Данные для создания нового пользователя с ограничениями, которые накладываются на таблицу в БД
    fio = TextAreaField(label=' Новое ФИО:')
    phone_number = StringField(label='Новый телефон:')
    address = TextAreaField(label='Новый адрес:')
    birthday = DateField(label='Новая дата рождения:')
    user_photo = StringField(label='Ссылка на новое фото пользователя с размером близким к 300х300')
    submit_update = SubmitField(label='Обновить')


# Форма авторизации на сайте
class LoginForm(FlaskForm):
    login = StringField(label="Логин:", validators=[DataRequired()])
    password = PasswordField(label="Пароль:", validators=[DataRequired()])
    submit = SubmitField(label='Вход')


# Форма для перехода в окно информации о маршруте
class RouteInfoById(FlaskForm):
    id_route = HiddenField()
    submit_info = SubmitField(label='Подробнее о маршруте')


# Форма для перехода изменения маршрута
class RouteUpdateById(FlaskForm):
    id_route = HiddenField()
    submit_info = SubmitField(label='Подробнее о маршруте')


# Форма для перехода в окно информации о маршруте
class BookRoute(FlaskForm):
    id_route = HiddenField()
    id_booking_status = 1
    type_payment = SelectField(label="Вид оплаты", choices=['Наличными', 'По карте'])
    submit_book = SubmitField(label='Забронировать')


# Форма для смены статуса бронирования
class UpdateBookStatus(FlaskForm):
    id_contract = HiddenField()
    book_status = SelectField(label="Статус бронирования", choices=[])
    submit_update = SubmitField(label='Изменить')
