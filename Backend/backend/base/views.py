from django.http import JsonResponse
from .models import *
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json
from django.views.decorators.http import require_http_methods
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.db.models import Q
from django.db.models.expressions import RawSQL
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

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStudentUser])
def user_student(request):
    user = request.user
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)

class ListClassesAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role='school')
    serializer_class = StudentListSerializer

class ListStudentsAPIView(generics.ListAPIView):
    serializer_class = StudentListSerializer
    def get_queryset(self):
        name = self.kwargs['name']
        classe = self.kwargs['classe']
        queryset = CustomUser.objects.filter(role='student', school_name=name, student_class=classe)
        return queryset

class ClasseOneAPIView(generics.ListAPIView):
    serializer_class = StudentListSerializer
    def get_queryset(self):
        name = self.kwargs['school_name']
        queryset = CustomUser.objects.filter(role='school', school_name=name)
        return queryset

class StudentSearchedAPIView(generics.ListAPIView) :
    serializer_class = StudentListSerializer
    def get_queryset(self):
        name = self.kwargs['name']
        school = self.kwargs['school']
        queryset = CustomUser.objects.filter(Q(school_name=school) , Q(student_name__icontains=name) | Q(student_lastname__icontains=name))
        return queryset
    
class StudentCountAPIView(APIView):
    def get(self, request, name):
        count = CustomUser.objects.filter(role='student', school_name=name).count()
        return Response({'count': count}, status=status.HTTP_200_OK)
    
class StudentCountByClasseAPIView(APIView):
    def get(self, request, name, classe):
        count = CustomUser.objects.filter(role='student', school_name=name, student_class=classe).count()
        return Response({'count': count}, status=status.HTTP_200_OK)
    
class StudentAPIView(generics.ListAPIView):
    serializer_class = StudentListSerializer
    def get_queryset(self):
        student_id = self.kwargs['student_id']
        queryset = CustomUser.objects.filter(role='student', id=student_id)
        return queryset
    
#list student added recently
class StudentAddedRecentlyAPIView(generics.ListAPIView):
    serializer_class = StudentListSerializer
    def get_queryset(self):
        schoolName = self.kwargs['schoolName']
        queryset = CustomUser.objects.filter(role='student', school_name=schoolName).order_by('-date_joined')[:2]
        return queryset

class MatiereListAPIView(generics.ListAPIView) :
    serializer_class = MatiereListSerializer
    def get_queryset(self):
        school_name = self.kwargs['school_name']
        queryset = Matiere.objects.filter(school=school_name)
        return queryset

class MatiereCreateAPIView(generics.CreateAPIView) :
    queryset = Matiere.objects.all()
    serializer_class = MatiereListSerializer

class InfoFamilialeCreateAPIView(generics.CreateAPIView) :
    queryset = InfoFamiliale.objects.all()
    serializer_class = InfoFamilialeSerializer

@api_view(['PUT', 'PATCH'])
def update_infoFamiliale(request, student_id) :
    try :
        student = InfoFamiliale.objects.get(student=student_id)
    except InfoFamiliale.DoesNotExist:
        return Response({'error':'Student Not Found'}, status=404)
    
    serializer = InfoFamilialeSerializer(student, data=request.data, partial=True)
    if serializer.is_valid() :
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InfoFamilialeAPIView(generics.ListAPIView) :
    serializer_class = InfoFamilialeSerializer
    def get_queryset(self):
        student_id = self.kwargs['student_id']
        queryset = InfoFamiliale.objects.filter(student = student_id)
        return queryset
    
class CourseInfoCreateAPIView(generics.CreateAPIView) :
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseInfoAPIView(generics.ListAPIView) :
    serializer_class = CourseSerializer
    def get_queryset(self):
        school_name = self.kwargs['school_name']
        classe_name = self.kwargs['classe_name']
        queryset = Course.objects.filter(nameSchool=school_name, classe=classe_name)
        return queryset
    
class CourseOneInfoAPIView(generics.RetrieveAPIView) :
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class TeacherListBySchoolAPIView(generics.ListAPIView) :
    serializer_class = CustomUserSerializer
    def get_queryset(self):
        name = self.kwargs['name']
        queryset = CustomUser.objects.filter(role='teacher', school_name=name)
        return queryset
    
class ScheduleCreateAPIView(generics.CreateAPIView) :
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

class ScheduleAPIView(generics.ListAPIView) :
    serializer_class = ScheduleSerializer
    def get_queryset(self):
        school_name = self.kwargs['school_name']
        classe = self.kwargs['classe']
        queryset = Schedule.objects.filter(school = school_name, classe = classe)
        return queryset
    
class NoteCreateAPIView(generics.CreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class NoteListAPIView(generics.ListAPIView) :
    serializer_class = NoteSerializer
    def get_queryset(self):
        school_name = self.kwargs['school_name']
        student_name = self.kwargs['student_name']
        queryset = Note.objects.filter(school=school_name, student=student_name)
        return queryset
    
class NotesAPIView(APIView):
    def get(self, request):
        school = request.query_params.get('school')
        student = request.query_params.get('student')

        notes = Note.objects.all()

        # Filtrer par établissement si un ID est fourni
        if school:
            notes = notes.filter(school=school)

        # Filtrer par élève si un ID est fourni
        if student:
            notes = notes.filter(student=student)

        # Regrouper les notes par school_year et semester
        grouped_notes = {}
        for note in notes:
            key = f"{note.school_year}_{note.semester}"
            if key not in grouped_notes:
                grouped_notes[key] = []
            grouped_notes[key].append({
                'id': note.id,
                'school': note.school,
                'student': note.student,
                'classe': note.classe,
                'school_year': note.school_year,
                'semester': note.semester,
                'matiere': note.matiere,
                'note': note.note,
                'coef': note.coef,
            })

        return Response(grouped_notes)
    
class NoteOneAPIView(generics.RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class RegistrationDataCreateAPIView(generics.CreateAPIView) :
    queryset = RegistrationData.objects.all()    
    serializer_class = RegistrationDataSerializer
