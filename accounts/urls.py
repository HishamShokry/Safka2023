from django.urls import include, path
from . import views

from rest_framework.routers import DefaultRouter



urlpatterns = [
    path("", views.index, name="index"),
    path("signin", views.signin, name="signin"),
    path("singupMarketer", views.signupMarketer, name="signupMarketer"),
    path("singupVendor", views.signupVendor, name="signupVendor"),
    path("logout", views.user_logout, name="logout"),
    

]
