from django.http import JsonResponse
from .models import *
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .permissions import *
from .serializers import *

# Create your views here.
class CustomUserCreateView(generics.CreateAPIView) :
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs) :
        serializer = self.serializer_class(data=request.data, context={'request': request})

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSchoolUser])
def user_profile(request):
    user = request.user
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)

@login_required
@require_http_methods(["GET"])
def get_school_classes(request, school_class):
    if request.user.role != 'school':
        return JsonResponse({'error': 'Non autorisé'}, status=403)
    return JsonResponse({'school_classes': request.user.school_classes})

@login_required
@require_http_methods(["GET"])
def get_students_by_class(request, school_class):
    if request.user.role != 'school':
        return JsonResponse({'error': 'Non autorisé'}, status=403)
    students = CustomUser.objects.filter(
        role='student', 
        student_class=school_class,
        school_name=request.user.school_name
    ).values('student_name', 'student_lastname')
    return JsonResponse({'students': list(students)})