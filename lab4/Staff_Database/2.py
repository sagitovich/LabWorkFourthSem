# повысить з/п сотруднику по его почте
from main import factory, Employees

session = factory()

input_email = input('Email: ')
u = session.query(Employees).where(Employees.email == input_email).first()

u.salary = u.salary * 1.2

session.commit()
