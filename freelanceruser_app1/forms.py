from django import forms
from freelanceruser_app1 import models


class ProjectNewForm(forms.ModelForm):
    class Meta:
        model = models.ProjectNew
        fields = "__all__"
        exclude = ['user']
        
class Contactus_Form(forms.ModelForm):
    class Meta:
        model = models.Contact_us
        fields = "__all__"

