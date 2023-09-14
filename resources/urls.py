# Last Modified: 09/05/2023
# Modified by: Andrew Roney

from django.urls import path, include
from . import views

# Variable: app_name - The name of the app
app_name = 'resources'

# Variable: urlpatterns - The URL patterns for the app
urlpatterns = [
    path('', views.home, name='home'),
    path('community/', include('community.urls'))
]
