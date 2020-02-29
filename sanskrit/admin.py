from django.contrib import admin
from .models import SanskritLessons,SanskritQuestions,SanskritAnswers,UserProfile,Audio

admin.site.register(SanskritLessons)
admin.site.register(SanskritQuestions)
admin.site.register(SanskritAnswers)
admin.site.register(UserProfile)
admin.site.register(Audio)