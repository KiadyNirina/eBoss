<script>
  import Icon from '@iconify/svelte';
  
  export let currentFolder;
  export let navigateUp;
</script>

<nav class="flex" aria-label="Breadcrumb">
  <ol class="flex items-center space-x-4">
    <li>
      <div>
        <a href="#" class="text-gray-400 hover:text-gray-500">
          <Icon icon="heroicons:home" class="flex-shrink-0 h-5 w-5" />
          <span class="sr-only">Accueil</span>
        </a>
      </div>
    </li>
    {#each currentFolder.path as folder}
      <li>
        <div class="flex items-center">
          <Icon icon="heroicons:chevron-right" class="flex-shrink-0 h-5 w-5 text-gray-400" />
          <a 
            href="#" 
            class="ml-4 text-sm font-medium text-gray-500 hover:text-gray-700"
            on:click|preventDefault={() => navigateUp()}
          >
            {folder.name}
          </a>
        </div>
      </li>
    {/each}
    <li>
      <div class="flex items-center">
        <Icon icon="heroicons:chevron-right" class="flex-shrink-0 h-5 w-5 text-gray-400" />
        <span class="ml-4 text-sm font-medium text-gray-500">
          {currentFolder.name}
        </span>
      </div>
    </li>
  </ol>
</nav>