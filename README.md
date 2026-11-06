# NextMind Study Assistant

NextMind is a full-stack AI-powered study management application built with Flask, MongoDB, vanilla JavaScript, HTML, and CSS. It combines note-taking, file analysis, task planning, syllabus tracking, AI assistance, account management, and note sharing in one responsive interface.

**Live application:** https://nextmind-study-assistant.onrender.com

## Key Features

### User and Account
- Register and sign in with email and password.
- JWT-based API authentication.
- Optional Google and GitHub OAuth login.
- View and update profile information.
- Change the account password.
- View study statistics.

### Dashboard
- Search notes and tasks from the global search bar.
- View account and task progress.
- Open the AI chat assistant, notes, and study tasks.
- Upload or review learning materials.

### Digital Notebook
- Create, edit, search, and delete notes.
- Organize notes by subject and topic.
- Write rich note content.
- Draw and save diagrams on a canvas.
- Share notes with other registered users.
- View and manage shared note permissions.

### Intelligent Study Planner
- Add tasks with a title, deadline, and priority.
- Search and filter tasks by status.
- Mark tasks complete or pending.
- Delete tasks.
- Add, view, and remove examination countdowns.
- Manage subjects and syllabus units.
- Mark units complete and calculate subject progress.
- Use the syllabus completion tracker to view overall progress.
- Planner data for subjects, units, and exam countdowns is stored in browser local storage.

### AI Study Assistant
- Ask academic questions.
- Generate short answers or explanations.
- Summarize selected text or uploaded study files.
- Generate practice quizzes.
- Analyze supported uploaded files.

### Files and Documents
- Upload documents and study materials.
- List uploaded files.
- Download or delete files.
- Extract text from PDF, DOCX, images, and supported text formats where configured dependencies are available.

## Technology Stack

| Area | Technology |
|---|---|
| Backend | Python, Flask |
| Database | MongoDB, PyMongo |
| Authentication | Flask-JWT-Extended, bcrypt, OAuth endpoints |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| AI | OpenAI-compatible API, including Groq-compatible configuration |
| File Processing | pypdf, python-docx, Pillow, pytesseract |
| Testing | pytest, pytest-flask, mongomock |
| Production Server | Gunicorn |
| Deployment | Render |

## Project Structure

```text
NextMind-study-assistant-/
├── backend/
│   ├── app.py                 # Flask application and API registration
│   ├── start.py               # Production Gunicorn launcher
│   ├── controllers/           # Authentication, notes, tasks, AI, files, users
│   ├── routes/                # Flask API blueprints
│   ├── models/                # Reserved model package
│   ├── utils/                 # Shared backend helpers
│   └── uploads/               # Uploaded files
├── frontend/
│   ├── index.html             # Login page
│   ├── register.html          # Registration page
│   ├── dashboard.html         # Main dashboard
│   ├── notebook.html          # Notes and AI interface
│   ├── planner.html           # Study planner
│   ├── profile.html           # Profile and account settings
│   ├── app.js                 # Shared API and authentication helpers
│   ├── neural-bg.js           # Neural background animation
│   └── styles.css             # Application styles
├── tests/
├── .env.example
├── render.yaml
├── Procfile
└── README.md
```

## Requirements

- Python 3.10 or newer recommended
- MongoDB local instance or MongoDB Atlas
- An OpenAI-compatible API key for AI features
- Git
- Tesseract OCR is optional for image text extraction

## Local Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Vishal-203/NextMind-study-assistant-.git
cd NextMind-study-assistant-
```

### 2. Create and Activate a Virtual Environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
```

### 4. Configure Environment Variables

Copy the example configuration:

```bash
# macOS/Linux
cp .env.example .env
```

```powershell
# Windows PowerShell
Copy-Item .env.example .env
```

Then edit `.env`.

| Variable | Required | Description |
|---|---:|---|
| `APP_ENV` | Yes | Set to `development` locally or `production` in deployment |
| `SECRET_KEY` | Production | Flask signing secret |
| `JWT_SECRET_KEY` | Production | JWT signing secret |
| `MONGO_URI` | Production | MongoDB connection string |
| `OPENAI_API_KEY` | For AI | API key for an OpenAI-compatible provider |
| `OPENAI_BASE_URL` | Optional | Custom API base URL |
| `OPENAI_MODEL` | Optional | Model name; defaults to `allam-2-7b` in this project configuration |
| `GOOGLE_CLIENT_ID` | For Google OAuth | Google OAuth application client ID |
| `GOOGLE_CLIENT_SECRET` | For Google OAuth | Google OAuth application secret |
| `GOOGLE_REDIRECT_URI` | Optional | Google callback URL |
| `GITHUB_CLIENT_ID` | For GitHub OAuth | GitHub OAuth application client ID |
| `GITHUB_CLIENT_SECRET` | For GitHub OAuth | GitHub OAuth application secret |
| `GITHUB_REDIRECT_URI` | Optional | GitHub callback URL |
| `HOST` | Optional | Flask development host |
| `PORT` | Optional | Flask development port |

Example local configuration:

```dotenv
APP_ENV=development
SECRET_KEY=replace_with_a_random_secret
JWT_SECRET_KEY=replace_with_a_different_random_secret
MONGO_URI=mongodb://localhost:27017/ai_study_assistant

OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.groq.com/openai/v1
OPENAI_MODEL=allam-2-7b

HOST=127.0.0.1
PORT=5000
```

### 5. Start MongoDB

Start a local MongoDB service or provide an Atlas connection string through `MONGO_URI`.

### 6. Run the Application

```bash
python backend/app.py
```

Open http://127.0.0.1:5000 in a browser.

The Flask application serves both the API and the frontend static pages.

## API Overview

Authentication is required for protected API endpoints. Send the JWT as:

```text
Authorization: Bearer <token>
```

### Authentication and Users

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Register |
| POST | `/api/auth/login` | Log in |
| GET | `/api/auth/profile` | Current authentication profile |
| GET | `/api/auth/oauth/<provider>/start` | Start OAuth |
| GET | `/api/auth/oauth/google/callback` | Google OAuth callback |
| GET | `/api/auth/oauth/github/callback` | GitHub OAuth callback |
| GET | `/api/user/profile` | Get user profile |
| PUT | `/api/user/profile` | Update profile |
| POST | `/api/user/change-password` | Change password |
| GET | `/api/user/stats` | Study and account statistics |

### Notes and Sharing

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/notes/` | List notes |
| POST | `/api/notes/` | Create note |
| GET | `/api/notes/<note_id>` | Get note |
| PUT | `/api/notes/<note_id>` | Update note |
| DELETE | `/api/notes/<note_id>` | Delete note |
| POST | `/api/notes/<note_id>/share` | Share a note |
| DELETE | `/api/notes/<note_id>/share/<user_id>` | Remove sharing access |
| GET | `/api/notes/shared` | List shared notes |
| GET | `/api/notes/<note_id>/shares` | List note permissions |

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/tasks/` | List tasks |
| POST | `/api/tasks/` | Create task |
| PUT | `/api/tasks/<task_id>` | Update task status or details |
| DELETE | `/api/tasks/<task_id>` | Delete task |

### Files

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/files/` | Upload file |
| GET | `/api/files/` | List files |
| DELETE | `/api/files/<file_id>` | Delete file |
| GET | `/api/files/<file_id>/download` | Download file |

### AI

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/ai/chat` | Chat with AI |
| POST | `/api/ai/ask` | Ask an academic question |
| POST | `/api/ai/summarize` | Summarize text or a file |
| POST | `/api/ai/quiz` | Generate a quiz |
| POST | `/api/ai/analyze-file` | Analyze an uploaded file |

### Service Health

`GET /api/health` returns application health and whether an AI key is configured.

## Using the Study Planner

1. Sign in and open **Tasks** from the sidebar.
2. Select **Add Task** and enter the task title, deadline, and priority.
3. Save the task. Use the checkbox to change its completed state.
4. Filter tasks with **All Tasks**, **In Progress**, or **Completed**.
5. Add exams in the **Upcoming Exam Countdown** section.
6. Add subjects under **Subjects & Syllabus**.
7. Expand a subject and add its unit names.
8. Mark units complete with their right-side checkboxes.
9. Overall syllabus completion is calculated from completed units, while the tracker lists subject names and their progress.

## Testing

Run the backend test suite:

```bash
python -m pytest
```

The current tests use mongomock and Flask's test client, so they do not require a running MongoDB server for unit-level database operations.

## Deployment

### Render

The repository includes [render.yaml](render.yaml), which configures:

- Python web service
- Production environment
- Gunicorn through `backend/start.py`
- Generated Flask and JWT secrets
- MongoDB URI provided by the Render environment
- Groq-compatible OpenAI API defaults
- `/api/health` health checks

The live deployment is:

https://nextmind-study-assistant.onrender.com

Set the following values in Render before starting a production deployment:

- `MONGO_URI`
- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `OPENAI_MODEL`
- OAuth credentials if OAuth is enabled

### Production Checklist

- Use strong, unique Flask and JWT secrets.
- Use MongoDB Atlas or another persistent MongoDB service.
- Configure HTTPS.
- Do not commit `.env`.
- Configure persistent storage for uploads; local `backend/uploads` storage may be ephemeral on managed hosting.
- Restrict OAuth redirect URLs to deployed domains.
- Keep API keys outside source control.

## Storage Notes

- Notes, tasks, users, files, sharing permissions, and statistics are persisted in MongoDB.
- Subject names, syllabus units, unit completion, and exam countdown entries currently use browser `localStorage`.
- Clearing browser storage removes planner subjects and countdowns stored on that browser.
- Uploaded file content is stored under `backend/uploads` in the current implementation.

## Troubleshooting

### MongoDB connection refused

- Verify MongoDB is running locally.
- Check that `MONGO_URI` is valid.
- Confirm the database user has access when using MongoDB Atlas.

### AI features do not respond

- Set `OPENAI_API_KEY`.
- Verify `OPENAI_BASE_URL` matches the provider.
- Confirm `OPENAI_MODEL` is available from that provider.
- Review provider quotas and logs.

### Redirected back to login

- Sign in again to create a fresh JWT.
- Clear invalid browser local storage values if the token is stale.
- Confirm `JWT_SECRET_KEY` is stable across application restarts.

### OAuth login does not work

- Configure both OAuth client credentials.
- Register the callback URL with the provider.
- Ensure the callback environment variable matches the deployed URL exactly.

### Uploaded files are missing after deployment

The Render filesystem can be ephemeral. Configure persistent disk storage or migrate uploads to object storage for production reliability.

## Contributing

1. Create a feature branch.
2. Make focused changes.
3. Run relevant tests with `python -m pytest`.
4. Commit and open a pull request.

```bash
git checkout -b feature/your-feature
git add .
git commit -m "Describe your change"
git push origin feature/your-feature
```

## License

No license file is currently included in the repository. Add a LICENSE file before applying a specific open-source license.

## Support

Report bugs and request features through the repository issue tracker.

---

**Last Updated:** November 6, 2026
**Version:** 1.1.0
**Status:** Active development and deployment
