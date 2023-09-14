"""
URL configuration for PulsePoint project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from . import views
from .views import send_email

# Variable: urlpatterns - The URL patterns for the project as a whole
urlpatterns = [
    path("admin/", admin.site.urls), # Admin site
    path(
        "", views.root_homepage, name="root_home"
    ),  # Root homepage for the entire project
    path("moodtracker/", include("moodtracker.urls", namespace="moodtracker")),  # Moodtracker app
    path("community/", include("community.urls", namespace="community")),  # Community app
    path("resources/", include("resources.urls", namespace="resources")),  # Resources app
    path(
        "accounts/", include("django.contrib.auth.urls")
    ),  # This line includes all auth views like login, logout, password reset, etc.
    path("delete_account/", views.delete_account, name="delete_account"),  # Delete account
    path("signup/", views.signup, name="signup"),  # Sign up
    path("account/settings/", views.account_settings, name="account_settings"),  # Account settings
    path("activate/<str:uidb64>/<str:token>/", views.activate, name="activate"),  # Activate account
    path("send_email/", send_email, name="send_email"),  # Send email
    path("thank_you/", views.thank_you, name="thank_you"),  # Thank you
    path("about/", views.about, name="about"),  # About
    path("contact/", views.contact, name="contact"),  # Contact
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        views.password_reset_confirm,
        name="password_reset_confirm",
    ),  # Password reset confirm
    path("password_reset/", views.password_reset_view, name="password_reset"),
    path('password_reset_success/', views.password_reset_success, name='password_reset_success'),

]
