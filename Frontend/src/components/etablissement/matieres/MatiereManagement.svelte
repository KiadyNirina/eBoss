<script>
  import { onMount } from 'svelte';
  import Icon from '@iconify/svelte';
  import { authApi } from '$lib/api';
  
  let matieres = [];
  let loading = true;
  let error = null;
  let successMessage = null;
  
  let showForm = false;

  let etablissementId = null;
  
  // Formulaire
  let isEditing = false;
  let currentMatiereId = null;
  let newMatiere = {
    nom: '',
    description: '',
    etablissement: null
  };
  
  // Filtres
  let searchTerm = '';
  let filteredMatieres = [];
  
  onMount(async () => {
    await loadData();
  });
  
  async function loadData() {
    loading = true;
    error = null;
    try {
      const profile = await authApi.getProfile();
      etablissementId = profile.profile?.id || profile.etablissement?.id;
      
      if (!etablissementId) {
        throw new Error('Établissement non trouvé');
      }
      
      const data = await authApi.getMatieres({ etablissement: etablissementId });
      matieres = data.results || data;
      
      applyFilters();
    } catch (err) {
      error = err.message || 'Erreur lors du chargement des matières';
      console.error('Erreur:', err);
    } finally {
      loading = false;
    }
  }
  
  function applyFilters() {
    let result = [...matieres];
    
    if (searchTerm) {
      const search = searchTerm.toLowerCase();
      result = result.filter(m => 
        m.nom?.toLowerCase().includes(search) ||
        m.description?.toLowerCase().includes(search)
      );
    }
    
    filteredMatieres = result;
  }
  
  function resetForm() {
    isEditing = false;
    currentMatiereId = null;
    showForm = false;
    newMatiere = {
      nom: '',
      description: '',
      etablissement: etablissementId
    };
  }
  
  function openAddForm() {
    resetForm();
    showForm = true;
  }
  
  function editMatiere(matiere) {
    isEditing = true;
    currentMatiereId = matiere.id;
    showForm = true;
    newMatiere = {
      nom: matiere.nom,
      description: matiere.description || '',
      etablissement: matiere.etablissement
    };
  }
  
  async function saveMatiere() {
    if (!newMatiere.nom) {
      error = 'Le nom de la matière est obligatoire';
      setTimeout(() => error = null, 3000);
      return;
    }
    
    loading = true;
    error = null;
    
    try {
      const matiereData = {
        nom: newMatiere.nom,
        description: newMatiere.description || '',
        etablissement: etablissementId
      };
      
      if (isEditing && currentMatiereId) {
        await authApi.updateMatiere(currentMatiereId, matiereData);
        successMessage = 'Matière modifiée avec succès !';
      } else {
        await authApi.createMatiere(matiereData);
        successMessage = 'Matière ajoutée avec succès !';
      }
      
      setTimeout(() => successMessage = null, 3000);
      resetForm();
      await loadData();
    } catch (err) {
      error = err.message || 'Erreur lors de la sauvegarde';
      console.error('Erreur:', err);
      setTimeout(() => error = null, 3000);
    } finally {
      loading = false;
    }
  }
  
  async function deleteMatiere(id) {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette matière ?')) return;
    
    loading = true;
    error = null;
    
    try {
      await authApi.deleteMatiere(id);
      successMessage = 'Matière supprimée avec succès !';
      setTimeout(() => successMessage = null, 3000);
      await loadData();
    } catch (err) {
      error = err.message || 'Erreur lors de la suppression';
      console.error('Erreur:', err);
      setTimeout(() => error = null, 3000);
    } finally {
      loading = false;
    }
  }
  
  // Obtenir une couleur pour chaque matière
  function getMatiereColor(index) {
    const colors = [
      'bg-blue-100 text-blue-800',
      'bg-green-100 text-green-800',
      'bg-purple-100 text-purple-800',
      'bg-yellow-100 text-yellow-800',
      'bg-pink-100 text-pink-800',
      'bg-indigo-100 text-indigo-800',
      'bg-red-100 text-red-800',
      'bg-teal-100 text-teal-800'
    ];
    return colors[index % colors.length];
  }
  
  $: applyFilters();
</script>

<div>
  <!-- En-tête -->
  <div class="sm:flex sm:items-center justify-between">
    <div class="mb-4 sm:mb-0">
      <h1 class="text-2xl font-bold text-gray-900">Gestion des Matières</h1>
      <p class="mt-2 text-sm text-gray-700">
        {matieres.length} matière au total
      </p>
    </div>
    <div class="flex space-x-3">
      <button
        on:click={openAddForm}
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
      >
        <Icon icon="heroicons:plus-sm" class="-ml-1 mr-2 h-5 w-5" />
        Nouvelle matière
      </button>
    </div>
  </div>
  
  <!-- Messages -->
  {#if successMessage}
    <div class="m-4 p-4 bg-green-50 border border-green-200 rounded-md">
      <div class="flex items-center">
        <Icon icon="heroicons:check-circle" class="h-5 w-5 text-green-400 mr-2" />
        <p class="text-sm text-green-700">{successMessage}</p>
      </div>
    </div>
  {/if}
  
  {#if error}
    <div class="m-4 p-4 bg-red-50 border border-red-200 rounded-md">
      <div class="flex items-center">
        <Icon icon="heroicons:x-circle" class="h-5 w-5 text-red-400 mr-2" />
        <p class="text-sm text-red-700">{error}</p>
      </div>
    </div>
  {/if}
  
  <!-- Formulaire -->
  {#if showForm}
    <div class="mt-6 mb-6 p-4 border border-gray-200 rounded-lg bg-gray-50">
      <h4 class="text-sm font-medium text-gray-700 mb-4">
        {isEditing ? 'Modifier la matière' : 'Ajouter une nouvelle matière'}
      </h4>
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div>
          <label for="matiere-nom" class="block text-xs font-medium text-gray-700">
            Nom <span class="text-red-500">*</span>
          </label>
          <input
            type="text"
            id="matiere-nom"
            bind:value={newMatiere.nom}
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-1.5 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
            placeholder="Ex: Mathématiques"
          />
        </div>
        
        <div class="sm:col-span-2">
          <label for="matiere-description" class="block text-xs font-medium text-gray-700">
            Description
          </label>
          <input
            type="text"
            id="matiere-description"
            bind:value={newMatiere.description}
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-1.5 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
            placeholder="Description de la matière"
          />
        </div>
        
        <div class="flex items-end space-x-2">
          <button
            on:click={saveMatiere}
            disabled={loading}
            class="inline-flex items-center px-4 py-1.5 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {#if loading}
              <Icon icon="heroicons:arrow-path" class="h-4 w-4 animate-spin mr-1" />
            {/if}
            {isEditing ? 'Modifier' : 'Ajouter'}
          </button>
          
          <button
            on:click={resetForm}
            class="inline-flex items-center px-4 py-1.5 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
          >
            Annuler
          </button>
        </div>
      </div>
    </div>
  {/if}
  
  <!-- Recherche -->
  <div class="mt-6 bg-white shadow-sm rounded-lg p-6 border border-gray-200">
    <div>
      <label for="search" class="block text-sm font-medium text-gray-700">Recherche</label>
      <div class="mt-1 relative rounded-lg shadow-sm bg-gray-50">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Icon icon="heroicons:magnifying-glass" class="h-5 w-5 text-gray-400" />
        </div>
        <input
          type="text"
          id="search"
          bind:value={searchTerm}
          class="block w-full pl-9 pr-3 py-1.5 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-green-500 focus:border-green-500 sm:text-sm"
          placeholder="Rechercher une matière..."
          on:input={applyFilters}
        />
      </div>
    </div>
  </div>
  
  <!-- Liste des matières -->
  <div class="mt-6 shadow-sm border border-gray-200 rounded-lg overflow-hidden">
  {#if loading && matieres.length === 0}
    <div class="flex justify-center items-center py-12">
      <Icon icon="heroicons:arrow-path" class="h-8 w-8 animate-spin text-green-600" />
      <span class="ml-2 text-gray-600">Chargement...</span>
    </div>
  {:else if filteredMatieres.length === 0}
    <div class="text-center py-12">
      <Icon icon="heroicons:book-open" class="h-12 w-12 text-gray-400 mx-auto mb-4" />
      <p class="text-gray-500 text-sm">
        {searchTerm ? 'Aucune matière ne correspond à votre recherche' : 'Aucune matière trouvée'}
      </p>
      {#if !searchTerm}
        <button
          on:click={openAddForm}
          class="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-green-700 bg-green-100 hover:bg-green-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        >
          <Icon icon="heroicons:plus-sm" class="-ml-1 mr-2 h-5 w-5" />
          Ajouter une matière
        </button>
      {/if}
    </div>
  {:else}
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Matière
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Description
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Cours associés
            </th>
            <th scope="col" class="relative px-6 py-3">
              <span class="sr-only">Actions</span>
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          {#each filteredMatieres as matiere, index}
            <tr class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class={`flex-shrink-0 h-10 w-10 rounded-full flex items-center justify-center ${getMatiereColor(index)}`}>
                    <Icon icon="heroicons:book-open" class="h-5 w-5" />
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{matiere.nom}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm text-gray-900 max-w-xs truncate">{matiere.description || '-'}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">
                  {matiere.cours_count || 0} cours
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex justify-end space-x-3">
                  <button
                    on:click={() => editMatiere(matiere)}
                    class="text-green-600 hover:text-green-900"
                  >
                    <Icon icon="heroicons:pencil-square" class="h-5 w-5" />
                  </button>
                  <button
                    on:click={() => deleteMatiere(matiere.id)}
                    class="text-red-600 hover:text-red-900"
                  >
                    <Icon icon="heroicons:trash" class="h-5 w-5" />
                  </button>
                </div>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
    
    <!-- Statistiques -->
    <div class="bg-gray-50 px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
      <div class="text-sm text-gray-700">
        Affichage de <span class="font-medium">{filteredMatieres.length}</span> matière{filteredMatieres.length > 1 ? 's' : ''}
        {#if matieres.length > filteredMatieres.length}
          sur <span class="font-medium">{matieres.length}</span> au total
        {/if}
      </div>
      <button
        on:click={loadData}
        disabled={loading}
        class="inline-flex items-center px-3 py-1 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
      >
        <Icon icon="heroicons:arrow-path" class={`h-4 w-4 mr-1 ${loading ? 'animate-spin' : ''}`} />
        Rafraîchir
      </button>
    </div>
  {/if}
  </div>
</div>

<style>
  .animate-spin {
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
</style>