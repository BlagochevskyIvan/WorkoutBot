from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)

    gender = Column(String, nullable=True)
    experience = Column(String, nullable=True)
    place = Column(String, nullable=True)
    birth_date = Column(String, nullable=True)

    programs = relationship(
        "Program",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_template = Column(Boolean, default=False)

    owner = relationship("User", back_populates="programs")
    workouts = relationship(
        "Workout",
        back_populates="program",
        cascade="all, delete-orphan"
    )

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)

    name = Column(String, nullable=False)
    order_index = Column(Integer, nullable=False)

    program = relationship("Program", back_populates="workouts")
    exercises = relationship(
        "Exercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, autoincrement=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)

    name = Column(String, nullable=False)
    sets = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)
    rest_seconds = Column(Integer, nullable=True)

    order_index = Column(Integer, nullable=False)

    workout = relationship("Workout", back_populates="exercises")

