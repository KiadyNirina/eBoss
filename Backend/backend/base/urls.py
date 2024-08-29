from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    path('schoolRegistration/', CustomUserCreateView.as_view(), name='signup_school'),
    path('studentRegistration/', CustomUserCreateView.as_view(), name='signup_student'),
    path('schoolLogin/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('schoolLogin/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user_profile/', user_profile, name='user_profile'),
    path('user_student/', user_student, name='user_student'),
    path('schoolClasses/', ListClassesAPIView.as_view()),                                           # liste Etablissement 
    path('schoolClasse/<str:school_name>', ClasseOneAPIView.as_view()),                                      # Detail Etablissement par id
    path('schoolStudents/<str:name>/<str:classe>', ListStudentsAPIView.as_view()),                  # Liste eleves par etablissement et classe
    path('search_students/<str:school>/<str:name>/', StudentSearchedAPIView.as_view()),                          # Liste eleve rechercher
    path('countStudents/<str:name>/', StudentCountAPIView.as_view()),                               # Nombre d eleve dans l etablissement
    path('countStudents/<str:name>/<str:classe>/', StudentCountByClasseAPIView.as_view()),          # Nombre d eleve par etablissment et classe
    path('student/<int:student_id>/', StudentAPIView.as_view()),                                # Liste d eleve par etablissement 
    path('studentAddedRecently/<str:schoolName>/', StudentAddedRecentlyAPIView.as_view()), 
    path('classMatiere/<str:school_name>/', MatiereListAPIView.as_view()),                            # liste des matiere dans l etablissement
    path('createClassMatiere/', MatiereCreateAPIView.as_view()),                                    # Creation de matiere 
    path('createInfoFamiliale/', InfoFamilialeCreateAPIView.as_view()),                             # Creation de l info familiale de l'eleve
    path('infoFamiliale/<int:student_id>/', InfoFamilialeAPIView.as_view()),    
    path('updateInfoFamiliale/<int:student_id>/', update_infoFamiliale),  
    path('courseCreateAPI/', CourseInfoCreateAPIView.as_view()),
    path('courseAPI/<str:school_name>/<str:classe_name>/', CourseInfoAPIView.as_view()),
    path('courseOneAPI/<int:pk>/', CourseOneInfoAPIView.as_view()),
    path('listTeacher/<str:name>/', TeacherListBySchoolAPIView.as_view()),
    path('scheduleCreateView/', ScheduleCreateAPIView.as_view()),
    path('scheduleAPIView/<str:school_name>/<str:classe>', ScheduleAPIView.as_view()),
    path('noteCreateView/', NoteCreateAPIView.as_view()),
    path('noteListAPIView/', NotesAPIView.as_view(), name='notes-by-year-semester'),
    path('noteAPIView/<int:pk>', NoteOneAPIView.as_view()),
    path('createRegistrationData/', RegistrationDataCreateAPIView.as_view()),
    # path('schoolDetail/', SchoolAPIView.as_view()),
]