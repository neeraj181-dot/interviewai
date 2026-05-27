from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Interview System
    path('interview/<str:category>/', views.interview_start, name='interview_start'),
    path('interview/<str:category>/question/<int:question_id>/', views.interview_question, name='interview_question'),
    path('interview/<str:category>/submit/<int:question_id>/', views.submit_answer, name='submit_answer'),
    path('interview/result/<int:history_id>/', views.interview_result, name='interview_result'),
    
    # History and Profile
    path('history/', views.interview_history, name='interview_history'),
    path('profile/', views.profile, name='profile'),
]
