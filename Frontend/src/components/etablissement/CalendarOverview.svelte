<script>
  import Icon from '@iconify/svelte';
  
  const events = [
    { name: 'Réunion des professeurs', date: 'Aujourd\'hui, 14h', color: 'bg-green-500' },
    { name: 'Date limite paiement', date: 'Demain', color: 'bg-blue-500' },
    { name: 'Conseil de classe 3ème A', date: 'Jeudi, 16h', color: 'bg-purple-500' },
    { name: 'Sortie scolaire', date: 'Vendredi, toute la journée', color: 'bg-yellow-500' }
  ];
</script>

<div class="bg-white shadow rounded-lg overflow-hidden">
  <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
    <div class="flex justify-between items-center">
      <h3 class="text-lg leading-6 font-medium text-gray-900">Calendrier</h3>
      <button class="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
        <Icon icon="heroicons:plus-sm" class="-ml-1 mr-1 h-4 w-4" />
        Ajouter
      </button>
    </div>
  </div>
  <div class="px-4 py-5 sm:p-6">
    <div class="space-y-4">
      {#each events as event}
        <div class="flex items-start">
          <div class={`flex-shrink-0 h-3 w-3 rounded-full mt-1 ${event.color}`}></div>
          <div class="ml-3 flex-1">
            <p class="text-sm font-medium text-gray-900">{event.name}</p>
            <p class="text-sm text-gray-500">{event.date}</p>
          </div>
          <button class="ml-3 text-gray-400 hover:text-gray-500">
            <Icon icon="heroicons:ellipsis-vertical" class="h-5 w-5" />
          </button>
        </div>
      {/each}
    </div>
  </div>
  <div class="bg-gray-50 px-4 py-4 sm:px-6">
    <div class="text-sm">
      <a href="#" class="font-medium text-green-600 hover:text-green-500">
        Voir le calendrier complet
      </a>
    </div>
  </div>
</div>