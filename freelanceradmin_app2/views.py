from django.shortcuts import render,redirect
from django.http import HttpResponse
from freelanceradmin_app2 import forms
from .models import*
from freelancer_app3 import models
from django.contrib import messages
# --
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from freelanceruser_app1.models import Feedback

# Create your views here.
def demo(request):
    return HttpResponse('heloowww hyeeeeeee')

def index(request):
    user = models.User.objects.all().count()
    freelancer= models.FreeLancer.objects.all().count()
    client = models.Client.objects.all().count()
    
    print(user,freelancer,client)
    context = {
        'user':user,
        'freelancer':freelancer,
        'client':client
    }
    return render(request, "adminapp/index.html",context)

def feedback_list(request):  
    feedbacks = Feedback.objects.order_by('-submitted_at')
    return render(request, 'adminapp/feedback_list.html', {'feedbacks': feedbacks})

@login_required
def admin_change_password(request):
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
            return redirect(index)  # Make sure 'index_free' exists in urls.py

    return render(request, 'adminapp/admin_change_password.html')

from django.shortcuts import render, redirect
from django.contrib import messages

def users_profile(request):
    user = request.user  # Get the logged-in user

    if request.method == "POST":
        username = request.POST.get("username")
        contact = request.POST.get("contact")
        gender = request.POST.get("gender")
        image = request.FILES.get("image")

        if username:
            user.username = username
        if contact:
            user.contact = contact
        if gender:
            user.gender = gender
        if image:
            user.image = image

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('users_profile')  # Use the name of the URL pattern, not the view function

    return render(request, "adminapp/users-profile.html", {"user": user})


def pages_contact(request):
    return render(request,"adminapp/pages-contact.html")
         
def freelancer_requests(request):
    users = models.User.objects.filter(is_staff=True,is_superuser= False)
    context = {
        'users':users
    }
    return render(request,'adminapp/freelancer_requests.html',context)

def approve_freelancer(request,id):
    data = models.User.objects.get(id=id)
    data.is_active = True
    data.save()
    return redirect(freelancer_requests)

def reject_freelancer(request,id):
    data = models.User.objects.get(id=id)
    data.is_active = False
    data.save()
    return redirect(freelancer_requests)

# -------------------manage client----------------------

from freelancer_app3.models import Client
from django.shortcuts import render, redirect, get_object_or_404
def user_requests(request):
    # Fetch clients that are staff but not superusers
    Client = models.Client.objects.all()
    context = {
        'Client': Client
    }
    return render(request, 'adminapp/manage_user.html', context)

def user_requests_deleteview(request, id):
    client = get_object_or_404(Client, id=id)
    client.delete()
    return redirect('user_requests')  