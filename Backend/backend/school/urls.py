from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    path('schoolRegistration/', CustomUserCreateView.as_view(), name='signup_school'),
    path('studentRegistration/', CustomUserCreateView.as_view(), name='signup_student'),
    path('schoolLogin/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('schoolLogin/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user_profile/', user_profile, name='user_profile'),
    path('students/<str:school_class>/', get_students_by_class),
    path('schoolClasses/', get_school_classes),
    # path('schoolDetail/', SchoolAPIView.as_view()),
]