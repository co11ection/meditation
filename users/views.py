from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

# import vonage

from .models import CustomUser
from .serializers import UsersSerializer
from users import db_communication as db
from users import utils


@api_view(["POST"])
@permission_classes([AllowAny])
def registration_get_code(request):
    """
    Получение смс кода для регистрации пользователя или аутентификации пользователя.

    Параметры:
    - login (str): Логин пользователя (номер телефона).


    Возвращает:
    - Статус отправки смс сообщения и сам код.


    Если логин не является номером телефона, возвращает ошибку неверного запроса.
    """
    try:
        values = request.data
        if not utils.is_phone_number(values["login"]):
            return Response(
                "login must be phone number", status=status.HTTP_400_BAD_REQUEST
            )
        phone = values["login"]
        is_registered = False
        if CustomUser.objects.filter(phone_number__contains=utils.ru_phone(phone)):
            is_registered = True
        code, text = utils.send_phone_reset(phone)
        # code = 12345
        # text = "test"
        return Response(
            {
                "code": code,
                "text": text,
                "is_registered": is_registered,
            }
        )
    except Exception as ex:
        return Response(
            {"error": f"Something goes wrong: {ex}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def check_registration(request):
    """
    Проверка регистрации пользователя.

    Параметры:
    - login (str): Логин пользователя (номер телефона или email).


    Возвращает:
    - Статус регистрации пользователя.


    Если логин не является номером телефона, возвращает ошибку неверного запроса.
    """
    try:
        values = request.data
        login = values["login"]
        is_registered = False
        login_is_email = None
        if (not utils.is_phone_number(login)) and (not utils.is_email(login)):
            return Response(
                "login must be phone number or email",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if utils.is_phone_number(login) and CustomUser.objects.filter(
                phone_number__exact=login).exists():
            is_registered = True
            login_is_email = False

        if utils.is_email(login) and CustomUser.objects.filter(
                email__exact=login).exists():
            is_registered = True
            login_is_email = True

        return Response(
            {
                "is_registered": is_registered,
                "login_is_email": login_is_email,
            }
        )
    except Exception as ex:
        return Response(
            {"error": f"Something goes wrong: {ex}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def registration(request):
    """
    Регистрация нового пользователя или аутентификация существующего.

    Параметры:
    - login (str): Логин пользователя (электронная почта или номер телефона).
    - fcm_token (str): Токен FCM для push-уведомлений.
    - nickname (str): Никнейм пользователя

    Возвращает:
    - Если пользователь существует, возвращает ответ с данными авторизации (токен и ID).
    - Если пользователь новый, возвращает ответ с данными регистрации (токен и ID).

    Если логин не является ни электронной почтой, ни номером телефона, возвращает ошибку неверного запроса.
    """
    try:
        values = request.data
        login = values.get("login")
        if (not utils.is_phone_number(login)) and (not utils.is_email(login)):
            return Response(
                "login must be phone number or email",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if utils.is_email(login) and "password" in values:
            token, user = db.add_user(values)
            return Response(
                {
                    "token": token,
                    "id": user.id,
                },
                status=status.HTTP_201_CREATED,
            )
        elif utils.is_phone_number(login) and "password" in values:
            token, user = db.add_user(values)
            return Response(
                {
                    "token": token,
                    "id": user.id,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"error": "Invalid registration request"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    except Exception as ex:
        return Response(
            {"error": f"Something goes wrong: {ex}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def auth(request):
    """
    Аутентификация пользователя.

    Параметры:
    - login (str): Логин пользователя (электронная почта или номер телефона).
    - password (str): Пароль пользователя.
    - fcm_token (str): Токен FCM для push-уведомлений.

    Возвращает:
    - Если пользователь существует и аутентификация успешна, возвращает токен и ID пользователя.
    - Если пользователь не существует или аутентификация не удалась, возвращает ошибку.

    Пример запроса:
    POST /api/auth/
    {
        "login": "user@example.com",
        "password": "password123",
        "fcm_token": "FCM_TOKEN_HERE"
    }

    Пример успешного ответа:
    {
        "authorized": True,
        "token": "TOKEN_STRING_HERE",
        "id": 123
    }

    Пример ответа с ошибкой:
    {
        "authorized": False,
        "error": "User with such login does not exist"
    }
    """
    try:
        values = request.data
        login = values.get("login")
        password = values.get("password")
        fcm_token = values.get("fcm_token")
        user = None
        if not (utils.is_phone_number(login) or utils.is_email(login)):
            return Response(
                {"error": "Login must be email or phone number"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if utils.is_phone_number(login) and "password" in values:
            user = db.get_user(login=login)
        if utils.is_email(login) and "password" in values:
            user = db.get_user(login=login)
        if user is None:
            return Response(
                {"authorized": False, "error": "User with such login does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if utils.is_email(login) and check_password(password, user.password):
            if fcm_token:
                user.fcm_token = fcm_token
                user.save()
            token_obj = Token.objects.get(user=user)
            token = token_obj.key
            return Response(
                {
                    "authorized": True,
                    "token": token,
                    "id": user.id,
                }
            )
        elif utils.is_phone_number(login) and check_password(password, user.password):
            if fcm_token:
                user.fcm_token = fcm_token
                user.save()
            token_obj = Token.objects.get(user=user)
            token = token_obj.key
            return Response(
                {
                    "authorized": True,
                    "token": token,
                    "id": user.id,
                }
            )
        else:
            return Response(
                {"authorized": False, "error": "Wrong credentials"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as ex:
        return Response(
            {"error": f"Something goes wrong: {ex}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request):
    """
    Отправляет код для сброса пароля на телефон или email пользователя.

    Параметры:
    - login (str): Логин пользователя (электронная почта или номер телефона).

    Пример запроса POST:
    POST /api/reset_password/
    {
        "login": "user@example.com"
    }
    """
    try:
        values = request.data
        return Response(db.reset_password1(values))
    except ObjectDoesNotExist:
        return Response("Can't find user", status=status.HTTP_400_BAD_REQUEST)
    except ValidationError as ex:
        return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        return Response(
            {"error": f"Something goes wrong: {ex}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def check_code(request):
    """
    Проверяет код для сброса пароля пользователя.

    Параметры:
    - login (str): Логин пользователя (электронная почта или номер телефона).
    - code (str): Код для сброса пароля.

    Метод:
    - POST: Проверяет переданный код для сброса пароля пользователя.

    Пример запроса POST:
    POST /api/check_code/
    {
    "login": "user@example.com",
    "code": "123456"
    }
    """
    try:
        values = request.data
        return Response(db.check_code(values))
    except ObjectDoesNotExist:
        return Response("Can't find user", status=status.HTTP_400_BAD_REQUEST)
    except ValidationError as ex:
        return Response({"error": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        return Response(
            {"error": f"Something goes wrong: {ex}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password_confirm(request):
    """
    Устанавливает новый пароль пользователя после подтверждения сброса.

    Параметры:
    - login (str): Новый пароль пользователя.

    Метод:
    - POST: Сбрасывает пароль пользователя после подтверждения сброса.

    Пример запроса POST:
    POST /api/reset_password_confirm/
    {
        "password": "new_password_here"
    }

    Пример успешного ответа:
    HTTP/1.1 204 No Content
    """
    try:
        token_key = request.headers.get("Authorization").split(" ")[1]
        token = Token.objects.get(key=token_key)

        values = request.data
        db.reset_password2(token.user, values["password"])
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Token.DoesNotExist:
        return Response("Invalid token", status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response("Can't find user", status=status.HTTP_404_NOT_FOUND)
    except Exception as ex:
        return Response(
            {"error": f"Something goes wrong: {ex}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Получить, обновить или удалить профиль пользователя.

    Параметры:
    - request: объект запроса Django REST framework.

    Методы:
    - GET: Получить информацию о пользователе.
    - PUT: Обновить информацию о пользователе.
    - DELETE: Удалить пользователя.

    Возвращает:
    - Ответ с данными пользователя в случае GET и PUT.
    - Пустой ответ в случае успешного удаления пользователя.
    - Ответ с ошибкой "Пользователь не найден" в случае отсутствия пользователя с указанным ID.

    Пример запроса GET:
    GET /api/users/1/
    Возвращает данные пользователя с ID=1.

    Пример запроса PUT:
    PUT /api/users/1/
    {
        "username": "Новое имя пользователя",
        "email": "новаяпочта@example.com",
        ...
    }
    Обновляет информацию о пользователе с ID=1.

    Пример запроса DELETE:
    DELETE /api/users/1/
    Удаляет пользователя с ID=1.
    """
    try:
        user = request.user

        if user is None:
            return Response(
                {"error": "Can't find user"}, status=status.HTTP_404_NOT_FOUND
            )

        if request.method == "GET":
            serializer = UsersSerializer(user)
            token_obj = Token.objects.get(user=user)
            token = token_obj.key
            serializer_data = serializer.data
            serializer_data["token"] = token

            return Response(serializer_data)

        elif request.method == "PUT":
            serializer = UsersSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == "DELETE":
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as ex:
        return Response(
            {"error": f"Something goes wrong: {ex}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_photo(request):
    """
    Обновить фото пользователя.
    parameters:
      - name: photo
        type: string
        required: true
        description: Base64-encoded image string.

    responses:
      200:
        description: User photo updated successfully.
    """
    try:
        user = request.user
        values = request.data
        db.change_photo(user, values.get("photo"))

        serializer = UsersSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)

    except Exception as ex:
        return Response(
            {"error": f"Something goes wrong: {ex}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
