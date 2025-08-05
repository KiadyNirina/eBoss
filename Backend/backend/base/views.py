from rest_framework import generics, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
import csv
from django.http import HttpResponse
from django.db.models import Q
from .serializers import (
    CustomTokenObtainPairSerializer,
    EtablissementSerializer, 
    ProfesseurSerializer, 
    EleveSerializer, 
    ParentSerializer,
    UserProfileSerializer
)
from .models import *

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
    
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class EleveViewSet(viewsets.ModelViewSet):
    queryset = Eleve.objects.all().select_related('user', 'etablissement')
    serializer_class = EleveSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        classe = self.request.query_params.get('classe', None)
        statut = self.request.query_params.get('statut', None)
        annee = self.request.query_params.get('annee', None)

        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search)
            )
        if classe:
            queryset = queryset.filter(classe=classe)
        if statut:
            queryset = queryset.filter(statut=statut)
        if annee:
            queryset = queryset.filter(annee_scolaire=annee)

        return queryset

    @action(detail=False, methods=['get'])
    def filter_options(self, request):
        classes = Eleve.objects.values('classe').distinct()
        statuts = [{'value': choice[0], 'label': choice[1]} for choice in Eleve.STATUS_CHOICES]
        annees = Eleve.objects.values('annee_scolaire').distinct().exclude(annee_scolaire__isnull=True)
        return Response({
            'classes': [{'value': c['classe'], 'label': c['classe']} for c in classes],
            'statuts': statuts,
            'annees': [{'value': a['annee_scolaire'], 'label': a['annee_scolaire']} for a in annees]
        })

    @action(detail=False, methods=['post'])
    def bulk(self, request):
        action_type = request.data.get('action')
        ids = request.data.get('ids', [])

        if not ids:
            return Response({'error': 'Aucun étudiant sélectionné'}, status=status.HTTP_400_BAD_REQUEST)

        if action_type == 'delete':
            Eleve.objects.filter(id__in=ids).delete()
            return Response({'message': f'{len(ids)} étudiants supprimés'}, status=status.HTTP_200_OK)
        elif action_type == 'export':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="etudiants.csv"'
            writer = csv.writer(response)
            writer.writerow(['ID', 'Prénom', 'Nom', 'Email', 'Téléphone', 'Classe', 'Établissement'])
            for eleve in Eleve.objects.filter(id__in=ids).select_related('user', 'etablissement'):
                writer.writerow([
                    eleve.id,
                    eleve.user.first_name,
                    eleve.user.last_name,
                    eleve.user.email,
                    eleve.user.telephone,
                    eleve.classe,
                    eleve.etablissement.nom if eleve.etablissement else ''
                ])
            return response
        else:
            return Response({'error': 'Action non valide'}, status=status.HTTP_400_BAD_REQUEST)