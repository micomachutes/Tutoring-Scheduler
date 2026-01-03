from django.contrib import admin
from .models import User, Student, Tutor, Subject, Session


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'role', 'is_staff', 'is_superuser', 'created_at')
    list_filter = ('role', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_per_page = 50
    ordering = ('-created_at',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'full_name', 'user', 'user_email')
    search_fields = ('full_name', 'user__email', 'user__username')
    list_per_page = 50
    ordering = ('student_id',)
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('tutor_id', 'full_name', 'specialization', 'user', 'user_email')
    search_fields = ('full_name', 'specialization', 'user__email', 'user__username')
    list_filter = ('specialization',)
    list_per_page = 50
    ordering = ('tutor_id',)
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'subject_id')
    search_fields = ('subject_name',)


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'student', 'tutor', 'subject', 'session_date', 'session_time', 'status', 'created_at')
    list_filter = ('status', 'session_date', 'subject', 'created_at')
    search_fields = ('student__full_name', 'tutor__full_name', 'subject__subject_name', 'notes')
    date_hierarchy = 'session_date'
    list_per_page = 50
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

