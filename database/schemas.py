from database.engine import Base
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, \
                                      ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(55), nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(55))
    last_name = Column(String(75))

    contacts = relationship("Contact")
    employee = relationship("Employee")

    __table_args__ = (
        UniqueConstraint('username'),
    )
    
class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(45), nullable=False)
    description = Column(String(125), nullable=False)

class Organisation(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True)
    name = Column(String(125), nullable=False)
    description = Column(String(255))

    employees = relationship("Employee")
    services = relationship("Service")
    clients = relationship("Client")
    advices = relationship("Advice")

    __table_args__ = (
        UniqueConstraint('name'),
    )

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    title = Column(String(55), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    org_id = Column(Integer, ForeignKey("organisations.id"))
    write = Column(Boolean, nullable=False)
    chek = Column(Boolean, nullable=False)
    delete = Column(Boolean, nullable=False)


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organisations.id"))
    title = Column(String(55), nullable=False)
    description = Column(String(255))

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organisations.id"))
    first_name = Column(String(55), nullable=False)
    middle_name = Column(String(55), nullable=False)
    last_name = Column(String(55), nullable=False)
    source = Column(String(255))
    email = Column(String(55))
    is_potentincial = Column(Boolean, nullable=False)
    phone = Column(String(20))
    address = Column(String(255))

class Advice(Base):
    __tablename__ = "advices"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organisations.id"))
    title = Column(String(55), nullable=False)
    description = Column(String(255), nullable=False)

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organisations.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    empl_id = Column(Integer, ForeignKey("employees.id"))
    title = Column(String(55), nullable=False)
    description = Column(String(255))
    status = Column(String(255))
    created_date = Column(DateTime(), default=datetime.now)
    

    employee = relationship("Employee")
    organisation = relationship("Organisation")
    service = relationship("Service")
    client = relationship("Client")

