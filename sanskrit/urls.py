from django.urls import path
from sanskrit import views

app_name = 'sanskrit'

urlpatterns = [
    
    path('',views.redirect_to_home, name='home'),
    path('home/',views.home,name='home'),
    path('lessons/',views.lessons,name = 'lessons'),
    path('lessons/<str:str_id>',views.lesson,name='lesson'),
    path('ajax/lessons',views.lesson_complete,name="lesson_complete"),
    path('ajax/translate-audio',views.translate_audio,name="translate_audio"),
    path('profile/',views.profile_page,name='profile_page'),
]
