from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views


app_name = "demo"

router = routers.DefaultRouter()

router.register('home', views.ContactView, basename="contact")

urlpatterns = [
    path('', include(router.urls))
]

urlpatterns += router.urls