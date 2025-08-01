from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Etablissement, Professeur, Eleve, Parent

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
        
        user = User.objects.create(**user_data)
        
        etablissement = Etablissement.objects.create(user=user, **validated_data)
        return etablissement

class ProfesseurSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    
    class Meta:
        model = Professeur
        fields = '__all__'
        extra_kwargs = {
            'matiere': {'required': True},
        }
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['user_type'] = 'professeur'
        
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        return Professeur.objects.create(user=user, **validated_data)

class EleveSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    
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
    enfants_text = serializers.CharField(
        write_only=True, 
        required=False,
        help_text="Liste des enfants séparés par des virgules"
    )
    
    class Meta:
        model = Parent
        fields = '__all__'
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        enfants_text = validated_data.pop('enfants_text', '')
        user_data['user_type'] = 'parent'
        
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        parent = Parent.objects.create(user=user, **validated_data)
        
        return parent