from app.database.database import Base
from sqlalchemy import Column, String, ForeignKey, Integer, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


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
