from django.urls import path
from .views import *

urlpatterns = [
    path('', PostAPIView.as_view()),
]