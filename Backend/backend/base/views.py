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
        etablissement = serializer.save()  # On récupère l'instance créée
        
        # Génération du token
        user = etablissement.user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "message": "Inscription réussie pour l'établissement",
            "etablissement": {
                "id": etablissement.id,
                "nom": etablissement.nom,
                "type_etablissement": etablissement.type_etablissement
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

class AnneeScolaireViewSet(viewsets.ModelViewSet):
    queryset = AnneeScolaire.objects.all().order_by('-date_debut')
    serializer_class = AnneeScolaireSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        annee = self.get_object()
        # Désactive toutes les autres années
        AnneeScolaire.objects.exclude(pk=pk).update(est_active=False)
        # Active l'année sélectionnée
        annee.est_active = True
        annee.save()
        return Response({'status': 'année scolaire activée'})

    @action(detail=False, methods=['get'])
    def current(self, request):
        annee_active = AnneeScolaire.objects.filter(est_active=True).first()
        if not annee_active:
            return Response({'detail': 'Aucune année scolaire active'}, 
                          status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(annee_active)
        return Response(serializer.data)

class ClasseViewSet(viewsets.ModelViewSet):
    serializer_class = ClasseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        etablissement_id = self.request.query_params.get('etablissement')
        queryset = Classe.objects.all()
        if etablissement_id:
            queryset = queryset.filter(etablissement_id=etablissement_id)
        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        etablissement = serializer.validated_data['etablissement']
        annee_scolaire = serializer.validated_data['annee_scolaire']
        
        # Crée d'abord l'association
        etablissement.annees_scolaires.add(annee_scolaire)
        
        # Puis sauvegarde la classe
        serializer.save()

        # Met à jour le cache des associations
        etablissement.refresh_from_db()

    def perform_update(self, serializer):
        instance = self.get_object()
        new_annee = serializer.validated_data.get('annee_scolaire', instance.annee_scolaire)
        
        if new_annee != instance.annee_scolaire:
            if not instance.etablissement.annees_scolaires.filter(id=new_annee.id).exists():
                raise serializers.ValidationError({
                    'annee_scolaire': "Cette année scolaire n'est pas associée à l'établissement"
                })
        
        serializer.save()

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
        etablissement_id = request.query_params.get('etablissement')
        
        if not etablissement_id and hasattr(request.user, 'etablissement'):
            etablissement_id = request.user.etablissement.id

        if not etablissement_id:
            return Response({'error': 'Établissement requis'}, status=400)

        classes = Classe.objects.filter(
            etablissement_id=etablissement_id
        ).distinct().values('id', 'nom', 'annee_scolaire__nom')

        annees = AnneeScolaire.objects.filter(
            etablissement__id=etablissement_id
        ).distinct().values('id', 'nom')

        return Response({
            'classes': [{
                'value': c['id'],
                'label': f"{c['nom']} ({c['annee_scolaire__nom']})" 
            } for c in classes],
            'annees': [{
                'value': a['id'],
                'label': a['nom']
            } for a in annees],
            'statuts': [{
                'value': choice[0], 
                'label': choice[1]
            } for choice in Eleve.STATUS_CHOICES]
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