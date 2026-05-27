# InterviewAI - Futuristic Interview Preparation Platform

A modern, full-stack Django web application for interview preparation with a futuristic dark-themed UI featuring neon glow effects and glassmorphism design.

## Features

### User Authentication
- User registration with email validation
- Secure login/logout system
- Session-based authentication
- Profile management

### Dashboard
- Modern futuristic dark-themed interface
- Sidebar navigation
- Welcome message with personalized username
- Interview category cards with progress tracking
- Real-time statistics display

### Interview System
- Multiple interview categories:
  - Python
  - Django
  - HR (Human Resources)
  - Web Development
- Interactive question display
- Answer submission system
- Real-time scoring and feedback
- Performance analysis

### UI/UX Features
- **Futuristic Dark Theme**: Modern dark interface with neon accents
- **Neon Glow Effects**: Eye-catching glow effects on interactive elements
- **Glassmorphism Design**: Frosted glass card effects
- **Responsive Design**: Fully responsive across all devices
- **Smooth Animations**: Fluid transitions and animations
- **Modern Dashboard Layout**: Intuitive and user-friendly interface

### Additional Features
- Interview history tracking
- User score statistics
- Progress analysis per category
- Detailed profile section
- Performance feedback and recommendations

## Tech Stack

- **Backend**: Django 4.2+
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **CSS Framework**: Bootstrap 5.3
- **Icons**: Font Awesome 6.4
- **Authentication**: Django's built-in authentication system

## Project Structure

```
interviewai_project/
├── interviewai_project/          # Main project directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── interviewai/                  # Main app directory
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── management/              # Custom management commands
│   │   └── commands/
│   │       └── load_sample_data.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/                    # HTML templates
│   ├── base.html               # Base template with futuristic theme
│   └── interviewai/            # App-specific templates
│       ├── dashboard.html
│       ├── interview_history.html
│       ├── interview_question.html
│       ├── interview_result.html
│       ├── login.html
│       ├── profile.html
│       └── register.html
├── manage.py
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or navigate to the project directory**
   ```bash
   cd interviewai_project
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Load sample data (optional)**
   ```bash
   python manage.py load_sample_data
   ```

6. **Create a superuser (for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and navigate to: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## Usage

### First Steps

1. **Register an account**: Click on the registration link and create your account
2. **Login**: Use your credentials to access the dashboard
3. **Choose a category**: Select from Python, Django, HR, or Web Development
4. **Start interview**: Answer questions one by one
5. **View results**: See your score and detailed feedback after completion

### Dashboard Features

- **Statistics Cards**: View total score, interviews completed, and average score
- **Category Cards**: See progress for each interview category
- **Recent History**: Quick access to your latest interview results

### Profile Section

- View detailed statistics
- Track category-wise performance
- Review interview history
- Monitor progress over time

## Models

### Question
- Category (Python, Django, HR, Web Development)
- Question text
- Correct answer
- Difficulty level (Easy, Medium, Hard)

### Answer
- Question reference
- User reference
- User's answer
- Correct/incorrect status
- Timestamp

### InterviewHistory
- User reference
- Category
- Score
- Total questions
- Completion timestamp

### UserProfile
- User reference (One-to-One)
- Total score
- Interviews completed
- Creation and update timestamps

## Customization

### Adding New Questions

You can add questions through:
1. **Admin Panel**: Access `/admin/` and use the Django admin interface
2. **Management Command**: Create custom management commands
3. **Direct Database**: Use Django shell or database tools

### Modifying the UI

The futuristic theme is defined in `templates/base.html`. Key CSS variables:
- `--primary-neon`: Cyan neon color
- `--secondary-neon`: Magenta neon color
- `--accent-neon`: Green neon color
- `--bg-dark`: Dark background color
- `--bg-card`: Glass card background

## Development

### Running Tests
```bash
python manage.py test
```

### Creating New Features
1. Add models in `interviewai/models.py`
2. Create views in `interviewai/views.py`
3. Define URLs in `interviewai/urls.py`
4. Create templates in `templates/interviewai/`
5. Run migrations: `python manage.py makemigrations && python manage.py migrate`

## Security Notes

- Change the `SECRET_KEY` in `settings.py` for production
- Set `DEBUG = False` in production
- Use environment variables for sensitive configuration
- Implement proper CSRF protection (already included)
- Use HTTPS in production

## License

This project is created for educational purposes.

## Support

For issues or questions, please refer to the Django documentation or create an issue in the project repository.

---

**Built with Django 4.2+ and modern web technologies**
