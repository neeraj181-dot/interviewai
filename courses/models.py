from django.db import models
from django.contrib.auth.models import User


class CourseTrack(models.Model):
    TRACK_CHOICES = [
        ('programming', 'Programming'),
        ('ai', 'AI & Future Tech'),
        ('placement', 'Placement Prep'),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    track = models.CharField(max_length=20, choices=TRACK_CHOICES, default='programming')
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, default='fas fa-code')
    color = models.CharField(max_length=20, default='#00d4ff')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['track', 'order', 'name']

    def __str__(self):
        return f"[{self.track}] {self.name}"

    @property
    def question_count(self):
        return self.questions.count()

    @property
    def beginner_count(self):
        return self.questions.filter(difficulty='easy').count()

    @property
    def intermediate_count(self):
        return self.questions.filter(difficulty='medium').count()

    @property
    def advanced_count(self):
        return self.questions.filter(difficulty='hard').count()


class CourseQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Beginner'),
        ('medium', 'Intermediate'),
        ('hard', 'Advanced'),
    ]
    course = models.ForeignKey(CourseTrack, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    correct_answer = models.TextField(help_text='Comma-separated keywords')
    explanation = models.TextField(blank=True)
    points = models.IntegerField(default=10)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['difficulty', 'order', 'id']

    def __str__(self):
        return f"[{self.course.name}/{self.difficulty}] {self.text[:60]}"


class CourseSession(models.Model):
    DIFFICULTY_CHOICES = [
        ('all', 'All Levels'),
        ('easy', 'Beginner'),
        ('medium', 'Intermediate'),
        ('hard', 'Advanced'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_sessions')
    course = models.ForeignKey(CourseTrack, on_delete=models.CASCADE, related_name='sessions')
    difficulty_filter = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='all')
    score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    xp_earned = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"

    @property
    def percentage(self):
        if self.max_score == 0:
            return 0
        return round((self.score / self.max_score) * 100)

    @property
    def grade(self):
        p = self.percentage
        if p >= 90: return ('A+', '#00ff88')
        elif p >= 80: return ('A', '#00d4ff')
        elif p >= 70: return ('B', '#7b68ee')
        elif p >= 60: return ('C', '#ffd700')
        elif p >= 50: return ('D', '#ff8c00')
        else: return ('F', '#ff4757')

    @property
    def feedback(self):
        p = self.percentage
        if p >= 90: return 'Outstanding! You have mastered this topic.'
        elif p >= 80: return 'Excellent work! Strong grasp of the subject.'
        elif p >= 70: return 'Good job! A bit more practice will make you an expert.'
        elif p >= 60: return 'Not bad! Keep studying to improve.'
        elif p >= 50: return 'You passed, but there is room for improvement.'
        else: return 'Keep practicing! Review the material and try again.'

    @property
    def duration_minutes(self):
        if self.completed_at and self.created_at:
            return round((self.completed_at - self.created_at).total_seconds() / 60, 1)
        return 0


class CourseAnswer(models.Model):
    session = models.ForeignKey(CourseSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(CourseQuestion, on_delete=models.CASCADE)
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
