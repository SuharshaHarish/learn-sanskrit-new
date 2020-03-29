from django.shortcuts import render,redirect
from django.urls import reverse
from django.utils import timezone
from .models import Forum,ForumComment
from django.shortcuts import render, get_object_or_404
from .forms import ForumForm
from django.http import JsonResponse
from accounts.models import Profile


def forum_list(request):
    forums = Forum.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    profiles=[]
    for forum in forums:
        # print(forum.author)
        profiles.append(Profile.objects.get(user=forum.author))
        print(profiles)
    args={
        'forums':forums,
        'user':request.user,
        'profiles': profiles      
    }
    return render(request, 'forums/forum_list.html',args)

def forum_detail(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    comments = ForumComment.objects.filter(forum_key = forum)
    user = request.user
    forum_author = forum.author
    args= {
        'forum': forum,
        'comments':comments,
        'user':user,
        'forum_author':forum_author,
        'profile': Profile.objects.get(user=request.user) 
        }
    return render(request, 'forums/forum_detail.html', args)

def forum_new(request):
    if request.method == "POST":
        form = ForumForm(request.POST)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.author = request.user
            forum.forum_profile=Profile.objects.get(user=request.user) 
            forum.published_date = timezone.now()
            forum.save()
            return redirect('forums:forum_detail', pk=forum.pk)
    else:
        form = ForumForm()
    return render(request, 'forums/forum_edit.html', {'form': form})

def forum_edit(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    
    if request.method == "POST":
        form = ForumForm(request.POST, instance=forum)
        if form.is_valid():
            forum = form.save(commit=False)
            forum.author = request.user
            forum.published_date = timezone.now()
            forum.save()
            return redirect('forums:forum_detail', pk=forum.pk)
    else:
        form = ForumForm(instance=forum)
    
    args={
        'form': form,        
    }
    return render(request, 'forums/forum_edit.html', args)

def add_comment(request,pk):
    forum = get_object_or_404(Forum,pk=pk)
    if request.method == 'POST':
        
        comment_ajax = request.POST.get('comment',None)
        comment = ForumComment.objects.create(comment = comment_ajax,author = request.user,forum_key=forum,forum_profile=Profile.objects.get(user=request.user) )
        comment.save()

        data={"success":"success"}
        return(JsonResponse(data))
    
    return redirect('forums:forum_detail',pk=forum.pk)