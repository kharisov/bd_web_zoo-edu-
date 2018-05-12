# -*- coding: utf-8 -*-
from flask import render_template, redirect, flash, url_for, request
from app import app, db
from app.forms import NewStaffForm, SelectStaffForm, LoginForm, CategoryForm, CategoryChooseForm
from app.models import Staff, User, Category, StaffCategoryLink
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/new_staff', methods=['GET', 'POST'])
@login_required
def new_staff():
    if current_user.urole != 'admin':
        flash('You have no rights')
        return redirect('/index')
    form = NewStaffForm()
    if form.validate_on_submit():
        staff = Staff(first_name=form.first_name.data, second_name=form.second_name.data, gender=form.gender.data,
                      age=form.age.data, salary=form.salary.data, employment_date=form.employment_date.data)
        db.session.add(staff)
        db.session.commit()
        flash('New user added')
        return redirect(url_for('new_staff'))
    return render_template('newStaff.html', title='New staff', form=form)


@app.route('/show_staff', methods=['GET', 'POST'])
@login_required
def show_staff():
    form = SelectStaffForm()
    query = Staff.query
    if form.validate_on_submit():
        gender_data = form.gender.data
        if gender_data is not None:
            query = query.filter(Staff.gender == gender_data)
        age = form.age.data
        if age is not None:
            query = query.filter(Staff.age >= age)
        salary = form.salary.data
        if salary is not None:
            query = query.filter(Staff.salary >= salary)
        date = form.employment_date.data
        if date is not None:
            query = query.filter(Staff.employment_date >= date)
    staff = query.all()
    categories = Category.query.all()
    category_choose_forms = {}
    for s in staff:
        selected_categories = StaffCategoryLink.query.filter(StaffCategoryLink.staff_id == s.staff_id).all()
        choose_form = CategoryChooseForm(prefix=str(s.staff_id))
        choose_form.category_name.choices = [(c.category_id, c.category_name) for c in categories]
        choose_form.category_name.process_data(c.category_id for c in selected_categories)
        category_choose_forms[s.staff_id] = choose_form
    return render_template('showStaff.html', title='Show staff', staff=staff, form=form,
                           category_choose_forms=category_choose_forms)


@app.route('/update_staff_categories', methods=['POST'])
@login_required
def update_staff_categories():
    new_categories = request.form.getlist('categories[]')
    StaffCategoryLink.query.filter(StaffCategoryLink.staff_id == request.form['staff_id']).delete()
    for c in new_categories:
        link = StaffCategoryLink(staff_id=request.form['staff_id'], category_id=c)
        db.session.add(link)
    db.session.commit()
    return 'Ok'


@app.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    if current_user.urole != 'admin':
        flash('You have no rights')
        return redirect('/index')
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(category_name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('New category added')
        return redirect(url_for('categories'))
    categories = Category.query.all()
    return render_template('categories.html', categories=categories, title='Categories', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
