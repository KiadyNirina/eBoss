<script>
  import Icon from '@iconify/svelte';
  
  export let filters;
  
  const classOptions = [
    { value: '', label: 'Toutes les classes' },
    { value: '3ème A', label: '3ème A' },
    { value: '4ème B', label: '4ème B' },
    { value: '5ème C', label: '5ème C' }
  ];
  
  const subjectOptions = [
    { value: '', label: 'Toutes les matières' },
    { value: 'Mathématiques', label: 'Mathématiques' },
    { value: 'Français', label: 'Français' },
    { value: 'Histoire', label: 'Histoire-Géographie' }
  ];
  
  const periodOptions = [
    { value: '', label: 'Toutes les périodes' },
    { value: '1', label: '1er Trimestre' },
    { value: '2', label: '2ème Trimestre' },
    { value: '3', label: '3ème Trimestre' }
  ];
</script>

<div class="mt-6 bg-white shadow-sm rounded-lg p-4 border border-gray-200">
  <div class="grid grid-cols-1 gap-4 sm:grid-cols-4">
    <!-- Filtre Classe -->
    <div>
      <label for="class" class="block text-sm font-medium text-gray-700">Classe</label>
      <select
        id="class"
        name="class"
        bind:value={filters.classe}
        class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm rounded-md"
      >
        {#each classOptions as option}
          <option value={option.value}>{option.label}</option>
        {/each}
      </select>
    </div>
    
    <!-- Filtre Matière -->
    <div>
      <label for="subject" class="block text-sm font-medium text-gray-700">Matière</label>
      <select
        id="subject"
        name="subject"
        bind:value={filters.matiere}
        class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm rounded-md"
      >
        {#each subjectOptions as option}
          <option value={option.value}>{option.label}</option>
        {/each}
      </select>
    </div>
    
    <!-- Filtre Période -->
    <div>
      <label for="period" class="block text-sm font-medium text-gray-700">Période</label>
      <select
        id="period"
        name="period"
        bind:value={filters.periode}
        class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm rounded-md"
      >
        {#each periodOptions as option}
          <option value={option.value}>{option.label}</option>
        {/each}
      </select>
    </div>
    
    <!-- Bouton Appliquer -->
    <div class="flex items-end">
      <button
        type="button"
        on:click={() => dispatch('apply', filters)}
        class="w-full inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
      >
        <Icon icon="heroicons:funnel" class="-ml-1 mr-2 h-5 w-5" />
        Appliquer
      </button>
    </div>
  </div>
</div>