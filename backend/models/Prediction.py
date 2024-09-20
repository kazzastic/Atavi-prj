from sqlalchemy import Column, Integer, JSON
from database import Base, engine

class Predict(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON, nullable=True)  # This will hold your JSONB data

Base.metadata.create_all(bind=engine)
