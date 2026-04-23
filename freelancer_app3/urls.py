from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [

path('index_free/',views.index_free,name="index_free"),
path('available_project_list/',views.available_project_list,name="available_project_list"),
path('applied_project/',views.applied_project,name="applied_project"),
path('freelancer_myproject_list/',views.freelancer_myproject_list,name="freelancer_myproject_list"),
path('apply_now_project/',views.apply_now_project,name="apply_now_project"),
path('users_profile_free/',views.users_profile_free,name="users_profile_free"),
path('daily_updates/',views.daily_updates,name='daily_updates'),
path('change_password/',views.change_password,name='change_password'),
path('edit_user_profile/',views.edit_user_profile,name='edit_user_profile'),
   
path('freelancer_chat_view/<int:user_id>/', views.freelancer_chat_view, name='freelancer_chat_view'),





]