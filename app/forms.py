from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, PasswordField,\
    BooleanField, SelectMultipleField, validators
from wtforms.fields.html5 import DateField
from wtforms.ext.dateutil.fields import DateTimeField
from wtforms.validators import DataRequired, Optional


class NewStaffForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    second_name = StringField('Second name', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'male'), ('female', 'female'), ('other', 'other')])
    age = IntegerField('Age', [validators.NumberRange(min=0, max=100)])
    salary = IntegerField('Salary')
    employment_date = DateField('Employment date', validators=[DataRequired()])
    submit = SubmitField('Add new staff')


class SelectStaffForm(FlaskForm):
    gender = SelectField('Gender', choices=[('None', 'None'), ('male', 'male'), ('female', 'female'), ('other', 'other')],
                         default=('None', 'None'), validators=[Optional()])
    age = IntegerField('Age', [validators.NumberRange(min=0, max=100), Optional()])
    salary = IntegerField('Salary', validators=[Optional()])
    employment_date = DateField('In zoo longer than date', validators=[Optional()])
    categories = SelectMultipleField('Categories', coerce=int, validators=[Optional()])
    submit = SubmitField('Show filtered staff')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Add Category')


class CategoryChooseForm(FlaskForm):
    category_name = SelectMultipleField('Category')


class AnimalTypeForm(FlaskForm):
    name = StringField('Animal Type Name', validators=[DataRequired()])
    zone = SelectField('Zone', coerce=int, validators=[DataRequired()])
    feeding = SelectField('Feeding Type', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Animal Type')


class NewAnimalForm(FlaskForm):
    name = StringField('Animal Name', validators=[DataRequired()])
    type = SelectField('Animal Type', coerce=int, validators=[DataRequired()])
    age = IntegerField('Age', [validators.NumberRange(min=0, max=200)])
    height = IntegerField('Height(meters)')
    weight = IntegerField('Weight(kg)')
    gender = SelectField('Gender', choices=[('male', 'male'), ('female', 'female')], validators=[DataRequired()])
    arrival_date = DateField('Arrival Date', validators=[DataRequired()])
    arrival_reason = SelectField('Arrival Reason', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add new animal')


class ResponsibleStaffForm(FlaskForm):
    responsible_staff = SelectMultipleField('Responsible Staff')


class TypesArchiveQueryForm(FlaskForm):
    type = SelectField('Animal Type', coerce=int, validators=[Optional()])
    start = DateTimeField('Start', validators=[Optional()])
    end = DateTimeField('End', validators=[Optional()])
    submit = SubmitField('Sort')


class AnimalsArchiveQueryForm(FlaskForm):
    animal = SelectField('Animal', coerce=int, validators=[Optional()])
    start = DateTimeField('Start', validators=[Optional()])
    end = DateTimeField('End', validators=[Optional()])
    submit = SubmitField('Sort')


class SelectAnimalsForm(FlaskForm):
    types = SelectMultipleField('Animal Types', coerce=int, validators=[Optional()])
    gender = SelectField('Gender', choices=[('None', 'None'), ('male', 'male'), ('female', 'female'), ('other', 'other')],
                         default=('None', 'None'), validators=[Optional()])
    age = IntegerField('Age', [validators.NumberRange(min=0, max=100), Optional()])
    height = IntegerField('Height', validators=[Optional()])
    weight = IntegerField('Weight', validators=[Optional()])
    submit = SubmitField('Show filtered animals')


class MedicalCardForm(FlaskForm):
    age = IntegerField('Age', [validators.NumberRange(min=0, max=100), Optional()])
    height = IntegerField('Height', validators=[Optional()])
    weight = IntegerField('Weight', validators=[Optional()])
    submit = SubmitField('Submit')


class NewVaccineForm(FlaskForm):
    vaccine = SelectField('Vaccine', coerce=int, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Submit')


class NewDiseaseForm(FlaskForm):
    disease = SelectField('Disease', coerce=int, validators=[DataRequired()])
    start = DateField('Start', validators=[DataRequired()])
    end = DateField('End', validators=[DataRequired()])
    submit = SubmitField('Submit')
