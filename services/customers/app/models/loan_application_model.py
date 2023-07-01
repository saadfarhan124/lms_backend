from app.database.database import Base
from sqlalchemy import Column, String, DateTime, Date, Integer, Date, DECIMAL, Table, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.constants import TermModes, LoanStatus, LoanType, ModeOfPayments


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

loan_application_fees = Table('loan_application_fees', Base.metadata,
                              Column("loan_application_id", Integer,
                                     ForeignKey('loan_applications.id')),
                              Column('fees_id', Integer, ForeignKey('fees.id')))


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
        "LoanApplication", secondary=loan_application_guarantors, back_populates="guarantors")


class LoanApplication(Base):
    __tablename__ = "loan_applications"
    id = Column(Integer, primary_key=True)
    date_applied = Column(DateTime(timezone=True), nullable=False)
    purpose = Column(String, nullable=False)
    principal_amount = Column(DECIMAL(scale=2), nullable=False)
    interest_rate = Column(DECIMAL(scale=2), nullable=False, default=20)
    interest_rate_is_flat = Column(Boolean, default=False)
    o_and_s_rate = Column(DECIMAL(scale=2), nullable=False, default=10)
    o_and_s_rate_is_flat = Column(Boolean, default=False)
    length = Column(Integer, nullable=False)
    term = Column(Integer, default=TermModes
                  .WEEKS.value)
    status = Column(Integer, nullable=False,
                    default=LoanStatus.UNAPPROVED.value)
    loan_type = Column(Integer, nullable=False,
                       default=LoanType.PERSONAL.value)
    mode_of_payment = Column(Integer, nullable=False,
                       default=ModeOfPayments.CASH.value)
    loan_repayment_amount = Column(DECIMAL(scale=2), nullable=False)
    time_created = Column(DateTime(timezone=True),
                          server_default=func.now(), nullable=False)
    time_updated = Column(DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customers = relationship("Customer", back_populates="loan_applications")
    cheques = relationship("LoanApplicationCheques",
                           back_populates="loan_application")

    guarantors = relationship(
        "Guarantor", secondary=loan_application_guarantors, back_populates="loan_applications")
    co_borrowers = relationship(
        "Customer", secondary=loan_application_co_borrowers, back_populates="loan_applications")
    fees = relationship(
        "Fees", secondary=loan_application_fees, back_populates="loan_applications")


class LoanApplicationPaymentSchedule(Base):
    __tablename__ = "loan_application_payment_schedule"
    id = Column(Integer, primary_key=True)
    payment_date = Column(Date, nullable=False)
    bagging_balance = Column(DECIMAL(scale=2), nullable=False)
    balance = Column(DECIMAL(scale=2), nullable=False)

    time_created = Column(DateTime(timezone=True),
                          server_default=func.now(), nullable=False)
    time_updated = Column(DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class LoanApplicationCheques(Base):
    __tablename__ = "loan_application_cheques"
    id = Column(Integer, primary_key=True)
    bank = Column(String, nullable=False)
    branch = Column(String, nullable=False)
    cheque_no = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(DECIMAL(scale=2), nullable=False)
    loan_application_id = Column(Integer, ForeignKey('loan_applications.id'))
    loan_application = relationship(
        "LoanApplication", back_populates="cheques")

    time_created = Column(DateTime(timezone=True),
                          server_default=func.now(), nullable=False)
    time_updated = Column(DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class Fees(Base):
    __tablename__ = "fees"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    amount = Column(DECIMAL(scale=2), nullable=False)
    loan_applications = relationship(
        "LoanApplication", secondary=loan_application_fees, back_populates="fees")
    time_created = Column(DateTime(timezone=True),
                          server_default=func.now(), nullable=False)
    time_updated = Column(DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class PreDefinedFees(Base):
    __tablename__ = "predefined_fees"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    time_created = Column(DateTime(timezone=True),
                          server_default=func.now(), nullable=False)
    time_updated = Column(DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)