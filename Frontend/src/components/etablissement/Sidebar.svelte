<script>
  import Icon from '@iconify/svelte';
  import { page } from '$app/state';
  import { user } from '$lib/stores';

  export let onClose;

  const navigation = [
    { name: 'Tableau de bord', icon: 'heroicons:home', href: '/etablissement/dashboard' },
    { name: 'Étudiants', icon: 'heroicons:user-group', href: '/etablissement/etudiants' },
    { name: 'Classes', icon: 'heroicons:academic-cap', href: '/etablissement/classes', badge: 'new' },
    { name: 'Matières', icon: 'heroicons:book-open', href: '/etablissement/matieres' },
    { name: 'Professeurs', icon: 'heroicons:academic-cap', href: '/etablissement/professeurs' },
    { name: 'Cours & Emploi du temps', icon: 'heroicons:calendar', href: '/etablissement/cours' },
    { name: 'Notes & Évaluations', icon: 'mdi:clipboard-list-outline', href: '/etablissement/notes' },
    { name: 'Inscriptions', icon: 'heroicons:clipboard-document-check', href: '/etablissement/inscriptions' },
    { name: 'Communication', icon: 'heroicons:chat-bubble-left-right', href: '/etablissement/communication' },
    { name: 'Finances', icon: 'heroicons:currency-dollar', href: '/etablissement/finances' },
    { name: 'Documents', icon: 'heroicons:folder', href: '/etablissement/documents' },
    { name: 'Paramètres', icon: 'heroicons:cog', href: '/etablissement/parametres' }
  ];
</script>

<div class="flex flex-col h-full">
  <!-- Logo -->
  <div class="flex items-center h-16 flex-shrink-0 px-4">
    <img src="/icons/logo.png" class="h-10" alt="" />

    {#if onClose}
      <button
        on:click={onClose}
        class="ml-auto p-1 rounded-md text-white hover:bg-green-700 focus:outline-none"
      >
        <Icon icon="heroicons:x" class="h-6 w-6" />
      </button>
    {/if}
  </div>

  <!-- Navigation -->
  <div class="flex-1 flex flex-col overflow-y-auto">
    <nav class="flex-1 px-2 py-4 space-y-1">
      {#each navigation as item}
        <a
          href={item.href}
          class="group flex items-center px-2 py-2 text-sm font-medium rounded-md
          {page.url.pathname === item.href
            ? 'bg-green-100 text-green-700'
            : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}"
        >
          <Icon
            icon={item.icon}
            class="mr-3 flex-shrink-0 h-6 w-6
            {page.url.pathname === item.href
              ? 'text-green-500'
              : 'text-gray-400 group-hover:text-gray-500'}"
          />
          <span class="flex-1">{item.name}</span>
          {#if item.badge}
            <span class="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
              {item.badge}
            </span>
          {/if}
        </a>
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
            {$user.first_name
              ? `${$user.first_name} ${$user.last_name}`
              : $user.username || 'Utilisateur'}
          </p>

          <a href="/profil" class="text-xs font-medium text-green-600 hover:text-green-500">
            Voir profil
          </a>
        </div>
      </div>
    {:else}
      <div class="flex items-center">
        <div class="h-9 w-9 rounded-full bg-green-100 flex items-center justify-center">
          <Icon icon="heroicons:user-circle" class="h-6 w-6 text-green-600" />
        </div>
        <div class="ml-3">
          <p class="text-sm font-medium text-gray-700">Chargement...</p>
        </div>
      </div>
    {/if}
  </div>
</div>