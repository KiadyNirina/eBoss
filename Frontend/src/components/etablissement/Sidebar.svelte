<script>
  import Icon from '@iconify/svelte';
  import { currentView, user } from '$lib/stores';

  export let onClose;

  const navigation = [
    { name: 'Tableau de bord', icon: 'heroicons:home', view: 'dashboard' },
    { name: 'Étudiants', icon: 'heroicons:user-group', view: 'etudiants' },
    { name: 'Professeurs', icon: 'heroicons:academic-cap', view: 'professeurs' },
    { name: 'Cours & Emploi du temps', icon: 'heroicons:calendar', view: 'cours' },
    { name: 'Notes & Évaluations', icon: 'mdi:clipboard-list-outline', view: 'notes' },
    { name: 'Inscriptions', icon: 'heroicons:clipboard-document-check', view: 'inscriptions' },
    { name: 'Communication', icon: 'heroicons:chat-bubble-left-right', view: 'communication' },
    { name: 'Finances', icon: 'heroicons:currency-dollar', view: 'finances' },
    { name: 'Documents', icon: 'heroicons:folder', view: 'documents' },
    { name: 'Paramètres', icon: 'heroicons:cog', view: 'parametres' }
  ];
</script>

<div class="flex flex-col h-full">
  <!-- Logo -->
  <div class="flex items-center h-16 flex-shrink-0 px-4 bg-green-600">
    <img src="/icons/logo.png" class="h-8 w-8" alt="">
    <span class="ml-2 text-xl font-bold text-white">eBoss</span>
    {#if onClose}
      <button on:click={onClose} class="ml-auto p-1 rounded-md text-white hover:bg-green-700 focus:outline-none">
        <Icon icon="heroicons:x" class="h-6 w-6" />
      </button>
    {/if}
  </div>
  
  <!-- Navigation -->
  <div class="flex-1 flex flex-col overflow-y-auto">
    <nav class="flex-1 px-2 py-4 space-y-1">
      {#each navigation as item}
        <button
          on:click={() => currentView.set(item.view)}
          class="group flex items-center px-2 py-2 text-sm font-medium rounded-md w-full text-left {$currentView === item.view ? 'bg-green-100 text-green-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}"
        >
          <Icon icon={item.icon} class="mr-3 flex-shrink-0 h-6 w-6 {$currentView === item.view ? 'text-green-500' : 'text-gray-400 group-hover:text-gray-500'}" />
          {item.name}
        </button>
      {/each}
    </nav>
  </div>
  
  <!-- User Profile -->
  <div class="flex-shrink-0 flex border-t border-gray-200 p-4">
    {#if $user}
      <div class="flex items-center">
        <div class="h-9 w-9 rounded-full bg-green-100 flex items-center justify-center">
          <Icon icon="heroicons:user-circle" class="h-6 w-6 text-green-600" />
        </div>
        <div class="ml-3">
          <p class="text-sm font-medium text-gray-700">
            {$user.first_name ? `${$user.first_name} ${$user.last_name}` : $user.username || 'Utilisateur'}
          </p>
          <a href="#" class="text-xs font-medium text-green-600 hover:text-green-500">Voir profil</a>
        </div>
      </div>
    {:else}
      <div class="flex items-center">
        <div class="h-9 w-9 rounded-full bg-green-100 flex items-center justify-center">
          <Icon icon="heroicons:user-circle" class="h-6 w-6 text-green-600" />
        </div>
        <div class="ml-3">
          <p class="text-sm font-medium text-gray-700">Chargement...</p>
          <a href="#" class="text-xs font-medium text-green-600 hover:text-green-500">Voir profil</a>
        </div>
      </div>
    {/if}
  </div>
</div>