# Last modified: 09/05/2023
# Modified by: Andrew Roney

from django.shortcuts import render, redirect
from .models import Forum, Post
from community.forms import ForumForm, PostForm


def home(request):
    forums = Forum.objects.all() # Get all forums
    return render(request, "community/home.html")

def create_forum(request):
    if request.method == 'POST':
        form = ForumForm(request.POST)
        if form.is_valid():
            new_forum = form.save(commit=False)
            new_forum.save()
            return redirect('community/home.html')  # Redirect to the community home page
    else:
        form = ForumForm()
    return render(request, 'community/create_forum.html', {'form': form})

def forum_detail(request, forum_id):
    forum = Forum.objects.get(id=forum_id)
    posts = forum.post_set.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.forum = forum
            post.save()
            return redirect('community/forum_detail.html', forum_id=forum.id)
    else:
        form = PostForm()
    return render(request, 'community/forum_detail.html', {'forum': forum, 'posts': posts})