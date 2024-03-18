from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from .models import User, Destination
from .serializers import UserSerializer, DestinationSerializer

from django.core.exceptions import ObjectDoesNotExist
import json
import jwt
from datetime import datetime, timedelta
from django.conf import settings

# Create your views here.

@csrf_exempt
def destinationApi(request, id=0):
    if request.method == 'GET' and id == 0:
        destinations = Destination.objects.all()
        destination_serializer = DestinationSerializer(destinations, many = True)
        return JsonResponse(destination_serializer.data, safe = False, status = 200)
    
    if request.method == 'GET':
        try:
            destination = Destination.objects.get(id=id)
            destination_serializer = DestinationSerializer(destination, many=False)
            return JsonResponse(destination_serializer.data, safe=False, status = 200)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Not Found"}, status=404)

    elif getRoleFromToken(request) != 'ADMIN':
            return JsonResponse({"error": "Forbidden"}, status=403)

    elif request.method == 'POST':
        destination_data = json.loads(request.body)
        destination_serializer = DestinationSerializer(data=destination_data)
        if destination_serializer.is_valid():
            destination_serializer.save()
            return JsonResponse("Added successfully", safe = False, status = 201)
        return JsonResponse("Failed to add", safe = False)

    elif request.method == 'PUT':
        destination_data = json.loads(request.body)
        destination_to_update = Destination.objects.get(id=destination_data['id'])
        destination_serializer = DestinationSerializer(destination_to_update, data = destination_data)
        if destination_serializer.is_valid():
            destination_serializer.save()
            return JsonResponse("Update successfully", safe = False, status = 200)
        return JsonResponse("Failed to update", safe = False)

    elif request.method == 'DELETE':
        destination = Destination.objects.get(id = id)
        destination.delete()
        return JsonResponse("Deleted successfully", safe = False, status = 200)
    
@csrf_exempt
def loginApi(request):
    if request.method == 'POST':
        user_data = json.loads(request.body)
        try:
            user = User.objects.get(email=user_data.get('email'))

            if (user_data.get('password') != user.password):
                return JsonResponse({"error": "Not Found"}, status=404)
            
            token = generateJwt(user.id, user.role)
            return JsonResponse({"token": token}, status = 200)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Not Found"}, status=404)

@csrf_exempt
def registerApi(request):
    if request.method == 'POST':
        user_data = json.loads(request.body)
        users_serializer = UserSerializer(data=user_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse("Added successfully", safe = False, status = 201)
        return JsonResponse("Failed to add", safe = False)


def generateJwt(user_id, user_role):
    expiration_time = datetime.utcnow() + timedelta(hours = 6)
    payload = {
        "user_id": user_id,
        "user_role": user_role,
        "exp" : expiration_time
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token

def getRoleFromToken(request):
    token = getToken(request)
    if token is None:
        return None
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    user_role = decoded_token.get('user_role')
    return user_role

def getToken(request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        return token
    return None