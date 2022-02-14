from flask import Blueprint, render_template, redirect, url_for, session, flash
from tourist_app.models import TurfirimRoute, Contract, Voucher
from tourist_app.forms import BookRoute
from flask_login import current_user

turifirm = Blueprint('turifirm', __name__, template_folder="templates")


# Страница для получения информации об маршруте
@turifirm.route('/turifirm/<id_route>', methods=['GET', 'POST'])
def turifirm_page_view(id_route):
    # Получение всей информации по маршруту
    route_info = TurfirimRoute.get_routes(id_route)
    # Добавление формы для бронирования
    booking = BookRoute()

    # Активация формы бронирования маршрута
    if booking.submit_book.data:
        if current_user:
            if session['role'] != 1:
                # Добавление нового контракта
                Contract.add_contract(current_user.get_id(), booking.id_booking_status, booking.type_payment.data)
                # Получение номера добавленного контракта
                my_contract = Contract.get_last_contract_by_id_user(current_user.get_id())
                # Добавление нового ваучера
                Voucher.add_voucher(my_contract.id_contract, id_route)
                return redirect(url_for('home.home_page_view'))
            else:
                flash("Менеджеры не должны бронировать маршруты", category='danger')
                return redirect(url_for('home.home_page_view'))
        else:
            flash("Войдите в аккаунт, чтобы получить возможность бронирования маршрута", category='danger')
            return redirect(url_for('home.home_page_view'))

    return render_template('turifirm/view_route_turifirm.html', route_info=route_info, booking=booking)
