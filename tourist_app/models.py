from flask import flash
from flask_login import UserMixin
from tourist_app import db, login_manager, bcrypt
from sqlalchemy import and_


# Обязательный метод для получения текущего ID пользователя
@login_manager.user_loader
def load_user(user_id):
    return AppUser.query.get(int(user_id))


# Таблица пользователей
class AppUser(db.Model, UserMixin):
    __tablename__ = 'application_user'
    __table_args__ = {'extend_existing': True}

    id_application_user = db.Column(db.Integer(), primary_key=True)
    password = db.Column(db.String(length=150), nullable=False)

    # Метод получения ID пользователя из таблицы
    def get_id(self):
        return self.id_application_user

    # Получение пароля
    @property
    def unencrypted_password(self):
        return self.unencrypted_password

    # Шифрование пароля
    @unencrypted_password.setter
    def unencrypted_password(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    # Проверка пароля
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)

    @staticmethod
    def get_user_by_login(login):
        return AppUser.query.filter_by(login=login).first()

    @staticmethod
    def get_user_by_login_with_role(login):
        query = db.session.query(AppUser, RoleAppUser)
        query = query.join(RoleAppUser, AppUser.id_role == RoleAppUser.id_role_user)
        query = query.filter(AppUser.login == login)
        return query.first()

    @staticmethod
    def get_user_by_fio(fio):
        return AppUser.query.filter_by(login=fio).first()

    # Добавление нового пользователя
    @staticmethod
    def add_app_user(login, password, phone_number, fio, address, birthday, id_role, photo_application_user=None):
        new_app_user = AppUser(login=login, unencrypted_password=password, phone_number=phone_number, fio=fio,
                               address=address, birthday=birthday, photo_application_user=photo_application_user,
                               id_role=id_role)

        try:
            db.session.add(new_app_user)
            db.session.commit()
            flash("Пользователь был успешно добавлен.", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при добавлении пользователя. Повторите попытку.", category='danger')

    # Обновление пользователя
    @staticmethod
    def update_app_user(login, phone_number, fio, address, birthday, photo_application_user):
        try:
            # Поиск пользователя для изменения
            app_user_for_update = AppUser.get_user_by_login(login)

            # Внесение изменений в профиль пользователя
            app_user_for_update.fio = fio
            app_user_for_update.phone_number = phone_number
            app_user_for_update.address = address
            app_user_for_update.birthday = birthday
            app_user_for_update.photo_application_user = photo_application_user

            db.session.commit()
            flash("Профиль пользователя был успешно изменён.", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при изменении профиля пользователя.", category='danger')


# Таблица статусов бронирования
class BookStatus(db.Model):
    __tablename__ = 'booking_status'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def get_all_book_status():
        return BookStatus.query.all()

    @staticmethod
    def get_all_book_status_by_status(name_booking_status):
        return BookStatus.query.filter_by(name_booking_status=name_booking_status).first()


# Таблица обсуживаемых городов
class City(db.Model):
    __tablename__ = 'city'
    __table_args__ = {'extend_existing': True}


# Таблица контрактов
class Contract(db.Model):
    __tablename__ = 'contract'
    __table_args__ = {'extend_existing': True}

    # Информации по всем контрактам - бронирования
    @staticmethod
    def get_all_contracts():
        query = db.session.query(Contract, BookStatus, AppUser, Voucher, TurfirimRoute, StopRoute, City, Country)
        query = query.join(BookStatus, Contract.id_booking_status == BookStatus.id_booking_status)
        query = query.join(AppUser, AppUser.id_application_user == Contract.id_application_user)
        query = query.join(Voucher, Contract.id_contract == Voucher.id_contract)
        query = query.join(TurfirimRoute, Voucher.id_turfirim_route == TurfirimRoute.id_route)
        query = query.join(StopRoute, StopRoute.id_turfirim_route == TurfirimRoute.id_route)
        query = query.join(City, City.id_city == StopRoute.id_city)
        query = query.join(Country, Country.id_country == City.id_country)
        return query.all()

    # Поиск информации по контракту
    @staticmethod
    def get_contract_by_id_contract(id_contract):
        return Contract.query.filter_by(id_contract=id_contract).first()

    # Поиск информации по контракту
    @staticmethod
    def get_last_contract_by_id_user(id_application_user):
        return Contract.query.filter_by(id_application_user=
                                        id_application_user).order_by(Contract.id_contract.desc()).first()

    # Добавление контракта
    @staticmethod
    def add_contract(id_application_user, id_booking_status, type_payment):
        new_contract = Contract(id_application_user=id_application_user, id_booking_status=id_booking_status,
                                type_payment=type_payment)
        try:
            db.session.add(new_contract)
            db.session.commit()
            flash("Бронирование успешно оформлено.", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при оформлении бронирования.", category='danger')

    # Добавление контракта
    @staticmethod
    def update_contract(id_contract, id_booking_status):
        try:
            contract_for_update = Contract.get_contract_by_id_contract(id_contract)
            contract_for_update.id_booking_status = id_booking_status
            db.session.commit()
            flash("Статус бронирования успешно изменён.", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при статуса бронирования.", category='danger')


# Таблица обслуживаемых стран
class Country(db.Model):
    __tablename__ = 'country'
    __table_args__ = {'extend_existing': True}


# Таблица отелей
class Hotel(db.Model):
    __tablename__ = 'hotel'
    __table_args__ = {'extend_existing': True}


# Таблица с информацией о номере в отеле
class HotelRoom(db.Model):
    __tablename__ = 'hotel_room'
    __table_args__ = {'extend_existing': True}


# Таблица ролей пользователей
class RoleAppUser(db.Model):
    __tablename__ = 'role_application_user'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def get_all_roles():
        return RoleAppUser.query.all()

    @staticmethod
    def get_role_by_name(name_role_user):
        return RoleAppUser.query.filter_by(name_role_user=name_role_user).first()


# Таблица с информацией об остановках на маршруте
class StopRoute(db.Model):
    __tablename__ = 'stop_route'
    __table_args__ = {'extend_existing': True}


# Таблица с информацией о туристической группе
class TourGroup(db.Model):
    __tablename__ = 'tour_group'
    __table_args__ = {'extend_existing': True}


# Таблица с информацией о туристических маршрутов
class TurfirimRoute(db.Model):
    __tablename__ = 'turfirim_route'
    __table_args__ = {'extend_existing': True}

    # Метод получения всех маршрутов
    @staticmethod
    def get_routes(id_route=None):
        query = db.session.query(TurfirimRoute, StopRoute, HotelRoom, Hotel, City, Country)
        query = query.join(StopRoute, StopRoute.id_turfirim_route == TurfirimRoute.id_route)
        query = query.join(City, City.id_city == StopRoute.id_city)
        query = query.join(Country, Country.id_country == City.id_country)
        query = query.join(HotelRoom, and_(StopRoute.id_stop_route == HotelRoom.id_stop_route,
                                           StopRoute.id_turfirim_route == HotelRoom.id_turfirim_route))
        query = query.join(Hotel, Hotel.id_hotel == HotelRoom.id_hotel)

        if id_route:
            query = query.filter(TurfirimRoute.id_route == id_route)
            return query.first()
        else:
            return query.all()


# Таблица с информацией о ваучерах
class Voucher(db.Model):
    __tablename__ = 'voucher'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def add_voucher(id_contract, id_turfirim_route):
        new_voucher = Voucher(id_contract=id_contract, id_turfirim_route=id_turfirim_route)

        try:
            db.session.add(new_voucher)
            db.session.commit()
            flash("Добавлен новый ваучер.", category='success')
        except:
            db.session.rollback()
            flash("Произошла ошибка при добавлении ваучера.", category='danger')
