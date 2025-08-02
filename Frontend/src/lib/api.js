// src/lib/api.js
const API_BASE_URL = 'http://127.0.0.1:8000/school';

async function fetchWithAuth(endpoint, options = {}) {
    const accessToken = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');
    
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
    
    // Si token expiré, on tente un refresh
    if (response.status === 401 && refreshToken) {
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
    
    return response.json();
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
    }),

    refreshToken: () => {
        const refreshToken = localStorage.getItem('refresh_token');
        if (!refreshToken) throw new Error('No refresh token');
        return refreshAuthToken(refreshToken);
    },

    // Inscriptions
    registerEtablissement: (data) => fetchWithAuth('/register/etablissement/', {
        method: 'POST',
        body: JSON.stringify(data),
    }),

    registerProfesseur: (data) => fetchWithAuth('/register/professeur/', {
        method: 'POST',
        body: JSON.stringify(data),
    }),

    registerEleve: (data) => fetchWithAuth('/register/eleve/', {
        method: 'POST',
        body: JSON.stringify(data),
    }),

    registerParent: (data) => fetchWithAuth('/register/parent/', {
        method: 'POST',
        body: JSON.stringify(data),
    }),

    // Profil utilisateur
    getProfile: () => fetchWithAuth('/profile/'),
};

export const authStore = {
    subscribe(callback) {
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
        if (access) localStorage.setItem('access_token', access);
        if (refresh) localStorage.setItem('refresh_token', refresh);
        window.dispatchEvent(new Event('storage'));
    },
    
    clearTokens() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.dispatchEvent(new Event('storage'));
    },
    
    getAccessToken() {
        return localStorage.getItem('access_token');
    },
    
    getRefreshToken() {
        return localStorage.getItem('refresh_token');
    }
};