# Development Guide

## 🛠️ Setup for Development

### Prerequisites
- Python 3.7+
- MongoDB (local or Atlas)
- Git
- OpenAI API Key

### Initial Setup

```bash
# 1. Clone repository
git clone <repo-url>
cd project-va

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment (Windows)
.\venv\Scripts\activate

# 4. Install dependencies
pip install -r backend/requirements.txt

# 5. Create the project-root `.env` file
cp .env.example .env
# Edit .env with your local credentials.
# Do not place the file inside backend/; backend/app.py reads the root .env.
# 6. Start backend server
python backend/app.py
# Server runs on http://localhost:5000
```

## 📝 Code Style & Conventions

### Python (Backend)

**PEP 8 Guidelines**
- Use snake_case for functions and variables
- Use UPPER_CASE for constants
- Max line length: 100 characters
- Docstrings for all functions and modules

**Example Controller:**
```python
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from utils.helpers import resp

@jwt_required()
def get_item(app, item_id):
    """Retrieve item by ID for current user"""
    user_id = get_jwt_identity()
    
    # Validate ObjectId format
    try:
        obj_id = ObjectId(item_id)
    except:
        return resp(False, 'Invalid ID format', status=400)
    
    item = app.mongo.db.items.find_one({
        '_id': obj_id,
        'user_id': user_id
    })
    
    if not item:
        return resp(False, 'Item not found', status=404)
    
    item['id'] = str(item['_id'])
    del item['_id']
    return resp(True, 'Item fetched', item)
```

### JavaScript (Frontend)

**ES6+ Standards**
- Use `const`/`let` (avoid `var`)
- Arrow functions for callbacks
- Template literals for strings
- Async/await for promises

**Example Frontend Function:**
```javascript
async function loadItems(filter = '') {
  const res = await apiFetch('/items');
  
  if (!res.success) {
    console.error(res.message);
    return;
  }
  
  const container = document.getElementById('items-container');
  container.innerHTML = '';
  
  res.data
    .filter(item => item.name.toLowerCase().includes(filter.toLowerCase()))
    .forEach(item => {
      const el = document.createElement('div');
      el.className = 'card';
      el.innerHTML = `
        <h4>${item.name}</h4>
        <p>${item.description}</p>
        <button class="btn" onclick="editItem('${item.id}')">Edit</button>
      `;
      container.appendChild(el);
    });
}
```

## 🧪 Testing

### Manual Testing Checklist

Before committing, test:

- [ ] Auth: Register, Login, Token in localStorage
- [ ] Notes: Create, Read, Update, Delete with filters
- [ ] Tasks: Create with priority, Mark complete/pending
- [ ] AI: Ask question, Summarize, Generate quiz
- [ ] Profile: Update name, Change password, View stats
- [ ] Dark Mode: Toggle persists across pages
- [ ] Responsive: Test on mobile (DevTools)
- [ ] Errors: Check browser console for errors

### API Testing with Postman

1. Register user: `POST /api/auth/register`
   ```json
   {
     "name": "Test User",
     "email": "test@example.com",
     "password": "password123"
   }
   ```

2. Login: `POST /api/auth/login`
   ```json
   {
     "email": "test@example.com",
     "password": "password123"
   }
   ```

3. Copy token from response
4. Add to all requests:
   - Header: `Authorization: Bearer <token>`

## 🔄 Git Workflow

### Commit Message Format

```
<type>: <subject>

<body>
<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring
- `docs`: Documentation
- `style`: Formatting (no logic change)

**Examples:**
```
feat: Add task priority levels with color coding
fix: Dark mode not persisting across pages
refactor: Extract API utilities to app.js
docs: Add development guide
```

### Branch Naming

```
feature/feature-name
fix/bug-description
docs/documentation-name
```

## 📚 Adding New Features

### Step 1: Create Backend Controller

**File:** `backend/controllers/feature_controller.py`

```python
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.helpers import resp

@jwt_required()
def create_feature(app):
    """Create a new feature"""
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    # Validate required fields
    # Create document
    # Return response
    return resp(True, 'Feature created', {...})
```

### Step 2: Create Routes

**File:** `backend/routes/feature_routes.py`

```python
from flask import Blueprint, current_app
from flask_jwt_extended import jwt_required
from controllers.feature_controller import create_feature

feature_bp = Blueprint('feature', __name__)

@feature_bp.route('/', methods=['POST'])
@jwt_required()
def add_feature():
    return create_feature(current_app)
```

### Step 3: Register in app.py

```python
from routes.feature_routes import feature_bp

app.register_blueprint(feature_bp, url_prefix='/api/feature')
```

### Step 4: Create Frontend Page

**File:** `frontend/feature.html`

```html
<!doctype html>
<html>
<head>
  <title>Feature | AI Study Assistant</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="navbar">...</div>
  <div class="container">
    <h1>Feature</h1>
    <div class="card">
      <!-- Your UI here -->
    </div>
  </div>
  <script src="app.js"></script>
  <script>
    requireAuth();
    initDarkMode();
    // Your logic here
  </script>
</body>
</html>
```

### Step 5: Update Navigation

Add link to feature in navbar across all pages:
```html
<a href="feature.html">Feature</a>
```

## 🐛 Debugging

### Browser DevTools

- **Console**: Check for JS errors
- **Network**: Monitor API calls, check responses
- **Application → Storage**: View localStorage (tokens, user data)

### Backend Debugging

```python
# Add print statements
print(f"User ID: {user_id}")
print(f"Request data: {data}")

# Flask debug mode (already enabled)
# app.run(debug=True)
```

### Common Issues

**"ModuleNotFoundError"**
- Ensure virtual environment activated
- Run `pip install -r backend/requirements.txt`

**"Unauthorized" error**
- Token missing or expired
- Check localStorage for token
- Clear storage and login again

**MongoDB connection fails**
- Ensure MongoDB running: `mongod` or check service
- Verify MONGO_URI in .env
- Check connection string format

## 📊 Performance Tips

- Compress canvas drawings before upload
- Implement pagination for large lists
- Cache user stats after calculation
- Minimize API calls (batch requests when possible)
- Optimize database queries with proper indexes

## 🔐 Security Reminders

✅ Always hash passwords with bcrypt
✅ Validate user input on backend
✅ Check user_id matches on all operations
✅ Use JWT tokens for auth
✅ Never log sensitive data
✅ Sanitize error messages
✅ Keep .env out of git

---

**Questions?** Check README.md or STRUCTURE.md
