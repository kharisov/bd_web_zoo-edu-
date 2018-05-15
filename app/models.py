from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import event

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    urole = db.Column(db.String(64))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Staff(db.Model):
    staff_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(64))
    second_name = db.Column(db.String(64))
    gender = db.Column(db.String(64))
    age = db.Column(db.Integer)
    salary = db.Column(db.Integer)
    employment_date = db.Column(db.Date)
    dismissal_date = db.Column(db.Date)
    category_link = db.relationship('StaffCategoryLink', backref='staff', lazy='dynamic')


class StaffCategoryLink(db.Model):
    __tablename__ = 'staff_category_link'
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), primary_key=True)


class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(64))
    staff_link = db.relationship('StaffCategoryLink', backref='category', lazy='dynamic')
    attribute_link = db.relationship('CategoryAttributeLink', backref='attribute', lazy='dynamic')


class CategoryAttributeLink(db.Model):
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), primary_key=True)
    attribute_id = db.Column(db.Integer, db.ForeignKey('attributes.attribute_id'), primary_key=True)


class Attributes(db.Model):
    attribute_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attribute_name = db.Column(db.String(64))
    attribute_type = db.Column(db.String(64))
    category_link = db.relationship('CategoryAttributeLink', backref='category', lazy='dynamic')


class AttributeValues(db.Model):
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), primary_key=True)
    attribute_id = db.Column(db.Integer, db.ForeignKey('attributes.attribute_id'), primary_key=True)
    value_integer = db.Column(db.Integer)
    value_string = db.Column(db.String(64))


class StaffAnimalLink(db.Model):
    __tablename__ = 'staff_animal_link'
    staff_id = db.Column(db.Integer, db.ForeignKey('staff_category_link.staff_id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('staff_category_link.category_id'), primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.animal_id'), primary_key=True)
    start = db.Column(db.DateTime)


class StaffAnimalLinkArchive(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_id = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    animal_id = db.Column(db.Integer)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)


class Animals(db.Model):
    animal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    animal_name = db.Column(db.String(64))
    animal_type = db.Column(db.Integer, db.ForeignKey('animal_types.type_id'))
    medical_card = db.Column(db.Integer, db.ForeignKey('medical_cards.card_id'))
    transfer_card = db.Column(db.Integer, db.ForeignKey('transfer_cards.card_id'))
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.menu_id'))
    staff_link = db.relationship('StaffAnimalLink', backref='animal', lazy='dynamic')


class AnimalTypes(db.Model):
    __tablename__ = 'animal_types'
    type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(64))
    zone_id = db.Column(db.Integer, db.ForeignKey('climat_zones.zone_id'))
    feeding_type = db.Column(db.Integer, db.ForeignKey('feeding_types.type_id'))
    animal_link = db.relationship('Animals', backref='type', lazy='dynamic')


class StaffAnimalTypeLink(db.Model):
    __tablename__ = 'staff_animal_type_link'
    staff_id = db.Column(db.Integer, db.ForeignKey('staff_category_link.staff_id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('staff_category_link.category_id'), primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('animal_types.type_id'), primary_key=True)
    start = db.Column(db.DateTime)

    staff = db.relationship(StaffCategoryLink, foreign_keys=[staff_id])
    category = db.relationship(StaffCategoryLink, foreign_keys=[category_id])
    type = db.relationship(AnimalTypes, foreign_keys=[type_id])


class StaffAnimalTypeLinkArchive(db.Model):
    __tablename__ = 'staff_animal_type_link_archive'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    type_id = db.Column(db.Integer, db.ForeignKey('animal_types.type_id'))
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)

    staff = db.relationship(Staff, foreign_keys=[staff_id])
    category = db.relationship(Category, foreign_keys=[category_id])
    type = db.relationship(AnimalTypes, foreign_keys=[type_id])


class ClimatZones(db.Model):
    __tablename__ = 'climat_zones'
    zone_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    zone_name = db.Column(db.String(64))
    animal_type_link = db.relationship('AnimalTypes', backref='zone', lazy='dynamic')


class FeedingTypes(db.Model):
    __tablename__ = 'feeding_types'
    type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feeding_type_name = db.Column(db.String(64))
    animal_type_link = db.relationship('AnimalTypes', backref='ftype', lazy='dynamic')


class MedicalCards(db.Model):
    __tablename__ = 'medical_cards'
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    age = db.Column(db.Integer)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    gender = db.Column(db.String(64))
    animal_link = db.relationship('Animals', backref='mcard', lazy='dynamic')


class TransferCards(db.Model):
    __tablename__ = 'transfer_cards'
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    arrival_date = db.Column(db.Date)
    arrival_reason = db.Column(db.Integer, db.ForeignKey('arrival_reasons.reason_id'))
    transfered_from = db.Column(db.String(64))
    departure_date = db.Column(db.Date)
    departure_reason = db.Column(db.Integer, db.ForeignKey('departure_reasons.reason_id'))
    transfered_to = db.Column(db.String(64))
    animal_link = db.relationship('Animals', backref='tcard', lazy='dynamic')


class ArrivalReasons(db.Model):
    __tablename__ = 'arrival_reasons'
    reason_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reason_name = db.Column(db.String(64))
    transfer_card_link = db.relationship('TransferCards', backref='areason', lazy='dynamic')


class DepartureReasons(db.Model):
    __tablename__ = 'departure_reasons'
    reason_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reason_name = db.Column(db.String(64))
    transfer_card_link = db.relationship('TransferCards', backref='dreason', lazy='dynamic')


class Menu(db.Model):
    menu_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    food_type = db.Column(db.Integer, db.ForeignKey('food_types.type_id'))
    animal_link = db.relationship('Animals', backref='menu', lazy='dynamic')


class FoodTypes(db.Model):
    __tablename__ = 'food_types'
    type_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(64))
