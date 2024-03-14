from rest_framework.exceptions import ValidationError
from social_django.models import UserSocialAuth
from users.models import CustomUser


def create_profile(backend, user, *args, **kwargs):
    """
    Create user profile for social authentication
    """
    UserSocialAuth.objects.get_or_create(user=user)


def create_custom_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    email = details.get('email')
    username_prefix = email.split('@')[0]

    fields = {
        'login': email,
        'email': email,
        'nickname': username_prefix,
    }
    print(f"Fields: {fields}")
    try:
        custom_user = CustomUser.objects.create_user(**fields)

        return {
            'is_new': True,
            'user': custom_user,
        }
    except ValidationError as e:
        custom_user = CustomUser.objects.get(email=fields['email'])
        return {
            'is_new': False,
            'user': custom_user,
        }


def custom_get_username(strategy, details, user=None, *args, **kwargs):
    if user and user.login:
        print(user.login)
        return {'username': user.login, 'nickname': user.login}

    username = details.get('username') or details.get('email') or details.get('nickname') or ' '
    nickname = details.get('username') or details.get('email') or details.get('nickname') or ' '
    return {'username': username, 'nickname': nickname}
