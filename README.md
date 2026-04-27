# Task & Notes Manager API

A FastAPI application for managing tasks and notes with user authentication.

## Features

- User registration and authentication (JWT)
- Task management (CRUD operations)
- Task filtering and pagination
- Tag management
- Notes for tasks
- Task-tag relationships

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token

### Tasks
- `POST /tasks/` - Create a new task
- `GET /tasks/{id}` - Get a specific task
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a task
- `GET /tasks/` - Get paginated list of tasks with optional filtering
- `GET /tasks/by-tag` - Get tasks filtered by tag
- `POST /tasks/{task_id}/tags/{tag_id}` - Add tag to task

### Tags
- `POST /tags/` - Create a new tag
- `GET /tags/` - Get all tags

### Notes
- `POST /tasks/{task_id}/notes` - Add note to task
- `GET /tasks/{task_id}/notes` - Get notes for a task

### Health Check
- `GET /health` - Check server responsiveness

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   SECRET_KEY=your-secret-key-here
   ```

## Running the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Running Tests

```bash
pytest
```

## API Response Types

The API responses are **dynamic** - they are generated based on:
- Database queries and user data
- Request parameters (pagination, filtering, search)
- User authentication status
- Current server state

Responses are not static; they change based on the data in the database and the user's actions.

## Error Handling

The API includes comprehensive error handling for:
- Database connection issues (503 Service Unavailable)
- Authentication errors (401 Unauthorized)
- Resource not found (404 Not Found)
- Validation errors (400 Bad Request)
- Internal server errors (500 Internal Server Error)

## Database

The application uses PostgreSQL by default, but tests use SQLite for isolation.

## Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS middleware enabled
- Input validation with Pydantic