import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from base.models import Etablissement

def migrate_coordinates():
    """
    Migre les coordonnées existantes en les marquant comme vérifiées
    """
    establishments = Etablissement.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    )
    
    count = 0
    for est in establishments:
        est.coordinates_verified = True
        est.coordinates_updated_at = timezone.now()
        est.save()
        count += 1
        print(f"✅ {est.nom}: coordonnées vérifiées")
    
    print(f"\nTotal: {count} établissements mis à jour")

if __name__ == "__main__":
    migrate_coordinates()