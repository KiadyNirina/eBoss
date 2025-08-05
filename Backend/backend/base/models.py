from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('etablissement', 'Établissement'),
        ('professeur', 'Professeur'),
        ('eleve', 'Élève'),
        ('parent', 'Parent'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    
    # Champs communs
    adresse = models.TextField(blank=True, null=True)
    
    def clean(self):
        if self.user_type == 'etablissement' and not hasattr(self, 'etablissement'):
            if not self.pk: 
                return 
            raise ValidationError("Les établissements doivent avoir un profil établissement complété")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Etablissement(models.Model):
    TYPE_CHOICES = (
        ('ecole', 'École primaire'),
        ('college', 'Collège'),
        ('lycee', 'Lycée'),
        ('universite', 'Université'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='etablissement')
    type_etablissement = models.CharField(max_length=20, choices=TYPE_CHOICES)
    nom = models.CharField(max_length=255)
    adresse = models.TextField()
    
    def __str__(self):
        return self.nom

class Professeur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professeur')
    etablissement = models.ForeignKey(Etablissement, on_delete=models.SET_NULL, null=True, blank=True)
    matiere = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.matiere})"

class Eleve(models.Model):
    STATUS_CHOICES = (
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('suspendu', 'Suspendu'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='eleve')
    etablissement = models.ForeignKey(Etablissement, on_delete=models.SET_NULL, null=True, blank=True)
    classe = models.CharField(max_length=50)
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='actif')
    annee_scolaire = models.CharField(max_length=9, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.classe})"

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent')
    enfants = models.ManyToManyField(Eleve, blank=True)
    
    def __str__(self):
        return self.user.get_full_name()