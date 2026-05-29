from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('very_hard', 'Very Hard'),
    ]
    STATUS_CHOICES = [
        ('hiring', 'Actively Hiring'),
        ('limited', 'Limited Openings'),
        ('closed', 'Closed'),
        ('upcoming', 'Opening Soon'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo_icon = models.CharField(max_length=100, default='fas fa-building')
    color = models.CharField(max_length=20, default='#00d4ff')
    description = models.TextField(blank=True)
    hiring_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='hiring')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')
    salary_min = models.IntegerField(default=0, help_text='Annual salary in USD (thousands)')
    salary_max = models.IntegerField(default=0)
    open_positions = models.IntegerField(default=0)
    interview_rounds = models.IntegerField(default=4)
    required_skills = models.TextField(blank=True, help_text='Comma-separated skills')
    hiring_deadline = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True)
    careers_url = models.URLField(blank=True, help_text='Official careers/jobs page URL')
    ai_tips = models.TextField(blank=True, help_text='Pipe-separated AI preparation tips')
    interview_process = models.TextField(blank=True, help_text='Pipe-separated interview round descriptions')
    culture_tags = models.TextField(blank=True, help_text='Comma-separated culture keywords')
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    @property
    def skills_list(self):
        return [s.strip() for s in self.required_skills.split(',') if s.strip()]

    @property
    def ai_tips_list(self):
        return [t.strip() for t in self.ai_tips.split('|') if t.strip()]

    @property
    def interview_process_list(self):
        return [p.strip() for p in self.interview_process.split('|') if p.strip()]

    @property
    def culture_tags_list(self):
        return [t.strip() for t in self.culture_tags.split(',') if t.strip()]

    @property
    def apply_url(self):
        """Return careers URL if set, else website, else empty."""
        return self.careers_url or self.website or ''

    @property
    def salary_display(self):
        if self.salary_min and self.salary_max:
            return f"${self.salary_min}K – ${self.salary_max}K"
        return "Competitive"

    @property
    def status_color(self):
        return {
            'hiring': '#00ff88',
            'limited': '#ffd700',
            'closed': '#ff4757',
            'upcoming': '#7b68ee',
        }.get(self.hiring_status, '#8899aa')


class InterviewSlot(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    ROUND_CHOICES = [
        ('online_test', 'Online Test'),
        ('technical_1', 'Technical Round 1'),
        ('technical_2', 'Technical Round 2'),
        ('hr', 'HR Round'),
        ('managerial', 'Managerial Round'),
        ('final', 'Final Round'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='slots')
    round_type = models.CharField(max_length=20, choices=ROUND_CHOICES, default='technical_1')
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    max_candidates = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time_start']

    def __str__(self):
        return f"{self.company.name} - {self.round_type} - {self.date}"

    @property
    def booked_count(self):
        return self.bookings.filter(status__in=['confirmed', 'pending']).count()

    @property
    def is_available(self):
        return self.status == 'available' and self.booked_count < self.max_candidates


class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('in_progress', 'In Progress'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='applied')
    cover_note = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-applied_at']
        unique_together = ['user', 'company']

    def __str__(self):
        return f"{self.user.username} → {self.company.name} ({self.status})"

    @property
    def status_color(self):
        return {
            'applied': '#00d4ff',
            'shortlisted': '#7b68ee',
            'interview_scheduled': '#ffd700',
            'in_progress': '#ff8c00',
            'selected': '#00ff88',
            'rejected': '#ff4757',
            'withdrawn': '#8899aa',
        }.get(self.status, '#8899aa')

    @property
    def status_icon(self):
        return {
            'applied': 'fas fa-paper-plane',
            'shortlisted': 'fas fa-star',
            'interview_scheduled': 'fas fa-calendar-check',
            'in_progress': 'fas fa-spinner',
            'selected': 'fas fa-trophy',
            'rejected': 'fas fa-times-circle',
            'withdrawn': 'fas fa-undo',
        }.get(self.status, 'fas fa-circle')


class InterviewBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='bookings')
    slot = models.ForeignKey(InterviewSlot, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    confirmation_code = models.CharField(max_length=20, blank=True)
    booked_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-booked_at']

    def __str__(self):
        return f"{self.application.user.username} - {self.slot}"

    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            import random, string
            self.confirmation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        super().save(*args, **kwargs)
