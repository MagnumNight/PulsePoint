# Last Modified: 09/05/2023
# Modified by: Andrew Roney

from django.urls import path, include
from . import views

app_name = 'resources'

urlpatterns = [
    path('', views.home, name='home'),
    path('community/', include('community.urls'))
]
