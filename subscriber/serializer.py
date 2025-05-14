from rest_framework import serializers
from .models import Subscriber

class SubscriberSerialzier(serializers.ModelSerializer):
   class Meta:
        model = Subscriber
        fields = ['email', 'subscribeOn ']
        

