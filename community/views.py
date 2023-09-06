from django.shortcuts import render, redirect
from community.forms import ForumForm, PostForm
from .models import Forum
from django.contrib import messages


def home(request):
    forums = Forum.objects.all().order_by("-date_created")
    return render(request, "community/home.html", {"forums": forums})


def create_forum(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ForumForm(request.POST)
            if form.is_valid():
                new_forum = form.save(commit=False)
                new_forum.user = request.user
                new_forum.save()
                return redirect("community:home")  # Redirect to the community home page
        else:
            form = ForumForm()
        return render(request, "community/create_forum.html", {"form": form})
    else:
        messages.info(request, "You must be logged in to create a forum.")
        return redirect("community:home")


def forum_detail(request, forum_id):
    forum = Forum.objects.get(id=forum_id)
    posts = forum.post_set.all()
    if request.method == "POST":
        form = PostForm(request.POST)
        if (
            form.is_valid() and request.user.is_authenticated
        ):  # Check if user is authenticated
            post = form.save(commit=False)
            post.forum = forum
            post.user = request.user
            post.save()
            return redirect("community:forum_detail", forum_id=forum.id)
    else:
        form = PostForm()
    return render(
        request,
        "community/forum_detail.html",
        {
            "forum": forum,
            "posts": posts,
            "form": form,
            "user": request.user,
        },  # Pass user in context
    )
