from django.shortcuts import render,redirect
from django.urls import reverse
from accounts.forms import RegistrationForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

def register(request):
   
    if request.method == 'POST':
        userform = RegistrationForm(request.POST)
        if userform.is_valid()  :
            form1 = userform.save()            
            return redirect(reverse('accounts:login'))
    else:
        userform = RegistrationForm()
    args = {'form':userform} 

    return render(request,'accounts/reg_form.html',args)