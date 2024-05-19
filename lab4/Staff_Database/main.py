
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, DateTime

from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Так просто надо сделать
class Basis(DeclarativeBase):
    pass


class Employees(Basis):
    __tablename__ = "employees"
    employee_id = Column(Integer(), primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False, unique=True, index=True)
    phone_number = Column(Integer(), nullable=False, unique=True, index=True)
    hire_date = Column(DateTime(), default=None)
    job_id = Column(String(50), nullable=False, unique=True, index=True)
    salary = Column(Integer(), nullable=False, unique=True, index=True)
    commission_pct = Column(String(50), nullable=False, unique=True, index=True)
    manager_id = Column(Integer())
    department_id = Column(Integer())

    def __str__(self):
        return f"<{self.employee_id}> {self.first_name} {self.last_name} - {self.email}@gmail.com"

    def __repr__(self):
        return f"{self.email}@gmail.com - ({self.first_name} {self.last_name})"


class Department(Basis):
    __tablename__ = "departments"
    department_id = Column(Integer(), primary_key=True)
    # department_id = Column(Integer(), ForeignKey('employees.department_id'), primary_key=True)
    department_name = Column(String())
    manager_id = Column(Integer())
    location_id = Column(Integer())


engine = create_engine("sqlite:///Staff.db?echo=True")

Basis.metadata.create_all(engine)

factory = sessionmaker(bind=engine)
