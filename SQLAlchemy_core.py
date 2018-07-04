from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

engine = create_engine('sqlite:///database.db', echo=True)

metadata = MetaData()

users = Table('users',
              metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('fullname', String))

address = Table('address',
                metadata,
                Column('id', Integer, primary_key=True),
                Column('user_id', None, ForeignKey('users.id')),
                Column('email_address', String, nullable=False))

metadata.create_all(engine)
conn = engine.connect()
conn.execute(users.insert(), [dict(name='jack', fullname='Jack Jones'),
                              dict(name='wendy', fullname='Wendy Williams')])
conn.execute(address.insert(), [
    {'user_id': 1, 'email_address': 'jack@yahoo.com'}
])

from sqlalchemy.sql import select

s = select([users])
result = conn.execute(s)
for row in result:
    # <class 'sqlalchemy.engine.result.RowProxy'>
    print(type(row))
    # (6, 'wendy', 'Wendy Williams')
    print(row)

s = select([users, address]).where(users.c.id == address.c.user_id)
for row in conn.execute(s):
    print(row)

from sqlalchemy.sql import text

s = text(
    "SELECT users.fullname || ', ' || address.email_address AS title "
    "FROM users, address "
    "WHERE users.id = address.user_id "
    "AND users.name BETWEEN :x AND :y "
    "OR address.email_address LIKE :e2)"
)
