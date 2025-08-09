from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Etablissement, Professeur, Eleve, Parent, AnneeScolaire, Classe

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email_or_username = attrs.get('email') or attrs.get('username')
        
        if not email_or_username:
            raise serializers.ValidationError("Email ou nom d'utilisateur requis")
        
        user = authenticate(
            request=self.context.get('request'),
            username=email_or_username,
            password=attrs.get('password')
        )
        
        if not user:
            raise serializers.ValidationError("Identifiants invalides")
        
        if not user.is_active:
            raise serializers.ValidationError("Ce compte est désactivé")
        
        refresh = self.get_token(user)
        
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email,
            'user_type': user.user_type,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        
        return data

class AnneeScolaireSerializer(serializers.ModelSerializer):
    est_active = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = AnneeScolaire
        fields = ['id', 'nom', 'date_debut', 'date_fin', 'est_active']
        read_only_fields = ['id']

class ClasseSerializer(serializers.ModelSerializer):
    annee_scolaire = AnneeScolaireSerializer(read_only=True)
    annee_scolaire_id = serializers.PrimaryKeyRelatedField(
        queryset=AnneeScolaire.objects.all(),
        source='annee_scolaire',
        write_only=True
    )
    
    class Meta:
        model = Classe
        fields = '__all__'
    
    def validate(self, data):
        etablissement = data.get('etablissement')
        annee_scolaire = data.get('annee_scolaire')
        
        if self.context['request'].method == 'POST':
            return data
            
        if etablissement and annee_scolaire:
            if not etablissement.annees_scolaires.filter(id=annee_scolaire.id).exists():
                raise serializers.ValidationError(
                    "Cette année scolaire n'est pas associée à l'établissement"
                )
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'telephone', 'user_type', 'profile']
    
    def get_profile(self, obj):
        if hasattr(obj, 'etablissement'):
            return EtablissementSerializer(obj.etablissement).data
        elif hasattr(obj, 'professeur'):
            return ProfesseurSerializer(obj.professeur).data
        elif hasattr(obj, 'eleve'):
            return EleveSerializer(obj.eleve).data
        elif hasattr(obj, 'parent'):
            return ParentSerializer(obj.parent).data
        return None

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 
                 'first_name', 'last_name', 'telephone', 'user_type']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, data):
        if 'username' not in data or not data['username']:
            data['username'] = data['email'] 
        return data
    
    def create(self, validated_data):
        if not validated_data.get('username'):
            validated_data['username'] = validated_data['email']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class EtablissementSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    annees_scolaires = AnneeScolaireSerializer(many=True, read_only=True)
    classes = ClasseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Etablissement
        fields = '__all__'
        extra_kwargs = {
            'nom': {'required': True},
            'type_etablissement': {'required': True},
        }
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['user_type'] = 'etablissement'
        
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        return Etablissement.objects.create(user=user, **validated_data)

class ProfesseurSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    classes = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Classe.objects.all(),
        required=False
    )
    
    class Meta:
        model = Professeur
        fields = '__all__'
        extra_kwargs = {
            'matiere': {'required': True},
        }
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        classes = validated_data.pop('classes', [])
        user_data['user_type'] = 'professeur'
        
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        professeur = Professeur.objects.create(user=user, **validated_data)
        professeur.classes.set(classes)
        return professeur

class EleveSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    classe = serializers.PrimaryKeyRelatedField(
        queryset=Classe.objects.all(),
        required=True
    )
    
    class Meta:
        model = Eleve
        fields = '__all__'
        extra_kwargs = {
            'classe': {'required': True},
        }
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['user_type'] = 'eleve'
        
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        return Eleve.objects.create(user=user, **validated_data)

class ParentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    enfants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Eleve.objects.all(),
        required=False
    )
    
    class Meta:
        model = Parent
        fields = '__all__'
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        enfants = validated_data.pop('enfants', [])
        user_data['user_type'] = 'parent'
        
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        parent = Parent.objects.create(user=user, **validated_data)
        parent.enfants.set(enfants)
        return parent