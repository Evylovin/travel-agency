from flask import Blueprint, render_template, redirect, url_for
from tourist_app.models import Contract, BookStatus
from tourist_app.forms import UpdateBookStatus
from flask_login import login_required

manager = Blueprint('manager', __name__, template_folder="templates")


# Страница для получения информации об маршруте
@manager.route('/manager_view', methods=['GET', 'POST'])
@login_required
def manager_page_view():
    # Вывод всех бронирований
    all_brones = Contract.get_all_contracts()
    # Форма изменения бронирования
    update_book_status = UpdateBookStatus()
    # Заполнения списка изменения статуса бронирования
    book_status_for_form = BookStatus.get_all_book_status()
    update_book_status.book_status.choices = [i.name_booking_status for i in book_status_for_form]

    if update_book_status.submit_update.data:
        book_for_update = BookStatus.get_all_book_status_by_status(update_book_status.book_status.data)
        Contract.update_contract(update_book_status.id_contract.data, book_for_update.id_booking_status)
        return redirect(url_for('manager.manager_page_view'))

    return render_template('manager/view_manager_page.html', all_brones=all_brones,
                           update_book_status=update_book_status)
