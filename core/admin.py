from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_interviews', 'average_score', 'level', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
