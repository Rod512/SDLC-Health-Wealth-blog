# Create your views here.
from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializer import CategorySerializer
from .models import Categories
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
import re

User = get_user_model()

 # regex for category name
name_regex = r'^([A-Za-z_]{2,})(\s[A-Za-z_]+)*+$'

@api_view(['POST'])
def post_category(request):

    name = request.data.get('name')
    description = request.data.get('description')
    user_id = request.data.get('user_id')

    try :
        user = User.objects.get(id=user_id)

    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=404)



    # Perform validation or any other logic you need
    if not all([name, description, user_id]):
        # Data PreProcessing & Santization
        return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    if not re.match(name_regex, name):
        return Response({"error": "Name must be between 3 and 50 characters and can only contain letters and underscores (_). No spaces, numbers, or special characters allowed."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Save the input to the UserProfile model
        category_created = Categories(name=name,description=description, user=user )
        category_created.save()
    
    # Example response data
    response_data = {
        "message": "Category registered successfully!",
        "categories": {
            "name": name,
            "description":description,
            "user_id" : user_id,
            "user_name" : user.name
        }
    }
    
    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_category(request):
    category = Categories.objects.all()

    if not category.exists():
        return Response({"message":"No category Found!"})
    
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data,  status=200)


@api_view(['PATCH'])
def patch_category(request, id):
    try:
        categories = Categories.objects.get(id=id)
    except Categories.DoesNotExist:
        return Response({"message": "Categories does not found!!"}, status=400)
    
    data = request.data.copy()
    
    if 'name' in data:
        name = data['name']
        if not re.fullmatch(name_regex, name):
            return Response({"error": "Name must be between 3 and 50 characters and can only contain letters and underscores (_). No spaces, numbers, or special characters allowed."}, status=status.HTTP_400_BAD_REQUEST)
            
    serializer = CategorySerializer(categories, data=request.data , partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    else:
        return Response(serializer.errors, status=400)


@api_view(['PUT'])
def put_category(request,id):
    try:
        categories = Categories.objects.get(id=id)
    except Categories.DoesNotExist:
        return Response({"Message":"Category does not exist"})
    
    data = request.data.copy()
   

    if 'name' in data:
        name = data["name"]
        if not re.fullmatch(name_regex, name):
            return Response({"error": "Name must be between 3 and 50 characters and can only contain letters and underscores (_). No spaces, numbers, or special characters allowed."}, status=status.HTTP_400_BAD_REQUEST)
        
    serializer = CategorySerializer(categories, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Data updates!!",
            "data": serializer.data
        })
    else:
        return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_category(request):
    id = request.data.get("id")
    if not id:
        return Response({'error': 'ID not provided'}, status=400)
    try:
        category = Categories.objects.get(id=id)
        category.delete()
        return Response({"message":"category delete successfully!!"}, status=200)
    except:
        return Response({"message":"category dose not exist!!"}, status=400)
