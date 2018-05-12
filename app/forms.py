from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, PasswordField,\
    BooleanField, SelectMultipleField, validators
from wtforms.fields.html5 import DateField
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
    gender = SelectField('Gender', choices=[('male', 'male'), ('female', 'female'), ('other', 'other')], validators=[Optional()])
    age = IntegerField('Age', [validators.NumberRange(min=0, max=100), Optional()])
    salary = IntegerField('Salary', validators=[Optional()])
    employment_date = DateField('In zoo longer than date', validators=[Optional()])
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
    submit_categories = SubmitField('Submit Categories')
