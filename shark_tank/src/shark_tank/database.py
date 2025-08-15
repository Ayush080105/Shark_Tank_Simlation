#!/usr/bin/env python
"""
Database module for Shark Tank application
Handles PostgreSQL connection and data models for storing pitch and Q&A data
"""

import os
from datetime import datetime
from pickle import TRUE
from typing import Dict, List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
import json

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv(override=TRUE)
except ImportError:
    pass

Base = declarative_base()

class PitchSession(Base):
    """Model for storing pitch sessions"""
    __tablename__ = 'pitch_sessions'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(100), unique=True, nullable=False)
    pitch_text = Column(Text, nullable=False)
    amount_invested = Column(Integer, nullable=False)
    percentage_equity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to Q&A entries
    qa_entries = relationship("QAEntry", back_populates="pitch_session", cascade="all, delete-orphan")
    
    def to_dict(self) -> Dict:
        """Convert pitch session to dictionary"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'pitch_text': self.pitch_text,
            'amount_invested': self.amount_invested,
            'percentage_equity': self.percentage_equity,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class QAEntry(Base):
    """Model for storing Q&A entries"""
    __tablename__ = 'qa_entries'
    
    id = Column(Integer, primary_key=True)
    pitch_session_id = Column(Integer, ForeignKey('pitch_sessions.id'), nullable=False)
    shark_name = Column(String(100), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    round_number = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to pitch session
    pitch_session = relationship("PitchSession", back_populates="qa_entries")
    
    def to_dict(self) -> Dict:
        """Convert QA entry to dictionary"""
        return {
            'id': self.id,
            'pitch_session_id': self.pitch_session_id,
            'shark_name': self.shark_name,
            'question': self.question,
            'answer': self.answer,
            'round_number': self.round_number,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, connection_string: Optional[str] = None):
        """Initialize database manager with connection string"""
        if connection_string is None:
            # Check for custom connection string first
            custom_connection = os.getenv('DB_CONNECTION_STRING')
            if custom_connection:
                connection_string = custom_connection
            else:
                # Build connection string from individual environment variables
                host = os.getenv('DB_HOST', 'localhost')
                port = os.getenv('DB_PORT', '5432')
                database = os.getenv('DB_NAME', 'shark_tank')
                username = os.getenv('DB_USERNAME', 'postgres')
                password = os.getenv('DB_PASSWORD', 'password')
                
                connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
        
        self.engine = create_engine(connection_string)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Create tables if they don't exist
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Get a new database session"""
        return self.SessionLocal()
    
    def create_pitch_session(self, session_id: str, pitch_text: str, 
                           amount_invested: int, percentage_equity: int) -> PitchSession:
        """Create a new pitch session"""
        session = self.get_session()
        try:
            pitch_session = PitchSession(
                session_id=session_id,
                pitch_text=pitch_text,
                amount_invested=amount_invested,
                percentage_equity=percentage_equity
            )
            session.add(pitch_session)
            session.commit()
            session.refresh(pitch_session)
            return pitch_session
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Failed to create pitch session: {e}")
        finally:
            session.close()
    
    def add_qa_entry(self, pitch_session_id: int, shark_name: str, 
                     question: str, answer: str, round_number: int = 1) -> QAEntry:
        """Add a new Q&A entry"""
        session = self.get_session()
        try:
            qa_entry = QAEntry(
                pitch_session_id=pitch_session_id,
                shark_name=shark_name,
                question=question,
                answer=answer,
                round_number=round_number
            )
            session.add(qa_entry)
            session.commit()
            session.refresh(qa_entry)
            return qa_entry
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Failed to add QA entry: {e}")
        finally:
            session.close()
    
    def get_pitch_session(self, session_id: str) -> Optional[PitchSession]:
        """Get pitch session by session ID"""
        session = self.get_session()
        try:
            return session.query(PitchSession).filter(PitchSession.session_id == session_id).first()
        finally:
            session.close()
    
    def get_qa_history(self, pitch_session_id: int) -> List[QAEntry]:
        """Get all Q&A entries for a pitch session"""
        session = self.get_session()
        try:
            return session.query(QAEntry).filter(QAEntry.pitch_session_id == pitch_session_id).order_by(QAEntry.created_at).all()
        finally:
            session.close()
    
    def get_complete_conversation(self, session_id: str) -> Dict:
        """Get complete conversation data for a session"""
        pitch_session = self.get_pitch_session(session_id)
        if not pitch_session:
            return None
        
        qa_entries = self.get_qa_history(pitch_session.id)
        
        return {
            'pitch_session': pitch_session.to_dict(),
            'qa_history': [qa.to_dict() for qa in qa_entries],
            'conversation_summary': self._generate_conversation_summary(pitch_session, qa_entries)
        }
    
    def _generate_conversation_summary(self, pitch_session: PitchSession, qa_entries: List[QAEntry]) -> str:
        """Generate a summary of the complete conversation"""
        summary_parts = [
            f"Pitch: {pitch_session.pitch_text}",
            f"Investment Request: ${pitch_session.amount_invested:,} for {pitch_session.percentage_equity}% equity"
        ]
        
        if qa_entries:
            summary_parts.append("\nQ&A History:")
            for qa in qa_entries:
                summary_parts.append(f"\n{qa.shark_name} (Round {qa.round_number}):")
                summary_parts.append(f"Q: {qa.question}")
                summary_parts.append(f"A: {qa.answer}")
        
        return "\n".join(summary_parts)
    
    def close(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
