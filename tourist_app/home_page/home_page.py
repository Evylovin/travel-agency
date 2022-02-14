from flask import Blueprint, render_template, redirect, url_for
from tourist_app.models import TurfirimRoute
from tourist_app.forms import RouteInfoById

home = Blueprint('home', __name__, template_folder="templates")


# Начальная страница сайта
@home.route('/')
@home.route('/main', methods=['GET', 'POST'])
def home_page_view():
    # Получение списка всех маршрутов
    all_routes = TurfirimRoute.get_routes()
    # Подключение формы для перехода за большей информацией о маршруте
    info_about_route = RouteInfoById()

    # Переход по форме "узнать больше"
    if info_about_route.submit_info.data:
        return redirect(url_for('turifirm.turifirm_page_view', id_route=info_about_route.id_route.data))

    return render_template('home/main.html', all_routes=all_routes, info_about_route=info_about_route)
