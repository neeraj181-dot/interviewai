from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Avg
from django.http import JsonResponse
from .models import Category, Question, InterviewSession, UserAnswer
from core.models import UserProfile
import json


@login_required
def category_list(request):
    categories = Category.objects.annotate(q_count=Count('questions'))
    # Per-category user stats
    for cat in categories:
        user_sessions = InterviewSession.objects.filter(
            user=request.user, category=cat, is_completed=True
        )
        cat.user_sessions = user_sessions.count()
        avg = user_sessions.aggregate(a=Avg('score'))['a'] or 0
        max_s = user_sessions.aggregate(m=Avg('max_score'))['m'] or 1
        cat.user_avg = round((avg / max_s) * 100) if max_s and user_sessions.count() else 0
    return render(request, 'interviews/categories.html', {'categories': categories})


@login_required
def start_interview(request, slug):
    category = get_object_or_404(Category, slug=slug)
    difficulty = request.GET.get('difficulty', 'all')

    qs = Question.objects.filter(category=category)
    if difficulty in ('easy', 'medium', 'hard'):
        qs = qs.filter(difficulty=difficulty)
    qs = qs.order_by('order', 'id')

    if not qs.exists():
        messages.warning(request, f'No questions for {category.name} at that level.')
        return redirect('categories')

    session = InterviewSession.objects.create(
        user=request.user,
        category=category,
        difficulty_filter=difficulty,
        total_questions=qs.count(),
        max_score=sum(q.points for q in qs),
    )
    return redirect('interview_question', session_id=session.id, question_index=0)


@login_required
def interview_question(request, session_id, question_index):
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)

    if session.is_completed:
        return redirect('interview_result', session_id=session.id)

    qs = Question.objects.filter(category=session.category)
    if session.difficulty_filter in ('easy', 'medium', 'hard'):
        qs = qs.filter(difficulty=session.difficulty_filter)
    questions = list(qs.order_by('order', 'id'))
    total = len(questions)

    if question_index >= total:
        return redirect('finish_interview', session_id=session.id)

    question = questions[question_index]
    answered_ids = list(session.answers.values_list('question_id', flat=True))
    already_answered = question.id in answered_ids

    # Load saved answer if navigating back
    saved_answer = ''
    if already_answered:
        ua = session.answers.filter(question=question).first()
        if ua:
            saved_answer = ua.answer_text

    progress = round(((question_index) / total) * 100)

    if request.method == 'POST':
        answer_text = request.POST.get('answer', '').strip()
        if not answer_text:
            messages.error(request, 'Please provide an answer.')
            return render(request, 'interviews/question.html', {
                'session': session, 'question': question,
                'question_index': question_index, 'total': total,
                'progress': progress, 'next_index': question_index + 1,
                'saved_answer': saved_answer,
            })

        # Keyword scoring
        correct_keywords = [kw.strip().lower() for kw in question.correct_answer.split(',') if kw.strip()]
        answer_lower = answer_text.lower()
        matched = sum(1 for kw in correct_keywords if kw in answer_lower)
        is_correct = matched >= max(1, len(correct_keywords) // 2)
        points_earned = question.points if is_correct else max(0, int(question.points * matched / max(len(correct_keywords), 1)))

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
            UserAnswer.objects.create(
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
            return redirect('finish_interview', session_id=session.id)
        return redirect('interview_question', session_id=session.id, question_index=next_index)

    context = {
        'session': session, 'question': question,
        'question_index': question_index, 'total': total,
        'progress': progress, 'next_index': question_index + 1,
        'saved_answer': saved_answer, 'already_answered': already_answered,
        'answered_count': len(answered_ids),
    }
    return render(request, 'interviews/question.html', context)


@login_required
def finish_interview(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)

    if not session.is_completed:
        session.is_completed = True
        session.completed_at = timezone.now()
        session.save()

        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.total_interviews += 1
        profile.total_score += session.percentage

        # XP: base 50 + bonus for score
        xp_earned = 50 + int(session.percentage * 0.5)
        profile.xp_points += xp_earned

        # Streak
        today = timezone.now().date()
        if profile.last_interview_date:
            delta = (today - profile.last_interview_date).days
            if delta == 1:
                profile.streak_days += 1
            elif delta > 1:
                profile.streak_days = 1
        else:
            profile.streak_days = 1
        profile.last_interview_date = today
        profile.save()

        session.xp_earned = xp_earned
        session.save()

    return redirect('interview_result', session_id=session.id)


@login_required
def interview_result(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    answers = session.answers.select_related('question').order_by('created_at')
    grade, grade_color = session.grade

    # Topic breakdown by difficulty
    breakdown = {'easy': {'correct': 0, 'total': 0}, 'medium': {'correct': 0, 'total': 0}, 'hard': {'correct': 0, 'total': 0}}
    for ans in answers:
        d = ans.question.difficulty
        breakdown[d]['total'] += 1
        if ans.is_correct:
            breakdown[d]['correct'] += 1

    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    context = {
        'session': session, 'answers': answers,
        'grade': grade, 'grade_color': grade_color,
        'breakdown': breakdown, 'profile': profile,
        'xp_earned': getattr(session, 'xp_earned', 50 + int(session.percentage * 0.5)),
    }
    return render(request, 'interviews/result.html', context)


@login_required
def interview_history(request):
    search = request.GET.get('q', '').strip()
    sessions = InterviewSession.objects.filter(
        user=request.user, is_completed=True
    ).select_related('category').order_by('-created_at')

    if search:
        sessions = sessions.filter(category__name__icontains=search)

    category_stats = {}
    for session in sessions:
        cat = session.category.name
        if cat not in category_stats:
            category_stats[cat] = {'count': 0, 'total_pct': 0, 'color': session.category.color, 'icon': session.category.icon}
        category_stats[cat]['count'] += 1
        category_stats[cat]['total_pct'] += session.percentage
    for cat in category_stats:
        cnt = category_stats[cat]['count']
        category_stats[cat]['avg'] = round(category_stats[cat]['total_pct'] / cnt) if cnt else 0

    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    context = {
        'sessions': sessions, 'category_stats': category_stats,
        'profile': profile, 'total_completed': sessions.count(),
        'search': search,
    }
    return render(request, 'interviews/history.html', context)
