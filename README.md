# InterviewAI 🚀

A futuristic full-stack Django web application for AI-powered interview preparation.

## Features
- **User Authentication** — Register, Login, Logout with session-based auth
- **Futuristic Dark UI** — Neon glow effects, glassmorphism cards, particle animations
- **4 Interview Categories** — Python, Django, HR Interview, Web Development
- **32 Questions** — 8 per category with Easy/Medium/Hard difficulty
- **Smart Scoring** — Keyword-based answer evaluation with partial credit
- **Interview History** — Track all sessions with scores and grades
- **Profile Page** — Stats, level system (Beginner → Expert), avatar upload
- **Progress Tracking** — Per-category performance charts

## Quick Start

```bash
# Install dependencies
pip install django pillow

# Run migrations
python manage.py migrate

# Seed questions
python manage.py seed_data

# Start server
python manage.py runserver
```

## Access
- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- Admin credentials: `admin` / `admin123`

## Project Structure
```
interviewai/          # Django project settings & URLs
core/                 # Auth, dashboard, profile
interviews/           # Categories, questions, sessions, results
templates/            # HTML templates
static/css/           # Futuristic CSS with neon effects
static/js/            # Particle animations, counters, typing effect
```

## Tech Stack
- Django 6.x + SQLite
- Vanilla CSS (glassmorphism + neon theme)
- Font Awesome 6 icons
- Google Fonts (Orbitron, Rajdhani)
- Vanilla JavaScript (particles, animations)
