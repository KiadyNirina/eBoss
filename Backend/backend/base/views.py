from rest_framework import generics, status
from rest_framework.response import Response
from .models import Etablissement, Professeur, Eleve, Parent
from .serializers import (
    EtablissementSerializer, 
    ProfesseurSerializer, 
    EleveSerializer, 
    ParentSerializer
)

class EtablissementRegistrationView(generics.CreateAPIView):
    serializer_class = EtablissementSerializer
    
    def create(self, request, *args, **kwargs):
        print("Données reçues:", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Inscription réussie pour l'établissement"},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class ProfesseurRegistrationView(generics.CreateAPIView):
    serializer_class = ProfesseurSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Inscription réussie pour le professeur"},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class EleveRegistrationView(generics.CreateAPIView):
    serializer_class = EleveSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Inscription réussie pour l'élève"},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class ParentRegistrationView(generics.CreateAPIView):
    serializer_class = ParentSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Inscription réussie pour le parent"},
            status=status.HTTP_201_CREATED,
            headers=headers
        )