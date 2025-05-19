from django.urls import path
from . import views

app_name = "linauth"

urlpatterns = [
    path("login", views.linlogin, name="login"),
    path("logout", views.linlogout, name="logout"),
    path("register", views.register, name="register"),
    path("captcha", views.send_email_captcha, name="email_captcha"),
]
