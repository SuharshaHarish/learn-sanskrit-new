from django.shortcuts import render
from .models import SanskritLessons,SanskritQuestions,SanskritAnswers
from django.utils.safestring import mark_safe
from django.core import serializers
import json

def home(request):
    args = {
        'name': mark_safe(json.dumps("Suharsha")),
        'list': mark_safe(json.dumps([1,2,3,4,]))
        }
    return render(request,'sanskrit/home.html',args)

def lessons(request):
    
    lesson_list = SanskritLessons.objects.all()
    
    args={
        'my_lessons' : lesson_list,
        
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
    print(serialized_questions)
    args={
        'my_lesson' : lesson,
        'my_questions' : questions,
        'serialized_questions':serialized_questions,
        'q_choices' : q_choices,
        'serialized_q_choices':serialized_q_choices,
    }

    return render(request,'sanskrit/lesson.html',args)