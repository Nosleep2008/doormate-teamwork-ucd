from django.urls import path, include
from django.conf import settings
from main.views import google_auth_redirect, google_auth_code_handler

urlpatterns = [
    path('', google_auth_redirect),
    path('complete/google-oauth2/', google_auth_code_handler)
]
