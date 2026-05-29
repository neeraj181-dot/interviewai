from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_list, name='categories'),
    path('interview/start/<slug:slug>/', views.start_interview, name='start_interview'),
    path('interview/<int:session_id>/question/<int:question_index>/', views.interview_question, name='interview_question'),
    path('interview/<int:session_id>/finish/', views.finish_interview, name='finish_interview'),
    path('interview/<int:session_id>/result/', views.interview_result, name='interview_result'),
    path('history/', views.interview_history, name='history'),
]
