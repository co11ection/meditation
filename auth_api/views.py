import requests
import jwt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from social_django.utils import psa
from django.http import HttpResponseRedirect
from urllib.parse import urlencode

from users.models import CustomUser
from users.serializers import UsersSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
@psa("social:complete", "google-oauth2")
def google_authenticate(request):
    print(True)
    return Response({"token": request.backend.strategy.session_get("access_token")})


@api_view(["POST"])
@permission_classes([AllowAny])
@psa("social:complete", "apple")
def apple_authenticate(request):
    return Response({"token": request.backend.strategy.session_get("access_token")})


def handle_user_creation(email, username, fcm_token):
    try:
        existing_user = CustomUser.objects.filter(email__exact=email).first()
        if existing_user:
            if fcm_token:
                existing_user.fcm_token = fcm_token
                existing_user.save()
            token_obj, created = Token.objects.get_or_create(user=existing_user)
            token = token_obj.key
            return existing_user, token
        else:
            user = CustomUser.objects.create_user(login=email, email=email,
                                                  nickname=username, fcm_token=fcm_token)
            token_obj, created = Token.objects.get_or_create(user=user)
            token = token_obj.key
            return user, token
    except Exception as e:
        return Response({'Error': {e}})


@api_view(["POST"])
@permission_classes([AllowAny])
def google_signin(request):
    token = request.data.get('token')
    fcm_token = request.data.get('fcm_token')
    response = requests.get('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=' + token)
    if response.status_code == 200:
        user_data = response.json()
        email = user_data.get('email')
        username = user_data.get('name')

        user, token = handle_user_creation(email, username, fcm_token)
        user_serializer = UsersSerializer(user)

        return Response({'success': True, 'user_data': user_data, 'user': user_serializer.data, 'token': token})
    else:
        return Response({'success': False, 'error': 'Token verification failed'})


def sign_in_with_apple_callback(request):
    body_params = request.POST

    query_string = urlencode(body_params)

    redirect = f"intent://callback?{query_string}#Intent;package=com.example.omtogether;scheme=signinwithapple;end"

    print(f"Redirecting to {redirect}")

    return HttpResponseRedirect(redirect)


@api_view(["POST"])
@permission_classes([AllowAny])
def apple_signin(request):
    try:
        fcm_token = request.data.get('fcm_token')
        email = request.data.get('email')
        username = request.data.get('name')

        user, token = handle_user_creation(email, username, fcm_token)
        user_serializer = UsersSerializer(user)

        return Response({'success': True, 'user': user_serializer.data, 'token': token})
    except Exception:
        return Response({'success': False, 'error': 'Internal Server Error'}, status=500)


def fetch_apple_public_key():
    apple_public_key_url = 'https://appleid.apple.com/auth/keys'
    response = requests.get(apple_public_key_url)
    keys = response.json().get('keys')
    return keys[0]['n'], keys[0]['e']


def validate_id_token(id_token):
    apple_public_key_n, apple_public_key_e = fetch_apple_public_key()

    decoded_token = jwt.decode(
        id_token,
        algorithms='RS256',
        audience='com.omtogether.service',
        options={'verify_aud': True},
        key={
            'kty': 'RSA',
            'kid': 'apple_public_key_kid',
            'n': apple_public_key_n,
            'e': apple_public_key_e
        }
    )
    return Response({'Decoded_token': decoded_token}, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def validate_apple_token(request):
    try:
        id_token = request.data.get('idToken')
        return validate_id_token(id_token)
    except Exception as e:
        return Response({'Error': str(e)})
