import { writable, get } from 'svelte/store';

// Initialiser les stores avec des valeurs par défaut appropriées
export const token = writable('');

if(typeof window !== 'undefined') {
    const storedToken = localStorage.getItem('jwtToken');
    token.set(storedToken || '');
}

export const refreshToken = writable('');
export const userProfile = writable(null);
export const userRole = writable('');
export const classes = writable([]);
export const students = writable([]);
export const teacher = writable([]);
export const userStudent = writable(null);
export const studentSearched = writable('');
export const studentsCount = writable(0);
export const studentCount = writable(0);
export const matiere = writable('');
export const schoolName = writable('');
export const infoFamiliale = writable('');
export const courses = writable([]);
export const schedule = writable([]);
export const notes = writable([]);

token.subscribe($token => {
    if (typeof window !== 'undefined') {
        if($token) {
            localStorage.setItem('jwtToken', $token);
        } else {
            localStorage.removeItem('jwtToken');
        }
    }
})

export function getStoreValue(store) {
    let value;
    const unsubscribe = store.subscribe($value => {
        value = $value;
    });
    unsubscribe();
    return value;
}