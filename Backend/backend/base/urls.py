from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

router = DefaultRouter()
router.register(r'eleves', EleveViewSet, basename='eleve')

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('register/etablissement/', EtablissementRegistrationView.as_view(), name='register-etablissement'),
    path('register/professeur/', ProfesseurRegistrationView.as_view(), name='register-professeur'),
    path('register/eleve/', EleveRegistrationView.as_view(), name='register-eleve'),
    path('register/parent/', ParentRegistrationView.as_view(), name='register-parent'),

    path('profile/', UserProfileView.as_view(), name='profile'),
    
    path('api/', include(router.urls)),
]