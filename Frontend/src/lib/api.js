// src/lib/api.js
const API_BASE_URL = 'http://127.0.0.1:8000';

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function fetchWithAuth(endpoint, options = {}) {
    const csrfToken = getCookie('csrftoken');
    
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
        'X-Requested-With': 'XMLHttpRequest',
        ...options.headers,
    };

    const config = {
        ...options,
        headers,
        credentials: 'include',
    };

    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
    
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || "Une erreur s'est produite");
    }
    
    return response.json();
}

export const authApi = {
    registerEtablissement: (data) => fetchWithAuth('/school/register/etablissement/', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
    registerProfesseur: (data) => fetchWithAuth('/school/register/professeur/', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
    registerEleve: (data) => fetchWithAuth('/school/register/eleve/', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
    registerParent: (data) => fetchWithAuth('/school/register/parent/', {
        method: 'POST',
        body: JSON.stringify(data),
    }),
};