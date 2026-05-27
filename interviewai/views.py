from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Avg, Count, Sum
from .models import Question, Answer, InterviewHistory, UserProfile


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'interviewai/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'interviewai/register.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user)
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')
    
    return render(request, 'interviewai/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'interviewai/login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')


@login_required
def dashboard(request):
    user_profile = request.user.profile
    recent_histories = InterviewHistory.objects.filter(user=request.user).order_by('-completed_at')[:5]
    
    # Get category statistics
    category_stats = {}
    categories = ['python', 'django', 'hr', 'web']
    
    for category in categories:
        histories = InterviewHistory.objects.filter(user=request.user, category=category)
        if histories.exists():
            avg_score = histories.aggregate(Avg('percentage'))['percentage__avg'] or 0
            total_completed = histories.count()
            category_stats[category] = {
                'avg_score': round(avg_score, 2),
                'completed': total_completed
            }
        else:
            category_stats[category] = {
                'avg_score': 0,
                'completed': 0
            }
    
    context = {
        'user_profile': user_profile,
        'recent_histories': recent_histories,
        'category_stats': category_stats,
    }
    return render(request, 'interviewai/dashboard.html', context)


@login_required
def interview_start(request, category):
    questions = Question.objects.filter(category=category)
    if not questions.exists():
        messages.error(request, 'No questions available for this category!')
        return redirect('dashboard')
    
    # Get first question
    first_question = questions.first()
    return redirect('interview_question', category=category, question_id=first_question.id)


@login_required
def interview_question(request, category, question_id):
    question = get_object_or_404(Question, id=question_id, category=category)
    questions = Question.objects.filter(category=category).order_by('id')
    
    # Get current question index
    question_ids = list(questions.values_list('id', flat=True))
    current_index = question_ids.index(question_id)
    total_questions = len(question_ids)
    
    # Check if this is the last question
    is_last_question = (current_index == total_questions - 1)
    
    # Get next question ID
    next_question_id = question_ids[current_index + 1] if not is_last_question else None
    
    context = {
        'question': question,
        'current_index': current_index + 1,
        'total_questions': total_questions,
        'is_last_question': is_last_question,
        'next_question_id': next_question_id,
        'category': category,
    }
    return render(request, 'interviewai/interview_question.html', context)


@login_required
def submit_answer(request, category, question_id):
    if request.method != 'POST':
        return redirect('interview_question', category=category, question_id=question_id)
    
    question = get_object_or_404(Question, id=question_id, category=category)
    user_answer = request.POST.get('answer')
    
    # Check if answer is correct (simple comparison - can be enhanced)
    is_correct = user_answer.lower().strip() == question.correct_answer.lower().strip()
    
    # Save the answer
    Answer.objects.create(
        question=question,
        user=request.user,
        user_answer=user_answer,
        is_correct=is_correct
    )
    
    # Get action parameter
    action = request.POST.get('action')
    
    if action == 'finish':
        # Calculate score for this interview session
        questions = Question.objects.filter(category=category)
        answers = Answer.objects.filter(
            user=request.user,
            question__category=category
        ).order_by('-created_at')[:questions.count()]
        
        score = sum(1 for answer in answers if answer.is_correct)
        total = answers.count()
        
        # Save interview history
        history = InterviewHistory.objects.create(
            user=request.user,
            category=category,
            score=score,
            total_questions=total
        )
        
        # Update user profile
        profile = request.user.profile
        profile.total_score += score
        profile.interviews_completed += 1
        profile.save()
        
        return redirect('interview_result', history_id=history.id)
    else:
        # Move to next question
        next_question_id = request.POST.get('next_question_id')
        if next_question_id:
            return redirect('interview_question', category=category, question_id=next_question_id)
        else:
            # No more questions, finish interview
            questions = Question.objects.filter(category=category)
            answers = Answer.objects.filter(
                user=request.user,
                question__category=category
            ).order_by('-created_at')[:questions.count()]
            
            score = sum(1 for answer in answers if answer.is_correct)
            total = answers.count()
            
            history = InterviewHistory.objects.create(
                user=request.user,
                category=category,
                score=score,
                total_questions=total
            )
            
            profile = request.user.profile
            profile.total_score += score
            profile.interviews_completed += 1
            profile.save()
            
            return redirect('interview_result', history_id=history.id)


@login_required
def interview_result(request, history_id):
    history = get_object_or_404(InterviewHistory, id=history_id, user=request.user)
    
    # Get answers for this interview
    answers = Answer.objects.filter(
        user=request.user,
        question__category=history.category
    ).order_by('-created_at')[:history.total_questions]
    
    context = {
        'history': history,
        'answers': answers,
    }
    return render(request, 'interviewai/interview_result.html', context)


@login_required
def interview_history(request):
    histories = InterviewHistory.objects.filter(user=request.user).order_by('-completed_at')
    
    context = {
        'histories': histories,
    }
    return render(request, 'interviewai/interview_history.html', context)


@login_required
def profile(request):
    user_profile = request.user.profile
    histories = InterviewHistory.objects.filter(user=request.user).order_by('-completed_at')
    
    # Calculate statistics
    category_performance = {}
    for category in ['python', 'django', 'hr', 'web']:
        cat_histories = histories.filter(category=category)
        if cat_histories.exists():
            avg_score = cat_histories.aggregate(Avg('percentage'))['percentage__avg'] or 0
            category_performance[category] = {
                'count': cat_histories.count(),
                'avg_score': round(avg_score, 2)
            }
        else:
            category_performance[category] = {
                'count': 0,
                'avg_score': 0
            }
    
    context = {
        'user_profile': user_profile,
        'histories': histories,
        'category_performance': category_performance,
    }
    return render(request, 'interviewai/profile.html', context)
