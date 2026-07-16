from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Boolean, Float, Date, func
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
    birth_date = Column(Date, nullable=True)
    is_registered = Column(Boolean, nullable=False, default=False, server_default="false")

    programs = relationship(
        "Program",
        back_populates="owner",
        cascade="all, delete-orphan",
        order_by=lambda: (Program.position, Program.id)
    )

    fact_workouts = relationship("FactWorkout", back_populates="user", cascade="all, delete-orphan")
    params = relationship("Params", back_populates="user", cascade="all, delete-orphan")

class Params(Base):
    __tablename__ = "params"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    body_fat_percentage = Column(Float, nullable=True)
    muscle_mass_percentage = Column(Float, nullable=True)
    water_percentage = Column(Float, nullable=True)
    bone_mass_percentage = Column(Float, nullable=True)
    date = Column(Date, default=func.current_date())

    user = relationship("User", back_populates="params")

class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_template = Column(Boolean, nullable=False, default=False)
    position = Column(Integer, nullable=False, default=0, server_default="0")

    owner = relationship("User", back_populates="programs")
    workouts = relationship(
        "Workout",
        back_populates="program",
        cascade="all, delete-orphan",
        order_by=lambda: (Workout.position, Workout.id)
    )

class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)
    name = Column(String, nullable=False)
    position = Column(Integer, nullable=False, default=0, server_default="0")

    program = relationship("Program", back_populates="workouts")
    exercises = relationship(
        "Exercise",
        back_populates="workout",
        cascade="all, delete-orphan",
        order_by=lambda: (Exercise.position, Exercise.id)
    )
    fact_workouts = relationship("FactWorkout", back_populates="workout", cascade="all, delete-orphan")

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, autoincrement=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    name = Column(String, nullable=False)
    position = Column(Integer, nullable=False, default=0, server_default="0")

    workout = relationship("Workout", back_populates="exercises")
    sets = relationship(
        "Set",
        back_populates="exercise",
        cascade="all, delete-orphan",
        order_by=lambda: (Set.position, Set.id)
    )

class Set(Base):
    __tablename__ = "sets" 

    id = Column(Integer, primary_key=True, autoincrement=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    weight = Column(Float, nullable=True)
    reps = Column(Integer, nullable=True)
    position = Column(Integer, nullable=False, default=0, server_default="0")
    
    exercise = relationship("Exercise", back_populates="sets")

class FactWorkout(Base):
    __tablename__ = "fact_workouts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(Date, default=func.current_date())
    workout_id = Column(Integer, ForeignKey("workouts.id"))
    name = Column(String, nullable=False)


    user = relationship("User", back_populates="fact_workouts")
    fact_exercises = relationship(
        "FactExercise",
        back_populates="fact_workout",
        cascade="all, delete-orphan"
    )
    workout = relationship("Workout", back_populates="fact_workouts")
    
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
    weight = Column(Float,nullable=False)
    fact_exercise_id = Column(Integer, ForeignKey("fact_exercises.id"), nullable=False)
    nom_reps = Column(Integer, nullable=False)

    fact_exercise = relationship("FactExercise", back_populates="fact_sets")
