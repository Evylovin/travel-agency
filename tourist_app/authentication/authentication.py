from flask import Blueprint, render_template, redirect, url_for, flash, session
from tourist_app.models import AppUser, RoleAppUser
from tourist_app.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user

# Создание с логикой регистрации, авторизации и выхода
authentication = Blueprint('authentication', __name__, template_folder="templates")


# Маршрут с логикой организации регистрации на сайте через форму с ошибками и добавлением в БД
@authentication.route('/register', methods=['GET', 'POST'])
def register_page():
    # Форма с регистрацией
    reg_form = RegisterForm()
    # Список всех ролей
    role_for_form = RoleAppUser.get_all_roles()
    reg_form.role.choices = [i.name_role_user for i in role_for_form]

    # Проверка нажатия кнопки "Создать аккаунт"
    if reg_form.validate_on_submit():
        # Получение ID роли по её именованию
        role_for_add = RoleAppUser.get_role_by_name(reg_form.role.data)
        # Создание нового аккаунта
        AppUser.add_app_user(reg_form.login.data, reg_form.password1.data, reg_form.phone_number.data,
                             reg_form.fio.data, reg_form.address.data, reg_form.birthday.data,
                             role_for_add.id_role_user, reg_form.user_photo.data)

        return redirect(url_for('authentication.login_page'))

    # Механизм вывода ошибок при создании нового пользователя
    if reg_form.errors != {}:
        for err_msg in reg_form.errors.values():
            flash(f'Произошла ошибка при создании нового пользователя: {err_msg}', category='danger')

    # Вовзрашение html шаблона с формой регистрации
    return render_template('authentication/register.html', reg_form=reg_form)


# Маршрут с логикой авторизации на сайте с обращением к таблице пользователей в БД
# При успешном входе в переменной session сохраняется идентификатор должности пользователя
@authentication.route('/login', methods=['GET', 'POST'])
def login_page():
    log_form = LoginForm()
    # Проверка нажатия на клавишу "Вход"
    if log_form.validate_on_submit():
        attempted_user = AppUser.get_user_by_login(login=log_form.login.data)
        # Проверка на наличие пользователя в базе
        if attempted_user:
            # Проверка на совпадение введённого пароля и пароля в базе
            if attempted_user.check_password_correction(attempted_password=log_form.password.data):
                login_user(attempted_user)
                flash(f'Вход выполнен успешно! Вы зашли как {attempted_user.login}', category='success')
                # Запись должности сотрудника
                session['role'] = attempted_user.id_role
                session['login'] = attempted_user.login
            else:
                flash('Пароль неверный! Попробуйте снова', category='danger')

            return redirect(url_for('home.home_page_view'))
        else:
            flash('Логин не найден! Попробуйте снова', category='danger')

    return render_template('authentication/login.html', log_form=log_form)


# Маршрут с логикой выхода из аккаунта на сайте - организован через flask_login, который выходит из сессии
# Обнуление переменной session['role'] и возвращение на главную страницу
@authentication.route('/logout')
def logout_page():
    # Выход пользователя из аккаунта
    logout_user()
    session.pop('role', None)
    session.pop('login', None)
    # Очистка куки с дополнительными данными о пользователе
    session.clear()

    flash("Вы вышли из аккаунта", category='info')
    return redirect(url_for('home.home_page_view'))

