<script>
  import { onMount } from 'svelte';
  import Icon from '@iconify/svelte';
  import { authApi } from '$lib/api';
  
  let rooms = [];
  let etablissementNom = '';
  let loading = true;
  let error = null;
  let successMessage = null;
  let showForm = false;
  
  // Formulaire d'ajout/modification
  let isEditing = false;
  let currentRoomId = null;
  let newRoom = {
    name: '',
    capacite: '',
    etablissement: null
  };
  
  // Filtres
  let searchTerm = '';
  
  onMount(async () => {
    await loadEtablissementInfo();
    await loadRooms();
  });

  async function loadEtablissementInfo() {
    try {
      const profile = await authApi.getProfile();
      etablissementNom = profile.profile?.nom || 'Mon Établissement';
    } catch (err) {
      console.error('Erreur chargement établissement:', err);
      etablissementNom = 'N/A';
    }
  }
  
  async function loadRooms() {
    loading = true;
    error = null;
    try {
      const data = await authApi.getSalles();
      rooms = data.results || data;
    } catch (err) {
      error = err.message || 'Erreur lors du chargement des salles';
      console.error('Erreur:', err);
    } finally {
      loading = false;
    }
  }
  
  function resetForm() {
    isEditing = false;
    currentRoomId = null;
    showForm = false;
    newRoom = {
      name: '',
      capacite: '',
      etablissement: null
    };
  }
  
  function editRoom(room) {
    showForm = true;
    isEditing = true;
    currentRoomId = room.id;
    newRoom = {
      name: room.nom,
      capacite: room.capacite,
      etablissement: room.etablissement
    };
  }
  
  async function saveRoom() {
    if (!newRoom.name || !newRoom.capacite) {
      error = 'Le nom et la capacité sont requis';
      setTimeout(() => error = null, 3000);
      return;
    }
    
    loading = true;
    error = null;
    
    try {
      // Récupérer l'ID de l'établissement depuis le profil ou localStorage
      const profile = await authApi.getProfile();
      const etablissementId = profile.profile?.id || profile.etablissement?.id;
      
      if (!etablissementId) {
        throw new Error('Établissement non trouvé');
      }
      
      const roomData = {
        nom: newRoom.name,
        capacite: parseInt(newRoom.capacite),
        etablissement: etablissementId
      };
      
      if (isEditing && currentRoomId) {
        await authApi.updateSalle(currentRoomId, roomData);
        successMessage = 'Salle modifiée avec succès !';
      } else {
        await authApi.createSalle(roomData);
        successMessage = 'Salle ajoutée avec succès !';
      }
      
      setTimeout(() => successMessage = null, 3000);
      resetForm();
      await loadRooms();
    } catch (err) {
      error = err.message || 'Erreur lors de la sauvegarde';
      console.error('Erreur:', err);
      setTimeout(() => error = null, 3000);
    } finally {
      loading = false;
    }
  }
  
  async function deleteRoom(id) {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette salle ?')) return;
    
    loading = true;
    error = null;
    
    try {
      await authApi.deleteSalle(id);
      successMessage = 'Salle supprimée avec succès !';
      setTimeout(() => successMessage = null, 3000);
      await loadRooms();
    } catch (err) {
      error = err.message || 'Erreur lors de la suppression';
      console.error('Erreur:', err);
      setTimeout(() => error = null, 3000);
    } finally {
      loading = false;
    }
  }
  
  // Filtrage des salles
  $: filteredRooms = rooms.filter(room => 
    room.nom?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    room.capacite?.toString().includes(searchTerm)
  );
</script>

<div class="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
  <!-- En-tête -->
  <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
    <div class="flex items-center justify-between">
      <div>
        <h3 class="text-lg leading-6 font-medium text-gray-900">Gestion des Salles</h3>
        <p class="mt-1 text-sm text-gray-500">
          Liste et configuration des salles de classe et espaces pédagogiques
        </p>
      </div>
      <div class="flex items-center space-x-2">
        <button
          on:click={() => {
            resetForm();
            showForm = true;
          }}
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        >
          <Icon icon="heroicons:plus-sm" class="-ml-1 mr-2 h-5 w-5" />
          Nouvelle salle
        </button>
      </div>
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
  
  <!-- Formulaire d'ajout/modification -->
  {#if showForm}
  <div class="px-4 py-5 sm:p-6 border-b border-gray-200 bg-gray-50">
    <div class="grid grid-cols-1 gap-6 sm:grid-cols-3">
      <div>
        <label for="room-name" class="block text-sm font-medium text-gray-700">
          Nom de la salle <span class="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="room-name"
          bind:value={newRoom.name}
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
          placeholder="Salle 101, Laboratoire, etc."
        />
      </div>
      
      <div>
        <label for="room-capacity" class="block text-sm font-medium text-gray-700">
          Capacité <span class="text-red-500">*</span>
        </label>
        <input
          type="number"
          id="room-capacity"
          bind:value={newRoom.capacite}
          min="1"
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
          placeholder="30"
        />
      </div>
      
      <div class="flex items-end space-x-2">
        <button
          on:click={saveRoom}
          disabled={loading}
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {#if loading}
            <Icon icon="heroicons:arrow-path" class="h-5 w-5 animate-spin mr-2" />
          {/if}
          {isEditing ? 'Modifier' : 'Ajouter'}
        </button>
        
        {#if isEditing}
          <button
            on:click={resetForm}
            class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
          >
            Annuler
          </button>
        {/if}
      </div>
    </div>
  </div>
  {/if}
  
  <!-- Barre de recherche -->
  <div class="px-4 py-3 border-b border-gray-200">
    <div class="relative">
      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <Icon icon="heroicons:magnifying-glass" class="h-5 w-5 text-gray-400" />
      </div>
      <input
        type="text"
        bind:value={searchTerm}
        class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-green-500 focus:border-green-500 sm:text-sm"
        placeholder="Rechercher une salle..."
      />
    </div>
  </div>
  
  <!-- Liste des salles -->
  {#if loading && rooms.length === 0}
    <div class="flex justify-center items-center py-12">
      <Icon icon="heroicons:arrow-path" class="h-8 w-8 animate-spin text-green-600" />
      <span class="ml-2 text-gray-600">Chargement...</span>
    </div>
  {:else if filteredRooms.length === 0}
    <div class="text-center py-12">
      <Icon icon="heroicons:building-office-2" class="h-12 w-12 text-gray-400 mx-auto mb-4" />
      <p class="text-gray-500 text-sm">
        {searchTerm ? 'Aucune salle ne correspond à votre recherche' : 'Aucune salle trouvée'}
      </p>
      {#if !searchTerm}
        <button
          on:click={() => { resetForm(); showForm = true; }}
          class="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-green-700 bg-green-100 hover:bg-green-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        >
          <Icon icon="heroicons:plus-sm" class="-ml-1 mr-2 h-5 w-5" />
          Ajouter une salle
        </button>
      {/if}
    </div>
  {:else}
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Salle
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Capacité
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Établissement
            </th>
            <th scope="col" class="relative px-6 py-3">
              <span class="sr-only">Actions</span>
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          {#each filteredRooms as room}
            <tr class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10 bg-green-100 rounded-full flex items-center justify-center">
                    <Icon icon="heroicons:building-office-2" class="h-6 w-6 text-green-600" />
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{room.nom}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{room.capacite} places</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                  {etablissementNom || 'N/A'}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex justify-end space-x-3">
                  <button
                    on:click={() => editRoom(room)}
                    class="text-green-600 hover:text-green-900"
                  >
                    <Icon icon="heroicons:pencil-square" class="h-5 w-5" />
                  </button>
                  <button
                    on:click={() => deleteRoom(room.id)}
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
      <div class="flex-1 flex justify-between sm:hidden">
        <span class="text-sm text-gray-700">
          Total: <span class="font-medium">{filteredRooms.length}</span> salles
        </span>
      </div>
      <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
        <div>
          <p class="text-sm text-gray-700">
            Affichage de <span class="font-medium">{filteredRooms.length}</span> salle{filteredRooms.length > 1 ? 's' : ''}
            {#if rooms.length > filteredRooms.length}
              sur <span class="font-medium">{rooms.length}</span> au total
            {/if}
          </p>
        </div>
        <div class="flex items-center space-x-4">
          <button
            on:click={loadRooms}
            disabled={loading}
            class="inline-flex items-center px-3 py-1 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
          >
            <Icon icon="heroicons:arrow-path" class={`h-4 w-4 mr-1 ${loading ? 'animate-spin' : ''}`} />
            Rafraîchir
          </button>
        </div>
      </div>
    </div>
  {/if}
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