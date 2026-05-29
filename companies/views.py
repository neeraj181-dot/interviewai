from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Company, InterviewSlot, Application, InterviewBooking
from core.models import UserProfile


@login_required
def company_list(request):
    status_filter = request.GET.get('status', 'all')
    companies = Company.objects.all()
    if status_filter != 'all':
        companies = companies.filter(hiring_status=status_filter)

    # Annotate with user application status
    user_apps = {a.company_id: a for a in Application.objects.filter(user=request.user)}
    for company in companies:
        company.user_application = user_apps.get(company.id)

    statuses = [('all', 'All Companies'), ('hiring', 'Actively Hiring'),
                ('limited', 'Limited'), ('upcoming', 'Opening Soon'), ('closed', 'Closed')]

    # AI recommendations based on user profile
    from core.models import UserProfile
    from interviews.models import InterviewSession
    from courses.models import CourseSession
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # Compute avg scores per skill area
    user_skills = profile.skills_list
    completed_interviews = InterviewSession.objects.filter(user=request.user, is_completed=True).count()
    avg_score = profile.average_score

    # Smart recommendations
    recommended = []
    if avg_score >= 70 and completed_interviews >= 3:
        recommended = list(Company.objects.filter(hiring_status='hiring', difficulty__in=['medium', 'hard'])[:3])
    elif avg_score >= 50:
        recommended = list(Company.objects.filter(hiring_status='hiring', difficulty='medium')[:3])
    else:
        recommended = list(Company.objects.filter(hiring_status='hiring', difficulty__in=['easy', 'medium'])[:3])

    return render(request, 'companies/company_list.html', {
        'companies': companies,
        'statuses': statuses,
        'active_status': status_filter,
        'profile': profile,
        'recommended': recommended,
        'avg_score': avg_score,
        'completed_interviews': completed_interviews,
    })


@login_required
def company_detail(request, slug):
    company = get_object_or_404(Company, slug=slug)
    slots = InterviewSlot.objects.filter(company=company, status='available').order_by('date', 'time_start')
    user_app = Application.objects.filter(user=request.user, company=company).first()
    user_bookings = []
    if user_app:
        user_bookings = InterviewBooking.objects.filter(
            application=user_app).select_related('slot').order_by('-booked_at')

    return render(request, 'companies/company_detail.html', {
        'company': company, 'slots': slots,
        'user_app': user_app, 'user_bookings': user_bookings,
    })


@login_required
def apply_company(request, slug):
    company = get_object_or_404(Company, slug=slug)
    if company.hiring_status == 'closed':
        messages.error(request, f'{company.name} is not currently hiring.')
        return redirect('company_detail', slug=slug)

    app, created = Application.objects.get_or_create(
        user=request.user, company=company,
        defaults={'status': 'applied'}
    )
    if created:
        messages.success(request, f'Successfully applied to {company.name}!')
    else:
        messages.info(request, f'You have already applied to {company.name}.')
    return redirect('company_detail', slug=slug)


@login_required
def book_slot(request, slot_id):
    slot = get_object_or_404(InterviewSlot, id=slot_id)
    user_app = Application.objects.filter(user=request.user, company=slot.company).first()

    if not user_app:
        messages.error(request, 'You must apply to this company before booking an interview slot.')
        return redirect('company_detail', slug=slot.company.slug)

    if not slot.is_available:
        messages.error(request, 'This slot is no longer available.')
        return redirect('company_detail', slug=slot.company.slug)

    existing = InterviewBooking.objects.filter(
        application=user_app, slot=slot, status__in=['pending', 'confirmed']).exists()
    if existing:
        messages.info(request, 'You have already booked this slot.')
        return redirect('my_applications')

    booking = InterviewBooking.objects.create(application=user_app, slot=slot, status='confirmed')
    user_app.status = 'interview_scheduled'
    user_app.save()

    messages.success(request, f'Interview booked! Confirmation: {booking.confirmation_code}')
    return redirect('my_applications')


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(InterviewBooking, id=booking_id, application__user=request.user)
    booking.status = 'cancelled'
    booking.save()
    booking.application.status = 'applied'
    booking.application.save()
    messages.success(request, 'Booking cancelled successfully.')
    return redirect('my_applications')


@login_required
def my_applications(request):
    applications = Application.objects.filter(
        user=request.user).select_related('company').prefetch_related('bookings__slot').order_by('-applied_at')
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    status_counts = {}
    for app in applications:
        status_counts[app.status] = status_counts.get(app.status, 0) + 1

    return render(request, 'companies/my_applications.html', {
        'applications': applications,
        'profile': profile,
        'status_counts': status_counts,
    })
