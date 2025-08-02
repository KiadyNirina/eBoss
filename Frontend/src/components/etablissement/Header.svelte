<script>
  import Icon from '@iconify/svelte';
  export let onToggleSidebar;
  
  let searchQuery = '';
</script>

<header class="bg-white shadow-sm">
  <div class="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between">
      <!-- Bouton menu mobile -->
      <button
        type="button"
        class="md:hidden bg-white p-1 rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        on:click={onToggleSidebar}
      >
        <Icon icon="heroicons:menu" class="h-6 w-6" />
      </button>
      
      <!-- Barre de recherche -->
      <div class="flex-1 max-w-xs md:max-w-md mx-4">
        <div class="relative text-gray-400 focus-within:text-gray-500">
          <div class="pointer-events-none absolute inset-y-0 left-0 pl-3 flex items-center">
            <Icon icon="heroicons:magnifying-glass" class="h-5 w-5" />
          </div>
          <input
            id="search"
            name="search"
            class="block w-full bg-white py-2 pl-10 pr-3 border border-gray-300 rounded-md leading-5 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 sm:text-sm"
            placeholder="Rechercher"
            type="search"
            bind:value={searchQuery}
          />
        </div>
      </div>
      
      <!-- Actions droite -->
      <div class="flex items-center space-x-4">
        <button class="bg-white p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
          <Icon icon="heroicons:bell" class="h-6 w-6" />
        </button>
        <button class="bg-white p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
          <Icon icon="heroicons:envelope" class="h-6 w-6" />
        </button>
        <div class="relative ml-3">
          <div class="h-8 w-8 rounded-full bg-green-100 flex items-center justify-center cursor-pointer">
            <Icon icon="heroicons:user-circle" class="h-6 w-6 text-green-600" />
          </div>
        </div>
      </div>
    </div>
  </div>
</header>