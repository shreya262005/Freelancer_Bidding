from django.db import models
from freelancer_app3.models import User
from freelancer_app3.models import FreeLancer

    
# imp
class ProjectNew(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='project_user')
    freelancer = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='assigned_freelancer')
    name = models.CharField(max_length=255)
    project_image = models.ImageField(upload_to='project_imag')
    description = models.TextField(null=True,blank=True)
    budget = models.CharField(max_length=255)
    deadline = models.DateTimeField()
    category = models.CharField(max_length=255)
    status = models.CharField(max_length=255,null=True,blank=True,default='Pending')
    is_assigned = models.BooleanField(default=False)
    payment_mode = models.CharField(max_length=255,null=True,blank=True)
    is_paid = models.BooleanField(default=False)
    
class ProjectResponse(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(ProjectNew,on_delete=models.CASCADE,related_name='project_response')
    freelancer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='project_freelancer')
    budget = models.IntegerField()
    deadline = models.DateTimeField()
    status = models.CharField(max_length=255,null=True,blank=True,default='Pending')
    description = models.TextField(null=True,blank=True)
 
class Contact_us(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.CharField(max_length=255)

class Feedback(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    user_type = models.CharField(max_length=20)
    rating = models.IntegerField()
    comments = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_type} - {self.rating}⭐"
        
    