from flask import render_template, Blueprint, redirect, url_for, session
from tourist_app.models import AppUser
from tourist_app.forms import UpdateUser
from flask_login import login_required

# Создание узла связанного с профилем и его изменением
profile = Blueprint('profile', __name__, template_folder="templates")


# Просмотр информации о пользователе
@profile.route('/profile_view', methods=['GET', 'POST'])
@login_required
def profile_view():
    user_info = AppUser.get_user_by_login_with_role(session['login'])
    return render_template('profile/user_profile.html', user_info=user_info)


# Обновление профиля пользователя
@profile.route('/update_profile_view', methods=['GET', 'POST'])
@login_required
def profile_update_view():
    # Форма для обновления профиля
    update_profile_form = UpdateUser()
    # Получение текущей информации о пользователе
    activated_user = AppUser.get_user_by_login(session['login'])

    if update_profile_form.submit_update.data:
        # Проверка на введённые в форме данные

        # ФИО
        if update_profile_form.fio.data:
            fio = update_profile_form.fio.data
        else:
            fio = activated_user.fio
        # Дата рождения
        if update_profile_form.birthday.data:
            birthday = update_profile_form.fio.data
        else:
            birthday = activated_user.birthday
        # Номер телефона
        if update_profile_form.phone_number.data:
            phone_number = update_profile_form.phone_number.data
        else:
            phone_number = activated_user.phone_number
        # Номер телефона
        if update_profile_form.address.data:
            address = update_profile_form.address.data
        else:
            address = activated_user.address
        # Фото пользователя
        if update_profile_form.user_photo.data:
            photo = update_profile_form.user_photo.data
        else:
            photo = activated_user.photo_application_user

        # Обновление профиля пользователя
        AppUser.update_app_user(session['login'], phone_number, fio, address, birthday, photo)

        return redirect(url_for('profile.profile_view'))

    return render_template('profile/update_user_profile.html', activated_user=activated_user,
                           update_profile_form=update_profile_form)
