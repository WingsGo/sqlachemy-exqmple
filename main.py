from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "User<name='{}', fullname='{}'>".format(self.name, self.fullname)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

ed_user = User(name='ed', fullname='Ed Jones', password='edpassword')
session.add(ed_user)

session.add_all([
    User(name='wendy', fullname='Wendy Williams', password='foobar'),
    User(name='mary', fullname='Mary Contrary', password='xxg527'),
    User(name='fred', fullname='Fred Flinstone', password='blah')])

ed_user.password = 'f805'

session.commit()

for instance in session.query(User).filter(User.name.in_(['wendy', 'mary'])).all():
    print(instance)
print('\n')

for instance in session.query(User.name, User.fullname):
    print(instance)
print('\n')

for named_tuple in session.query(User, User.name).all():
    print(named_tuple.User, named_tuple.name)


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship('User', back_populates='addresses', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<Address(email_address='{}'>".format(self.email_address)


Base.metadata.create_all(engine)

User.addresses = relationship('Address', order_by=Address.id, back_populates='user')

jack = User(name='jack', fullname='Jack Bean', password='safasd')
print(jack.addresses)
jack.addresses = [Address(email_address='jk@google.com'),
                  Address(email_address='jk@qq.com')]
print(jack.addresses[1])
print(jack.addresses[1].user)
session.add(jack)
session.commit()

jack = session.query(User).filter_by(name='jack').one()
print(jack)
print(jack.addresses)

for u, a in session.query(User, Address).filter(User.id == Address.user_id).filter(
        Address.email_address == 'jack@google.com').all():
    print(u)
    print(a)

session.query(User).join(Address).filter(Address.email_address == 'jack@google.com').all()

session.query.join(Address, User.id == Address.user_id)  # explicit condition
session.query.join(User.addresses)  # specify relationship from left to right
session.query.join(Address, User.addresses)  # same, with explicit target
session.query.join('addresses')  # same, using a string


#简单查询
    print(session.query(User).all())
    print(session.query(User.name, User.fullname).all())
    print(session.query(User, User.name).all())
    
    #带条件查询
    print(session.query(User).filter_by(name='user1').all())
    print(session.query(User).filter(User.name == "user").all())
    print(session.query(User).filter(User.name.like("user%")).all())
    
    #多条件查询
    print(session.query(User).filter(and_(User.name.like("user%"), User.fullname.like("first%"))).all())
    print(session.query(User).filter(or_(User.name.like("user%"), User.password != None)).all())
    
    #sql过滤
    print(session.query(User).filter("id>:id").params(id=1).all())
    
    #关联查询 
    print(session.query(User, Address).filter(User.id == Address.user_id).all())
    print(session.query(User).join(User.addresses).all())
    print(session.query(User).outerjoin(User.addresses).all())
    
    #聚合查询
    print(session.query(User.name, func.count('*').label("user_count")).group_by(User.name).all())
    print(session.query(User.name, func.sum(User.id).label("user_id_sum")).group_by(User.name).all())
    
    #子查询
    stmt = session.query(Address.user_id, func.count('*').label("address_count")).group_by(Address.user_id).subquery()
    print(session.query(User, stmt.c.address_count).outerjoin((stmt, User.id == stmt.c.user_id)).order_by(User.id).all())
    
    #exists
    print(session.query(User).filter(exists().where(Address.user_id == User.id)))
    print(session.query(User).filter(User.addresses.any()))
    
    
    from sqlalchemy import func

# count User records, without
# using a subquery.
session.query(func.count(User.id))

# return count of user "id" grouped
# by "name"
session.query(func.count(User.id)).\
        group_by(User.name)

from sqlalchemy import distinct

# count distinct "name" values
session.query(func.count(distinct(User.name)))


person = session.query(Person.name, Person.created_at,                     
             Person.updated_at).filter_by(name="zhongwei").order_by(            
             Person.created_at).first()

stmt = select([users_table]).where(and_(users_table.c.name == 'wendy, users_table.c.entrolled == True))
stmt = select([users_table]).where((users_table.c.name == 'wendy) && (users_table.c.entrolled == True))
                                        
stmt = (users_table.update().
        where(user_table.c.name == bindparam('username')).
        values(fullname=bindparam('fullname'))
        )

connection.execute(
    stmt, [{"username": "wendy", "fullname": "Wendy Smith"},
           {"username": "jack", "fullname": "Jack Jones"},
           ]
)
                 
stmt = select([users_table]).where(users_table.c.name == 'Wendy')
result = connection.execute(stmt)
                                   
from sqlalchemy import funcfilter
funcfilter(func.count(1), MyClass.name == 'some name')
select([func.count(table.c.id)])
stmt = select([func.count(SourceFuncTable.device_id)])
for result in self._session.execute(stmt):
    print(result.items())

from sqlalchemy import text
# bind parameters by name
t = text("SELECT * FROM users WHERE id=:user_id")
result = connection.execute(t, user_id=12)
t = text("SELECT * FROM users WHERE id=:user_id").bindparams(user_id=7).columns(id=Integer, name=String)
for id, name in connection.execute(t):
    print(id, name)
    
# LIKE
stmt = select([SourceFuncTable]).where(SourceFuncTable.type_.contains('test'))
stmt = select([SourceFuncTable]).where(SourceFuncTable.type_.startswith('test'))
print(stmt)
