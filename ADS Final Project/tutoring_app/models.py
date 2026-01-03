from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


class User(AbstractUser):
    """Extended user model with role"""
    id = models.AutoField(primary_key=True, db_column='user_id')
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=10,
        choices=[('student', 'Student'), ('tutor', 'Tutor'), ('admin', 'Admin')],
        default='student'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        return f"{self.email} ({self.role})"


class Student(models.Model):
    """Student profile model"""
    student_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id')
    full_name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'students'
    
    def __str__(self):
        return self.full_name


class Tutor(models.Model):
    """Tutor profile model"""
    tutor_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id')
    full_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = 'tutors'
        indexes = [
            models.Index(fields=['specialization']),
        ]
    
    def __str__(self):
        return self.full_name


class Subject(models.Model):
    """Subject model"""
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        db_table = 'subjects'
        indexes = [
            models.Index(fields=['subject_name']),
        ]
    
    def __str__(self):
        return self.subject_name


class Session(models.Model):
    """Tutoring session model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
    ]
    
    session_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='student_id')
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, db_column='tutor_id')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, db_column='subject_id')
    session_date = models.DateField()
    session_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sessions'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['session_date']),
            models.Index(fields=['student', 'status']),
            models.Index(fields=['tutor', 'status']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.subject.subject_name} - {self.session_date}"

