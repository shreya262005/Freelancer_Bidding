from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
   path('user_register/',views.user_register,name='user_register'),
   path('admin_register/',views.admin_register,name='admin_register'),
   path('freelancer_register/',views.freelancer_register,name='freelancer_register'),
   path('login_page/',views.login_page,name='login_page'),
   path('logout_view/',views.logout_view,name='logout_view'),
   path('validate-username/',views.validate_username, name='validate_username'),
   path('forgot_password_view/', views.forgot_password_view, name='forgot_password_view'),
   path('reset-password/', views.reset_password_view, name='reset_password'),
   path('user_change_password/', views.user_change_password, name='user_change_password'),
   
   
   path('demo/',views.demo,name='demo'),
   path('',views.userside_index,name='userside_index'),
   path('blog_detail/',views.blog_detail,name='blog_detail'),
   path('service_details/',views.service_details,name='service_details'),
   path('starter_page/',views.starter_page,name='starter_page'),
   path('client_add_project/',views.client_add_project,name='client_add_project'),
   path('client_list_project/',views.client_list_project,name='client_list_project'),
   path('contactus/',views.contactus,name='contactus'),
   path('contactus_list/',views.contactus_list,name='contactus_list'),
   path('view_details/<int:id>/',views.view_details,name='view_details'),
   
   path('approve_freelancer_project/<int:id>/',views.approve_freelancer_project,name='approve_freelancer_project'),  
   path('reject_freelancer_project/<int:id>/',views.reject_freelancer_project,name='reject_freelancer_project'),
   
   path('client_profile/', views.client_profile, name='client_profile'),
   path('update_client_profile/', views.update_client_profile, name='update_client_profile'),
   
   path('chat_view/<int:user_id>/', views.chat_view, name='chat_view'),

   path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
]