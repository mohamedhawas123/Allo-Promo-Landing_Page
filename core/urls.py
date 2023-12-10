
from django.contrib import admin
from django.urls import path, include
from .views import home, get_user_tweets, get_facebook_posts, send_message, create_contact



urlpatterns = [
    path('', home, name='home' ),
    path('twitter', get_user_tweets, name='twitter' ),
    path('facebook', get_facebook_posts, name='facebook' ),
    path('message', send_message, name='message' ),
    path('create_contact', create_contact, name='create_contact' )




    
]
