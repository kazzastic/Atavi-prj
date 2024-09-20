from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base, engine

class Predict(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key = True, index = True)


Base.metadata.create_all(bind = engine)