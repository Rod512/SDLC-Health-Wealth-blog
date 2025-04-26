from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializer import RegisterSerializer
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import User
import re

name_regex = r'^([A-Za-z]{2,})(\s[A-Za-z]{2,})+$'
email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.{1,}[a-zA-Z]{2,}$'
pass_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&!*_-])[A-Za-z\d@#$%^&!*_-]{6,}$'

# POST request
@api_view(["POST"])
def create_register_api(request):
    name = request.data.get("name")
    email = request.data.get("email")
    password = request.data.get("password")
    
    # name validation
    if not re.fullmatch(name_regex, name):
        return Response({"Message": "Plsease enter your full name. Avoid any number and special charecter."} , status=400)

    # email validation
    if not re.fullmatch(email_regex, email):
        return Response({"Message" : "The email is not correct format"}, status=400)
    
    # password validation
    if not re.fullmatch(pass_regex, password):
        return Response({"Message":"Password should be minimum 6 charecter with upercase, lowercae,number and special charecter"}, status=400)

    # check email uniq or not
    if User.objects.filter(email=email).exists():
        return Response({"Message": "This Email is already registerd"}, status=400)
    
    if not all([name, email, password]):
        return Response({"Message": "Please fill up all the fields"}, status=400)
    else:
        user_created = User(
            name = name,
            email = email,
            password= make_password(password)
        )
        user_created.save()
        
    
    response_data = {
        "message" : "User create succesfully",

        "user" :{
            "name" : name,
            "email" : email,
            "password" : password
        }
    }

    return Response(response_data, status=200)

# GET request user data
@api_view(['GET'])
def get_registerd_user(request):
    users = User.objects.all()
    serilizer_data = RegisterSerializer(users, many=True)
    return Response(serilizer_data.data, status=200)

# PATCH request for partial update
@api_view(['PATCH'])
def patch_user(request,id):
    try:
        users = User.objects.get(id=id)
    except:
        return Response({"message": "User doesn't exist"},status=status.HTTP_404_NOT_FOUND)
    
    data = request.data.copy()
    
    # password validation
    if 'password' in data:
        password = data['password']

        if not re.fullmatch(pass_regex, password):
            return Response({"Message":"Password should be minimum 6 charecter with upercase, lowercae,number and special charecter"}, status=400)
        
        data['password'] = make_password(data['password'])

    #name validation
    if 'name' in data:
        name = data['name']

        if not re.fullmatch(name_regex, name):
            return Response({"Message": "Plsease enter your full name. Avoid any number and special charecter."} , status=400)
        
    #email validation
    if 'email' in data:
        email = data["email"]

        if not re.fullmatch(email_regex, email):
            return Response({"message": "Please enter a valid email address."}, status=400)


    
    serilizer_data = RegisterSerializer(users, data=data, partial=True)
    
    if serilizer_data.is_valid():
        serilizer_data.save()
        return Response({"message": "Data Change successfully","Data":serilizer_data.data}, status=200)
    else:
        return Response(serilizer_data.data, status=status.HTTP_400_BAD_REQUEST)
    
# for delete user
@api_view(['DELETE'])
def delete_user(request,id):
    try:
        user = User.objects.get(id=id)
        user.delete()
        return Response({"message":"User delete succesfully"})
    except:
        return Response({"message":"User invalid"})
    
#for user login
@api_view(['POST'])
def user_login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({'message': "Email and password both are required"})

    user = authenticate(request, email=email, password=password)

    if user is not None:
        return Response(
            {
                'message': "Login success!!",
                'user':{
                    'email' : user.email,
                    'password' : user.password,
                }
            }
        )
    else:
        return Response({"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)



    
        

        
        


    


