from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, default='fas fa-code')
    color = models.CharField(max_length=20, default='#00d4ff')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

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


class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Beginner'),
        ('medium', 'Intermediate'),
        ('hard', 'Advanced'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    correct_answer = models.TextField()
    explanation = models.TextField(blank=True)
    points = models.IntegerField(default=10)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['difficulty', 'order', 'id']

    def __str__(self):
        return f"[{self.category.name}/{self.difficulty}] {self.text[:60]}"


class InterviewSession(models.Model):
    DIFFICULTY_CHOICES = [
        ('all', 'All Levels'),
        ('easy', 'Beginner'),
        ('medium', 'Intermediate'),
        ('hard', 'Advanced'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sessions')
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
        return f"{self.user.username} - {self.category.name} ({self.created_at.date()})"

    @property
    def percentage(self):
        if self.max_score == 0:
            return 0
        return round((self.score / self.max_score) * 100)

    @property
    def grade(self):
        pct = self.percentage
        if pct >= 90:
            return ('A+', '#00ff88')
        elif pct >= 80:
            return ('A', '#00d4ff')
        elif pct >= 70:
            return ('B', '#7b68ee')
        elif pct >= 60:
            return ('C', '#ffd700')
        elif pct >= 50:
            return ('D', '#ff8c00')
        else:
            return ('F', '#ff4757')

    @property
    def feedback(self):
        pct = self.percentage
        if pct >= 90:
            return 'Outstanding! You have mastered this topic.'
        elif pct >= 80:
            return 'Excellent work! Strong grasp of the subject.'
        elif pct >= 70:
            return 'Good job! A bit more practice will make you an expert.'
        elif pct >= 60:
            return 'Not bad! Keep studying to improve.'
        elif pct >= 50:
            return 'You passed, but there is room for improvement.'
        else:
            return 'Keep practicing! Review the material and try again.'

    @property
    def duration_minutes(self):
        if self.completed_at and self.created_at:
            delta = self.completed_at - self.created_at
            return round(delta.total_seconds() / 60, 1)
        return 0


class UserAnswer(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.session.user.username} - Q{self.question.id}"
