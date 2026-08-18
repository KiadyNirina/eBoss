<!-- src/components/etablissement/map/FilterBar.svelte -->
<script>
  import { createEventDispatcher } from 'svelte';
  import Icon from '@iconify/svelte';

  export let searchQuery = '';
  export let filterType = 'all';
  export let count = 0;

  const dispatch = createEventDispatcher();
</script>

<div class="p-4 sm:px-5 bg-gray-50/50 border-b border-gray-100 shrink-0 space-y-3">
  <div class="relative">
    <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
      <Icon icon="heroicons:magnifying-glass" class="h-4 w-4 text-gray-400" />
    </div>
    <input
      type="text"
      placeholder="Nom, adresse, type..."
      value={searchQuery}
      on:input={(e) => dispatch('search', e.target.value)}
      class="block w-full pl-10 pr-4 py-2.5 bg-white border border-gray-200 rounded-full text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#20784d]/50 focus:border-[#20784d] transition-all"
    />
  </div>

  <div class="flex gap-2">
    <div class="relative flex-1">
      <select
        value={filterType}
        on:change={(e) => dispatch('filter', e.target.value)}
        class="block w-full pl-3 pr-8 py-2 bg-white border border-gray-200 rounded-full text-sm text-gray-700 appearance-none focus:outline-none focus:ring-2 focus:ring-[#20784d]/50 focus:border-[#20784d] transition-all"
      >
        <option value="all">Tous les types</option>
        <option value="ecole">École primaire</option>
        <option value="college">Collège</option>
        <option value="lycee">Lycée</option>
        <option value="universite">Université</option>
      </select>
      <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
        <Icon icon="heroicons:chevron-down" class="h-4 w-4 text-gray-400" />
      </div>
    </div>

    <button
      on:click={() => dispatch('clear')}
      class="px-4 py-2 text-sm font-medium text-gray-600 bg-white border border-gray-200 rounded-full hover:bg-gray-50 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-200 transition-all flex items-center gap-1"
      title="Réinitialiser"
    >
      <Icon icon="heroicons:arrow-path" class="h-4 w-4" />
    </button>
  </div>

  <div class="text-sm text-gray-600 pt-1 font-medium">
    {count} établissement{count > 1 ? 's' : ''} trouvé{count > 1 ? 's' : ''}
  </div>
</div>