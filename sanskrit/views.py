import re
import json
from django.shortcuts import render,redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.core import serializers
from django.http import JsonResponse,HttpResponse
from gtts import gTTS 
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from django.contrib import messages
import datetime
from datetime import date, timedelta
from django.utils import timezone
from .models import SanskritLessons,SanskritQuestions,SanskritAnswers,UserProgress,Audio
from accounts.models import Profile
from django.contrib.auth.models import User
from sanskrit.forms import ProfileForm
from learn_sanskrit import settings
def home(request):  
     
    return render(request,'sanskrit/home.html')

def lessons(request):
    
    lesson_list = SanskritLessons.objects.all().order_by('q_number')
    user = request.user
    user_profiles = UserProgress.objects.filter(user=user).order_by('lesson_key')
    serialized_user_profiles = serializers.serialize('json', user_profiles)    
    serialized_lesson_list = serializers.serialize('json', lesson_list)  

    # translate_questions_all()

    args={
        'my_lessons' : lesson_list,
        'profile': Profile.objects.get(user=request.user),
        'serialized_user_profiles' : serialized_user_profiles,
        'serialized_lesson_list' : serialized_lesson_list        
    }

    return render(request,'sanskrit/lessons.html',args)

def lesson(request,str_id):
    
    lesson_str = re.findall('[A-Z][^A-Z]*', str_id) #for 2 word lessons
    lesson_name = (" ").join(lesson_str)
    lesson = SanskritLessons.objects.get(lesson_name= lesson_name)    
    questions = SanskritQuestions.objects.filter(key_question = lesson).order_by('q_number')
    q_choices= SanskritAnswers.objects.filter(key_answer= questions[0])
    #audio sources
    correct_audio = Audio.objects.get(name = "Correct")
    wrong_audio = Audio.objects.get(name = "Wrong")

    
    for i in range(len(questions)):
        answer = SanskritAnswers.objects.filter(key_answer= questions[i])
        if answer:
            q_choices = q_choices|answer
    #questions_json = mark_safe(json.dumps(list(questions), cls=DjangoJSONEncoder))
    serialized_questions = serializers.serialize('json', questions)
    # print(serialized_questions)
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
        'correct_audio_src': correct_audio.file.name,
        'wrong_audio_src': wrong_audio.file.name,
        'media_url': settings.MEDIA_URL

    }

    return render(request,'sanskrit/lesson.html',args)

def lesson_complete(request):

    complete = request.GET.get('completed', None)
    lesson_ajax = request.GET.get('lesson_name',None)

    if(complete=="True"):
        username = request.user
        lesson= SanskritLessons.objects.get(lesson_name=lesson_ajax)
        if(UserProgress.objects.filter(user=username,lesson_key=lesson).exists()):
            user_lesson = UserProgress.objects.get(user=username,lesson_key=lesson)
            
        else:
            user_lesson = UserProgress.objects.create(user=username,lesson_key=lesson)
        user_lesson.completed=True
        user_lesson.save()
        data={ "completed":"True"}

        return JsonResponse(data)

    return redirect(reverse('sanskrit:lessons'))


def translate_audio(request):    
    
    # mytext = 'जय श्रिराम'

    if request.GET.get('text', None) :
        text = request.GET.get('text',None)

        if Audio.objects.filter(name = text).exists():

            audio = Audio.objects.get(name = text)
            data = {'audio_src':audio.file.name}
            return JsonResponse(data)

        else:
            
            translate_questions(text)  

        
        # myobj = gTTS(text=mytext, lang=language, slow=False)  
        # audio_temp_file = NamedTemporaryFile()
        # myobj.write_to_fp(audio_temp_file)      
        # temp_file = File(audio_temp_file, name="translated_audio.mp3")

        
        
        # if Audio.objects.filter(name = "translated_audio").exists():
            
        #     audio = Audio.objects.get(name = "translated_audio")
        #     audio.file = temp_file
        #     audio.save() 
        #     # print(File.file.field.storage.exists("translated_audio"))
        #     print(text)
                    
        # else:
        #     audio = Audio.objects.create(file = temp_file, name= "translated_audio")
        #     audio.save()     
      
    return redirect(reverse('sanskrit:home'))

#for generating audio files for all questions for the first time
def translate_questions_all():

    language = 'hi'
    questions = SanskritQuestions.objects.all()
    for question in questions:
        ques = question.question
        if Audio.objects.filter(name = ques).exists():
            continue
        else:        
            myobj = gTTS(text=ques, lang=language, slow=False)  
            audio_temp_file = NamedTemporaryFile()
            myobj.write_to_fp(audio_temp_file)      
            temp_file = File(audio_temp_file, name=ques+".mp3")                                            
            audio = Audio.objects.create(file = temp_file, name = ques)
            audio.save()

#for generating audio file for the given text if already not present
def translate_questions(text):

    language = 'hi' 
    ques = text
    myobj = gTTS(text=ques, lang=language, slow=False)  
    audio_temp_file = NamedTemporaryFile()
    myobj.write_to_fp(audio_temp_file)      
    temp_file = File(audio_temp_file, name=ques+".mp3")                                            
    audio = Audio.objects.create(file = temp_file, name = ques)
    audio.save()




def profile_page(request):
    sun,mon,tue,wed,thu,fri,sat=0,0,0,0,0,0,0
    if request.method == 'POST': 
        profile, created = Profile.objects.get_or_create(user=request.user)
        form = ProfileForm(request.POST, request.FILES,instance=profile) 
  
        if form.is_valid(): 
            form.save()            
            messages.add_message(request,messages.SUCCESS,"Profile picture updated successfully")
            return redirect('sanskrit:profile_page') 
    else: 
        form = ProfileForm() 
    lesson_list = SanskritLessons.objects.all().order_by('q_number')
    user = request.user
    user_profiles = UserProgress.objects.filter(user=user,day__lte=datetime.datetime.today(), day__gt=datetime.datetime.today()-datetime.timedelta(days=7))
    for user_profile in user_profiles:
        day = user_profile.day.isoweekday()        
        if day==1:
            mon+=1
        if day==2:
            tue+=1
        if day==3:
            wed+=1
        if day==4:
            thu+=1
        if day==5:
            fri+=1
        if day==6:
            sat+=1
        if day==7:
            sun+=1
    args = {
        'profile': Profile.objects.get(user=request.user),
        'form' : form,
        'user': request.user,
        'completed_lessons' : user_profiles.count(),
        'total_lessons' : lesson_list.count() ,
        'sun':sun,
        'mon':mon,
        'tue':tue,
        'wed':wed,
        'thu':thu,
        'fri':fri,
        'sat':sat
    }
    return render(request,'sanskrit/profile_page.html', args)


def redirect_to_home(request):

    return redirect(reverse('sanskrit:home'))