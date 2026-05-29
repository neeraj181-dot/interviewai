from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg, Count, Sum
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from .models import UserProfile
from interviews.models import Category, InterviewSession
from courses.models import CourseTrack, CourseSession
from companies.models import Company, Application


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to InterviewAI, {user.first_name or user.username}!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(request.GET.get('next', 'dashboard'))
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('login')


@login_required
def dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # Interview stats
    interview_sessions = InterviewSession.objects.filter(user=request.user, is_completed=True)
    course_sessions = CourseSession.objects.filter(user=request.user, is_completed=True)
    total_completed = interview_sessions.count() + course_sessions.count()
    all_pcts = list(interview_sessions.values_list('score', 'max_score')) + \
               list(course_sessions.values_list('score', 'max_score'))
    avg_score = 0
    if all_pcts:
        total_s = sum(s for s, m in all_pcts if m > 0)
        total_m = sum(m for s, m in all_pcts if m > 0)
        avg_score = round((total_s / total_m) * 100) if total_m else 0

    # Recent activity (combined)
    recent_interviews = InterviewSession.objects.filter(
        user=request.user).select_related('category').order_by('-created_at')[:3]
    recent_courses = CourseSession.objects.filter(
        user=request.user).select_related('course').order_by('-created_at')[:3]

    # Category performance
    categories = Category.objects.all()
    cat_performance = []
    for cat in categories:
        s = InterviewSession.objects.filter(user=request.user, category=cat, is_completed=True)
        avg = s.aggregate(a=Avg('score'))['a'] or 0
        max_s = s.aggregate(m=Avg('max_score'))['m'] or 1
        pct = round((avg / max_s) * 100) if s.count() else 0
        cat_performance.append({'name': cat.name, 'pct': pct, 'color': cat.color, 'count': s.count()})

    # Course track performance
    tracks = CourseTrack.objects.filter(is_active=True)
    track_performance = []
    for t in tracks[:6]:
        s = CourseSession.objects.filter(user=request.user, course=t, is_completed=True)
        avg = s.aggregate(a=Avg('score'))['a'] or 0
        max_s = s.aggregate(m=Avg('max_score'))['m'] or 1
        pct = round((avg / max_s) * 100) if s.count() else 0
        track_performance.append({'name': t.name, 'pct': pct, 'color': t.color, 'count': s.count()})

    # AI Recommendations
    weak_areas = [p for p in cat_performance + track_performance if p['pct'] < 60 and p['count'] > 0]
    suggested_courses = CourseTrack.objects.filter(is_active=True).order_by('?')[:3]
    featured_companies = Company.objects.filter(hiring_status='hiring', is_featured=True)[:3]
    user_apps = Application.objects.filter(user=request.user).count()

    # Readiness score
    profile.compute_readiness()
    level_info = profile.level_info
    badges = profile.badges

    context = {
        'profile': profile,
        'total_completed': total_completed,
        'avg_score': avg_score,
        'recent_interviews': recent_interviews,
        'recent_courses': recent_courses,
        'cat_performance': cat_performance,
        'track_performance': track_performance,
        'level_info': level_info,
        'badges': badges,
        'weak_areas': weak_areas[:3],
        'suggested_courses': suggested_courses,
        'featured_companies': featured_companies,
        'user_apps': user_apps,
        'categories': categories,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    interview_sessions = InterviewSession.objects.filter(
        user=request.user, is_completed=True).select_related('category').order_by('-created_at')
    course_sessions = CourseSession.objects.filter(
        user=request.user, is_completed=True).select_related('course').order_by('-created_at')

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            accent = request.POST.get('theme_accent', '#00d4ff')
            valid_accents = ['#00d4ff', '#00ff88', '#ff6b9d', '#ffd700', '#7b68ee', '#ff8c00']
            if accent in valid_accents:
                profile.theme_accent = accent
            form.save()
            profile.compute_readiness()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    # Category breakdown
    cat_stats = {}
    for session in interview_sessions:
        cat = session.category.name
        if cat not in cat_stats:
            cat_stats[cat] = {'count': 0, 'total': 0, 'color': session.category.color, 'icon': session.category.icon}
        cat_stats[cat]['count'] += 1
        cat_stats[cat]['total'] += session.percentage
    for k in cat_stats:
        cat_stats[k]['avg'] = round(cat_stats[k]['total'] / cat_stats[k]['count'])

    level_info = profile.level_info
    badges = profile.badges
    applications = Application.objects.filter(user=request.user).select_related('company').order_by('-applied_at')[:5]

    # ── AI Resume Analysis ──
    user_skills = set(s.lower() for s in profile.skills_list)
    high_demand_skills = ['python', 'django', 'react', 'javascript', 'sql', 'aws',
                          'machine learning', 'docker', 'git', 'rest api', 'node.js', 'typescript']
    missing_skills = [s for s in high_demand_skills if s not in user_skills][:5]

    # ATS score: based on profile completeness
    ats_score = 0
    ats_checks = []
    if profile.resume:
        ats_score += 25
        ats_checks.append({'label': 'Resume uploaded', 'ok': True})
    else:
        ats_checks.append({'label': 'Upload your resume', 'ok': False})
    if len(profile.skills_list) >= 5:
        ats_score += 20
        ats_checks.append({'label': f'{len(profile.skills_list)} skills listed', 'ok': True})
    else:
        ats_checks.append({'label': 'Add at least 5 skills', 'ok': False})
    if request.user.first_name and request.user.last_name:
        ats_score += 15
        ats_checks.append({'label': 'Full name set', 'ok': True})
    else:
        ats_checks.append({'label': 'Add your full name', 'ok': False})
    if request.user.email:
        ats_score += 10
        ats_checks.append({'label': 'Email address set', 'ok': True})
    else:
        ats_checks.append({'label': 'Add your email', 'ok': False})
    if profile.github_url or profile.linkedin_url:
        ats_score += 15
        ats_checks.append({'label': 'Social links added', 'ok': True})
    else:
        ats_checks.append({'label': 'Add GitHub or LinkedIn', 'ok': False})
    if profile.experience_years > 0:
        ats_score += 10
        ats_checks.append({'label': f'{profile.experience_years} years experience', 'ok': True})
    else:
        ats_checks.append({'label': 'Set years of experience', 'ok': False})
    if profile.bio:
        ats_score += 5
        ats_checks.append({'label': 'Bio/summary written', 'ok': True})
    else:
        ats_checks.append({'label': 'Write a short bio', 'ok': False})

    # Recommended tracks based on missing skills
    from courses.models import CourseTrack
    recommended_tracks = []
    skill_to_course = {
        'python': 'python', 'django': 'django', 'react': 'react',
        'javascript': 'javascript', 'machine learning': 'ml',
        'aws': 'ai-engineering', 'sql': 'dsa', 'node.js': 'nodejs',
    }
    seen = set()
    for skill in missing_skills:
        slug = skill_to_course.get(skill)
        if slug and slug not in seen:
            try:
                track = CourseTrack.objects.get(slug=slug)
                recommended_tracks.append({'skill': skill, 'track': track})
                seen.add(slug)
            except CourseTrack.DoesNotExist:
                pass
        if len(recommended_tracks) >= 3:
            break

    context = {
        'profile': profile, 'form': form,
        'interview_sessions': interview_sessions,
        'course_sessions': course_sessions,
        'level_info': level_info, 'badges': badges,
        'cat_stats': cat_stats, 'applications': applications,
        'ats_score': ats_score,
        'ats_checks': ats_checks,
        'missing_skills': missing_skills,
        'recommended_tracks': recommended_tracks,
    }
    return render(request, 'core/profile.html', context)
