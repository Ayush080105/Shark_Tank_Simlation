# Shark Tank with PostgreSQL Storage

This Shark Tank application now stores all pitch and Q&A data in PostgreSQL, ensuring that sharks can make verdicts based on the complete conversation history rather than just the latest answer.

## Features

- **Persistent Storage**: All pitch sessions and Q&A rounds are stored in PostgreSQL
- **Complete Conversation History**: Sharks can access the full conversation when making decisions
- **Session Management**: Unique session IDs for each pitch session with refresh/reset capabilities
- **Session Continuation**: Continue with existing sessions or refresh them before pitching
- **Data Integrity**: Proper database relationships and constraints

## Prerequisites

1. **PostgreSQL**: Install and run PostgreSQL on your system
2. **Python Dependencies**: Install required Python packages

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. PostgreSQL Setup

#### Option A: Using the Setup Script (Recommended)

```bash
cd shark_tank
python setup_database.py
```

#### Option B: Manual Setup

1. Create a PostgreSQL database named `shark_tank`
2. The application will automatically create the necessary tables on first run

### 3. Environment Variables (Optional)

You can customize database settings by setting these environment variables:

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=shark_tank
export DB_USERNAME=postgres
export DB_PASSWORD=your_password
```

### 4. Run the Application

```bash
cd shark_tank/src
python -m shark_tank.main
```

## Session Management

### Before Pitching

When you start the application, you'll see these options:

1. **Start new session** (default) - Create a fresh session
2. **Continue with existing session ID** - Resume a previous session
3. **Refresh existing session** - Keep pitch, reset Q&A to round 1

### Session Continuation

**To continue with an existing session:**
1. Run the application
2. Choose option 2
3. Enter the session ID you want to continue
4. Your pitch data will be preserved, and Q&A will continue from where you left off

**To refresh a session:**
1. Run the application
2. Choose option 3
3. Enter the session ID you want to refresh
4. Your pitch data will be preserved, but Q&A will reset to round 1

### During Q&A Rounds

While answering shark questions, you can use these commands:

- **`refresh`** - Refresh current session (keep pitch, reset Q&A to round 1)
- **`reset`** - Reset completely to session 1 (clear all sessions)
- **`sessions`** - Show all active sessions
- **`stats`** - Show session statistics
- **`help`** - Show available commands
- **`exit`** - Exit Q&A and go to verdicts

### Session Utilities

**View active sessions:**
```bash
cd shark_tank
python view_sessions.py
```

**Advanced session management:**
```bash
cd shark_tank
python manage_sessions.py
```

**Demo session features:**
```bash
cd shark_tank
python demo_sessions.py
```

## Database Schema

### Tables

#### `pitch_sessions`
- Stores basic pitch information
- Links to Q&A entries
- Includes session metadata

#### `qa_entries`
- Stores all Q&A interactions
- Links to pitch sessions
- Tracks round numbers and timestamps

### Relationships
- One pitch session can have multiple Q&A entries
- Q&A entries are automatically deleted when pitch session is deleted (CASCADE)

## How It Works

1. **Session Creation**: Each pitch gets a unique session ID and sequential number
2. **Session Continuation**: Users can resume existing sessions or refresh them
3. **Data Storage**: Pitch and Q&A data is stored in PostgreSQL in real-time
4. **Session Management**: Users can refresh sessions or reset completely
5. **Verdict Generation**: Sharks receive the complete conversation history for decision-making
6. **Data Persistence**: All data remains available for analysis and review

## Benefits

- **No Data Loss**: Q&A responses are never overwritten
- **Better Decisions**: Sharks can consider the full conversation context
- **Session Control**: Continue, refresh, or start completely fresh
- **Audit Trail**: Complete history of all interactions
- **Scalability**: Database storage allows for multiple concurrent sessions

## Use Cases

### Session Continuation
Perfect when you want to:
- Resume a pitch that was interrupted
- Continue Q&A from where you left off
- Keep your progress across multiple sessions

### Refreshing a Session
Perfect when you want to:
- Try different answers to the same questions
- Practice your responses
- Keep your pitch but improve your Q&A performance

### Resetting to Session 1
Useful when you want to:
- Start completely fresh
- Try a different pitch approach
- Clear all previous attempts

## Workflow Examples

### Example 1: Continue Existing Session
```
1. Run: python -m shark_tank.main
2. Choose: Continue with existing session ID
3. Enter: your-session-id-here
4. Pitch: Your pitch (can be updated)
5. Q&A: Continues from where you left off
```

### Example 2: Refresh Session
```
1. Run: python -m shark_tank.main
2. Choose: Refresh existing session
3. Enter: your-session-id-here
4. Pitch: Your pitch (preserved)
5. Q&A: Fresh start, round 1
```

### Example 3: View Sessions
```
1. Run: python view_sessions.py
2. See all active sessions and IDs
3. Copy the session ID you want to use
4. Use it in the main application
```

## Troubleshooting

### Common Issues

1. **Connection Error**: Ensure PostgreSQL is running and accessible
2. **Permission Error**: Check that your database user has CREATE and INSERT permissions
3. **Table Creation Error**: Run the setup script to create tables manually
4. **Session Not Found**: Use `python view_sessions.py` to see available sessions

### Database Connection Test

```bash
python -c "
from shark_tank.database import DatabaseManager
db = DatabaseManager()
print('Database connection successful!')
db.close()
"
```

### Session Management Test

```bash
cd shark_tank
python manage_sessions.py
```

## Development

The application gracefully handles database failures:
- If database storage fails, it continues with in-memory session management
- Warnings are displayed for database errors
- The application remains functional even without database connectivity

## License

This project is part of the Shark Tank simulation application.
