from django.urls import path
from .views import *

urlpatterns = [
    path('register/etablissement/', EtablissementRegistrationView.as_view(), name='register-etablissement'),
    path('register/professeur/', ProfesseurRegistrationView.as_view(), name='register-professeur'),
    path('register/eleve/', EleveRegistrationView.as_view(), name='register-eleve'),
    path('register/parent/', ParentRegistrationView.as_view(), name='register-parent'),
]