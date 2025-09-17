from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from db.base import Base


class Rooms(Base):
    __tablename__ = "rooms"
    __table_args__ = {'schema': 'dwarka'}

    room_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    type = Column(String(20), nullable=False)  # classroom or lab
    capacity = Column(Integer, nullable=False)
    availability = Column(JSON, default={})  # JSONB-like

    timetable_entries = relationship("Timetable", back_populates="room")