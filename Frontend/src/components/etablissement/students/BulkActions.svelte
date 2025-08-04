<script>
  import Icon from '@iconify/svelte';
  
  export let count;
</script>

<div class="bg-green-50 border-l-4 border-green-400 p-4 mb-4">
  <div class="flex items-center justify-between">
    <div class="flex items-center">
      <Icon icon="heroicons:check-circle" class="h-5 w-5 text-green-400" />
      <p class="ml-3 text-sm text-green-700">
        <span class="font-medium">{count} étudiants</span> sélectionnés
      </p>
    </div>
    <div class="flex space-x-3">
      <button
        on:click={() => dispatch('export')}
        class="inline-flex items-center px-3 py-1 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
      >
        <Icon icon="heroicons:arrow-down-tray" class="-ml-1 mr-1 h-4 w-4" />
        Exporter
      </button>
      <button
        on:click={() => dispatch('delete')}
        class="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
      >
        <Icon icon="heroicons:trash" class="-ml-1 mr-1 h-4 w-4" />
        Supprimer
      </button>
    </div>
  </div>
</div>