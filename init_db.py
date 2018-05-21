from app.models import *

db.session.execute('CREATE TRIGGER arch_an_st_link BEFORE DELETE ON staff_animal_link FOR EACH ROW BEGIN '
                   'INSERT INTO staff_animal_link_archive (staff_id, category_id, animal_id, start, end) '
                   'VALUES (OLD.staff_id, OLD.category_id, OLD.animal_id, OLD.start, datetime(\'now\', \'localtime\')); '
                   'END;')

db.session.execute('CREATE TRIGGER arch_an_tp_st_link BEFORE DELETE ON staff_animal_type_link FOR EACH ROW BEGIN '
                   'INSERT INTO staff_animal_type_link_archive (staff_id, category_id, type_id, start, end) '
                   'VALUES (OLD.staff_id, OLD.category_id, OLD.type_id, OLD.start, datetime(\'now\', \'localtime\')); '
                   'END;')

a = User(username='admin', urole='admin')
a.set_password('admin')
db.session.add(a)
u = User(username='user', urole='user')
u.set_password('user')
db.session.add(u)

db.session.add(ClimatZones(zone_name='Forest'))
db.session.add(ClimatZones(zone_name='Desert'))
db.session.add(ClimatZones(zone_name='Mountains'))

db.session.add(FeedingTypes(feeding_type_name='Predator'))
db.session.add(FeedingTypes(feeding_type_name='Vegan'))
db.session.add(FeedingTypes(feeding_type_name='Omnivorous'))

db.session.add(ArrivalReasons(reason_name='Birth'))
db.session.add(ArrivalReasons(reason_name='Transfer'))

db.session.add(DepartureReasons(reason_name='Birth'))
db.session.add(DepartureReasons(reason_name='Transfer'))

db.session.add(Category(category_name='Cleaner'))
db.session.add(Category(category_name='Vet'))
db.session.add(Category(category_name='Trainer'))
db.session.add(Category(category_name='Guard'))

db.session.add(AnimalTypes(type_name='Bear', zone_id='1', feeding_type='1'))
db.session.add(AnimalTypes(type_name='Snake', zone_id='2', feeding_type='1'))
db.session.add(AnimalTypes(type_name='Monkey', zone_id='3', feeding_type='3'))

db.session.add(Diseases(disease_name='Cold'))
db.session.add(Diseases(disease_name='Diarrhea'))

db.session.add(Vaccines(vaccine_name='Anti Cold'))
db.session.add(Vaccines(vaccine_name='Anti Diarrhea'))

db.session.commit()
