from django import forms
from freelancer_app3 import models

 
class Project_daily_updates_form(forms.ModelForm):
    class Meta:
        model =models.Project_daily_updates
        fields = '__all__'  
                     
class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = models.ChatMessage
        fields = ['msg']
        widgets = {
            'msg': forms.Textarea(attrs={
                'class': 'message-input',
                'placeholder': 'Type your message...',
                'rows': 1
            })
        }