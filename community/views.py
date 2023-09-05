# Last modified: 09/05/2023
# Modified by: Andrew Roney

from django.shortcuts import render
from .models import Forum
from community.forms import ForumForm


def home(request):
    forums = Forum.objects.all() # Get all forums
    return render(request, "community/home.html")

def create_forum(request):
    if request.method == 'POST':
        form = ForumForm(request.POST)
        if form.is_valid():
            new_forum = form.save(commit=False)
            new_forum.save()
            return redirect('community_home')  # Redirect to the community home page
    else:
        form = ForumForm()
    return render(request, 'create_forum.html', {'form': form})