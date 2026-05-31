from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Avg
from .models import CourseTrack, CourseQuestion, CourseSession, CourseAnswer
from interviews.models import Category, InterviewSession
from core.models import UserProfile


@login_required
def interview_prep(request):
    """Merged Interview Prep page: Interview Tracks + Courses in one place."""
    track_filter = request.GET.get('track', 'all')

    # Courses (all tracks)
    courses = CourseTrack.objects.filter(is_active=True).annotate(q_count=Count('questions'))
    if track_filter not in ('all', 'interview'):
        courses = courses.filter(track=track_filter)
    elif track_filter == 'interview':
        courses = courses.none()

    for course in courses:
        user_sessions = CourseSession.objects.filter(
            user=request.user, course=course, is_completed=True)
        course.user_sessions = user_sessions.count()
        avg = user_sessions.aggregate(a=Avg('score'))['a'] or 0
        max_s = user_sessions.aggregate(m=Avg('max_score'))['m'] or 1
        course.user_avg = round((avg / max_s) * 100) if user_sessions.count() else 0

    # Interview categories
    categories = Category.objects.all()
    if track_filter == 'interview':
        show_categories = True
        show_courses = False
    elif track_filter == 'all':
        show_categories = True
        show_courses = True
    else:
        show_categories = False
        show_courses = True

    # Per-category user stats
    for cat in categories:
        user_sessions = InterviewSession.objects.filter(
            user=request.user, category=cat, is_completed=True)
        cat.user_sessions = user_sessions.count()
        avg = user_sessions.aggregate(a=Avg('score'))['a'] or 0
        max_s = user_sessions.aggregate(m=Avg('max_score'))['m'] or 1
        cat.user_avg = round((avg / max_s) * 100) if user_sessions.count() else 0

    tabs = [
        ('all', 'All', 'fas fa-layer-group'),
        ('interview', 'Interview Tracks', 'fas fa-comments'),
        ('programming', 'Programming', 'fas fa-code'),
        ('ai', 'AI & Future Tech', 'fas fa-brain'),
        ('placement', 'Placement Prep', 'fas fa-briefcase'),
    ]

    return render(request, 'courses/interview_prep.html', {
        'courses': courses,
        'categories': categories,
        'tabs': tabs,
        'active_track': track_filter,
        'show_categories': show_categories,
        'show_courses': show_courses,
    })


@login_required
def course_list(request):
    track_filter = request.GET.get('track', 'all')
    courses = CourseTrack.objects.filter(is_active=True).annotate(q_count=Count('questions'))
    if track_filter != 'all':
        courses = courses.filter(track=track_filter)
    for course in courses:
        user_sessions = CourseSession.objects.filter(
            user=request.user, course=course, is_completed=True)
        course.user_sessions = user_sessions.count()
        avg = user_sessions.aggregate(a=Avg('score'))['a'] or 0
        max_s = user_sessions.aggregate(m=Avg('max_score'))['m'] or 1
        course.user_avg = round((avg / max_s) * 100) if user_sessions.count() else 0
    tracks = [('all', 'All Tracks'), ('programming', 'Programming'),
              ('ai', 'AI & Future Tech'), ('placement', 'Placement Prep')]
    return render(request, 'courses/course_list.html', {
        'courses': courses, 'tracks': tracks, 'active_track': track_filter,
    })


@login_required
def start_course(request, slug):
    course = get_object_or_404(CourseTrack, slug=slug, is_active=True)
    difficulty = request.GET.get('difficulty', 'all')

    qs = CourseQuestion.objects.filter(course=course)
    if difficulty in ('easy', 'medium', 'hard'):
        qs = qs.filter(difficulty=difficulty)
    qs = qs.order_by('order', 'id')

    if not qs.exists():
        messages.warning(request, f'No questions for {course.name} at that level yet.')
        return redirect('course_list')

    session = CourseSession.objects.create(
        user=request.user, course=course,
        difficulty_filter=difficulty,
        total_questions=qs.count(),
        max_score=sum(q.points for q in qs),
    )
    return redirect('course_question', session_id=session.id, question_index=0)


@login_required
def course_question(request, session_id, question_index):
    session = get_object_or_404(CourseSession, id=session_id, user=request.user)
    if session.is_completed:
        return redirect('course_result', session_id=session.id)

    qs = CourseQuestion.objects.filter(course=session.course)
    if session.difficulty_filter in ('easy', 'medium', 'hard'):
        qs = qs.filter(difficulty=session.difficulty_filter)
    questions = list(qs.order_by('order', 'id'))
    total = len(questions)

    if question_index >= total:
        return redirect('finish_course', session_id=session.id)

    question = questions[question_index]
    answered_ids = list(session.answers.values_list('question_id', flat=True))
    already_answered = question.id in answered_ids
    saved_answer = ''
    if already_answered:
        ua = session.answers.filter(question=question).first()
        if ua:
            saved_answer = ua.answer_text

    progress = round((question_index / total) * 100)

    if request.method == 'POST':
        answer_text = request.POST.get('answer', '').strip()
        if not answer_text:
            messages.error(request, 'Please provide an answer.')
            return render(request, 'courses/course_question.html', {
                'session': session, 'question': question,
                'question_index': question_index, 'total': total,
                'progress': progress, 'next_index': question_index + 1,
                'saved_answer': saved_answer,
            })

        keywords = [k.strip().lower() for k in question.correct_answer.split(',') if k.strip()]
        answer_lower = answer_text.lower()
        matched = sum(1 for k in keywords if k in answer_lower)
        is_correct = matched >= max(1, len(keywords) // 2)
        points_earned = question.points if is_correct else max(0, int(question.points * matched / max(len(keywords), 1)))

        if already_answered:
            ua = session.answers.filter(question=question).first()
            if ua:
                session.score -= ua.points_earned
                if ua.is_correct:
                    session.correct_answers -= 1
                ua.answer_text = answer_text
                ua.is_correct = is_correct
                ua.points_earned = points_earned
                ua.save()
        else:
            CourseAnswer.objects.create(
                session=session, question=question,
                answer_text=answer_text, is_correct=is_correct,
                points_earned=points_earned,
            )

        session.score += points_earned
        if is_correct and not already_answered:
            session.correct_answers += 1
        session.save()

        next_index = question_index + 1
        if next_index >= total:
            return redirect('finish_course', session_id=session.id)
        return redirect('course_question', session_id=session.id, question_index=next_index)

    return render(request, 'courses/course_question.html', {
        'session': session, 'question': question,
        'question_index': question_index, 'total': total,
        'progress': progress, 'next_index': question_index + 1,
        'saved_answer': saved_answer, 'already_answered': already_answered,
        'answered_count': len(answered_ids),
    })


@login_required
def finish_course(request, session_id):
    session = get_object_or_404(CourseSession, id=session_id, user=request.user)
    if not session.is_completed:
        session.is_completed = True
        session.completed_at = timezone.now()
        xp_earned = 50 + int(session.percentage * 0.5)
        session.xp_earned = xp_earned
        session.save()

        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.total_interviews += 1
        profile.total_score += session.percentage
        profile.xp_points += xp_earned
        today = timezone.now().date()
        if profile.last_interview_date:
            delta = (today - profile.last_interview_date).days
            profile.streak_days = profile.streak_days + 1 if delta == 1 else (1 if delta > 1 else profile.streak_days)
        else:
            profile.streak_days = 1
        profile.last_interview_date = today
        profile.save()
        profile.compute_readiness()

    return redirect('course_result', session_id=session.id)


@login_required
def course_result(request, session_id):
    session = get_object_or_404(CourseSession, id=session_id, user=request.user)
    answers = session.answers.select_related('question').order_by('created_at')
    grade, grade_color = session.grade
    breakdown = {'easy': {'correct': 0, 'total': 0},
                 'medium': {'correct': 0, 'total': 0},
                 'hard': {'correct': 0, 'total': 0}}
    for ans in answers:
        d = ans.question.difficulty
        breakdown[d]['total'] += 1
        if ans.is_correct:
            breakdown[d]['correct'] += 1
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'courses/course_result.html', {
        'session': session, 'answers': answers,
        'grade': grade, 'grade_color': grade_color,
        'breakdown': breakdown, 'profile': profile,
        'xp_earned': session.xp_earned,
    })

from django.contrib.auth.models import User
from django.http import HttpResponse

def create_admin(request):
    user, created = User.objects.get_or_create(
        username='admin55',
        defaults={'email': 'neeraj1812000@gmail.com'}
    )

    user.is_staff = True
    user.is_superuser = True
    user.set_password('94949494')
    user.save()

    return HttpResponse("Admin reset successfully")

