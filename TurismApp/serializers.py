from rest_framework import serializers
from TurismApp.models import User, Destination

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id', 'firstName','lastName', 'email', 'password','role')
        
class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Destination
        fields=('title', 'location','price','numberOfGuests')        