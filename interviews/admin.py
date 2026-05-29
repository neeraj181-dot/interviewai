from django.contrib import admin
from .models import Category, Question, InterviewSession, UserAnswer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'question_count', 'color')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'category', 'difficulty', 'points', 'order')
    list_filter = ('category', 'difficulty')
    search_fields = ('text',)
    list_editable = ('difficulty', 'points', 'order')


@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'score', 'max_score', 'is_completed', 'created_at')
    list_filter = ('category', 'is_completed')
    readonly_fields = ('created_at', 'completed_at')


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('session', 'question', 'is_correct', 'points_earned')
    list_filter = ('is_correct',)
