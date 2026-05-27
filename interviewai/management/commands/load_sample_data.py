from django.core.management.base import BaseCommand
from interviewai.models import Question


class Command(BaseCommand):
    help = 'Load sample interview questions into the database'

    def handle(self, *args, **kwargs):
        # Clear existing questions
        Question.objects.all().delete()
        
        # Python Questions
        python_questions = [
            {
                'category': 'python',
                'question_text': 'What is the difference between list and tuple in Python?',
                'correct_answer': 'Lists are mutable and can be modified, while tuples are immutable and cannot be changed after creation.',
                'difficulty': 'easy'
            },
            {
                'category': 'python',
                'question_text': 'Explain the difference between __init__ and __new__ in Python classes.',
                'correct_answer': '__new__ is responsible for creating a new instance of the class, while __init__ is responsible for initializing the instance after it has been created.',
                'difficulty': 'medium'
            },
            {
                'category': 'python',
                'question_text': 'What are decorators in Python and how do they work?',
                'correct_answer': 'Decorators are functions that modify the behavior of other functions. They wrap a function to extend its behavior without permanently modifying it.',
                'difficulty': 'medium'
            },
            {
                'category': 'python',
                'question_text': 'Explain the Global Interpreter Lock (GIL) in Python.',
                'correct_answer': 'The GIL is a mutex that protects access to Python objects, preventing multiple native threads from executing Python bytecodes at once.',
                'difficulty': 'hard'
            },
            {
                'category': 'python',
                'question_text': 'What is the difference between deep copy and shallow copy?',
                'correct_answer': 'Shallow copy creates a new object but references the same nested objects, while deep copy creates a new object and recursively copies all nested objects.',
                'difficulty': 'medium'
            },
        ]

        # Django Questions
        django_questions = [
            {
                'category': 'django',
                'question_text': 'What is the difference between render() and redirect() in Django?',
                'correct_answer': 'render() returns a HttpResponse with a rendered template, while redirect() returns an HttpResponseRedirect to a different URL.',
                'difficulty': 'easy'
            },
            {
                'category': 'django',
                'question_text': 'Explain the purpose of middleware in Django.',
                'correct_answer': 'Middleware is a hook system for modifying Django request/response objects globally. It processes requests before they reach the view and responses after they leave the view.',
                'difficulty': 'medium'
            },
            {
                'category': 'django',
                'question_text': 'What is the difference between select_related and prefetch_related?',
                'correct_answer': 'select_related uses SQL JOIN to fetch related objects in a single query for ForeignKey and OneToOne fields, while prefetch_related uses separate queries for ManyToMany and reverse ForeignKey relationships.',
                'difficulty': 'hard'
            },
            {
                'category': 'django',
                'question_text': 'Explain Django signals and give an example use case.',
                'correct_answer': 'Signals allow decoupled applications to get notified when certain actions occur. Example: post_save signal to create user profile when a new user is created.',
                'difficulty': 'medium'
            },
            {
                'category': 'django',
                'question_text': 'What is the purpose of Django Context Processors?',
                'correct_answer': 'Context processors make variables available in all templates globally. They add context to template contexts automatically.',
                'difficulty': 'medium'
            },
        ]

        # HR Questions
        hr_questions = [
            {
                'category': 'hr',
                'question_text': 'Tell me about yourself.',
                'correct_answer': 'This is an open-ended question to introduce yourself professionally, highlighting your background, skills, and career goals.',
                'difficulty': 'easy'
            },
            {
                'category': 'hr',
                'question_text': 'What are your greatest strengths and weaknesses?',
                'correct_answer': 'Strengths should be relevant to the job. Weaknesses should be honest but show self-awareness and efforts to improve.',
                'difficulty': 'medium'
            },
            {
                'category': 'hr',
                'question_text': 'Why do you want to work for this company?',
                'correct_answer': 'This question tests your research and genuine interest. Mention company values, culture, and how you align with them.',
                'difficulty': 'medium'
            },
            {
                'category': 'hr',
                'question_text': 'Describe a challenging situation and how you handled it.',
                'correct_answer': 'Use the STAR method: Situation, Task, Action, Result. Focus on problem-solving and positive outcomes.',
                'difficulty': 'medium'
            },
            {
                'category': 'hr',
                'question_text': 'Where do you see yourself in 5 years?',
                'correct_answer': 'Show ambition and alignment with company growth while being realistic about career development.',
                'difficulty': 'easy'
            },
        ]

        # Web Development Questions
        web_questions = [
            {
                'category': 'web',
                'question_text': 'What is the difference between GET and POST HTTP methods?',
                'correct_answer': 'GET requests data from a server and parameters are in the URL. POST sends data to the server and parameters are in the request body.',
                'difficulty': 'easy'
            },
            {
                'category': 'web',
                'question_text': 'Explain the concept of RESTful API.',
                'correct_answer': 'RESTful API follows REST architecture principles using standard HTTP methods (GET, POST, PUT, DELETE) and stateless communication.',
                'difficulty': 'medium'
            },
            {
                'category': 'web',
                'question_text': 'What is CORS and why is it important?',
                'correct_answer': 'CORS (Cross-Origin Resource Sharing) is a security feature that controls which domains can access resources on another domain.',
                'difficulty': 'medium'
            },
            {
                'category': 'web',
                'question_text': 'Explain the difference between cookies, session storage, and local storage.',
                'correct_answer': 'Cookies are sent with HTTP requests, session storage clears when tab closes, local storage persists until manually cleared.',
                'difficulty': 'hard'
            },
            {
                'category': 'web',
                'question_text': 'What is the purpose of CSS Box Model?',
                'correct_answer': 'The Box Model describes how elements are rendered with content, padding, border, and margin affecting layout and spacing.',
                'difficulty': 'easy'
            },
        ]

        # Create all questions
        all_questions = python_questions + django_questions + hr_questions + web_questions
        
        for q_data in all_questions:
            Question.objects.create(**q_data)

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(all_questions)} sample questions into the database.'))
