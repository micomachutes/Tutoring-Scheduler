from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Student views
    path('student/create-session/', views.student_create_session, name='student_create_session'),
    
    # Tutor views
    path('tutor/requests/', views.tutor_requests_view, name='tutor_requests'),
    path('tutor/accept/<int:session_id>/', views.tutor_accept_session, name='tutor_accept_session'),
    path('tutor/decline/<int:session_id>/', views.tutor_decline_session, name='tutor_decline_session'),
    
    # Session log (both student and tutor)
    path('sessions/', views.session_log_view, name='session_log'),
    path('sessions/complete/<int:session_id>/', views.complete_session, name='complete_session'),
    path('sessions/delete/<int:session_id>/', views.delete_session, name='delete_session'),
    
    # Root redirect
    path('', views.dashboard_view, name='home'),
]

