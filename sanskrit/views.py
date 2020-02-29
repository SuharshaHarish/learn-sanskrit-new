from django.shortcuts import render,redirect
from django.urls import reverse
from .models import SanskritLessons,SanskritQuestions,SanskritAnswers,UserProfile
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.core import serializers
import json
from django.http import JsonResponse

def home(request):
    args = {
        'name': mark_safe(json.dumps("Suharsha")),
        'list': mark_safe(json.dumps([1,2,3,4,]))
        }
    return render(request,'sanskrit/home.html',args)

def lessons(request):
    
    lesson_list = SanskritLessons.objects.all()
    user = request.user
    user_profiles = UserProfile.objects.filter(user=user)
    serialized_user_profiles = serializers.serialize('json', user_profiles)
    serialized_lesson_list = serializers.serialize('json', lesson_list)   
    
    args={
        'my_lessons' : lesson_list,
        'serialized_user_profiles' : serialized_user_profiles,
        'serialized_lesson_list' : serialized_lesson_list        
    }

    return render(request,'sanskrit/lessons.html',args)

def lesson(request,str_id):
    
    lesson = SanskritLessons.objects.get(lesson_name= str_id)    
    questions = SanskritQuestions.objects.filter(key_question = lesson)
    q_choices= SanskritAnswers.objects.filter(key_answer= questions[0])
    
    for i in range(len(questions)):
        answer = SanskritAnswers.objects.filter(key_answer= questions[i])
        if answer:
            q_choices = q_choices|answer
    #questions_json = mark_safe(json.dumps(list(questions), cls=DjangoJSONEncoder))
    serialized_questions = serializers.serialize('json', questions)
    serialized_q_choices = serializers.serialize('json', q_choices)
    #q_choices = SanskritAnswers.objects.filter(key_answer= questions)
    
    # for i in range(len(user_profile)):
    #     completed = user_profile[i].completed
    #     if completed == True:
    #         q_choices = q_choices|answer
    
    args={
        'my_lesson' : lesson,
        'my_questions' : questions,
        'serialized_questions':serialized_questions,
        'q_choices' : q_choices,
        'serialized_q_choices':serialized_q_choices,
    }

    return render(request,'sanskrit/lesson.html',args)

def lesson_complete(request):

    complete = request.GET.get('completed', None)
    lesson_ajax = request.GET.get('lesson_name',None)

    if(complete=="True"):
        username = request.user
        lesson= SanskritLessons.objects.get(lesson_name=lesson_ajax)
        if(UserProfile.objects.filter(user=username,lesson_key=lesson).exists()):
            user_lesson = UserProfile.objects.get(user=username,lesson_key=lesson)
            
        else:
            user_lesson = UserProfile.objects.create(user=username,lesson_key=lesson)
        user_lesson.completed=True
        user_lesson.save()
        data={ "completed":"True"}

        return JsonResponse(data)

    return redirect(reverse('sanskrit:lessons'))