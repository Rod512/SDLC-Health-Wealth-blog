from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.views.decorators.csrf import csrf_exempt

from .serializer import RegisterSerializer
from rest_framework import status, exceptions
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from django.contrib.auth import authenticate,logout
from .models import User, UserToken
import re
from .authentication import create_access_token,create_refresh_token,decode_refresh_token,JWTauthentication
from rest_framework.permissions import IsAuthenticated

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
    
# PUT request for full data update
@api_view(['PUT'])
def put_user(request,id):
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
    serilizer_data = RegisterSerializer(users, data=data)
    
    if serilizer_data.is_valid():
        serilizer_data.save()
        return Response({"message": "Data Change successfully","Data":serilizer_data.data}, status=200)
    else:
        return Response(serilizer_data.data, status=status.HTTP_400_BAD_REQUEST)


# for delete user
@api_view(['DELETE'])
def delete_user(request):
    id = request.data.get("user_id")
    if not id:
        return Response({'error': 'ID not provided'}, status=400)
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
    user = User.objects.filter(email=email).first()

    if user is None:
        raise exceptions.AuthenticationFailed('Invalid Cradential')

    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('Invalid Cradential')

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    UserToken.objects.create(
        user = user,
        tokens = refresh_token,
        expired_at = timezone.now() + timedelta(days=7)
    )

    response = Response()
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    response.data = {
        "Message" : 'Login Successfull',
        "access_token" : access_token,
        "refresh_token" : refresh_token,
        "name" : user.name,
        "email" : user.email
    }

    return response


    

#Generate new access token and refresh token using old access and refrsh token
@api_view(['POST'])
def refresh_view_check(request):
    refresh_token = request.data.get('refresh_token') or request.COOKIES.get('refresh_token')

    if not refresh_token:
        return Response({"message":"Refresh token not provided"}, status=400)
    
    try:
        user_id = decode_refresh_token(refresh_token)
        user = User.objects.get(id=user_id)

        token_obj =UserToken.objects.filter(
            user = user,
            tokens = refresh_token,
            expired_at__gt = timezone.now()
        ).first()

        if not token_obj:
            return Response({"Message" : "Invalid token or expired refresh token"}, status=400)
    except User.DoesNotExist:
        return Response({"Message" : "Invalid User!!"}, status=400)
    except Exception as e:
        return Response({'error': f'Invalid token: {str(e)}'}, status=401)
    
    token_obj.delete()

    new_access_token = create_access_token(user.id)
    new_refresh_token = create_refresh_token(user.id)

    UserToken.objects.create(
        user = user,
        tokens = new_refresh_token,
        expired_at = timezone.now()+timedelta(days=7)
    )

    response = Response({
        'user' : RegisterSerializer(user).data,
        'access_token' : new_access_token,
        'refresh_token' : new_refresh_token

    })
    response.set_cookie(key="refresh_token", value=new_refresh_token, httponly=True)
    return response



@api_view(['get'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTauthentication])
def user_api(request):
    user = request.user
    serializer = RegisterSerializer(user)
    return Response({
        "user" : serializer.data
    })



# for logout
@api_view(['POST'])
@csrf_exempt
def user_logout(request):
    refresh_token = request.data.get("refresh_token") or request.COOKIES.get("refresh_token")

    if not refresh_token:
        return Response({"Message": "Token missing"}, status=400)
    
    token_obj = UserToken.objects.filter(tokens=refresh_token).first()
    
    if not token_obj:
        return Response({"detail": "Invalid or already logged out"}, status=401)
    
    UserToken.objects.filter(tokens=refresh_token).delete()

    response = Response({
        "message" : "Logout Successfull"
    }, status=200)
    response.delete_cookie(key="refresh_token")

    return response

    
        

        
        


    


