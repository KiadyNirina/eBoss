import GeocodingService from './geocoding.js';

class GeocodingCache {
    constructor() {
        this.cache = new Map();
        this.MAX_CACHE_SIZE = 100;
        this.CACHE_DURATION = 24 * 60 * 60 * 1000; // 24 heures
    }

    async geocode(address) {
        const key = address.toLowerCase().trim();
        
        // Vérifier le cache
        if (this.cache.has(key)) {
            const cached = this.cache.get(key);
            if (Date.now() - cached.timestamp < this.CACHE_DURATION) {
                console.log('Cache hit:', address);
                return cached.data;
            } else {
                this.cache.delete(key);
            }
        }

        // Géocoder
        try {
            const result = await GeocodingService.geocode(address);
            
            if (result) {
                // Mettre en cache
                this.cache.set(key, {
                    data: result,
                    timestamp: Date.now()
                });

                // Limiter la taille du cache
                if (this.cache.size > this.MAX_CACHE_SIZE) {
                    const firstKey = this.cache.keys().next().value;
                    this.cache.delete(firstKey);
                }
            }

            return result;
        } catch (error) {
            console.error('Erreur de géocodage:', error);
            throw error;
        }
    }

    async reverseGeocode(lat, lng) {
        const key = `${lat.toFixed(6)},${lng.toFixed(6)}`;
        
        if (this.cache.has(key)) {
            const cached = this.cache.get(key);
            if (Date.now() - cached.timestamp < this.CACHE_DURATION) {
                return cached.data;
            }
        }

        const result = await GeocodingService.reverseGeocode(lat, lng);
        
        if (result) {
            this.cache.set(key, {
                data: result,
                timestamp: Date.now()
            });
        }

        return result;
    }

    clearCache() {
        this.cache.clear();
        console.log('Cache vidé');
    }
}

export default new GeocodingCache();