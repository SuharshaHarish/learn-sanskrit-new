from django.conf import settings
from django.db import models
from django.utils import timezone
from accounts.models import Profile



class Forum(models.Model):
    author = models.ForeignKey (settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    forum_profile = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class ForumComment(models.Model):
    author = models.ForeignKey (settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    forum_profile = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    forum_key = models.ForeignKey(Forum,on_delete=models.CASCADE)
    comment = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.author.username
