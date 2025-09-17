# db/public_models.py
from sqlalchemy import Column, Integer, String
from db.base import Public_Base

class User(Public_Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    institute_code = Column(String, nullable=False)  # for tenant schema switching
