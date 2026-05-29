from django.contrib import admin
from .models import CourseTrack, CourseQuestion, CourseSession, CourseAnswer


@admin.register(CourseTrack)
class CourseTrackAdmin(admin.ModelAdmin):
    list_display = ('name', 'track', 'question_count', 'color', 'is_active', 'order')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('track', 'is_active')


@admin.register(CourseQuestion)
class CourseQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'course', 'difficulty', 'points', 'order')
    list_filter = ('course', 'difficulty')
    list_editable = ('difficulty', 'points', 'order')
    search_fields = ('text',)


@admin.register(CourseSession)
class CourseSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'score', 'max_score', 'is_completed', 'created_at')
    list_filter = ('course', 'is_completed')
    readonly_fields = ('created_at', 'completed_at')


@admin.register(CourseAnswer)
class CourseAnswerAdmin(admin.ModelAdmin):
    list_display = ('session', 'question', 'is_correct', 'points_earned')
