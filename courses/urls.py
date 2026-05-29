from django.urls import path
from . import views

urlpatterns = [
    path('interview-prep/', views.interview_prep, name='interview_prep'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/start/<slug:slug>/', views.start_course, name='start_course'),
    path('courses/<int:session_id>/question/<int:question_index>/', views.course_question, name='course_question'),
    path('courses/<int:session_id>/finish/', views.finish_course, name='finish_course'),
    path('courses/<int:session_id>/result/', views.course_result, name='course_result'),
]
