// src/lib/api.js
import { browser } from '$app/environment';

const API_BASE_URL = 'http://127.0.0.1:8000/school';

async function fetchWithAuth(endpoint, options = {}) {
    const accessToken = browser ? localStorage.getItem('access_token') : null;
    const refreshToken = browser ? localStorage.getItem('refresh_token') : null;
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`;
    }

    const config = {
        ...options,
        headers,
        credentials: 'include',
    };

    let response = await fetch(`${API_BASE_URL}${endpoint}`, config);
    
    if (response.status === 401 && refreshToken && browser) {
        try {
            const newTokens = await refreshAuthToken(refreshToken);
            headers['Authorization'] = `Bearer ${newTokens.access}`;
            response = await fetch(`${API_BASE_URL}${endpoint}`, { ...config, headers });
        } catch (refreshError) {
            authStore.clearTokens();
            throw new Error('Session expirée, veuillez vous reconnecter');
        }
    }
    
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || errorData.message || "Une erreur s'est produite");
    }
    
    return response;
}

async function refreshAuthToken(refreshToken) {
    const response = await fetch(`${API_BASE_URL}/token/refresh/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken })
    });

    if (!response.ok) {
        throw new Error('Échec du rafraîchissement du token');
    }

    const tokens = await response.json();
    authStore.setTokens(tokens);
    return tokens;
}

export const authApi = {
    // Authentification
    login: (username, password) => fetchWithAuth('/token/', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
    }).then(response => response.json()),

    refreshToken: () => {
        const refreshToken = browser ? localStorage.getItem('refresh_token') : null;
        if (!refreshToken) throw new Error('No refresh token');
        return refreshAuthToken(refreshToken);
    },

    // Inscriptions
    registerEtablissement: (data) => fetchWithAuth('/register/etablissement/', {
        method: 'POST',
        body: JSON.stringify(data),
    }).then(response => response.json()),

    registerProfesseur: (data) => fetchWithAuth('/register/professeur/', {
        method: 'POST',
        body: JSON.stringify(data),
    }).then(response => response.json()),

    registerEleve: (data) => fetchWithAuth('/register/eleve/', {
        method: 'POST',
        body: JSON.stringify(data),
    }).then(response => response.json()),

    registerParent: (data) => fetchWithAuth('/register/parent/', {
        method: 'POST',
        body: JSON.stringify(data),
    }).then(response => response.json()),

    // Profil utilisateur
    getProfile: () => fetchWithAuth('/profile/').then(response => response.json()),

    // Gestion des élèves
    getEleves: (filters = {}) => {
        const query = new URLSearchParams(filters).toString();
        return fetchWithAuth(`/api/eleves/?${query}`).then(response => response.json());
    },

    getFilterOptions: () => fetchWithAuth('/api/eleves/filter_options/').then(response => response.json()),

    createEleve: (data) => fetchWithAuth('/api/eleves/', {
        method: 'POST',
        body: JSON.stringify(data),
    }).then(response => response.json()),

    updateEleve: (id, data) => fetchWithAuth(`/api/eleves/${id}/`, {
        method: 'PUT',
        body: JSON.stringify(data),
    }).then(response => response.json()),

    deleteEleve: (id) => fetchWithAuth(`/api/eleves/${id}/`, {
        method: 'DELETE',
    }).then(() => ({ message: 'Élève supprimé' })),

    bulkAction: (action, ids) => {
        if (action === 'export') {
            return fetchWithAuth('/api/eleves/bulk/', {
                method: 'POST',
                body: JSON.stringify({ action, ids }),
            });
        }
        return fetchWithAuth('/api/eleves/bulk/', {
            method: 'POST',
            body: JSON.stringify({ action, ids }),
        }).then(response => response.json());
    },
};

export const authStore = {
    subscribe(callback) {
        if (!browser) {
            callback({
                accessToken: null,
                refreshToken: null,
                isAuthenticated: false,
            });
            return () => {};
        }

        const handler = () => {
            callback({
                accessToken: localStorage.getItem('access_token'),
                refreshToken: localStorage.getItem('refresh_token'),
                isAuthenticated: !!localStorage.getItem('access_token'),
            });
        };

        window.addEventListener('storage', handler);
        handler();
        return () => window.removeEventListener('storage', handler);
    },
    
    setTokens({ access, refresh }) {
        if (!browser) return;
        if (access) localStorage.setItem('access_token', access);
        if (refresh) localStorage.setItem('refresh_token', refresh);
        window.dispatchEvent(new Event('storage'));
    },
    
    clearTokens() {
        if (!browser) return; 
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.dispatchEvent(new Event('storage'));
    },
    
    getAccessToken() {
        return browser ? localStorage.getItem('access_token') : null;
    },
    
    getRefreshToken() {
        return browser ? localStorage.getItem('refresh_token') : null;
    }
};