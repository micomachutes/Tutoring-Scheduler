from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, Avg, Case, When, IntegerField
from django.db import connection
from django.http import JsonResponse
from django.utils import timezone
from django.utils.safestring import mark_safe
import json
from datetime import datetime, timedelta
from .models import User, Student, Tutor, Subject, Session
from .forms import CustomUserCreationForm, SessionForm, SessionFilterForm


def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            full_name = form.cleaned_data.get('full_name')
            
            # Create student or tutor profile
            if role == 'student':
                Student.objects.create(user=user, full_name=full_name)
            elif role == 'tutor':
                specialization = form.cleaned_data.get('specialization')
                Tutor.objects.create(user=user, full_name=full_name, specialization=specialization)
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Since USERNAME_FIELD is 'email', authenticate using email directly
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.email}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'registration/login.html')


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard_view(request):
    """Dashboard with data visualization"""
    user = request.user
    
    # Get user profile
    if user.role == 'student':
        try:
            profile = Student.objects.get(user=user)
            sessions = Session.objects.filter(student=profile)
        except Student.DoesNotExist:
            messages.error(request, 'Student profile not found.')
            return redirect('logout')
    elif user.role == 'tutor':
        try:
            profile = Tutor.objects.get(user=user)
            sessions = Session.objects.filter(tutor=profile)
        except Tutor.DoesNotExist:
            messages.error(request, 'Tutor profile not found.')
            return redirect('logout')
    else:
        messages.error(request, 'Invalid user role.')
        return redirect('logout')
    
    # Advanced queries for dashboard statistics
    # Using subquery to get session statistics
    total_sessions = sessions.count()
    pending_sessions = sessions.filter(status='pending').count()
    approved_sessions = sessions.filter(status='approved').count()
    declined_sessions = sessions.filter(status='declined').count()
    completed_sessions = sessions.filter(status='completed').count()
    
    # Subquery to get sessions by subject
    sessions_by_subject = sessions.values('subject__subject_name').annotate(
        count=Count('session_id')
    ).order_by('-count')[:5]
    
    # Subquery to get sessions by month
    sessions_by_month = sessions.extra(
        select={'month': "DATE_FORMAT(session_date, '%%Y-%%m')"}
    ).values('month').annotate(
        count=Count('session_id')
    ).order_by('month')[:12]
    
    # Subquery to get average sessions per week
    weeks_ago = timezone.now().date() - timedelta(weeks=4)
    recent_sessions = sessions.filter(session_date__gte=weeks_ago)
    avg_per_week = recent_sessions.count() / 4 if recent_sessions.exists() else 0
    
    # Get upcoming sessions (next 7 days)
    upcoming_date = timezone.now().date() + timedelta(days=7)
    upcoming_sessions = sessions.filter(
        session_date__gte=timezone.now().date(),
        session_date__lte=upcoming_date,
        status__in=['pending', 'approved']
    ).order_by('session_date', 'session_time')[:5]
    
    context = {
        'user': user,
        'profile': profile,
        'total_sessions': total_sessions,
        'pending_sessions': pending_sessions,
        'approved_sessions': approved_sessions,
        'declined_sessions': declined_sessions,
        'completed_sessions': completed_sessions,
        'sessions_by_subject': mark_safe(json.dumps(list(sessions_by_subject))),
        'sessions_by_month': mark_safe(json.dumps(list(sessions_by_month))),
        'avg_per_week': round(avg_per_week, 2),
        'upcoming_sessions': upcoming_sessions,
    }
    
    return render(request, 'dashboard.html', context)


@login_required
def student_create_session(request):
    """Student creates a new session request"""
    if request.user.role != 'student':
        messages.error(request, 'Only students can create session requests.')
        return redirect('dashboard')
    
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.student = student
            
            # Get a tutor for the subject
            # Try to find a tutor with matching specialization, otherwise get any tutor
            subject = form.cleaned_data.get('subject')
            tutor = Tutor.objects.filter(
                specialization__icontains=subject.subject_name
            ).first()
            
            # If no tutor with matching specialization, get a random tutor
            if not tutor:
                tutor = Tutor.objects.order_by('?').first()
            
            if not tutor:
                messages.error(request, 'No tutors available. Please contact administrator.')
                return redirect('student_create_session')
            
            session.tutor = tutor
            session.status = 'pending'
            session.save()
            
            messages.success(request, f'Session request created successfully! Assigned to {tutor.full_name}.')
            return redirect('session_log')
    else:
        form = SessionForm()
    
    return render(request, 'student/create_session.html', {'form': form})


@login_required
def tutor_requests_view(request):
    """Tutor views and manages session requests"""
    if request.user.role != 'tutor':
        messages.error(request, 'Only tutors can view session requests.')
        return redirect('dashboard')
    
    try:
        tutor = Tutor.objects.get(user=request.user)
    except Tutor.DoesNotExist:
        messages.error(request, 'Tutor profile not found.')
        return redirect('dashboard')
    
    # Get pending and approved sessions for this tutor
    pending_sessions = Session.objects.filter(
        tutor=tutor,
        status='pending'
    ).select_related('student', 'subject').order_by('session_date', 'session_time')
    
    approved_sessions = Session.objects.filter(
        tutor=tutor,
        status='approved'
    ).select_related('student', 'subject').order_by('session_date', 'session_time')
    
    context = {
        'tutor': tutor,
        'pending_sessions': pending_sessions,
        'approved_sessions': approved_sessions,
    }
    
    return render(request, 'tutor/requests.html', context)


@login_required
def tutor_accept_session(request, session_id):
    """Tutor accepts a session request"""
    if request.user.role != 'tutor':
        messages.error(request, 'Only tutors can accept sessions.')
        return redirect('dashboard')
    
    try:
        tutor = Tutor.objects.get(user=request.user)
        session = get_object_or_404(Session, session_id=session_id, tutor=tutor)
        
        if session.status != 'pending':
            messages.error(request, 'Only pending sessions can be accepted.')
        else:
            session.status = 'approved'
            session.save()
            messages.success(request, 'Session accepted successfully!')
    except Tutor.DoesNotExist:
        messages.error(request, 'Tutor profile not found.')
    
    return redirect('tutor_requests')


@login_required
def tutor_decline_session(request, session_id):
    """Tutor declines a session request"""
    if request.user.role != 'tutor':
        messages.error(request, 'Only tutors can decline sessions.')
        return redirect('dashboard')
    
    try:
        tutor = Tutor.objects.get(user=request.user)
        session = get_object_or_404(Session, session_id=session_id, tutor=tutor)
        
        if session.status != 'pending':
            messages.error(request, 'Only pending sessions can be declined.')
        else:
            session.status = 'declined'
            session.save()
            messages.success(request, 'Session declined.')
    except Tutor.DoesNotExist:
        messages.error(request, 'Tutor profile not found.')
    
    return redirect('tutor_requests')


@login_required
def session_log_view(request):
    """View all sessions with filtering"""
    user = request.user
    
    # Get user profile and sessions
    if user.role == 'student':
        try:
            profile = Student.objects.get(user=user)
            sessions = Session.objects.filter(student=profile)
        except Student.DoesNotExist:
            messages.error(request, 'Student profile not found.')
            return redirect('dashboard')
    elif user.role == 'tutor':
        try:
            profile = Tutor.objects.get(user=user)
            sessions = Session.objects.filter(tutor=profile)
        except Tutor.DoesNotExist:
            messages.error(request, 'Tutor profile not found.')
            return redirect('dashboard')
    else:
        messages.error(request, 'Invalid user role.')
        return redirect('dashboard')
    
    # Apply filters
    form = SessionFilterForm(request.GET)
    if form.is_valid():
        status = form.cleaned_data.get('status')
        subject = form.cleaned_data.get('subject')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        
        if status:
            sessions = sessions.filter(status=status)
        if subject:
            sessions = sessions.filter(subject=subject)
        if date_from:
            sessions = sessions.filter(session_date__gte=date_from)
        if date_to:
            sessions = sessions.filter(session_date__lte=date_to)
    
    # Order by date
    sessions = sessions.select_related('student', 'tutor', 'subject').order_by('-session_date', '-session_time')
    
    context = {
        'profile': profile,
        'sessions': sessions,
        'form': form,
    }
    
    return render(request, 'session_log.html', context)


@login_required
def complete_session(request, session_id):
    """Mark a session as completed"""
    user = request.user
    
    if user.role == 'student':
        try:
            profile = Student.objects.get(user=user)
            session = get_object_or_404(Session, session_id=session_id, student=profile)
        except Student.DoesNotExist:
            messages.error(request, 'Student profile not found.')
            return redirect('session_log')
    elif user.role == 'tutor':
        try:
            profile = Tutor.objects.get(user=user)
            session = get_object_or_404(Session, session_id=session_id, tutor=profile)
        except Tutor.DoesNotExist:
            messages.error(request, 'Tutor profile not found.')
            return redirect('session_log')
    else:
        messages.error(request, 'Invalid user role.')
        return redirect('session_log')
    
    if session.status == 'approved':
        session.status = 'completed'
        session.save()
        messages.success(request, 'Session marked as completed!')
    else:
        messages.error(request, 'Only approved sessions can be marked as completed.')
    
    return redirect('session_log')


@login_required
def delete_session(request, session_id):
    """Delete a session (only pending or declined)"""
    user = request.user
    
    if user.role == 'student':
        try:
            profile = Student.objects.get(user=user)
            session = get_object_or_404(Session, session_id=session_id, student=profile)
        except Student.DoesNotExist:
            messages.error(request, 'Student profile not found.')
            return redirect('session_log')
    else:
        messages.error(request, 'Only students can delete their session requests.')
        return redirect('session_log')
    
    if session.status in ['pending', 'declined']:
        session.delete()
        messages.success(request, 'Session deleted successfully!')
    else:
        messages.error(request, 'Only pending or declined sessions can be deleted.')
    
    return redirect('session_log')

