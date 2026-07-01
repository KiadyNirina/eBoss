<script>
  import Icon from '@iconify/svelte';
  import { user } from '$lib/stores';
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  
  export let onToggleSidebar;
  
  let searchQuery = '';
  let showDropdown = false;
  let showLogoutModal = false;
  
  function toggleDropdown() {
    showDropdown = !showDropdown;
  }
  
  function openLogoutModal() {
    showDropdown = false;
    showLogoutModal = true;
  }
  
  function closeLogoutModal() {
    showLogoutModal = false;
  }
  
  function handleLogout() {
    user.set(null);
    localStorage.removeItem('token');
    closeLogoutModal();
    goto('/login');
  }
  
  onMount(() => {
    function handleClickOutside(event) {
      const dropdown = document.querySelector('.profile-dropdown');
      if (dropdown && !dropdown.contains(event.target)) {
        showDropdown = false;
      }
    }
    
    document.addEventListener('click', handleClickOutside);
    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  });
</script>

<header class="bg-white shadow-sm">
  <div class="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between">
      <!-- Bouton menu mobile -->
      <button
        type="button"
        class="md:hidden bg-white p-1 rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        on:click={onToggleSidebar}
      >
        <Icon icon="heroicons:menu" class="h-6 w-6" />
      </button>
      
      <!-- Barre de recherche -->
      <div class="flex-1 max-w-xs md:max-w-md mx-4">
        <div class="relative text-gray-400 focus-within:text-gray-500">
          <div class="pointer-events-none absolute inset-y-0 left-0 pl-3 flex items-center">
            <Icon icon="heroicons:magnifying-glass" class="h-5 w-5" />
          </div>
          <input
            id="search"
            name="search"
            class="block w-full bg-white py-2 pl-10 pr-3 border border-gray-300 rounded-md leading-5 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 sm:text-sm"
            placeholder="Rechercher"
            type="search"
            bind:value={searchQuery}
          />
        </div>
      </div>
      
      <!-- Actions droite -->
      <div class="flex items-center space-x-4">
        <button class="bg-white p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
          <Icon icon="heroicons:bell" class="h-6 w-6" />
        </button>
        <button class="bg-white p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
          <Icon icon="heroicons:envelope" class="h-6 w-6" />
        </button>
        
        <!-- Profil avec dropdown -->
        <div class="relative ml-3 profile-dropdown">
          <div 
            class="h-8 w-8 rounded-full bg-green-100 flex items-center justify-center cursor-pointer hover:bg-green-200 transition-colors"
            on:click={toggleDropdown}
          >
            <Icon icon="heroicons:user-circle" class="h-6 w-6 text-green-600" />
          </div>
          
          <!-- Menu déroulant -->
          {#if showDropdown}
            <div class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 ring-1 ring-black ring-opacity-5 z-50">
              <div class="px-4 py-2 border-b border-gray-100">
                <p class="text-sm font-medium text-gray-900">
                  {$user.first_name
                  ? `${$user.first_name} ${$user.last_name}`
                  : $user.username || 'Utilisateur'}
                </p>
                <p class="text-xs text-gray-500 truncate">{$user?.email || 'email@exemple.com'}</p>
              </div>
              <a href="/profile" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors">
                <Icon icon="heroicons:user" class="inline h-4 w-4 mr-2" />
                Mon profil
              </a>
              <a href="/settings" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors">
                <Icon icon="heroicons:cog" class="inline h-4 w-4 mr-2" />
                Paramètres
              </a>
              <button 
                on:click={openLogoutModal}
                class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors border-t border-gray-100"
              >
                <Icon icon="heroicons:arrow-right-on-rectangle" class="inline h-4 w-4 mr-2" />
                Se déconnecter
              </button>
            </div>
          {/if}
        </div>
      </div>
    </div>
  </div>
</header>

<!-- Modal de confirmation de déconnexion -->
{#if showLogoutModal}
  <div class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-center justify-center min-h-screen p-4">
      <!-- Overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" on:click={closeLogoutModal}></div>

      <!-- Modal -->
      <div class="relative bg-white rounded-lg shadow-xl max-w-sm w-full mx-auto p-6">
        <div class="flex items-start space-x-4">
          <div class="flex-shrink-0">
            <div class="h-10 w-10 rounded-full bg-red-100 flex items-center justify-center">
              <Icon icon="heroicons:exclamation-triangle" class="h-6 w-6 text-red-600" />
            </div>
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-medium text-gray-900" id="modal-title">
              Déconnexion
            </h3>
            <p class="mt-2 text-sm text-gray-500">
              Êtes-vous sûr de vouloir vous déconnecter ?
            </p>
          </div>
        </div>
        
        <div class="mt-6 flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-3 space-y-3 space-y-reverse sm:space-y-0">
          <button
            type="button"
            class="w-full sm:w-auto px-4 py-2 bg-white border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
            on:click={closeLogoutModal}
          >
            Annuler
          </button>
          <button
            type="button"
            class="w-full sm:w-auto px-4 py-2 bg-red-600 border border-transparent rounded-md text-sm font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            on:click={handleLogout}
          >
            Se déconnecter
          </button>
        </div>
      </div>
    </div>
  </div>
{/if}