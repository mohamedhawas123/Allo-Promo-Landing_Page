from django.shortcuts import render
from .models import Contact, Service, Testimonial, Post
from .twitter import twitter_api
from django.http import JsonResponse
import tweepy
from requests_oauthlib import OAuth1
from django.conf import settings
import requests
import base64
from django.http import HttpResponse


def home(request):
    services = Service.objects.all()
    testimonial = Testimonial.objects.all()
    posts = Post.objects.all()
    return render(request, 'core/home.html', {'services': services, 'testimonials': testimonial, 'posts': posts})

def get_user_tweets(request ):
    consumer_key = settings.TWITTER_CONSUMER_KEY
    consumer_secret = settings.TWITTER_CONSUMER_SECRET
    access_token =settings.TWITTER_ACCESS_TOKEN
    access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET


    encoded_consumer_key = consumer_key.encode("utf-8")
    encoded_consumer_secret = consumer_secret.encode("utf-8")
    encoded_access_token = access_token.encode("utf-8")
    encoded_access_token_secret = access_token_secret.encode("utf-8")

    credentials = "{}:{}{}:{}".format(encoded_consumer_key, encoded_consumer_secret, encoded_access_token, encoded_access_token_secret)
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    print(encoded_credentials)
    headers = {
        "Authorization": "Bearer " + encoded_credentials,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    parameters = {
        "grant_type": "client_credentials"
    }

    response = requests.post("https://api.twitter.com/oauth2/token", headers=headers, data=parameters)

    if response.status_code == 200:
        access_token = response.json()["access_token"]

        timeline_headers = {
            "Authorization": "Bearer " + access_token,
        }

        timeline_parameters = {
            "screen_name": "RaniahYousief",
            "count": 10,
        }

        timeline_response = requests.get("https://api.twitter.com/1.1/statuses/user_timeline.json", headers=timeline_headers, params=timeline_parameters)

        if timeline_response.status_code == 200:
            tweets = timeline_response.json()
            for tweet in tweets:
                print(tweet["text"])
        else:
            print("Error retrieving user timeline:", timeline_response.status_code)
    else:
        print("Error getting access token:", response.status_code)



def get_facebook_posts(request):
    page_id = ''
    
    access_token = ''
    
    params = {
        'access_token': access_token,
        'limit': 10,  
        'fields': 'message,created_time,id'  # Specify fields you want to retrieve
    }
    url = f'https://graph.facebook.com/v18.0/{page_id}/posts'

    try:
        res = requests.get(url, params=params)
        if res.status_code == 200:
            print(res.json())
        else:
            print(f"Failed to retrieve posts: {res.status_code}")
            print(res.content)
    except Exception as e:
        print("An error occurred:")
        print(e)



def send_message(request):
    if request.method == "POST":
        name = request.POST.get("name")
        subject = request.POST.get("subject")
        email =request.POST.get("email")
        message = request.POST.get("message")
        
        contact = Contact()
        contact.name= name 
        contact.subject = subject
        contact.email = email
        contact.body = message
        contact.save()
        return HttpResponse("Successfully Sent Message")


def create_contact(request):
    hubspot_api_key = ''
    endpoint = f'https://api.hubapi.com/contacts/v1/contact?hapikey={hubspot_api_key}'

    contact_data = {
        "properties": [
            {
                "property": "email",
                "value": "example@example.com"
            },
            {
                "property": "firstname",
                "value": "John"
            },
            {
                "property": "lastname",
                "value": "Doe"
            },
        ]
    }

    response = requests.post(endpoint, json=contact_data)
    return JsonResponse(response.json())