from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


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

    def __repr__(self):
        return '<Staff {} {} {} {} {} {} {}>'.format(self.staff_id, self.first_name, self.second_name,
                                                     self.gender, self.age, self.salary, self.employment_date)


class StaffCategoryLink(db.Model):
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), primary_key=True)

    def __repr__(self):
        return '<StaffCategoryLink {} {}>'.format(self.staff_id, self.category_id)


class Categories(db.Model):
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(64))
    staff_link = db.relationship('StaffCategoryLink', backref='category', lazy='dynamic')
    attribute_link = db.relationship('CategoryAttributeLink', backref='attribute', lazy='dynamic')

    def __repr__(self):
        return '<Categories {} {}>'.format(self.category_id, self.category_name)


class CategoryAttributeLink(db.Model):
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), primary_key=True)
    attribute_id = db.Column(db.Integer, db.ForeignKey('attributes.attribute_id'), primary_key=True)

    def __repr__(self):
        return '<CategoryAttributeLink {} {}>'.format(self.category_id, self.attribute_id)


class Attributes(db.Model):
    attribute_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attribute_name = db.Column(db.String(64))
    attribute_type = db.Column(db.String(64))
    category_link = db.relationship('CategoryAttributeLink', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Attributes {} {} {}>'.format(self.attribute_id, self.attribute_name, self.attribute_type)


class AttributeValues(db.Model):
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), primary_key=True)
    attribute_id = db.Column(db.Integer, db.ForeignKey('attributes.attribute_id'), primary_key=True)
    value_integer = db.Column(db.Integer)
    value_string = db.Column(db.String(64))

    def __repr__(self):
        return '<AttributeValues {} {}>'.format(self.staff_id, self.category_id, self.attribute_id)
