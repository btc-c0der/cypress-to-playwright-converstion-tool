from sqlalchemy.orm import Session
from models import User, StudyModule, StudyProgress, Question, CodeExample, get_db
from typing import List, Optional, Dict, Any
from datetime import datetime

class StudyService:
    """Service for managing study progress and content"""
    
    def __init__(self):
        pass
    
    def create_user(self, username: str, email: str) -> User:
        """Create a new user"""
        db = next(get_db())
        try:
            user = User(username=username, email=email)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        finally:
            db.close()
    
    def get_user(self, username: str) -> Optional[User]:
        """Get user by username"""
        db = next(get_db())
        try:
            return db.query(User).filter(User.username == username).first()
        finally:
            db.close()
    
    def get_study_modules(self, category: Optional[str] = None) -> List[StudyModule]:
        """Get all study modules, optionally filtered by category"""
        db = next(get_db())
        try:
            query = db.query(StudyModule)
            if category:
                query = query.filter(StudyModule.category == category)
            return query.all()
        finally:
            db.close()
    
    def get_user_progress(self, user_id: int) -> List[StudyProgress]:
        """Get user's study progress"""
        db = next(get_db())
        try:
            return db.query(StudyProgress).filter(StudyProgress.user_id == user_id).all()
        finally:
            db.close()
    
    def update_progress(self, user_id: int, module_id: int, progress_percentage: int, time_spent: int = 0) -> StudyProgress:
        """Update user's progress on a module"""
        db = next(get_db())
        try:
            progress = db.query(StudyProgress).filter(
                StudyProgress.user_id == user_id,
                StudyProgress.module_id == module_id
            ).first()
            
            if not progress:
                progress = StudyProgress(user_id=user_id, module_id=module_id)
                db.add(progress)
            
            progress.progress_percentage = progress_percentage
            progress.time_spent += time_spent
            
            if progress_percentage >= 100:
                progress.completed = True
                progress.completed_at = datetime.utcnow()
            
            db.commit()
            db.refresh(progress)
            return progress
        finally:
            db.close()
    
    def save_question(self, user_id: int, question: str, answer: str, category: str) -> Question:
        """Save a user question and AI answer"""
        db = next(get_db())
        try:
            question_obj = Question(
                user_id=user_id,
                question_text=question,
                answer_text=answer,
                category=category,
                answered_at=datetime.utcnow()
            )
            db.add(question_obj)
            db.commit()
            db.refresh(question_obj)
            return question_obj
        finally:
            db.close()
    
    def get_code_examples(self, category: Optional[str] = None, framework: Optional[str] = None) -> List[CodeExample]:
        """Get code examples filtered by category and/or framework"""
        db = next(get_db())
        try:
            query = db.query(CodeExample)
            if category:
                query = query.filter(CodeExample.category == category)
            if framework:
                query = query.filter(CodeExample.framework == framework)
            return query.all()
        finally:
            db.close()

# Singleton instance
study_service = StudyService()
