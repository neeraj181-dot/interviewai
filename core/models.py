from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    skills = models.TextField(blank=True, help_text='Comma-separated skills')
    experience_years = models.IntegerField(default=0)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    total_interviews = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    xp_points = models.IntegerField(default=0)
    streak_days = models.IntegerField(default=0)
    last_interview_date = models.DateField(null=True, blank=True)
    theme_accent = models.CharField(max_length=20, default='#00d4ff')
    readiness_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    @property
    def average_score(self):
        if self.total_interviews == 0:
            return 0
        return round(self.total_score / self.total_interviews, 1)

    @property
    def level_info(self):
        xp = self.xp_points
        levels = [
            (5000, None,  'Legend',       6, '#ff6b9d'),
            (2000, 5000,  'Expert',       5, '#ffd700'),
            (800,  2000,  'Advanced',     4, '#00ff88'),
            (300,  800,   'Intermediate', 3, '#00d4ff'),
            (100,  300,   'Apprentice',   2, '#7b68ee'),
            (0,    100,   'Beginner',     1, '#8899aa'),
        ]
        for (min_xp, next_xp, name, rank, color) in levels:
            if xp >= min_xp:
                if next_xp:
                    progress = min(100, round((xp - min_xp) / (next_xp - min_xp) * 100))
                else:
                    progress = 100
                return {'name': name, 'rank': rank, 'color': color,
                        'next': next_xp, 'progress': progress, 'min': min_xp}
        return {'name': 'Beginner', 'rank': 1, 'color': '#8899aa',
                'next': 100, 'progress': 0, 'min': 0}

    @property
    def level(self):
        return self.level_info['name']

    @property
    def badges(self):
        earned = []
        if self.total_interviews >= 1:
            earned.append({'name': 'First Step',   'icon': 'fas fa-shoe-prints', 'color': '#00d4ff'})
        if self.total_interviews >= 5:
            earned.append({'name': 'Consistent',   'icon': 'fas fa-fire',        'color': '#ff8c00'})
        if self.total_interviews >= 10:
            earned.append({'name': 'Dedicated',    'icon': 'fas fa-medal',       'color': '#ffd700'})
        if self.total_interviews >= 25:
            earned.append({'name': 'Veteran',      'icon': 'fas fa-user-shield', 'color': '#7b68ee'})
        if self.average_score >= 70:
            earned.append({'name': 'High Scorer',  'icon': 'fas fa-star',        'color': '#ffd700'})
        if self.average_score >= 90:
            earned.append({'name': 'Ace',          'icon': 'fas fa-crown',       'color': '#ff6b9d'})
        if self.streak_days >= 3:
            earned.append({'name': '3-Day Streak', 'icon': 'fas fa-bolt',        'color': '#00ff88'})
        if self.streak_days >= 7:
            earned.append({'name': 'Week Warrior', 'icon': 'fas fa-shield-alt',  'color': '#7b68ee'})
        if self.xp_points >= 1000:
            earned.append({'name': 'XP Hunter',    'icon': 'fas fa-gem',         'color': '#00d4ff'})
        return earned

    def compute_readiness(self):
        """0-100 score based on activity."""
        score = 0
        score += min(30, self.total_interviews * 3)
        score += min(30, int(self.average_score * 0.3))
        score += min(20, self.streak_days * 2)
        score += min(10, len(self.skills_list))
        score += 10 if self.resume else 0
        self.readiness_score = min(100, score)
        self.save(update_fields=['readiness_score'])
        return self.readiness_score
