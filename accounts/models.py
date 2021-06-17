from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)    
    profile_pic = models.ImageField(upload_to='pics/',default='pics/Default-Profile-Pic.png')
    # description = models.TextField(max_length=500, blank=True)
    # location = models.CharField(max_length=30, default = '')
    # birth_date = models.DateField(null=True, blank=True)
    # phone_number = models.IntegerField(default = 0 )

    def __str__(self):
            return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender= User)
