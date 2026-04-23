from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
    
    path('demo/',views.demo,name='demo'),
    path('index/',views.index,name="index"),
    path('users_profile/',views.users_profile,name='users_profile'),
    path('pages_contact/',views.pages_contact,name='pages_contact'),
    path('admin_change_password/',views.admin_change_password,name='admin_change_password'),
    
                
    path('freelancer_requests/',views.freelancer_requests,name="freelancer_requests"),
    path('approve_freelancer/<int:id>/',views.approve_freelancer,name="approve_freelancer"),
    path('reject_freelancer/<int:id>/',views.reject_freelancer,name="reject_freelancer"),
    
    path('user_requests/',views.user_requests,name="user_requests"),
    path('user_requests_deleteview/<int:id>/',views.user_requests_deleteview,name="user_requests_deleteview"),
    
    path('feedback_list/', views.feedback_list, name='feedback_list'),


    
]