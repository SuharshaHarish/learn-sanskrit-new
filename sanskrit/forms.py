from django import forms 
from accounts.models import Profile
  
class ProfileForm(forms.ModelForm): 
  
    class Meta: 
        model = Profile 
        fields = ['profile_pic']
        labels = {
            'profile_pic':None
        } 