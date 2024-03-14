from django.urls import path
from . import views

urlpatterns = [
    path("google/", views.google_authenticate, name="google_authenticate"),
    path("apple/", views.apple_authenticate, name="apple_authenticate"),
    path("google_signin/", views.google_signin, name="google_signin"),
    path("apple_signin/", views.apple_signin, name="apple_signin"),
    path("sign_in_with_apple_callback/", views.sign_in_with_apple_callback,
         name="sign_in_with_apple_callback"),
    path("validate_apple_token/", views.validate_apple_token,
         name="validate_apple_token"),
]
