from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
#from accounts.models import Profile

class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'email',
        )

        # help_texts = {
        #     'username': None,
        #     'password': None,
        # }

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    def save(self,commit=True):
        user = super(RegistrationForm,self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']


        if commit:
            user.save()

            return user

#class ProfileForm(forms.ModelForm):

    # class Meta:
    #     model = Profile
    #     fields = (
    #         'email',            

    #     )

    # def save(self,commit=True):
    #     profile = super(ProfileForm,self).save(commit=False)
    #     profile.description = self.cleaned_data['email']        
    #     id = User.objects.latest('date_joined')
    #     profile.user = id


    #     if commit:
    #         profile.save()

    #         return profile
    #pass