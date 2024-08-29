from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, JSONParser
from django.core.files.storage import FileSystemStorage
from .models import Post
from .serializers import PostSerializer

# Create your views here.
class PostAPIView(generics.ListAPIView) :
    queryset = Post.objects.all()
    serializer_class = PostSerializer
