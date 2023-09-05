# Last modified: 09/05/2023
# Modified by: Andrew Roney

from django.shortcuts import render, redirect
from django.http import JsonResponse



def home(request):
    return render(request, "community/home.html")


def create_new_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        # Create a new Post object and sve it to the database
        new_post = Post(title=title, content=content)
        new_post.save()

        return JsonResponse({'status': 'success', 'title': title, 'content': content})
    
    return JsonResponse({'status': 'error'})