<script>
  import Icon from '@iconify/svelte';
  import { fade } from 'svelte/transition';
  import { authApi, authStore } from '$lib/api';
  import { navigate } from 'svelte-routing';
  
  let activeTab = 'etablissement';
  let email = '';
  let password = '';
  let rememberMe = false;
  let isLoading = false;
  let errorMessage = '';
  
  const userTypes = [
    { id: 'etablissement', label: 'Établissement', icon: 'heroicons:building-office-2' },
    { id: 'professeur', label: 'Professeur', icon: 'heroicons:academic-cap' },
    { id: 'eleve', label: 'Élève', icon: 'heroicons:user' },
    { id: 'parent', label: 'Parent', icon: 'heroicons:users' }
  ];
  
  async function handleLogin() {
    if (!email || !password) {
      errorMessage = 'Veuillez remplir tous les champs';
      return;
    }
    
    isLoading = true;
    errorMessage = '';

    try {
      const { access, refresh, user_type } = await authApi.login(email, password);
      
      authStore.setTokens({ access, refresh });
      
      if (rememberMe) {
        document.cookie = `refresh_token=${refresh}; path=/; max-age=${7 * 24 * 60 * 60}`;
      }

      switch (user_type) {
        case 'etablissement':
          navigate('/etablissement/dashboard');
          break;
        case 'professeur':
          navigate('/dashboard/professeur');
          break;
        case 'eleve':
          navigate('/dashboard/eleve');
          break;
        case 'parent':
          navigate('/dashboard/parent');
          break;
        default:
          navigate('/dashboard');
      }
    } catch (err) {
      errorMessage = err.message || 'Erreur de connexion';
      authStore.clearTokens();
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
  <div class="sm:mx-auto sm:w-full sm:max-w-md">
    <a href="/" class="flex h-12 w-12 mx-auto">
      <img src="/icons/logo.png" class="h-12 w-12" alt="Logo">
    </a>
    <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
      Connectez-vous à votre compte
    </h2>
    <p class="mt-2 text-center text-sm text-gray-600">
      Sélectionnez votre profil pour continuer
    </p>
  </div>

  <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
    <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
      <!-- Sélecteur de type d'utilisateur -->
      <div class="mb-6">
        <div class="flex space-x-0 overflow-x-auto pb-2">
          {#each userTypes as type}
            <button
              on:click={() => activeTab = type.id}
              class={`px-4 py-2 rounded-md flex items-center space-x-2 whitespace-nowrap ${activeTab === type.id ? 'bg-green-100 text-green-700' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              <Icon icon={type.icon} class="h-5 w-5" />
              <span>{type.label}</span>
            </button>
          {/each}
        </div>
      </div>
      
      <!-- Formulaire de connexion -->
      {#if errorMessage}
        <div transition:fade class="mb-4 bg-red-50 border-l-4 border-red-400 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <Icon icon="heroicons:exclamation-circle" class="h-5 w-5 text-red-400" />
            </div>
            <div class="ml-3">
              <p class="text-sm text-red-700">{errorMessage}</p>
            </div>
          </div>
        </div>
      {/if}
      
      <form class="space-y-6" on:submit|preventDefault={handleLogin}>
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">
            Adresse email
          </label>
          <div class="mt-1">
            <input
              id="email"
              name="email"
              type="email"
              autocomplete="email"
              bind:value={email}
              required
              class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
            />
          </div>
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">
            Mot de passe
          </label>
          <div class="mt-1">
            <input
              id="password"
              name="password"
              type="password"
              autocomplete="current-password"
              bind:value={password}
              required
              class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
            />
          </div>
        </div>

        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input
              id="remember-me"
              name="remember-me"
              type="checkbox"
              bind:checked={rememberMe}
              class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
            />
            <label for="remember-me" class="ml-2 block text-sm text-gray-900">
              Se souvenir de moi
            </label>
          </div>

          <div class="text-sm">
            <a href="/forgot-password" class="font-medium text-green-600 hover:text-green-500">
              Mot de passe oublié ?
            </a>
          </div>
        </div>

        <div>
          <button
            type="submit"
            disabled={isLoading}
            class={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 ${isLoading ? 'opacity-70 cursor-not-allowed' : ''}`}
          >
            {#if isLoading}
              <Icon icon="heroicons:arrow-path" class="animate-spin h-5 w-5 mr-2" />
              Connexion en cours...
            {:else}
              Se connecter
            {/if}
          </button>
        </div>
      </form>

      <div class="mt-6">
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white text-gray-500">
              Pas encore de compte ?
            </span>
          </div>
        </div>

        <div class="mt-6">
          <a
            href="/signup"
            class="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
          >
            S'inscrire
          </a>
        </div>
      </div>
    </div>
  </div>
</div>