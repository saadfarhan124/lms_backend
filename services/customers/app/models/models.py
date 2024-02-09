# from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

# from ..database import Base

# class User(Base):
#     __tablename__ = "customers"
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     items = relationship("Item", back_populates="owner")


# class Item(Base):
#     __tablename__ = "items"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("customers.id"))
#     owner = relationship("User", back_populates="items")