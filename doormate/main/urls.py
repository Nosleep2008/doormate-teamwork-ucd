from django.urls import path, include
from django.conf import settings
from main import views

urlpatterns = [
    path('', views.index),
    path('google_auth_redirect', views.google_auth_redirect),
    path('complete/google-oauth2/', views.google_auth_code_handler),
    path('save_calendar/', views.save_calendar),
    #path('insert_event/<name>/<start_time>/<end_time>/<status>', views.insert_event),
    path('show_event/<start_time>/<end_time>',views.show_event),
    path('del_event/<summary>',views.del_event),
    path('get_event/<time>',views.get_event),
    path('next_event/<time>',views.next_event),
    path('update_event/<summary>/<name>/<start_time>/<end_time>/<status>',views.update_event),
    path('bot/<text>', views.telegram_message)
]
