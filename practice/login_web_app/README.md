
# User Authentication Project

This is a simple FastAPI project that demonstrates a basic **user login and registration system** using HTML.

## Project Structure
```bash
user_auth/                  # Root project folder
├── app/                    # FastAPI application code
│   ├── main.py             # Entry point for FastAPI
│   ├── models.py           # Pydantic models (User, LoginRequest, etc.)
│   ├── database.py         # In-memory DB or database setup
│   └── auth.py             # Routes for login/register logic
│
├── static/                 # Static files (CSS, JS)
│   └── style.css
│
├── templates/              # HTML templates
│   ├── index.html
    ├── signup.html        # Login/Register form
    ├── login.html
│   └── dashboard.html      # Example logged-in page
│
├── requirements.txt        # Python dependencies
└── README.md               # Project explanation
```

## How It Works
- **Backend (`app/`)**: Handles all API logic using FastAPI.
  - `main.py`: Starts the FastAPI server, mounts static files, and includes routes.
  - `auth.py`: Contains the login and registration endpoints.
  - `models.py`: Defines Pydantic models for request validation.
  - `database.py`: Contains a simple in-memory database for users (can be replaced with a real database).

- **Frontend (`templates/`)**: Contains HTML pages for login, registration, and post-login dashboard.

- **Static (`static/`)**: CSS and JavaScript files for styling and client-side interactivity.
