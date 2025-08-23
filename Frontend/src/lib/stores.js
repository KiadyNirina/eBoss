import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import { authApi, authStore } from '$lib/api';

export const currentView = writable('dashboard');
export const user = writable(null);

authStore.subscribe(async (state) => {
    if (browser && state.isAuthenticated) {
        try {
            const profile = await authApi.getProfile();
            user.set(profile);
        } catch (error) {
            console.error('Erreur lors de la récupération du profil:', error.message);
            authStore.clearTokens();
            user.set(null);
        }
    } else {
        user.set(null);
    }
});