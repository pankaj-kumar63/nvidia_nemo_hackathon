from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("home/", views.getHome, name="home"),
    path("questions/", views.getQuestions, name="questions"),
    path('save-answers/', views.save_answers, name='save_answers'),
    path('save-student/', views.save_student, name='save_student'),
    path('login/', views.get_students, name='get_students'),
    path('user/', views.user_profile, name = 'user_profile'),
    path('dashboard/', views.user_dashboard, name = 'user_dashboard'),
    path('llm-chat/', views.getBotResponse, name = 'llm-response')
]