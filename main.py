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
