from django.contrib import admin
from .models import SanskritLessons,SanskritQuestions,SanskritAnswers,UserProgress,Audio

admin.site.register(SanskritLessons)
admin.site.register(SanskritQuestions)
admin.site.register(SanskritAnswers)
admin.site.register(UserProgress)
admin.site.register(Audio)