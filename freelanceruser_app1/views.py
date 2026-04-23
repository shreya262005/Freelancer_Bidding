from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login,logout,authenticate
from .models import*
from freelancer_app3 import models
from freelanceradmin_app2.views import index
from freelancer_app3.views import index_free
from django.contrib import messages
from freelanceruser_app1 import forms
from freelanceruser_app1.models import ProjectNew
from django.views.decorators.csrf import csrf_exempt
import json
from freelancer_app3.models import FreeLancer 
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from freelancer_app3.models import Project_daily_updates
from freelancer_app3.models import Client
from freelanceruser_app1.models import Feedback


# Create your views here.

def demo(request):
   return HttpResponse("hyy")

def userside_index(request):
    freelancers = FreeLancer.objects.select_related('user').all()
    return render(request, 'userapp/userside_index.html', {'freelancers': freelancers})   

def blog_detail(request):
    return render(request,'userapp/blog-details.html')

def service_details(request):
    return render(request,'userapp/service-details.html')

def starter_page(request):
    return render(request,'userapp/starter-page.html')

def submit_feedback(request):
    if request.method == 'POST':
        Feedback.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            user_type=request.POST.get('user_type'),
            rating=request.POST.get('rating'),
            comments=request.POST.get('comments'),
        )
        return redirect(userside_index)
    return render(request,'userapp/Feedback.html')


@login_required
def client_profile(request):
    # Fetch the client profile based on the logged-in user
    client = Client.objects.get(user=request.user)
    return render(request, 'userapp/client_profile.html', {'client': client})


def update_client_profile(request):
    # Ensure the user is logged in
    user = request.user
    try:
        client = Client.objects.get(user=user)  # Get client profile for the user
    except Client.DoesNotExist:
        client = None

    if request.method == 'POST':
        # Fetch updated data from the form or request
        image = request.FILES.get('image')
        company_name = request.POST.get('company_name')
        owner_name = request.POST.get('owner_name')
        company_phone = request.POST.get('company_phone')
        location = request.POST.get('location')

        # Update user image
        if image:
            user.image = image

        # Update client profile or create if it doesn't exist
        if client:
            client.company_name = company_name
            client.owner_name = owner_name
            client.company_phone = company_phone
            client.location = location
            client.save()
        else:
            Client.objects.create(
                user=user,
                company_name=company_name,
                owner_name=owner_name,
                company_phone=company_phone,
                location=location
            )

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect(client_profile)  # Redirect to the profile page after update

    return render(request, 'userapp/client_profile_update.html', {'client': client})

# -------------------------change-Password-----------------------------------------------------

@login_required
def user_change_password(request):
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
            return redirect(login_page)  # Make sure 'index_free' exists in urls.py

    return render(request, 'userapp/user_change_password.html')

def contactus(request):
    if request.method == 'POST':
        form = forms.Contactus_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(userside_index)
        else:
            print(form.errors)
    return render(request,'userapp/contactus.html')

def contactus_list(request):
    contact = Contact_us.objects.all()
    return render(request,'adminapp/contactus_list.html',{'contact':contact})  

def view_details(request,id):
    data = ProjectNew.objects.get(id=id)    
    project_response = ProjectResponse.objects.filter(project=data)
    update = Project_daily_updates.objects.filter(project=data)
    
    if request.method == "POST":
        payment = request.POST.get('payment')
        data.payment_mode = payment
        data.is_paid = True
        data.save()
        return redirect(view_details,id)
    
    context = {
        'data':data,
        'project_response':project_response,
        'update':update, 
    }
    return render(request,'userapp/view_details.html',context)

def client_add_project(request):
    if request.method == "POST":
        form = forms.ProjectNewForm(request.POST,request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect(client_list_project)
        else:
            print(form.errors)
            
    return render(request,'userapp/client-addproject.html')
  
def client_list_project(request):
    data = ProjectNew.objects.filter(user=request.user)
    context = {'data':data}
    return render(request,'userapp/client_list_project.html',context)


# -------------------------------------forgot password-------------------------------------------------------------------

def forgot_password_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            request.session['reset_username'] = username  # Save to session
            return redirect('reset_password')
        except User.DoesNotExist:
            messages.error(request, 'Username not found.')
    return render(request, 'userapp/forgot_password.html')

# -------------------------------------reset password----------------------------------------------------------------------

def reset_password_view(request):
    username = request.session.get('reset_username')
    if not username:
        return redirect('forgot_password')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Confirm Passwords do not match.')
        else:
            user = User.objects.get(username=username)
            user.password = make_password(new_password)
            user.save()
            messages.success(request, 'Password reset successful.')
            return redirect(login_page)  # Adjust to your login page URL

    return render(request, 'userapp/reset_password.html')

# ---------------------------------------------login--------------------------------------------------------------------

# index --> admin, index_free --> freelancer, userside_index -->userside 

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Validate input fields
        if not username or not password:
            messages.error(request, "Please provide both username and password.")
            return render(request, 'userapp/login.html')
            
        user = authenticate(username=username, password=password)

        if user:
            # Log user activity
            login(request, user)
            
            # Redirect based on user type
            if user.is_superuser:
                return redirect(index)  # Admin index
            elif user.is_staff:
                if not user.is_active:
                    messages.warning(request, "Your account is pending approval. Please wait for admin verification.")
                    logout(request)
                    return render(request, 'userapp/login.html')
                return redirect(index_free)  # Staff index (company)
            else:
                return redirect(userside_index)  # User-side index
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'userapp/login.html')
        
    return render(request, 'userapp/login.html')


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        contact = request.POST.get('contact')
        image = request.FILES.get('image')
        gender = request.POST.get('gender')
        company_name = request.POST.get('company_name')
        # address = request.POST.get('address')
        owner_name = request.POST.get('owner_name')
        company_phone = request.POST.get('company_phone')
        location = request.POST.get('location')
        
        # Validate required fields
        if not all([username, password, password1, contact, gender, company_name, 
                    owner_name, company_phone, location]):
            messages.error(request, 'All fields are required. Please fill in all the details.')
            return redirect('user_register')
            
        # Validate image upload
        if not image:
            messages.error(request, 'Please upload a profile image.')
            return redirect('user_register')
        
        if password == password1:
            try:
                models.User.objects.get(username=username)
                messages.error(request, 'Username already exists. Please choose a different username.')
                return redirect('user_register')
            except:
                try:
                    user = models.User.objects.create_user(username=username,
                                                    password=password,
                                                    contact=contact,
                                                    gender=gender,
                                                    image=image,
                                                    )
                    client = models.Client.objects.create(user=user,
                                                        company_name=company_name,
                                                        # address=address,
                                                        owner_name=owner_name,
                                                        company_phone=company_phone,
                                                        location=location,
                                                        )
                    messages.success(request, 'Account created successfully! Please login.')
                    return redirect(login_page)
                except Exception as e:
                    messages.error(request, f'Error creating account: {str(e)}')
                    return redirect('user_register')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('user_register')
    return render(request,'userapp/user-register.html')

def admin_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')
        if password == password1:
            try:
                models.User.objects.get(username=username)
                messages.error(request, 'Username already exists. Please try again.')
                return redirect(admin_register)
            except:
                models.User.objects.create_user(username=username,
                                                password=password,
                                                contact=contact,
                                                gender=gender,
                                                is_superuser=True)
                messages.success(request, 'Admin account created successfully! Please login.')
                return redirect(login_page)
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect(admin_register)

    return render(request, 'adminapp/admin-register.html')

def freelancer_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')
        image = request.FILES.get('image')
        addhar_image = request.FILES.get('addhar_image')
        linkedin_url = request.POST.get('linkedin_url')
        category =request.POST.get('category')

        if password == password1:
            try:
                models.User.objects.get(username=username)
                messages.error(request, 'Username already exists. Please try again.')
                return redirect(freelancer_register)
            except:
                user = models.User.objects.create_user(username=username,
                                                password=password,
                                                contact=contact,
                                                gender=gender,
                                                image=image,
                                                is_staff=True,
                                                is_active=False)
                freelancer = models.FreeLancer.objects.create(user=user,
                                                              addhar_image=addhar_image,
                                                              linkedin_url=linkedin_url,
                                                              category=category
                                                              )
                print(user)
                print(freelancer)
                messages.success(request, 'Freelancer account created successfully! Please login.')
                return redirect(login_page)
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect(freelancer_register)

    return render(request, 'freelancerapp/freelancer-register.html')

# 1 function 3 url "logout"

def logout_view(request):
    logout(request)
    return redirect(login_page)


def approve_freelancer_project(request,id):
    response = ProjectResponse.objects.get(id=id)
    response.status = "Approved"
    response.save()
    response.project.status = "Booked"
    response.project.is_assigned = True
    response.project.freelancer = response.freelancer
    response.project.save()
    return redirect(view_details,response.project.id)

def reject_freelancer_project(request,id):
    response = ProjectResponse.objects.get(id=id)
    response.status = "Rejected"
    response.save()
    return redirect(view_details,response.project.id)

@csrf_exempt
def validate_username(request):
    """
    AJAX view to check if a username is available
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username', '')
        
        if not username:
            return JsonResponse({'valid': False, 'message': 'Username is required'})
            
        if len(username) < 3:
            return JsonResponse({'valid': False, 'message': 'Username must be at least 3 characters'})
        
        try:
            models.User.objects.get(username=username)
            return JsonResponse({'valid': False, 'message': 'Username already exists'})
        except:
            return JsonResponse({'valid': True, 'message': 'Username is available'})
    
    return JsonResponse({'valid': False, 'message': 'Invalid request'})

# -----------------------------------------------chat-----------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from freelancer_app3.models import ChatMessage
from freelancer_app3.forms import ChatMessageForm
from django.utils import timezone
from django.db.models import Q, Count
from freelancer_app3.models import User

@login_required
def chat_view(request, user_id=None):
    current_user = request.user
    # Filter freelancers (or clients if you're logged in as freelancer)
    freelancers = User.objects.filter(is_superuser=False)

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

        # Handle message sending
        if request.method == 'POST':
            form = ChatMessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.sender = current_user
                message.receiver = selected_user
                message.save()
                return redirect('chat_view', user_id=user_id)
        else:
            form = ChatMessageForm()
    else:
        form = ChatMessageForm()

    # Unread message count for each freelancer
    for freelancer in freelancers:
        unread = ChatMessage.objects.filter(
            sender=freelancer,
            receiver=current_user,
            is_read=False
        ).count()
        unread_messages[freelancer.id] = unread

    return render(request, 'userapp/chat.html', {
        'freelancers': freelancers,
        'selected_user': selected_user,
        'chats': chats,
        'form': form,
        'today': timezone.now().date(),
        'unread_messages': unread_messages,
    })



