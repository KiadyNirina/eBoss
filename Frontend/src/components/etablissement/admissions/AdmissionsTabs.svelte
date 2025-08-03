<script>
  import Icon from '@iconify/svelte';
  export let activeTab;
  
  const tabs = [
    { id: 'en_cours', name: 'En cours', icon: 'heroicons:inbox', count: 88 },
    { id: 'acceptees', name: 'Acceptées', icon: 'heroicons:check-circle', count: 124 },
    { id: 'rejetees', name: 'Rejetées', icon: 'heroicons:x-circle', count: 33 },
    { id: 'archivees', name: 'Archivées', icon: 'heroicons:archive-box', count: 0 }
  ];
</script>

<div class="border-b border-gray-200">
  <nav class="-mb-px flex space-x-8">
    {#each tabs as tab}
      <button
        on:click={() => activeTab = tab.id}
        class={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center ${activeTab === tab.id ? 'border-green-500 text-green-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
      >
        <Icon icon={tab.icon} class={`mr-2 h-5 w-5 ${activeTab === tab.id ? 'text-green-500' : 'text-gray-400'}`} />
        {tab.name}
        {#if tab.count > 0}
          <span class={`ml-2 py-0.5 px-2 rounded-full text-xs font-medium ${activeTab === tab.id ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
            {tab.count}
          </span>
        {/if}
      </button>
    {/each}
  </nav>
</div>