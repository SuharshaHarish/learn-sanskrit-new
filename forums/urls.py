from django.urls import path
from forums import views

app_name = 'forums'

urlpatterns = [
    path('',views.forum_list,name='forum_list'),
    path('forum/<int:pk>/', views.forum_detail, name='forum_detail'),
    path('forum/new/', views.forum_new, name='forum_new'),
    path('forum/<int:pk>/edit/', views.forum_edit, name='forum_edit'),
    path('forum/<int:pk>/comment',views.add_comment,name='add_comment')
]