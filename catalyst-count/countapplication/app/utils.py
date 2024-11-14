
from django.http import JsonResponse
from django.conf import settings
import json
import jwt
class JWTToken:
    """ Encode and decode JWT token """
    @staticmethod
    def encode_token(payload):
        jwt_encoded = jwt.encode(
            {"data": payload},
            settings.SECRET_KEY,
            algorithm="HS256"
        )
        return jwt_encoded

    @staticmethod
    def decode_token(token):
        decoded_token = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        return decoded_token

def generate_token(data):
    payload = {'email': data.get('email')}
    return JWTToken.encode_token(payload)


from rest_framework.permissions import BasePermission
import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed

class JWTAuthentication(BasePermission):
    """
    Custom permission class to authenticate users using JWT tokens.
    """

    def has_permission(self, request, view):
        # Check if the Authorization header exists
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            raise AuthenticationFailed('Authorization header is missing')

        # Extract token from the Authorization header
        token_type, token = auth_header.split()

        if token_type != 'Bearer':
            raise AuthenticationFailed('Authorization header must be a Bearer token')

        try:
            # Decode the token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            # Extract user email from the token payload
            email = payload.get("data", {}).get("email")
            
            if not email:
                raise AuthenticationFailed('Token does not contain valid user email')

            # Check if the user exists and is active
            user = User.objects.filter(email=email).first()
            if not user:
                raise AuthenticationFailed('User not found')

            # Attach the user to the request
            request.user = user

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.DecodeError:
            raise AuthenticationFailed('Error decoding token')

        return True


class CookieJWTAuthentication(BasePermission):
    """
    Custom permission class to authenticate users based on a JWT token in cookies.
    """

    def has_permission(self, request, view):
        # Look for JWT token in cookies
        token = request.COOKIES.get('jwt_token')
        
        if not token:
            return False

        try:
            # Decode token
            payload = JWTToken.decode_token(token)
            user = User.objects.filter(email=payload['data']['email']).first()

            if not user:
                return False

            request.user = user  # Set the authenticated user on the request
            return True

        except Exception as e:
            print("Token decoding failed:", e)
            return False
