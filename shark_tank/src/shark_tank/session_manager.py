#!/usr/bin/env python
"""
Session manager for Shark Tank application
Handles unique session ID generation and session tracking
"""

import uuid
from datetime import datetime
from typing import Dict, Any

class SessionManager:
    """Manages session creation and tracking"""
    
    def __init__(self):
        """Initialize session manager"""
        self.active_sessions = {}
        self.session_counter = 1  # Track session numbers
    
    def create_session(self, pitch_data: Dict[str, Any]) -> str:
        """Create a new session with unique ID"""
        session_id = str(uuid.uuid4())
        
        session_data = {
            'session_id': session_id,
            'session_number': self.session_counter,  # Add session number
            'created_at': datetime.utcnow(),
            'pitch_data': pitch_data,
            'qa_rounds': [],
            'current_round': 1
        }
        
        self.active_sessions[session_id] = session_data
        self.session_counter += 1  # Increment counter
        return session_id
    
    def continue_session(self, session_id: str, pitch_data: Dict[str, Any]) -> str:
        """Continue with an existing session ID, updating pitch data if needed"""
        if session_id in self.active_sessions:
            # Update existing session with new pitch data
            existing_session = self.active_sessions[session_id]
            existing_session['pitch_data'].update(pitch_data)
            existing_session['updated_at'] = datetime.utcnow()
            print(f"✅ Continuing with existing session #{existing_session['session_number']}")
            return session_id
        else:
            # Session not found, create new one
            print(f"⚠️  Session {session_id} not found, creating new session...")
            return self.create_session(pitch_data)
    
    def refresh_session(self, session_id: str) -> str:
        """Refresh/reset an existing session to start over"""
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found")
        
        # Get the original session data
        original_session = self.active_sessions[session_id]
        
        # Create a new session with the same pitch data but fresh Q&A
        new_session_id = str(uuid.uuid4())
        
        session_data = {
            'session_id': new_session_id,
            'session_number': self.session_counter,  # New session number
            'created_at': datetime.utcnow(),
            'pitch_data': original_session['pitch_data'],  # Keep original pitch
            'qa_entries': [],  # Fresh Q&A rounds
            'current_round': 1  # Reset to round 1
        }
        
        # Remove old session and add new one
        del self.active_sessions[session_id]
        self.active_sessions[new_session_id] = session_data
        self.session_counter += 1
        
        return new_session_id
    
    def refresh_session_by_id(self, session_id: str, pitch_data: Dict[str, Any]) -> str:
        """Refresh a session by ID, keeping the pitch data"""
        if session_id in self.active_sessions:
            # Refresh existing session
            new_session_id = self.refresh_session(session_id)
            # Update pitch data if provided
            if pitch_data:
                self.active_sessions[new_session_id]['pitch_data'].update(pitch_data)
            return new_session_id
        else:
            # Session not found, create new one
            print(f"⚠️  Session {session_id} not found, creating new session...")
            return self.create_session(pitch_data)
    
    def reset_to_session_1(self) -> str:
        """Reset completely and start from session 1"""
        # Clear all active sessions
        self.active_sessions.clear()
        
        # Reset session counter
        self.session_counter = 1
        
        # Create a fresh session 1
        return self.create_session({})
    
    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Get session data by ID"""
        return self.active_sessions.get(session_id)
    
    def get_session_by_number(self, session_number: int) -> Dict[str, Any]:
        """Get session data by session number"""
        for session in self.active_sessions.values():
            if session['session_number'] == session_number:
                return session
        return None
    
    def add_qa_round(self, session_id: str, shark_name: str, question: str, answer: str):
        """Add a Q&A round to the session"""
        if session_id in self.active_sessions:
            qa_round = {
                'shark_name': shark_name,
                'question': question,
                'answer': answer,
                'round_number': self.active_sessions[session_id]['current_round'],
                'timestamp': datetime.utcnow()
            }
            
            self.active_sessions[session_id]['qa_rounds'].append(qa_round)
            self.active_sessions[session_id]['current_round'] += 1
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get a summary of the session for the sharks to make decisions"""
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        
        # Build conversation summary
        summary_parts = [
            f"Session #{session['session_number']}",
            f"Pitch: {session['pitch_data'].get('pitch_text', 'N/A')}",
            f"Investment Request: ${session['pitch_data'].get('amount_invested', 0):,} for {session['pitch_data'].get('percentage_equity', 0)}% equity"
        ]
        
        if session['qa_rounds']:
            summary_parts.append("\nQ&A History:")
            for qa in session['qa_rounds']:
                summary_parts.append(f"\n{qa['shark_name']} (Round {qa['round_number']}):")
                summary_parts.append(f"Q: {qa['question']}")
                summary_parts.append(f"A: {qa['answer']}")
        
        return {
            'session_id': session_id,
            'session_number': session['session_number'],
            'pitch_data': session['pitch_data'],
            'qa_rounds': session['qa_rounds'],
            'conversation_summary': "\n".join(summary_parts),
            'total_qa_rounds': len(session['qa_rounds'])
        }
    
    def cleanup_session(self, session_id: str):
        """Clean up session data"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
    
    def list_active_sessions(self) -> list:
        """List all active session IDs with their numbers"""
        return [
            {
                'session_id': session_id,
                'session_number': session['session_number'],
                'created_at': session['created_at'],
                'pitch_text': session['pitch_data'].get('pitch_text', 'N/A')[:50] + '...'
            }
            for session_id, session in self.active_sessions.items()
        ]
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics about all sessions"""
        total_sessions = len(self.active_sessions)
        total_qa_rounds = sum(len(session['qa_rounds']) for session in self.active_sessions.values())
        
        return {
            'total_active_sessions': total_sessions,
            'total_qa_rounds': total_qa_rounds,
            'next_session_number': self.session_counter,
            'sessions': self.list_active_sessions()
        }
