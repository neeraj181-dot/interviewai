from django.contrib import admin
from .models import Question, Answer, InterviewHistory, UserProfile

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'question_text', 'difficulty']
    list_filter = ['category', 'difficulty']
    search_fields = ['question_text']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'user', 'is_correct', 'created_at']
    list_filter = ['is_correct', 'created_at']
    search_fields = ['user__username']

@admin.register(InterviewHistory)
class InterviewHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'category', 'score', 'total_questions', 'completed_at']
    list_filter = ['category', 'completed_at']
    search_fields = ['user__username']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_score', 'interviews_completed']
    search_fields = ['user__username']
