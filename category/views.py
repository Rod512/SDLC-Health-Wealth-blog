from django.shortcuts import render

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

@api_view(['POST'])
def post_category(request):

    name = request.data.get('name')
    description = request.data.get('description')
    user_id = request.data.get('user_id')

    # regex for category name
    name_regex = r'^([A-Za-z_]{2,})(\s[A-Za-z_]+)*+$'

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
