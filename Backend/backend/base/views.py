from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    CustomTokenObtainPairSerializer,
    EtablissementSerializer, 
    ProfesseurSerializer, 
    EleveSerializer, 
    ParentSerializer,
    UserProfileSerializer
)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class EtablissementRegistrationView(generics.CreateAPIView):
    serializer_class = EtablissementSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        print("Données reçues:", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Génération du token après inscription
        user = serializer.instance.user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "message": "Inscription réussie pour l'établissement",
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED, headers=headers)

class ProfesseurRegistrationView(generics.CreateAPIView):
    serializer_class = ProfesseurSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        user = serializer.instance.user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "message": "Inscription réussie pour le professeur",
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED, headers=headers)

class EleveRegistrationView(generics.CreateAPIView):
    serializer_class = EleveSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        user = serializer.instance.user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "message": "Inscription réussie pour l'élève",
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED, headers=headers)

class ParentRegistrationView(generics.CreateAPIView):
    serializer_class = ParentSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        user = serializer.instance.user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "message": "Inscription réussie pour le parent",
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED, headers=headers)

class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)