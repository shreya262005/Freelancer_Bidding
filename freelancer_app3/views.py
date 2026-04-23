from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from freelanceruser_app1.models import ProjectNew,ProjectResponse
from django.contrib import messages
from freelancer_app3 import forms
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from freelanceruser_app1 import models

# Create your views here.
def demo(request):
    return HttpResponse('hyeeee!!..')

def index_free(request):
    project = models.ProjectNew.objects.all().count()
    print(project)
    return render(request, "freelancerapp/index_free.html",{'project':project})

def daily_updates(request):
    if request.method == 'POST':
        form = forms.Project_daily_updates_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(index_free)  # Redirect back to the same page
        else:
            print(form.errors)
            
    projects = ProjectNew.objects.all()
    freelancers = FreeLancer.objects.all()
    daily_update = Project_daily_updates.objects.all().order_by('-date')  # Add this line

    return render(request, 'freelancerapp/daily_updates.html', {
        'projects': projects,
        'freelancers': freelancers,
        'daily_update': daily_update  # Send it to the template
    })

def available_project_list(request):
    project = ProjectNew.objects.filter(status='Pending') 
    if request.method == "POST":
        project_id = request.POST.get('project')
        project_data = ProjectNew.objects.get(id=project_id)
        deadline = request.POST.get('deadline')
        budget = request.POST.get('budget')
        description = request.POST.get('description')
        response = ProjectResponse.objects.create(project=project_data,
                                                  budget=budget,
                                                  freelancer=request.user,
                                                  deadline=deadline,
                                                  description=description,
                                                  )
        print(response)
        return redirect(available_project_list)
    context = {
        'project':project,
    }
    return render(request, "freelancerapp/available_project_list.html",context)

def apply_now_project(request):
    return render(request, "freelancerapp/apply_now_project.html")

def applied_project(request):
    return render(request, "freelancerapp/applied_project.html")

def users_profile_free(request):
    user = request.user  
    freelancer = FreeLancer.objects.get(user=user)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.contact = request.POST.get('contact')
        user.gender = request.POST.get('gender')

        freelancer.category = request.POST.get('category')
        freelancer.linkedin_url = request.POST.get('linkedin_url')

        # Check and update image if uploaded
        if 'image' in request.FILES:
            user.image = request.FILES['image']

        user.save()
        freelancer.save()

    context = {
        'user': user,
        'freelancer': freelancer,
    }
    return render(request, "freelancerapp/users_profile_free.html", context)

@login_required
def edit_user_profile(request):
    user = request.user
    freelancer = FreeLancer.objects.get(user=user)

    if request.method == 'POST':
        # Get form values
        username = request.POST.get('username')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')
        category = request.POST.get('category')
        linkedin_url = request.POST.get('linkedin_url')
        image = request.FILES.get('image')

        # Update User model fields
        user.username = username
        user.contact = contact
        user.gender = gender
        if image:
            user.image = image
        user.save()

        # Update Freelancer model fields
        freelancer.category = category
        freelancer.linkedin_url = linkedin_url
        freelancer.save()

        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('users_profile_free')  # 👈 change this to your profile page URL name

    context = {
        'user': user,
        'freelancer': freelancer,
    }
    return render(request, 'freelancerapp/users_profile_free.html', context)
        
def freelancer_myproject_list(request):
    project = ProjectNew.objects.filter(freelancer=request.user,is_assigned=True)
    print("project",project)
    context = {'project':project}
    return render(request, "freelancerapp/freelancer_myproject_list.html",context)

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        elif len(new_password) < 6:
            messages.error(request, 'New password must be at least 6 characters long.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Prevent logout
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('index_free')  # Make sure 'index_free' exists in urls.py

    return render(request, 'freelancerapp/change_password.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from freelancer_app3.models import ChatMessage, User
from freelancer_app3.forms import ChatMessageForm

@login_required
def freelancer_chat_view(request, user_id=None):
    current_user = request.user
    freelancers = User.objects.filter(is_superuser=False,is_staff=False)

    selected_user = None
    chats = []
    unread_messages = {}

    if user_id:
        selected_user = get_object_or_404(User, id=user_id)

        chats = ChatMessage.objects.filter(
            Q(sender=current_user, receiver=selected_user) |
            Q(sender=selected_user, receiver=current_user)
        ).order_by('timestamp')

        # Mark unread messages as read
        ChatMessage.objects.filter(
            sender=selected_user,
            receiver=current_user,
            is_read=False
        ).update(is_read=True)

        if request.method == 'POST':
            form = ChatMessageForm(request.POST)
            if form.is_valid():
                msg = form.save(commit=False)
                msg.sender = current_user
                msg.receiver = selected_user
                msg.save()
                return redirect('freelancer_chat_view', user_id=user_id)
        else:
            form = ChatMessageForm()
    else:
        form = ChatMessageForm()

    for freelancer in freelancers:
        unread = ChatMessage.objects.filter(
            sender=freelancer,
            receiver=current_user,
            is_read=False
        ).count()
        unread_messages[freelancer.id] = unread

    return render(request, 'freelancerapp/freelancer_chat.html', {
        'freelancers': freelancers,
        'selected_user': selected_user,
        'chats': chats,
        'form': form,
        'today': timezone.now().date(),
        'unread_messages': unread_messages,
    })
