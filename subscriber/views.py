from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Subscriber
from .serializer import SubscriberSerialzier
import re

@api_view(['POST'])
def subscribe(request):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.{1,}[a-zA-Z]{2,}$'

    email = request.data.get("email")

    if not re.fullmatch(email_regex, email):
        return Response({"Message" : "Please give correct email"}, status=400)

    if Subscriber.objects.filter(email=email).exists():
        return Response({"Message" : "Email is already exist"}, status=400)
    
    subscriber = Subscriber.objects.create(
        email = email
    )

    return Response({
        "Message" : "Subscribed Successfull !!",
        "Email" : subscriber.email
    })