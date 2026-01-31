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

    fact_workouts = relationship("FactWorkout", back_populates="user", cascade="all, delete-orphan")
    # добавить в факт ворк отношение и добить тут

class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_template = Column(Boolean, nullable=False, default=False)

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

    workout = relationship("Workout", back_populates="exercises")
    sets = relationship(
        "Set",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

class Set(Base):
    __tablename__ = "sets" 

    id = Column(Integer, primary_key=True, autoincrement=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    reps = Column(Integer, nullable=False)
    
    exercise = relationship("Exercise", back_populates="sets")

class FactWorkout(Base):
    __tablename__ = "fact_workouts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(String, nullable=False)


    user = relationship("User", back_populates="fact_workouts")
    fact_exercises = relationship(
        "FactExercise",
        back_populates="fact_workout",
        cascade="all, delete-orphan"
    )

class FactExercise(Base):
    __tablename__ = "fact_exercises"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    fact_workout_id = Column(Integer, ForeignKey("fact_workouts.id"), nullable=False)

    fact_workout = relationship("FactWorkout", back_populates="fact_exercises")
    fact_sets = relationship("FactSet", back_populates="fact_exercise", cascade="all, delete-orphan")

class FactSet(Base):
    __tablename__ = "fact_sets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reps = Column(Integer)
    fact_exercise_id = Column(Integer, ForeignKey("fact_exercises.id"), nullable=False)

    fact_exercise = relationship("FactExercise", back_populates="fact_sets")

