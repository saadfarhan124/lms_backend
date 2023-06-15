from sqlalchemy import Table, Column, String, ForeignKey, Integer, Date
from sqlalchemy.orm import relationship
from app.database.database import Base
from app.constants import CustomerType, CoBorrowerType, BusinessType, Gender, MaritalStatus, OccupationStatus


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    photo = Column(String)
    user_type = Column(Integer, default=CustomerType.INDIVIDUAL)
    individual = relationship("Individual", back_populates="customer")
    business = relationship("Business", back_populates="customer")
    co_borrowers = relationship("CoBorrowers", secondary="customer_coborrower", back_populates="customers")



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

    customer_id = Column(Integer, ForeignKey("customers.id"), unique=True, nullable=False)
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

    individual_id = Column(Integer, ForeignKey("individuals.id"), unique=True, nullable=False)
    individual = relationship("Individual", back_populates="employer")


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    street = Column(String, nullable=False)
    village = Column(String, nullable=False)
    district = Column(String, nullable=False)
    nearest_landmark = Column(String, nullable=False)
    country = Column(String, nullable=False)

    individual_id = Column(Integer, ForeignKey("individuals.id"), unique=True, nullable=False)
    individual = relationship("Individual", back_populates="address")


class MobileNumber(Base):
    __tablename__ = "mobile_numbers"
    id = Column(Integer, primary_key=True)
    number = Column(String)

    individual_id = Column(Integer, ForeignKey("individuals.id"), nullable=False)
    individual = relationship("Individual", back_populates="mobile_numbers")


class EmailAddress(Base):
    __tablename__ = "email_addresses"
    id = Column(Integer, primary_key=True)
    email = Column(String)

    individual_id = Column(Integer, ForeignKey("individuals.id"), nullable=False)
    individual = relationship("Individual", back_populates="email_addresses")


class Business(Base):
    __tablename__ = "bussinesses"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    business_type = Column(Integer, default=BusinessType.CORPORATION)
    business_number = Column(String)
    business_email = Column(String)

    customer_id = Column(Integer, ForeignKey("customers.id"), unique=True, nullable=False)
    customer = relationship("Customer", back_populates="business")


class CoBorrowers(Base):
    __tablename__ = "co_borrowers"
    id = Column(Integer, primary_key=True)
    type = Column(Integer, default=CoBorrowerType.INDIVIDUAL.value)
    individual = relationship("CoBorrowerIndividual", back_populates="co_borrower")
    business = relationship("CoBorrowerBusiness", back_populates="co_borrower")
    customers = relationship("Customer", secondary="customer_coborrower", back_populates="co_borrowers")


class CoBorrowerIndividual(Base):
    __tablename__ = "co_borrower_individuals"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String)
    last_name = Column(String, nullable= False)
    date_of_birth = Column(Date, nullable=False)
    mobile_number = Column(String)
    email = Column(String)
    co_borrower_id = Column(Integer, ForeignKey("co_borrowers.id"), unique=True, nullable=False)
    co_borrower = relationship("CoBorrowers", back_populates="individual")
    employer = relationship("CoBorrowerEmployer", uselist=False,
                            back_populates="co_borrower")
    address = relationship("CoBorrowerAddress", uselist=False,
                           back_populates="co_borrower")

class CoBorrowerAddress(Base):
    __tablename__ = "co_borrower_addresses"
    id = Column(Integer, primary_key=True)
    street_name = Column(String)
    village = Column(String)
    district = Column(String)
    nearest_landmark = Column(String)
    country = Column(String)
    co_borrower_id = Column(Integer, ForeignKey('co_borrower_individuals.id'), unique=True, nullable=False)
    co_borrower = relationship("CoBorrowerIndividual", back_populates="address")

class CoBorrowerEmployer(Base):
    __tablename__ = "co_borrower_employers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String)
    number = Column(String)
    co_borrower_id = Column(Integer, ForeignKey("co_borrower_individuals.id"), unique=True, nullable=False)
    co_borrower = relationship("CoBorrowerIndividual", back_populates="employer")

class CoBorrowerBusiness(Base):
    __tablename__ = "co_borrower_business"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    business_type = Column(Integer, default=BusinessType.CORPORATION)
    business_number = Column(String)
    business_email = Column(String)
    co_borrower_id = Column(Integer, ForeignKey("co_borrowers.id"), unique=True, nullable=False)
    co_borrower = relationship("CoBorrowers", back_populates="business")


customer_coborrower = Table(
    "customer_coborrower",
    Base.metadata,
    Column("customer_id", Integer, ForeignKey("customers.id")),
    Column("coborrower_id", Integer, ForeignKey("co_borrowers.id"))
)
