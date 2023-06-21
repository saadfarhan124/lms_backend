from sqlalchemy import Column, String, ForeignKey, Integer, Date, DateTime
from sqlalchemy.orm import relationship
from app.database.database import Base
from app.constants import CustomerType, BusinessType, Gender, MaritalStatus, OccupationStatus
from sqlalchemy.sql import func


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    photo = Column(String)
    user_type = Column(Integer, default=CustomerType.INDIVIDUAL)
    individual = relationship("Individual", back_populates="customer")
    business = relationship("Business", back_populates="customer")
    time_created = Column(DateTime(timezone=True),
                             server_default=func.now(), nullable=False)
    time_updated = Column(DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Individual(Base):
    __tablename__ = "individuals"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String)
    date_of_birth = Column(Date, nullable=False)
    citizenship = Column(String, nullable=False)
    marrital_status = Column(Integer, default=MaritalStatus.SINGLE)
    occupation_status = Column(Integer, default=OccupationStatus.EMPLOYED)
    gender = Column(Integer, default=Gender.Male)
    time_created = Column(DateTime(timezone=True),
                             server_default=func.now(), nullable=False)
    time_updated = Column(DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    customer_id = Column(Integer, ForeignKey(
        "customers.id"), unique=True, nullable=False)
    customer = relationship("Customer", back_populates="individual")

    employer = relationship("Employer", uselist=False,
                            back_populates="individual")
    address = relationship("Address", uselist=False,
                           back_populates="individual")
    email_addresses = relationship("EmailAddress", back_populates="individual")
    mobile_numbers = relationship("MobileNumber", back_populates="individual")


class Employer(Base):
    __tablename__ = "employers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String)
    number = Column(String)
    time_created = Column(DateTime(timezone=True),
                             server_default=func.now(), nullable=False)
    time_updated = Column(DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    individual_id = Column(Integer, ForeignKey(
        "individuals.id"), unique=True, nullable=False)
    individual = relationship("Individual", back_populates="employer")


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    street = Column(String, nullable=False)
    village = Column(String, nullable=False)
    district = Column(String, nullable=False)
    nearest_landmark = Column(String, nullable=False)
    country = Column(String, nullable=False)
    time_created = Column(DateTime(timezone=True),
                             server_default=func.now(), nullable=False)
    time_updated = Column(DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    individual_id = Column(Integer, ForeignKey(
        "individuals.id"), unique=True, nullable=False)
    individual = relationship("Individual", back_populates="address")


class MobileNumber(Base):
    __tablename__ = "mobile_numbers"
    id = Column(Integer, primary_key=True)
    number = Column(String)
    time_created = Column(DateTime(timezone=True),
                             server_default=func.now(), nullable=False)
    time_updated = Column(DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    individual_id = Column(Integer, ForeignKey(
        "individuals.id"), nullable=False)
    individual = relationship("Individual", back_populates="mobile_numbers")


class EmailAddress(Base):
    __tablename__ = "email_addresses"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    time_created = Column(DateTime(timezone=True),
                             server_default=func.now(), nullable=False)
    time_updated = Column(DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    individual_id = Column(Integer, ForeignKey(
        "individuals.id"), nullable=False)
    individual = relationship("Individual", back_populates="email_addresses")


class Business(Base):
    __tablename__ = "bussinesses"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    business_type = Column(Integer, default=BusinessType.CORPORATION)
    business_number = Column(String)
    business_email = Column(String)
    time_created = Column(DateTime(timezone=True),
                             server_default=func.now(), nullable=False)
    time_updated = Column(DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    customer_id = Column(Integer, ForeignKey(
        "customers.id"), unique=True, nullable=False)
    customer = relationship("Customer", back_populates="business")

