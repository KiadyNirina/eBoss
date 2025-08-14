<script>
  import { createEventDispatcher } from 'svelte';
  import Icon from '@iconify/svelte';
  import { authApi } from '$lib/api';

  export let filters;
  let classOptions = [];
  let statusOptions = [];
  let yearOptions = [];

  const dispatch = createEventDispatcher();

  async function fetchFilterOptions() {
    try {
      const data = await authApi.getFilterOptions();
      console.log('Filter options:', data);
      classOptions = data.classes;
      statusOptions = data.statuts;
      yearOptions = data.annees;
    } catch (error) {
      console.error('Erreur lors du chargement des options de filtrage:', error.message);
    }
  }

  fetchFilterOptions();

  function resetFilters() {
    filters.search = '';
    filters.classe = '';
    filters.statut = '';
    filters.annee = '';
    dispatch('apply', filters);
  }
</script>

<div class="mt-6 bg-white shadow-sm rounded-lg p-6 border border-gray-200">
  <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
    <!-- Recherche -->
    <div>
      <label for="search" class="block text-sm font-medium text-gray-700">Recherche</label>
      <div class="mt-1 relative rounded-lg shadow-sm bg-gray-50">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Icon icon="heroicons:magnifying-glass" class="h-5 w-5 text-gray-400" />
        </div>
        <input
          type="text"
          name="search"
          id="search"
          bind:value={filters.search}
          class="block w-full pl-10 pr-3 py-2 sm:text-sm border border-gray-300 rounded-lg focus:ring-green-500 focus:border-green-500 placeholder-gray-400"
          placeholder="Nom, email..."
          aria-label="Rechercher par nom ou email"
        />
      </div>
    </div>
    
    <!-- Filtre Classe -->
    <div>
      <label for="class" class="block text-sm font-medium text-gray-700">Classe</label>
      <select
        id="class"
        name="class"
        bind:value={filters.classe}
        class="mt-1 block w-full pl-3 pr-10 py-2 text-base border border-gray-300 rounded-lg bg-gray-50 focus:ring-green-500 focus:border-green-500 sm:text-sm"
        aria-label="Filtrer par classe"
      >
        {#each classOptions as option}
          <option value={option.value}>{option.label}</option>
        {/each}
      </select>
    </div>
    
    <!-- Filtre Statut -->
    <div>
      <label for="status" class="block text-sm font-medium text-gray-700">Statut</label>
      <select
        id="status"
        name="status"
        bind:value={filters.statut}
        class="mt-1 block w-full pl-3 pr-10 py-2 text-base border border-gray-300 rounded-lg bg-gray-50 focus:ring-green-500 focus:border-green-500 sm:text-sm"
        aria-label="Filtrer par statut"
      >
        {#each statusOptions as option}
          <option value={option.value}>{option.label}</option>
        {/each}
      </select>
    </div>
    
    <!-- Filtre Année -->
    <div>
      <label for="year" class="block text-sm font-medium text-gray-700">Année scolaire</label>
      <select
        id="year"
        name="year"
        bind:value={filters.annee}
        class="mt-1 block w-full pl-3 pr-10 py-2 text-base border border-gray-300 rounded-lg bg-gray-50 focus:ring-green-500 focus:border-green-500 sm:text-sm"
        aria-label="Filtrer par année scolaire"
      >
        {#each yearOptions as option}
          <option value={option.value}>{option.label}</option>
        {/each}
      </select>
    </div>
  </div>
  
  <div class="mt-6 flex justify-end space-x-3">
    <!-- Bouton Réinitialiser -->
    <button
      type="button"
      on:click={resetFilters}
      class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
    >
      <Icon icon="heroicons:arrow-path" class="h-5 w-5 mr-2 text-gray-500" />
      Réinitialiser
    </button>
    <!-- Bouton Appliquer -->
    <button
      type="button"
      on:click={() => dispatch('apply', filters)}
      class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
    >
      <Icon icon="heroicons:check" class="h-5 w-5 mr-2" />
      Appliquer les filtres
    </button>
  </div>
</div>