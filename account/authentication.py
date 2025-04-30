import jwt
from datetime import datetime,timedelta,timezone

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
