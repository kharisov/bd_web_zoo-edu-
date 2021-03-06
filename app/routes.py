# -*- coding: utf-8 -*-
from flask import render_template, redirect, flash, url_for, request
from app import app
from app.forms import *
from app.models import *
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import datetime
from sqlalchemy import or_


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
    form.categories.choices = [(c.category_id, c.category_name) for c in Category.query.all()]
    query = Staff.query
    if form.validate_on_submit():
        gender_data = form.gender.data
        if gender_data is not None and gender_data != 'None':
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
        categories = form.categories.data
        if categories is not None and categories:
            query = query.join(StaffCategoryLink).filter(StaffCategoryLink.category_id.in_(categories))
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
    StaffCategoryLink.query.filter(StaffCategoryLink.staff_id == int(request.form['staff_id'])).delete()
    for c in new_categories:
        link = StaffCategoryLink(staff_id=request.form['staff_id'], category_id=c)
        db.session.add(link)
    db.session.commit()
    return 'Ok'


@app.route('/update_responsible_staff', methods=['POST'])
@login_required
def update_responsible_staff():
    new_staff = request.form.getlist('staff[]')
    parsed = []
    for s in new_staff:
        split = s.split('_')
        parsed.append((int(split[0]), int(int(split[1]))))
    StaffAnimalLink.query.filter(StaffAnimalLink.animal_id == int(request.form['animal_id'])). \
        filter(or_(~StaffAnimalLink.staff_id.in_([p[0] for p in parsed]),
                   ~StaffAnimalLink.category_id.in_([p[1] for p in parsed]))).delete(synchronize_session='fetch')
    for p in parsed:
        if not StaffAnimalLink.query.filter(StaffAnimalLink.animal_id == int(request.form['animal_id'])). \
                filter(StaffAnimalLink.staff_id == p[0]). \
                filter(StaffAnimalLink.category_id == p[1]).first():
            link = StaffAnimalLink(animal_id=int(request.form['animal_id']), staff_id=p[0],
                                   category_id=p[1], start=datetime.datetime.now())
            db.session.add(link)
    db.session.commit()
    return 'Ok'


@app.route('/update_type_responsible_staff', methods=['POST'])
@login_required
def update_type_responsible_staff():
    new_staff = request.form.getlist('staff[]')
    parsed = []
    for s in new_staff:
        split = s.split('_')
        parsed.append((int(split[0]), int(int(split[1]))))
    StaffAnimalTypeLink.query.filter(StaffAnimalTypeLink.type_id == int(request.form['type_id'])). \
        filter(or_(~StaffAnimalTypeLink.staff_id.in_([p[0] for p in parsed]),
                   ~StaffAnimalTypeLink.category_id.in_([p[1] for p in parsed]))).delete(synchronize_session='fetch')
    for p in parsed:
        if not StaffAnimalTypeLink.query.filter(StaffAnimalTypeLink.type_id == int(request.form['type_id'])). \
                filter(StaffAnimalTypeLink.staff_id == p[0]). \
                filter(StaffAnimalTypeLink.category_id == p[1]).first():
            link = StaffAnimalTypeLink(type_id=int(request.form['type_id']), staff_id=p[0],
                                       category_id=p[1], start=datetime.datetime.now())
            db.session.add(link)
    db.session.commit()
    return 'Ok'


@app.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(category_name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('New category added')
        return redirect(url_for('categories'))
    categories = Category.query.all()
    return render_template('categories.html', categories=categories, title='Categories', form=form)


@app.route('/delete_category', methods=['POST'])
@login_required
def delete_category():
    category_id = int(request.form['id'])
    Category.query.filter(Category.category_id == category_id).delete()
    StaffCategoryLink.query.filter(StaffCategoryLink.category_id == category_id).delete()
    db.session.commit()
    return 'Ok'


@app.route('/animal_types', methods=['GET', 'POST'])
@login_required
def animal_types():
    form = AnimalTypeForm()
    form.zone.choices = [(z.zone_id, z.zone_name) for z in ClimatZones.query.all()]
    form.feeding.choices = [(f.type_id, f.feeding_type_name) for f in FeedingTypes.query.all()]
    if form.validate_on_submit():
        atype = AnimalTypes(type_name=form.name.data, zone_id=form.zone.data, feeding_type=form.feeding.data)
        db.session.add(atype)
        db.session.commit()
        flash('New animal type added')
        return redirect(url_for('animal_types'))
    types = AnimalTypes.query.all()
    types_dict = []
    staff_choose_forms = {}
    allowed_categories = {'Vet', 'Cleaner', 'Trainer'}
    staff = StaffCategoryLink.query.join(Staff).join(Category).all()
    for t in types:
        types_dict.append((t.type_name, t.zone.zone_name, t.ftype.feeding_type_name, t.type_id))
        selected_staff = StaffAnimalTypeLink.query.filter(StaffAnimalTypeLink.type_id == t.type_id).all()
        choose_form = ResponsibleStaffForm(prefix=str(t.type_id))
        choose_form.responsible_staff.choices = [(str(s.staff_id) + '_' + str(s.category.category_id),
                                                  s.staff.first_name + ' (' + s.category.category_name + ')')
                                                 for s in staff if s.category.category_name in allowed_categories]
        choose_form.responsible_staff.process_data(str(s.staff_id) + '_' + str(s.category_id) for s in selected_staff)
        staff_choose_forms[t.type_id] = choose_form
    return render_template('animalTypes.html', types=types_dict, title='Animal Types', form=form,
                           choose_forms=staff_choose_forms)


@app.route('/new_animal', methods=['GET', 'POST'])
@login_required
def new_animal():
    if current_user.urole != 'admin':
        flash('You have no rights')
        return redirect('/index')
    form = NewAnimalForm()
    form.type.choices = [(t.type_id, t.type_name) for t in AnimalTypes.query.all()]
    form.arrival_reason.choices = [(r.reason_id, r.reason_name) for r in ArrivalReasons.query.all()]
    if form.validate_on_submit():
        med_card = MedicalCards(age=form.age.data, height=form.height.data,
                                weight=form.weight.data, gender=form.gender.data)
        trans_card = TransferCards(arrival_date=form.arrival_date.data, arrival_reason=form.arrival_reason.data)
        db.session.add(med_card)
        db.session.add(trans_card)
        db.session.commit()
        animal = Animals(animal_name=form.name.data, animal_type=form.type.data,
                         medical_card=MedicalCards.query.order_by(MedicalCards.card_id.desc()).first().card_id,
                         transfer_card=TransferCards.query.order_by(TransferCards.card_id.desc()).first().card_id)
        db.session.add(animal)
        db.session.commit()
        flash('New animal added')
        return redirect(url_for('new_animal'))
    return render_template('newAnimal.html', title='New Animal', form=form)


@app.route('/show_animals', methods=['GET', 'POST'])
@login_required
def show_animals():
    form = SelectAnimalsForm()
    form.types.choices = [(t.type_id, t.type_name) for t in AnimalTypes.query.all()]
    query = Animals.query.join(AnimalTypes).join(MedicalCards)
    if form.validate_on_submit():
        types = form.types.data
        if types is not None:
            query = query.filter(AnimalTypes.type_id.in_(types))
        gender_data = form.gender.data
        if gender_data is not None and gender_data != 'None':
            query = query.filter(MedicalCards.gender == gender_data)
        age = form.age.data
        if age is not None:
            query = query.filter(MedicalCards.age >= age)
        height = form.height.data
        if height is not None:
            query = query.filter(MedicalCards.height >= height)
        weight = form.weight.data
        if weight is not None:
            query = query.filter(MedicalCards.weight >= weight)
    animals = query.all()

    staff = StaffCategoryLink.query.join(Staff).join(Category).all()
    staff_choose_forms = {}
    allowed_categories = {'Vet', 'Cleaner', 'Trainer'}
    for a in animals:
        selected_staff = StaffAnimalLink.query.filter(StaffAnimalLink.animal_id == a.animal_id).all()
        choose_form = ResponsibleStaffForm(prefix=str(a.animal_id))
        choose_form.responsible_staff.choices = [(str(s.staff_id) + '_' + str(s.category.category_id),
                                                  s.staff.first_name + ' (' + s.category.category_name + ')')
                                                 for s in staff if s.category.category_name in allowed_categories]
        choose_form.responsible_staff.process_data(str(s.staff_id) + '_' + str(s.category_id) for s in selected_staff)
        staff_choose_forms[a.animal_id] = choose_form
    return render_template('showAnimals.html', title='Show animals', form=form, animals=animals, choose_forms=staff_choose_forms)


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


@app.route('/show_types_archive', methods=['GET', 'POST'])
@login_required
def show_types_archive():
    form = TypesArchiveQueryForm()
    form.type.choices = [(t.type_id, t.type_name) for t in AnimalTypes.query.all()]
    form.type.choices.append((-1, 'None'))
    query = StaffAnimalTypeLinkArchive.query.join(Staff).join(Category).join(AnimalTypes)
    if form.validate_on_submit():
        type = form.type.data
        if type is not None and type != -1:
            query = query.filter(AnimalTypes.type_id == type)
        start = form.start.data
        if start is not None:
            query = query.filter(StaffAnimalTypeLinkArchive.start >= start)
        end = form.end.data
        if end is not None:
            query = query.filter(StaffAnimalTypeLinkArchive.end <= end)
    res = query.all()
    for r in res:
        r.start = r.start.replace(microsecond=0)
        r.end = r.end.replace(microsecond=0)
    return render_template('typesArchive.html', form=form, title='Archive', result=res)


@app.route('/show_animals_archive', methods=['GET', 'POST'])
@login_required
def show_animals_archive():
    form = AnimalsArchiveQueryForm()
    form.animal.choices = [(a.animal_id, a.animal_name) for a in Animals.query.all()]
    form.animal.choices.append((-1, 'None'))
    query = StaffAnimalLinkArchive.query.join(Staff).join(Category).join(Animals)
    if form.validate_on_submit():
        animal = form.animal.data
        if animal is not None and animal != -1:
            query = query.filter(Animals.animal_id == animal)
        start = form.start.data
        if start is not None:
            query = query.filter(StaffAnimalLinkArchive.start >= start)
        end = form.end.data
        if end is not None:
            query = query.filter(StaffAnimalLinkArchive.end <= end)
    res = query.all()
    for r in res:
        r.start = r.start.replace(microsecond=0)
        r.end = r.end.replace(microsecond=0)
    return render_template('animalsArchive.html', form=form, title='Archive', result=res)


@app.route('/medical_card/<animal_id>', methods=['GET', 'POST'])
@login_required
def medical_card(animal_id):
    animal_id = int(animal_id)
    medical_card_form = MedicalCardForm(prefix='card')
    animal = Animals.query.filter(Animals.animal_id == animal_id).join(MedicalCards).first()
    if medical_card_form.validate_on_submit():
        age = medical_card_form.age.data
        if age is not None:
            animal.mcard.age = age
        height = medical_card_form.height.data
        if height is not None:
            animal.mcard.height = height
        weight = medical_card_form.weight.data
        if weight is not None:
            animal.mcard.weight = weight
        db.session.commit()
        return redirect('/medical_card/' + str(animal_id))

    vaccine_form = NewVaccineForm(prefix='vaccine')
    vaccines = Vaccines.query.all()
    used_vaccines = Vaccination.query.filter(Vaccination.card_id == animal.mcard.card_id).join(Vaccines).all()
    vaccine_form.vaccine.choices = [(v.vaccine_id, v.vaccine_name) for v in vaccines
                                    if v.vaccine_id not in [u.vaccine_id for u in used_vaccines]]
    if vaccine_form.vaccine.data and vaccine_form.validate_on_submit():
        vac = Vaccination(vaccine_id=vaccine_form.vaccine.data, card_id=animal.mcard.card_id,
                          date=vaccine_form.date.data)
        db.session.add(vac)
        db.session.commit()
        return redirect('/medical_card/' + str(animal_id))

    disease_form = NewDiseaseForm(prefix='disease')
    prev_diseases = Illness.query.filter(Illness.card_id == animal.mcard.card_id).join(Diseases).all()
    diseases = Diseases.query.all()
    disease_form.disease.choices = [(d.disease_id, d.disease_name) for d in diseases]
    if disease_form.disease.data and disease_form.validate_on_submit():
        ill = Illness(disease_id=disease_form.disease.data, card_id=animal.mcard.card_id,
                      start=disease_form.start.data, end=disease_form.end.data)
        db.session.add(ill)
        db.session.commit()
        return redirect('/medical_card/' + str(animal_id))
    return render_template('medicalCard.html', animal=animal, medical_card_form=medical_card_form,
                           vaccines=used_vaccines, vaccine_form=vaccine_form,
                           diseases=prev_diseases, disease_form=disease_form)
