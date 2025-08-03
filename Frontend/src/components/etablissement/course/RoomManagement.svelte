<script>
  import Icon from '@iconify/svelte';
  
  export let rooms;
  
  let newRoom = {
    name: '',
    capacity: '',
    equipment: ''
  };
  
  function addRoom() {
    if (newRoom.name && newRoom.capacity) {
      rooms = [...rooms, {
        id: rooms.length + 1,
        ...newRoom
      }];
      newRoom = { name: '', capacity: '', equipment: '' };
    }
  }
</script>

<div class="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
  <!-- En-tête -->
  <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
    <h3 class="text-lg leading-6 font-medium text-gray-900">Gestion des Salles</h3>
    <p class="mt-1 text-sm text-gray-500">
      Liste et configuration des salles de classe et espaces pédagogiques
    </p>
  </div>
  
  <!-- Formulaire d'ajout -->
  <div class="px-4 py-5 sm:p-6 border-b border-gray-200">
    <div class="grid grid-cols-1 gap-6 sm:grid-cols-4">
      <div class="sm:col-span-1">
        <label for="room-name" class="block text-sm font-medium text-gray-700">Nom de la salle</label>
        <input
          type="text"
          id="room-name"
          bind:value={newRoom.name}
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
          placeholder="Salle 101"
        />
      </div>
      
      <div>
        <label for="room-capacity" class="block text-sm font-medium text-gray-700">Capacité</label>
        <input
          type="number"
          id="room-capacity"
          bind:value={newRoom.capacity}
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
          placeholder="30"
        />
      </div>
      
      <div class="sm:col-span-1">
        <label for="room-equipment" class="block text-sm font-medium text-gray-700">Équipement</label>
        <input
          type="text"
          id="room-equipment"
          bind:value={newRoom.equipment}
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
          placeholder="Projecteur, Tableau"
        />
      </div>
      
      <div class="flex items-end">
        <button
          on:click={addRoom}
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        >
          <Icon icon="heroicons:plus-sm" class="-ml-1 mr-2 h-5 w-5" />
          Ajouter
        </button>
      </div>
    </div>
  </div>
  
  <!-- Liste des salles -->
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
            Équipement
          </th>
          <th scope="col" class="relative px-6 py-3">
            <span class="sr-only">Actions</span>
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        {#each rooms as room}
          <tr class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-10 w-10 bg-green-100 rounded-full flex items-center justify-center">
                  <Icon icon="heroicons:building-office-2" class="h-6 w-6 text-green-600" />
                </div>
                <div class="ml-4">
                  <div class="text-sm font-medium text-gray-900">{room.name}</div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{room.capacity} places</div>
            </td>
            <td class="px-6 py-4">
              <div class="text-sm text-gray-900">{room.equipment}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <div class="flex justify-end space-x-3">
                <a href="#" class="text-green-600 hover:text-green-900">
                  <Icon icon="heroicons:pencil-square" class="h-5 w-5" />
                </a>
                <a href="#" class="text-red-600 hover:text-red-900">
                  <Icon icon="heroicons:trash" class="h-5 w-5" />
                </a>
              </div>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>