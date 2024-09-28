from django.urls import path
from . import views

urlpatterns = [
    path('chatbot/', views.chatbot, name='chatbot'),
    path('make-appointment/', views.make_appointment, name='make_appointment'),
    # appointment/urls.py
    path('chatbot-ui/', views.chatbot_interface, name='chatbot_interface')

]
