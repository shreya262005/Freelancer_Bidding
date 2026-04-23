from django.db import models
from django.contrib.auth.models import AbstractUser

# from freelanceruser_app1 import models



# Create your models here.

class User(AbstractUser):
    contact = models.IntegerField(null=True,blank=True)
    image = models.ImageField(upload_to='Img',null=True,blank=True)
    gender = models.CharField(max_length=255,null=True,blank=True)
    
    def __str__(self):  # Fixed the __str__ method
        return f"{self.username}"

class Client(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_client')
    company_name = models.CharField(max_length=255,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    owner_name = models.CharField(max_length=255,null=True,blank=True)
    company_phone = models.IntegerField(null=True,blank=True)
    location = models.CharField(max_length=255,null=True,blank=True)
    
    
class FreeLancer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_freelancer')
    addhar_image = models.ImageField(upload_to='freelancer_aadhar')
    linkedin_url = models.URLField()
    category = models.CharField(max_length=255,null=True,blank=True)

    
class Project_daily_updates(models.Model):
    project = models.ForeignKey('freelanceruser_app1.ProjectNew', on_delete=models.CASCADE, related_name='daily_updates')
    freelancer = models.ForeignKey(FreeLancer, on_delete=models.CASCADE, related_name='updates')
    date = models.DateField(null=True, blank=True)
    hours = models.IntegerField(null=True, blank=True)
    task_details = models.TextField(null=True, blank=True)  # Changed to TextField for longer inputs
    status = models.CharField(max_length=255, null=True, blank=True)
    

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    msg = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.msg[:20]}"

            