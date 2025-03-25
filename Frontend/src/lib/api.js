// src/lib/api.js
const API_BASE_URL = 'http://localhost:8000/';

async function fetchWithAuth(endpoint, options = {}) {
    const token = sessionStorage.getItem('access_token');
    
    const headers = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
    };

    const response = await fetch(`${API_BASE_URL}/${endpoint}`, {
        ...options,
        headers,
    });

    if (!response.ok) throw new Error(await response.text());
    return response.json();
}

export const api = {
    auth: {
        signup: (userData) => fetchWithAuth('school/studentRegistration/', {
            method: 'POST',
            body: JSON.stringify(userData),
        }),
        login: (credentials) => fetchWithAuth('school/schoolLogin/token/', { 
            method: 'POST', 
            body: JSON.stringify(credentials) 
        }),
    },
    students: {
        list: () => fetchWithAuth('students/'),
        create: (studentData) => fetchWithAuth('students/create/', {
            method: 'POST',
            body: JSON.stringify(studentData),
        }),
        delete: (studentId) => fetchWithAuth(`students/delete/${studentId}/`, {
            method: 'DELETE',
        }),
    },
    schools: {
        list: () => fetchWithAuth('school/schoolClasses/', {
            method: 'GET',
        })
    },
    parents: {
        list: () => fetchWithAuth('parents/'),
    },
};