# pip install django djangorestframework Pillow

- création du projet django
# django-admin startproject nom_du_projet

- création de l app
# python manage.py startapp nom_du_app

# pip freeze > requirements.txt

- Ajouter les app créés dans le settings du projet
- Mettre en place la base de données
- Définir le model de chaque app
- Lancer la migration
# python manage.py makemigrations
# python manage.py migrate

- Remplir la base de données
- Créer le serializers.py
- Créer le view
- créer le urls.py de l app
- installer cors_headers
# pip install django-cors-headers

- Ajouter dans le settings.py :
# INSTALLED_APPS = [
#    ...,
#    'corsheaders',
# ]
#
# MIDLLEWARE = [
#    '...',
#    '...',
#    'corsheaders.middleware.CorsMiddleware',
#    '...',
# ]
#
# CORS_ALLOWED_ORIGINS = ['http://127.0.0.1:5173', 'http://localhost:5173']



# FRONTEND

- Afficher les données du backend en format json
# Utilisation du onMount et la fonction fetch





Pour créer une application qui affiche la liste des classes et le nombre d'élèves dans chaque classe, vous pouvez utiliser Django pour le backend et Svelte pour le frontend. Voici un guide étape par étape pour y parvenir :

Étape 1 : Configurer Django
Installer Django :

Si ce n'est pas déjà fait, installez Django :

bash
Copier le code
pip install django
Créer un nouveau projet Django :

bash
Copier le code
django-admin startproject myproject
cd myproject
Créer une application Django :

bash
Copier le code
python manage.py startapp school
Définir les modèles dans school/models.py :

python
Copier le code
from django.db import models

class Classe(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def student_count(self):
        return self.students.count()

class Student(models.Model):
    name = models.CharField(max_length=100)
    classe = models.ForeignKey(Classe, related_name='students', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
Ajouter l'application à INSTALLED_APPS dans myproject/settings.py :

python
Copier le code
INSTALLED_APPS = [
    ...
    'school',
]
Créer et appliquer les migrations :

bash
Copier le code
python manage.py makemigrations
python manage.py migrate
Créer un API pour obtenir les classes et le nombre d'élèves dans school/views.py :

python
Copier le code
from django.http import JsonResponse
from .models import Classe

def class_list(request):
    classes = Classe.objects.all()
    data = [{'name': classe.name, 'student_count': classe.student_count()} for classe in classes]
    return JsonResponse(data, safe=False)
Configurer les URLs dans school/urls.py :

python
Copier le code
from django.urls import path
from .views import class_list

urlpatterns = [
    path('classes/', class_list, name='class_list'),
]
Inclure les URLs de l'application dans myproject/urls.py :

python
Copier le code
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('school/', include('school.urls')),
]
Ajouter des données dans l'administration Django ou utiliser des fixtures.

Étape 2 : Configurer Svelte
Configurer un nouveau projet Svelte :

Si vous ne l'avez pas encore fait, créez un nouveau projet Svelte :

bash
Copier le code
npx degit sveltejs/template svelte-frontend
cd svelte-frontend
npm install
Créer un composant Svelte pour afficher les classes :

Créez un fichier src/ClassList.svelte :

svelte
Copier le code
<script>
  import { onMount } from "svelte";

  let classes = [];

  onMount(async () => {
    const response = await fetch('http://127.0.0.1:8000/school/classes/');
    classes = await response.json();
  });
</script>

<style>
  .class-list {
    max-width: 600px;
    margin: auto;
    padding: 1em;
    background: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  .class-item {
    display: flex;
    justify-content: space-between;
    padding: 0.5em 0;
    border-bottom: 1px solid #ddd;
  }
</style>

<div class="class-list">
  {#if classes.length === 0}
    <p>Loading...</p>
  {:else}
    {#each classes as classe}
      <div class="class-item">
        <span>{classe.name}</span>
        <span>{classe.student_count} students</span>
      </div>
    {/each}
  {/if}
</div>
Utiliser le composant dans src/App.svelte :

svelte
Copier le code
<script>
  import ClassList from './ClassList.svelte';
</script>

<main>
  <h1>Classes</h1>
  <ClassList />
</main>

<style>
  main {
    text-align: center;
    padding: 1em;
    max-width: 800px;
    margin: 0 auto;
  }

  h1 {
    color: #ff6347;
  }
</style>
Lancer l'application Svelte :

bash
Copier le code
npm run dev
Étape 3 : Assurer la communication entre Django et Svelte
Configurer les CORS dans Django :

Installez django-cors-headers pour gérer les requêtes CORS :

bash
Copier le code
pip install django-cors-headers
Ajoutez corsheaders à INSTALLED_APPS dans myproject/settings.py :

python
Copier le code
INSTALLED_APPS = [
    ...
    'corsheaders',
]
Ajoutez le middleware CorsMiddleware :

python
Copier le code
MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    ...
]
Configurez les CORS pour autoriser votre frontend Svelte :

python
Copier le code
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5000",
]
Remarque : Assurez-vous que l'application Svelte fonctionne sur le port 5000, sinon ajustez l'URL en conséquence.

Lancer le serveur Django :

bash
Copier le code
python manage.py runserver
En suivant ces étapes, vous aurez une application Django qui fournit une API RESTful pour les classes et leurs comptes d'élèves, et une application Svelte qui consomme cette API pour afficher les données de manière attrayante.






