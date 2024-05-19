from main import factory, Employees, Department

session = factory()

user_id = int(input('Введите ID сотрудника: '))

# Получаем сотрудника по user_id
employee = session.query(Employees).filter_by(employee_id=user_id).first()

if employee:
    # Получаем department_id сотрудника
    department_id = employee.department_id

    # Получаем название департамента по department_id
    department = session.query(Department).filter_by(department_id=department_id).first()

    if department:
        print(f"Название департамента для сотрудника {employee.first_name} {employee.last_name}: {department.department_name}")
    else:
        print(f"Департамент с ID {department_id} не найден.")
else:
    print(f"Сотрудник с ID {user_id} не найден.")
