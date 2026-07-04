# services/geocoding.py
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class GeocodingService:
    """Service de géocodage d'adresses"""
    
    @staticmethod
    def geocode_with_nominatim(address):
        """
        Géocode une adresse avec Nominatim (OpenStreetMap) - Gratuit
        """
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': address,
                'format': 'json',
                'limit': 1,
                'addressdetails': 1
            }
            
            headers = {
                'User-Agent': 'VotreApplication/1.0'  # Obligatoire pour Nominatim
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data and len(data) > 0:
                return {
                    'latitude': float(data[0]['lat']),
                    'longitude': float(data[0]['lon']),
                    'display_name': data[0]['display_name']
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Erreur de géocodage Nominatim: {str(e)}")
            return None
    
    @staticmethod
    def geocode_with_google(address, api_key=None):
        """
        Géocode une adresse avec Google Geocoding API - Payant mais plus précis
        """
        try:
            api_key = api_key or getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
            
            if not api_key:
                logger.warning("Clé API Google Maps non configurée")
                return None
            
            url = "https://maps.googleapis.com/maps/api/geocode/json"
            params = {
                'address': address,
                'key': api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                result = data['results'][0]
                location = result['geometry']['location']
                
                return {
                    'latitude': location['lat'],
                    'longitude': location['lng'],
                    'display_name': result['formatted_address']
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Erreur de géocodage Google: {str(e)}")
            return None
    
    @staticmethod
    def geocode_address(address, use_google=False):
        """
        Géocode une adresse avec la méthode spécifiée
        """
        if use_google:
            result = GeocodingService.geocode_with_google(address)
            if result:
                return result
        
        # Fallback sur Nominatim
        return GeocodingService.geocode_with_nominatim(address)
    
    @staticmethod
    def batch_geocode_addresses(establishments):
        """
        Géocode en lot plusieurs établissements
        """
        results = []
        for est in establishments:
            coords = GeocodingService.geocode_address(est.adresse)
            if coords:
                est.latitude = coords['latitude']
                est.longitude = coords['longitude']
                est.save()
                results.append({
                    'id': est.id,
                    'nom': est.nom,
                    'success': True,
                    'latitude': coords['latitude'],
                    'longitude': coords['longitude']
                })
            else:
                results.append({
                    'id': est.id,
                    'nom': est.nom,
                    'success': False,
                    'error': 'Adresse non trouvée'
                })
        return results