from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Movies(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    year = Column(Integer, nullable=False)
    director = Column(String, nullable=False)
    actors = relationship("Actors", back_populates="movie")

class Actors(Base):
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True, index=True)
    actor_name = Column(String, nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    movie = relationship("Movies", back_populates="actors")

# models/summary.py or wherever you define schemas


