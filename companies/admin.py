from django.contrib import admin
from .models import Company, InterviewSlot, Application, InterviewBooking


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'hiring_status', 'difficulty', 'open_positions', 'salary_display', 'is_featured')
    list_editable = ('hiring_status', 'is_featured', 'open_positions')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('hiring_status', 'difficulty', 'is_featured')
    search_fields = ('name',)


@admin.register(InterviewSlot)
class InterviewSlotAdmin(admin.ModelAdmin):
    list_display = ('company', 'round_type', 'date', 'time_start', 'status', 'booked_count')
    list_filter = ('company', 'status', 'round_type')
    list_editable = ('status',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'status', 'applied_at')
    list_filter = ('status', 'company')
    list_editable = ('status',)
    search_fields = ('user__username', 'company__name')


@admin.register(InterviewBooking)
class InterviewBookingAdmin(admin.ModelAdmin):
    list_display = ('application', 'slot', 'status', 'confirmation_code', 'booked_at')
    list_filter = ('status',)
    readonly_fields = ('confirmation_code', 'booked_at')
