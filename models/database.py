from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    progress = relationship("StudyProgress", back_populates="user")
    questions = relationship("Question", back_populates="user")

class StudyModule(Base):
    __tablename__ = "study_modules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    category = Column(String(50))  # cypress_migration, best_practices, oop, solid, frameworks
    content = Column(Text)
    difficulty_level = Column(String(20))  # beginner, intermediate, advanced
    estimated_time = Column(Integer)  # in minutes
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    progress = relationship("StudyProgress", back_populates="module")

class StudyProgress(Base):
    __tablename__ = "study_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    module_id = Column(Integer, ForeignKey("study_modules.id"))
    completed = Column(Boolean, default=False)
    progress_percentage = Column(Integer, default=0)
    time_spent = Column(Integer, default=0)  # in minutes
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="progress")
    module = relationship("StudyModule", back_populates="progress")

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text)
    category = Column(String(50))
    difficulty = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    answered_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="questions")

class CodeExample(Base):
    __tablename__ = "code_examples"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50))
    language = Column(String(20))  # javascript, typescript, python
    framework = Column(String(20))  # cypress, playwright
    code_before = Column(Text)  # Original Cypress code
    code_after = Column(Text)   # Converted Playwright code
    explanation = Column(Text)
    difficulty_level = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./study_portal.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
