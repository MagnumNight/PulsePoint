from django.shortcuts import render


# Function: home - Renders home page
def home(request):
    return render(request, "resources/home.html")
