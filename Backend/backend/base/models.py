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

class AnneeScolaire(models.Model):
    nom = models.CharField(max_length=50)  # Ex: "2023-2024"
    date_debut = models.DateField()
    date_fin = models.DateField()
    est_active = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['-date_debut']
        verbose_name = "Année scolaire"
        verbose_name_plural = "Années scolaires"

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
    annees_scolaires = models.ManyToManyField(AnneeScolaire, blank=True)
    
    def __str__(self):
        return self.nom

class Classe(models.Model):
    etablissement = models.ForeignKey(Etablissement, on_delete=models.CASCADE, related_name='classes')
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE, related_name='classes')
    nom = models.CharField(max_length=100)  # Ex: "CE1 A" ou "Terminale S"
    niveau = models.CharField(max_length=50)  # Ex: "CE1", "Terminale", etc.
    section = models.CharField(max_length=10, blank=True, null=True)  # Ex: "A", "B", "S", "ES", etc.
    professeur_principal = models.ForeignKey('Professeur', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        section = f" {self.section}" if self.section else ""
        return f"{self.niveau}{section} - {self.annee_scolaire.nom}"
    
    class Meta:
        unique_together = ('etablissement', 'annee_scolaire', 'nom', 'niveau', 'section')
        verbose_name_plural = "Classes"

class Professeur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professeur')
    etablissement = models.ForeignKey(Etablissement, on_delete=models.SET_NULL, null=True, blank=True)
    matiere = models.CharField(max_length=100)
    classes = models.ManyToManyField(Classe, blank=True, related_name='professeurs')
    
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
    classe = models.ForeignKey(Classe, on_delete=models.SET_NULL, null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='actif')
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.classe.nom if self.classe else 'Non assigné'})"

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent')
    enfants = models.ManyToManyField(Eleve, blank=True)
    
    def __str__(self):
        return self.user.get_full_name()