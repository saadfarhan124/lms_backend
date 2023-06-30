from app.database.database import Base
from sqlalchemy import Column, String, DateTime, Integer, Date, DECIMAL, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.constants import TermModes


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


class LoanApplication(Base):
    __tablename__ = "loan_applications"
    id = Column(Integer, primary_key=True)
    date_applied = Column(DateTime(timezone=True), nullable=False)
    principal_amount = Column(DECIMAL(scale=2), nullable=False)
    interest = Column(DECIMAL(scale=2), nullable=False)
    length = Column(Integer, nullable=False)
    term = Column(Integer, default=TermModes
                  .DAYS.value)
    term = Column(Integer, nullable=False)
    time_created = Column(DateTime(timezone=True),
                          server_default=func.now(), nullable=False)
    time_updated = Column(DateTime(
        timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


loan_application_guarantors = Table('loan_application_guarantors', Base.metadata,
    Column('loan_applications', Integer, ForeignKey('loan_applications.id')),
    Column('guarantors', Integer, ForeignKey('guarantors.id'))
)
