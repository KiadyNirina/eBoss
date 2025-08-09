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
    UserProfileSerializer,
    AnneeScolaireSerializer,
    ClasseSerializer
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

class AnneeScolaireViewSet(viewsets.ModelViewSet):
    queryset = AnneeScolaire.objects.all()
    serializer_class = AnneeScolaireSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def active(self, request):
        annee_active = AnneeScolaire.objects.filter(est_active=True).first()
        if not annee_active:
            return Response({'detail': 'Aucune année scolaire active'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(annee_active)
        return Response(serializer.data)

class ClasseViewSet(viewsets.ModelViewSet):
    queryset = Classe.objects.all().select_related('annee_scolaire', 'professeur_principal', 'etablissement')
    serializer_class = ClasseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        etablissement_id = self.request.query_params.get('etablissement')
        annee_scolaire_id = self.request.query_params.get('annee_scolaire')
        niveau = self.request.query_params.get('niveau')
        
        if etablissement_id:
            queryset = queryset.filter(etablissement_id=etablissement_id)
        if annee_scolaire_id:
            queryset = queryset.filter(annee_scolaire_id=annee_scolaire_id)
        if niveau:
            queryset = queryset.filter(niveau=niveau)
            
        return queryset

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

class ProfesseurViewSet(viewsets.ModelViewSet):
    queryset = Professeur.objects.all().select_related('user', 'etablissement').prefetch_related('classes')
    serializer_class = ProfesseurSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        matiere = self.request.query_params.get('matiere')
        etablissement = self.request.query_params.get('etablissement')
        
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search)
            )
        if matiere:
            queryset = queryset.filter(matiere__icontains=matiere)
        if etablissement:
            queryset = queryset.filter(etablissement_id=etablissement)
            
        return queryset

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

class EleveViewSet(viewsets.ModelViewSet):
    queryset = Eleve.objects.all().select_related('user', 'etablissement', 'classe')
    serializer_class = EleveSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        classe_id = self.request.query_params.get('classe')
        statut = self.request.query_params.get('statut')
        etablissement_id = self.request.query_params.get('etablissement')

        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search)
            )
        if classe_id:
            queryset = queryset.filter(classe_id=classe_id)
        if statut:
            queryset = queryset.filter(statut=statut)
        if etablissement_id:
            queryset = queryset.filter(etablissement_id=etablissement_id)

        return queryset

    @action(detail=False, methods=['get'])
    def filter_options(self, request):
        classes = Classe.objects.values('id', 'nom').distinct()
        statuts = [{'value': choice[0], 'label': choice[1]} for choice in Eleve.STATUS_CHOICES]
        
        return Response({
            'classes': [{'value': c['id'], 'label': c['nom']} for c in classes],
            'statuts': statuts
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
            writer.writerow(['ID', 'Prénom', 'Nom', 'Email', 'Téléphone', 'Classe', 'Statut', 'Établissement'])
            for eleve in Eleve.objects.filter(id__in=ids).select_related('user', 'etablissement', 'classe'):
                writer.writerow([
                    eleve.id,
                    eleve.user.first_name,
                    eleve.user.last_name,
                    eleve.user.email,
                    eleve.user.telephone,
                    eleve.classe.nom if eleve.classe else '',
                    eleve.get_statut_display(),
                    eleve.etablissement.nom if eleve.etablissement else ''
                ])
            return response
        else:
            return Response({'error': 'Action non valide'}, status=status.HTTP_400_BAD_REQUEST)

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

class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all().select_related('user').prefetch_related('enfants')
    serializer_class = ParentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)