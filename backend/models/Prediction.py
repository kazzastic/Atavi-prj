from sqlalchemy import Column, Integer, Float, Text
from sqlalchemy.orm import relationship
from database import Base, engine

class Predict(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key = True, index = True)
    xmin = Column(Float, nullable = True)
    ymin = Column(Float, nullable = True)
    xmax = Column(Float, nullable = True)
    ymax = Column(Float, nullable = True)
    confidence = Column(Float, nullable = True)
    class_id = Column(Integer, nullable = True)
    class_name = Column(Text, nullable = True)

Base.metadata.create_all(bind = engine)