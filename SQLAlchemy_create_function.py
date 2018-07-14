from sqlalchemy import Column, String, Integer, ForeignKey, select
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    employees = relationship('Employee', secondary='department_employee')


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    departments = relationship('Department', secondary='department_employee')


class DepartmentEmployee(Base):
    __tablename__ = 'department_employee'
    department_id = Column(Integer, ForeignKey('department.id'), primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'), primary_key=True)


engine = create_engine('sqlite:///database.db')

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)


def custom_func(value, dest):
    if dest in value.split('-'):
        return 1
    return 0


if __name__ == '__main__':
    s = session()

    marry = Employee(name='marry')
    data1 = Employee(name='125.00-25.00-156.25')
    data2 = Employee(name='125.00-156.25')
    financial_department = Department(name='financial')
    financial_department.employees.append(marry)
    s.add(marry)
    s.add(data1)
    s.add(data2)
    s.add(financial_department)
    s.query(Employee).filter(Employee.name.contains('a')).all()
    s.commit()

    conn = s.bind.connect()  # equal to engine.connect()
    conn.connection.create_function("custom", 2, custom_func)
    cur = conn.connection.cursor()
    cur.execute("SELECT * FROM employee WHERE custom(name, '25.00') == 1")
    for i in cur.fetchall():
        print(i)
