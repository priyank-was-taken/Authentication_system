from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from rest_framework import views, viewsets, permissions
from . import  serializers
from demo.models import Contact


# Create your views here.

class ContactView(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = serializers.ContactSerializer
    permission_classes = [
        permissions.AllowAny
    ]
