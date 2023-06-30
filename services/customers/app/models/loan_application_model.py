from app.database.database import Base
from sqlalchemy import Column, String, DateTime, Date, Integer, Date, DECIMAL, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.constants import TermModes, LoanStatus, LoanType


loan_application_guarantors = Table('loan_application_guarantors', Base.metadata,
                                    Column('loan_application_id', Integer,
                                           ForeignKey('loan_applications.id')),
                                    Column('guarantor_id', Integer,
                                           ForeignKey('guarantors.id'))
                                    )

loan_application_customers = Table('loan_application_customers', Base.metadata,
                                   Column("loan_application_id", Integer,
                                          ForeignKey('loan_applications.id')),
                                   Column('customer_id', Integer, ForeignKey('customers.id')))

loan_application_co_borrowers = Table('loan_application_co_borrowers', Base.metadata,
                                      Column("loan_application_id", Integer,
                                             ForeignKey('loan_applications.id')),
                                      Column('customer_id', Integer, ForeignKey('customers.id')))


class Guarantor(Base):
    __tablename__ = "guarantors"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    mobile_number = Column(String, nullable=False)
    address = Column(String, nullable=False)
    employer_name = Column(String, nullable=False)
    employer_number = Column(String, nullable=False)
    employer_email = Column(String, nullable=False)
    employer_address = Column(String, nullable=False)
    time_created = Column(DateTime(timezone=True),
                          server_default=func.now(), nullable=False)
    time_updated = Column(DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    loan_applications = relationship(
        "LoanApplication", secondary=loan_application_guarantors, back_populates="gurantors")


class LoanApplication(Base):
    __tablename__ = "loan_applications"
    id = Column(Integer, primary_key=True)
    date_applied = Column(DateTime(timezone=True), nullable=False)
    purpose = Column(String, nullable=False)
    principal_amount = Column(DECIMAL(scale=2), nullable=False)
    interest_rate = Column(DECIMAL(scale=2), nullable=False)
    interest_rate_is_flat = Column(Boolean, default=False)
    o_and_s_rate = Column(DECIMAL(scale=2), nullable=False, default=10)
    o_and_s_rate_is_flat = Column(Boolean, default=False)
    length = Column(Integer, nullable=False)
    term = Column(Integer, default=TermModes
                  .DAYS.value)
    status = Column(Integer, nullable=False, default= LoanStatus.UNAPPROVED.value)
    loan_type = Column(Integer, nullable=False, default= LoanType.PERSONAL.value)
    term = Column(Integer, nullable=False)
    time_created = Column(DateTime(timezone=True),
                          server_default=func.now(), nullable=False)
    time_updated = Column(DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    guarantors = relationship(
        "Guarantor", secondary=loan_application_guarantors, back_populates="loan_applications")
    customers = relationship(
        "Customer", secondary=loan_application_customers, back_populates="loan_applications")
    co_borrowers = relationship(
        "Customer", secondary=loan_application_co_borrowers, back_populates="loan_applications")

class LoanApplicationPaymentSchedule(Base):
    __tablename__ = "loan_application_payment_schedule"
    id = Column(Integer, primary_key=True)
    payment_date = Column(Date, nullable=False)
    

    time_created = Column(DateTime(timezone=True),
                             server_default=func.now(), nullable=False)
    time_updated = Column(DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
