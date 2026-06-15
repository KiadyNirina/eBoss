<script>
  import Sidebar from '../../components/etablissement/Sidebar.svelte';
  import Header from '../../components/etablissement/Header.svelte';

  let sidebarOpen = false;
</script>

<div class="flex h-screen bg-gray-50">
  <div class="hidden md:flex md:flex-shrink-0">
    <div class="flex flex-col w-72 border-r border-gray-200 bg-white">
      <Sidebar />
    </div>
  </div>

  <div class="flex flex-col flex-1 overflow-hidden">
    <Header on:toggleSidebar={() => sidebarOpen = !sidebarOpen} />

    <main class="flex-1 overflow-y-auto p-4 md:p-6 bg-gray-50">
      <slot />
    </main>
  </div>
</div>