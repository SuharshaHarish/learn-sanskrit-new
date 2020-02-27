from django.urls import path
from sanskrit import views

app_name = 'sanskrit'

urlpatterns = [
    path('home/',views.home,name='home'),
    path('lessons/',views.lessons,name = 'lessons'),
    path('lessons/<str:str_id>',views.lesson,name='lesson'),
    path('ajax/lessons',views.lesson_complete,name="lesson_complete")
    

]
