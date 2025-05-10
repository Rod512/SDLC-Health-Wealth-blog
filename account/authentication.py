import jwt
from datetime import datetime,timedelta,timezone
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from .models import User


class JWTauthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request).split()

        if len(auth_header) != 2:
            raise AuthenticationFailed("Issue on authentication header")
        
        try:
            token = auth_header[1].decode('utf-8')
            print(f'Token received from client: {token}')
        except UnicodeDecodeError:
            raise AuthenticationFailed("Invalid token encoding")
        
        try:
            user_id =decode_access_token(token)
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed("user not found")
        except Exception as e:
            raise AuthenticationFailed(f'Token validation error: {str(e)}')
        #return (user, {'is_admin': user.is_superuser})                 
        return (user, None)      

def create_access_token(id):
    algorithm = "HS256"

    payload={
        'user_id' : id,
        'iat': datetime.now(timezone.utc),  
        'exp': datetime.now(timezone.utc) + timedelta(minutes=15),  # Expiration time (Current time + 30 seconds), 
    }

    secret_key = "@create_access_token!!"

    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

def decode_access_token(token):
    try:
        payload = jwt.decode(token, "@create_access_token!!", algorithms="HS256")
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return {'error': 'Token expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}


def create_refresh_token(id):
    algorithm = "HS256"

    payload={
        'user_id' : id,
        'iat': datetime.now(timezone.utc),  
        'exp': datetime.now(timezone.utc) + timedelta(days=7),  # Expiration time (Current time + 30 seconds), 
    }

    secret_key = "@create_refresh_token!!"

    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token

def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, "@create_refresh_token!!", algorithms="HS256")
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return {'error': 'Token expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}
