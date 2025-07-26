<script>
    import Icon from '@iconify/svelte';
    import { fade } from 'svelte/transition';
  
    let menuOpen = false;
</script>

<nav class="bg-white shadow-sm sticky top-0 z-50">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between h-16">
      <div class="flex items-center">
        <Icon icon="fluent:school-24-filled" class="h-8 w-8 text-indigo-600" />
        <img src="/icons/logo.png" class="h-8 w-8" alt="">
        <span class="ml-2 text-xl font-bold text-gray-900">eBoss</span>
      </div>
      
      <div class="hidden md:flex items-center space-x-8">
        <a href="#features" class="text-gray-700 hover:text-indigo-600 px-3 py-2 text-sm font-medium">Fonctionnalités</a>
        <!-- <a href="#pricing" class="text-gray-700 hover:text-indigo-600 px-3 py-2 text-sm font-medium">Tarifs</a>
        <a href="#testimonials" class="text-gray-700 hover:text-indigo-600 px-3 py-2 text-sm font-medium">Témoignages</a> -->
      </div>
      
      <div class="hidden md:flex items-center space-x-4">
        <a href="/login" class="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700 transition-colors">Connexion</a>
      </div>
      
      <div class="md:hidden flex items-center">
        <button on:click={() => menuOpen = !menuOpen} class="text-gray-500 hover:text-gray-900 focus:outline-none">
          <Icon icon={menuOpen ? 'heroicons-outline:x' : 'heroicons-outline:menu'} class="h-6 w-6" />
        </button>
      </div>
    </div>
  </div>
  
  {#if menuOpen}
    <div transition:fade class="md:hidden bg-white shadow-lg">
      <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
        <a href="#features" class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-indigo-600 hover:bg-gray-50">Fonctionnalités</a>
        <a href="#pricing" class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-indigo-600 hover:bg-gray-50">Tarifs</a>
        <a href="#testimonials" class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-indigo-600 hover:bg-gray-50">Témoignages</a>
        <div class="border-t border-gray-200 pt-4 pb-3">
          <a href="/login" class="block px-3 py-2 text-base font-medium text-gray-700 hover:text-indigo-600">Connexion</a>
          <a href="/register" class="mt-2 block w-full px-3 py-2 text-center text-base font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700">Essai gratuit</a>
        </div>
      </div>
    </div>
  {/if}
</nav>