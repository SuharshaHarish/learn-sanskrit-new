from learn_sanskrit.settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER
from django.shortcuts import render,redirect
from django.urls import reverse
from accounts.forms import RegistrationForm
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib import messages
# for email registration
import smtplib

from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings

def register(request):
   
    if request.method == 'POST':
        userform = RegistrationForm(request.POST)
        if userform.is_valid()  :
            
            user = userform.save()
            user.is_active = False
            user.save()       
            # for email registration
            current_site = get_current_site(request)    
            email_subject = 'Activate your account'
            message = render_to_string('accounts/activate.html',
            {
                'user':user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            }
            )
            s=smtplib.SMTP("smtp.gmail.com", 465)
            s.ehlo()
            s.starttls()
            s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],            
            )
            email_message.send()
            messages.add_message(request,messages.SUCCESS,"Please check your email to activate your account.")
            return redirect(reverse('accounts:login'))
    else:
        userform = RegistrationForm()
        print(settings.EMAIL_HOST_PASSWORD)
        print(settings.EMAIL_HOST_USER)
    args = {'form':userform} 

    return render(request,'accounts/reg_form.html',args)

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        print("Called activate")
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            print(user)
        except Exception as identifier:
            print("email auth error")
            user = None

        if user is not None and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
            messages.add_message(request,messages.SUCCESS,"User is activated. Please login with your credentials.")
            return redirect(reverse('accounts:login'))
        return render(request,'accounts/activate_failed.html',status=401)