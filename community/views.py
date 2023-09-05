# Last modified: 09/05/2023
# Modified by: Andrew Roney

from django.shortcuts import render


def home(request):
    return render(request, "community/home.html")
