# -*- coding: utf-8 -*-
from flask import render_template, redirect, flash
from app import app, db
from app.forms import NewStaffForm, SelectStaffForm
from app.models import Staff

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/new_staff', methods=['GET', 'POST'])
def new_staff():
    form = NewStaffForm()
    if form.validate_on_submit():
        staff = Staff(first_name=form.first_name.data, second_name=form.second_name.data, gender=form.gender.data,
                      age=form.age.data, salary=form.salary.data, employment_date=form.employment_date.data)
        db.session.add(staff)
        db.session.commit()
        flash('New user added')
        return redirect('/index')
    return render_template('newStaff.html', title='New staff', form=form)


@app.route('/show_staff', methods=['GET', 'POST'])
def show_staff():
    form = SelectStaffForm()
    if form.validate_on_submit():
        query = Staff.query
        gender_data = form.gender.data
        if gender_data != "None":
            query = query.filter(Staff.gender == gender_data)
        return render_template('showStaff.html', title='Show staff', staff=query.all(), form=form)
    return render_template('showStaff.html', title='Show staff', staff=None, form=form)
