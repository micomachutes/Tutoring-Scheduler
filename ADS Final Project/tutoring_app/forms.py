from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Session, Subject, Student, Tutor


class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(
        choices=[('student', 'Student'), ('tutor', 'Tutor')],
        widget=forms.RadioSelect
    )
    full_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    specialization = forms.ChoiceField(
        choices=[],
        required=False,
        help_text="Required for tutors",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2', 'role', 'full_name', 'specialization')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
        # Populate specialization dropdown with available subjects
        # Get distinct subject names from database
        subjects = Subject.objects.values_list('subject_name', flat=True).distinct().order_by('subject_name')
        self.fields['specialization'].choices = [('', 'Select a specialization')] + [(name, name) for name in subjects]
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        specialization = cleaned_data.get('specialization')
        
        if role == 'tutor' and not specialization:
            raise forms.ValidationError("Specialization is required for tutors.")
        
        return cleaned_data


class SessionForm(forms.ModelForm):
    """Form for creating/editing sessions"""
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.none(),  # Will be set in __init__
        empty_label="Select a subject",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    session_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    session_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes...'})
    )
    
    class Meta:
        model = Session
        fields = ['subject', 'session_date', 'session_time', 'notes']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get distinct subjects - one Subject per distinct subject_name
        # Use distinct() on subject_name and get the first Subject for each name
        from django.db.models import Min
        distinct_subject_ids = Subject.objects.values('subject_name').annotate(
            min_id=Min('subject_id')
        ).values_list('min_id', flat=True)
        self.fields['subject'].queryset = Subject.objects.filter(
            subject_id__in=distinct_subject_ids
        ).order_by('subject_name')
    
    def clean_session_date(self):
        from django.utils import timezone
        session_date = self.cleaned_data.get('session_date')
        if session_date and session_date < timezone.now().date():
            raise forms.ValidationError("Session date cannot be in the past.")
        return session_date


class SessionFilterForm(forms.Form):
    """Form for filtering sessions"""
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + Session.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.none(),  # Will be set in __init__
        required=False,
        empty_label="All Subjects",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get distinct subjects - one Subject per distinct subject_name
        from django.db.models import Min
        distinct_subject_ids = Subject.objects.values('subject_name').annotate(
            min_id=Min('subject_id')
        ).values_list('min_id', flat=True)
        self.fields['subject'].queryset = Subject.objects.filter(
            subject_id__in=distinct_subject_ids
        ).order_by('subject_name')
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

