import re

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse
from sanskrit.models import UserProfile,SanskritLessons

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]
class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')
        url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)    

        if request.user.is_authenticated and url_is_exempt:
            if path == reverse('accounts:register').lstrip('/'):
                return redirect(reverse('sanskrit:home'))
            
            if path == reverse('accounts:login').lstrip('/'):
                return redirect(reverse('sanskrit:home'))

            return None

        elif request.user.is_authenticated or url_is_exempt:
            
            return None

        else:
            if path == reverse('sanskrit:lessons').lstrip('/'):
                return redirect(settings.LOGIN_URL)

            if path == reverse('accounts:logout').lstrip('/'):
                return redirect(settings.LOGIN_URL)

            return redirect(reverse('sanskrit:home'.lstrip('/')))


class LessonsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')
       
        if (view_func.__name__) == "lesson":

            req_lesson = view_kwargs['str_id']
            lesson = SanskritLessons.objects.get(lesson_name=req_lesson)

            if lesson.q_number!=1:
                prev_lesson = SanskritLessons.objects.get(q_number=lesson.q_number-1)          
           
                if not UserProfile.objects.filter(user=request.user,lesson_key=prev_lesson.lesson_name).exists():
                    return redirect(reverse('sanskrit:lessons'))
               

