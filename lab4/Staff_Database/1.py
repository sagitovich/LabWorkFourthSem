# Добавим двух пользователей
from datetime import datetime
from main import factory
from main import Employees


u1 = Employees(first_name="Иван", last_name="Иванов", email="iivanov",
          hire_date=datetime.strptime('12.12.2012', '%d.%m.%Y'), salary=5000, job_id=10)

u2 = Employees(first_name="Пётр", last_name="Петров", email="ppetrov",
          hire_date=datetime.strptime('11.11.2011', '%d.%m.%Y'), salary=5000, job_id=10)

session = factory()
session.add_all([u1, u2])
session.commit()
