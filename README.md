# AI Study Assistant with Digital Notebook

Full-stack study assistant platform with Flask backend, JavaScript frontend, and MongoDB database.

## Features

- **User Authentication**: Secure signup, login with JWT tokens
- **Digital Notebook**: Create, edit, delete notes organized by subject/topic
- **Canvas Drawing**: Draw diagrams and save as note attachments
- **Study Planner**: Task management with deadlines and status tracking
- **AI Assistant**: 
  - Ask academic questions (powered by GPT-3.5-turbo)
  - Summarize notes automatically
  - Generate practice quizzes
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Beautiful gradient design with smooth interactions

## Technology Stack

- **Backend**: Python, Flask, PyMongo, JWT, OpenAI API
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: MongoDB
- **Styling**: Modern CSS with gradients and transitions

## Simple Architecture

This project has two main parts:

- **Backend**: `backend/` contains the Flask server, REST API endpoints, and MongoDB access.
- **Frontend**: `frontend/` contains static web pages, UI logic, and calls the backend APIs.

The app runs as a local Flask website and the browser pages use JWT tokens to access data.

## Prerequisites

- Python 3.7+
- MongoDB (local or Atlas)
- OpenAI API key
- Git

## Installation & Setup

### 1. Clone and Setup

Replace `<repo-url>` with the repository HTTPS URL (example shown).

```bash
# Clone the repository
git clone https://github.com/Vishal-203/NexMind-study-assistant-.git
cd NexMind-study-assistant-

# Create a Python virtual environment (cross-platform)
python -m venv venv
```

### 2. Activate Virtual Environment

On macOS / Linux (bash, zsh):

```bash
source venv/bin/activate
python -m pip install -r backend/requirements.txt
```

On Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
python -m pip install -r backend/requirements.txt
```

On Windows cmd.exe:

```cmd
venv\Scripts\activate.bat
python -m pip install -r backend/requirements.txt
```

> If your system Python points to python3, prefix commands with `python3`.

If the frontend has Node dependencies (check `frontend/`), install them from the repo root:

```bash
# from repo root
# if there is a package.json inside frontend/
cd frontend && npm install && cd ..
```

### 3. Configuration

Create `.env` in the **project root** by copying the included example:

```bash
cp .env.example .env
```

On Windows PowerShell, use `Copy-Item .env.example .env` if `cp` is unavailable.

Open `.env` and set the required values. Do not commit `.env` to Git.

- `APP_ENV=development` enables the local development configuration and Flask debug mode.
- `APP_ENV=production` requires `SECRET_KEY`, `JWT_SECRET_KEY`, and `MONGO_URI` to be set explicitly. Production debug mode is disabled.
- The hosting provider should receive these values as platform environment variables rather than a committed `.env` file.

### 4. Database Setup

Ensure MongoDB is running locally or update `MONGO_URI` for MongoDB Atlas:

```bash
# For local MongoDB
mongod
```

### 5. Start the Server

With the virtual environment active, you can start the backend:

```bash
# From repository root
python backend/app.py
# or (if you prefer Flask cli)
# export FLASK_APP=backend.app (macOS/Linux)
# set FLASK_APP=backend.app (Windows)
# flask run
```

The server will run on `http://localhost:5000` by default.

## Project Structure

```
NexMind-study-assistant-/
├── backend/
│   ├── app.py                 # Main Flask app
│   ├── requirements.txt        # Python dependencies
│   ├── controllers/           # Business logic
│   │   ├── auth_controller.py
│   │   ├── note_controller.py
│   │   ├── task_controller.py
│   │   ├── ai_controller.py
│   │   ├── file_controller.py
│   │   ├── file_analyzer.py
│   │   ├── share_controller.py
│   │   └── user_controller.py
│   ├── routes/               # API endpoints
│   │   ├── auth_routes.py
│   │   ├── note_routes.py
│   │   ├── task_routes.py
│   │   ├── ai_routes.py
│   │   ├── file_routes.py
│   │   └── share_routes.py
│   ├── models/               # Database models (reserved)
│   └── utils/
│       └── helpers.py        # Utility functions
├── frontend/
│   ├── index.html            # Login page
│   ├── register.html         # Registration page
│   ├── dashboard.html        # User dashboard
│   ├── notebook.html         # Note editor with canvas
│   ├── planner.html          # Task planner
│   ├── ai_assistant.html     # AI features
│   ├── app.js               # API utilities & helpers
│   └── styles.css           # Global styling
├── .env                      # Environment variables (DO NOT COMMIT)
├── .env.example              # Example environment variables (this file)
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/profile` - Get user profile (requires token)

### Notes
- `GET /api/notes?page=<n>&limit=<m>` - Fetch paginated notes (with optional subject/topic filters)
- `POST /api/notes` - Create new note
- `GET /api/notes/<id>` - Get specific note
- `PUT /api/notes/<id>` - Update note
- `DELETE /api/notes/<id>` - Delete note
- `POST /api/notes/<id>/share` - Share note with another user
- `DELETE /api/notes/<id>/share/<share_user_id>` - Revoke a share
- `GET /api/notes/shared` - List notes shared with current user
- `GET /api/notes/<id>/shares` - List users with access to a note

### Files
- `GET /api/files` - List uploaded files
- `POST /api/files` - Upload a new file
- `DELETE /api/files/<file_id>` - Delete a file
- `GET /api/files/<file_id>/download` - Download a file

### Tasks
- `GET /api/tasks?page=<n>&limit=<m>` - Fetch paginated tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/<id>` - Update task (title, deadline, status)
- `DELETE /api/tasks/<id>` - Delete task

### AI Features
- `POST /api/ai/ask` - Ask a question
- `POST /api/ai/summarize` - Summarize text or a selected uploaded file
- `POST /api/ai/quiz` - Generate quiz

## Usage Guide

### 1. Register & Login
- Visit `http://localhost:5000` or open `frontend/index.html`
- Create account or login with existing credentials

### 2. Dashboard
- View welcome message and recent notes
- Quick navigation to all features

### 3. Notebook
- Create notes with subject and topic
- Draw diagrams using the canvas
- Filter and search notes
- Edit or delete existing notes

### 4. Planner
- Add tasks with deadlines
- Mark tasks as complete
- Delete completed tasks
- Track study schedule

### 5. AI Assistant
- Ask academic questions
- Get instant answers powered by GPT
- Summarize long note content
- Generate practice quizzes on any topic

## Security Features

- Passwords hashed with bcrypt
- JWT token-based authentication
- CORS enabled for local development
- User data isolation (users see only their own content)
- Environment variable protection for sensitive keys

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `APP_ENV` | Runtime environment: `development` or `production` | `development` |
| `SECRET_KEY` | Flask secret key | `your-secret-key` |
| `JWT_SECRET_KEY` | JWT signing key | `your-jwt-key` |
| `MONGO_URI` | MongoDB connection string | `mongodb://localhost:27017/ai_study_assistant` |
| `OPENAI_API_KEY` | OpenAI-compatible or Groq API key | `gsk_...` |
| `OPENAI_BASE_URL` | OpenAI-compatible API base URL | `https://api.groq.com/openai/v1` |
| `OPENAI_MODEL` | AI model available from the configured provider | `allam-2-7b` |

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
```powershell
python -m pip install -r backend/requirements.txt
```

### "MongoDB connection refused"
- Ensure MongoDB is running: `mongod`
- Check MONGO_URI in .env file
- Verify MongoDB is properly installed

### "Unauthorized - Redirecting to login"
- Token expired or invalid
- Clear localStorage and login again
- Check JWT_SECRET_KEY matches in .env

### "AI service error"
- Verify OPENAI_API_KEY is set and valid
- Check API quota and usage limits
- Ensure API key has access to gpt-3.5-turbo model

## Development

### Code Style
- Backend: PEP 8 Python style
- Frontend: Vanilla JavaScript with ES6+
- CSS: BEM-like naming conventions

### Testing
The project uses Flask debug mode for development. Test endpoints via:
- Browser (for GET requests)
- Postman/Insomnia (for API testing)
- Browser DevTools (for frontend debugging)

### Performance Notes
- Canvas drawings are stored as base64 dataURLs (consider compression for production)
- Large drawings may impact response times
- Implement pagination for notes/tasks in production

## Deployment

### Production Checklist
- [ ] Set `debug=False` in app.py
- [ ] Use production MongoDB instance (MongoDB Atlas)
- [ ] Set strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Use HTTPS for all endpoints
- [ ] Implement rate limiting
- [ ] Add logging and monitoring
- [ ] Use production WSGI server (gunicorn)
- [ ] Compress canvas drawings before storage

### Deploy to Render

The application is currently deployed at **https://nextmind-study-assistant.onrender.com**.

To deploy or update it yourself:

1. Create a MongoDB Atlas database and copy its connection string.
2. Add the repository to Render as a Blueprint using [render.yaml](render.yaml).
3. Configure these environment variables in Render:
   - `MONGO_URI`
   - `OPENAI_API_KEY`
   - `OPENAI_BASE_URL=https://api.groq.com/openai/v1`
   - `OPENAI_MODEL=allam-2-7b`
4. Render generates `SECRET_KEY` and `JWT_SECRET_KEY` automatically from the Blueprint.
5. Verify deployment status at `https://nextmind-study-assistant.onrender.com/api/health`.

For a local production-style server after setting production environment variables:

```bash
python -m pip install -r backend/requirements.txt
python backend/start.py
```

> Important: uploaded files stored on Render's filesystem are ephemeral on the free plan and may be lost when the service restarts or redeploys. Configure persistent disk storage or migrate uploads to object storage before relying on file uploads in production.

## Optional Enhancements

- [ ] Add password reset with email verification
- [ ] Implement OAuth (Google, GitHub)
- [ ] Add real file upload instead of dataURL
- [ ] PDF export for notes
- [ ] Collaborative notes sharing
- [ ] Advanced search with tags
- [ ] Mobile app (React Native)
- [ ] Set reminders for tasks
- [ ] Export study progress

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m 'Add feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Submit pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please open an issue on GitHub or contact the development team.

---

**Last Updated**: March 31, 2026  
**Version**: 1.0.0  
**Status**: Ready for testing and deployment

