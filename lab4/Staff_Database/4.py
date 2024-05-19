# удаление пользователя по id
from main import Employees, factory

# Создаем сессию
session = factory()

id_ = int(input('Enter id: '))
# Находим пользователя по id
user = session.query(Employees).get(id_)  # замените 207 на конкретный id пользователя

# Если пользователь с таким id существует, удаляем его
try:
    session.delete(user)
    session.commit()
except Exception as ex:
    print(f'Error: {ex}')
