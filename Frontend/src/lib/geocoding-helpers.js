// src/lib/geocoding-helpers.js

/**
 * Formate une coordonnée pour respecter les contraintes Django
 * @param {number} value - La coordonnée à formater
 * @param {string} type - 'lat' ou 'lng'
 * @returns {number} - La coordonnée formatée
 */
export function formatCoordinate(value, type = 'lat') {
    if (value === null || value === undefined || isNaN(value)) {
        return null;
    }
    
    // Arrondir à 8 décimales maximum (respecte max_digits)
    const formatted = Number(parseFloat(value).toFixed(8));
    
    if (type === 'lat') {
        // Latitude: -90 à 90
        return Math.max(-90, Math.min(90, formatted));
    } else {
        // Longitude: -180 à 180
        return Math.max(-180, Math.min(180, formatted));
    }
}

/**
 * Valide et formate une paire de coordonnées
 * @param {number} lat - Latitude
 * @param {number} lng - Longitude
 * @returns {Object} - { lat, lng, valid, errors }
 */
export function validateAndFormatCoordinates(lat, lng) {
    const errors = [];
    
    // Vérifier que ce sont des nombres
    if (isNaN(lat) || isNaN(lng)) {
        errors.push('Veuillez saisir des nombres valides pour la latitude et la longitude');
        return { lat: null, lng: null, valid: false, errors };
    }
    
    // Vérifier la plage de la latitude
    if (lat < -90 || lat > 90) {
        errors.push('La latitude doit être comprise entre -90 et 90 degrés');
    }
    
    // Vérifier la plage de la longitude
    if (lng < -180 || lng > 180) {
        errors.push('La longitude doit être comprise entre -180 et 180 degrés');
    }
    
    // Formater les coordonnées (arrondi à 8 décimales)
    const formattedLat = Number(parseFloat(lat).toFixed(8));
    const formattedLng = Number(parseFloat(lng).toFixed(8));
    
    // Vérifier la précision (max 8 décimales)
    const latDecimals = String(lat).split('.')[1]?.length || 0;
    const lngDecimals = String(lng).split('.')[1]?.length || 0;
    
    // Vérifier le nombre total de chiffres
    const latDigits = String(formattedLat).replace('-', '').replace('.', '').length;
    const lngDigits = String(formattedLng).replace('-', '').replace('.', '').length;
    
    if (latDigits > 10) {
        errors.push('La latitude ne peut pas avoir plus de 10 chiffres au total');
    }
    
    if (lngDigits > 11) {
        errors.push('La longitude ne peut pas avoir plus de 11 chiffres au total');
    }
    
    return {
        lat: formattedLat,
        lng: formattedLng,
        valid: errors.length === 0,
        errors
    };
}

/**
 * Formate les coordonnées pour l'affichage
 * @param {number} lat - Latitude
 * @param {number} lng - Longitude
 * @param {number} decimals - Nombre de décimales à afficher
 * @returns {string} - Coordonnées formatées
 */
export function formatCoordinatesDisplay(lat, lng, decimals = 6) {
    if (lat === null || lng === null || isNaN(lat) || isNaN(lng)) {
        return 'N/A';
    }
    return `${parseFloat(lat).toFixed(decimals)}, ${parseFloat(lng).toFixed(decimals)}`;
}

/**
 * Vérifie si les coordonnées sont valides
 * @param {number} lat - Latitude
 * @param {number} lng - Longitude
 * @returns {boolean} - True si valides
 */
export function isValidCoordinates(lat, lng) {
    if (lat === null || lng === null || isNaN(lat) || isNaN(lng)) {
        return false;
    }
    return lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180;
}

/**
 * Nettoie une chaîne de coordonnées
 * @param {string} value - La chaîne à nettoyer
 * @returns {number|null} - La coordonnée nettoyée ou null
 */
export function cleanCoordinateString(value) {
    if (!value || value.trim() === '') {
        return null;
    }
    
    // Remplacer la virgule par un point pour les nombres décimaux
    const cleaned = value.trim().replace(',', '.');
    const num = parseFloat(cleaned);
    
    if (isNaN(num)) {
        return null;
    }
    
    return num;
}

export default {
    formatCoordinate,
    validateAndFormatCoordinates,
    formatCoordinatesDisplay,
    isValidCoordinates,
    cleanCoordinateString
};