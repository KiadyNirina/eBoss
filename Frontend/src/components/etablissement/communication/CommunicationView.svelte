<script>
  import Icon from '@iconify/svelte';
  import CommunicationTabs from './CommunicationTabs.svelte';
  import MessageList from './MessageList.svelte';
  import AnnouncementList from './AnnouncementList.svelte';
  import NotificationCenter from './NotificationCenter.svelte';
  import NewMessageModal from './NewMessageModal.svelte';
  import NewAnnouncementModal from './NewAnnouncementModal.svelte';
  
  let activeTab = 'messages';
  let showNewMessageModal = false;
  let showNewAnnouncementModal = false;
  
  // Données simulées
  const messages = [
    {
      id: 1,
      sender: 'Prof. Martin',
      subject: 'Devoir de mathématiques',
      preview: 'Le devoir de la semaine prochaine sera sur...',
      time: '10:30',
      read: false,
      important: true
    },
  ];
  
  const announcements = [
    {
      id: 1,
      title: 'Réunion parents-professeurs',
      content: 'La réunion parents-professeurs aura lieu le 15 juin...',
      author: 'Direction',
      date: '15/06/2023',
      pinned: true
    },
  ];
  
  const notifications = [
    {
      id: 1,
      type: 'absence',
      content: 'Jean Dupont absent aujourd\'hui',
      time: 'Il y a 2 heures',
      read: false
    },
  ];
</script>

<div>
  <!-- En-tête -->
  <div class="sm:flex sm:items-center justify-between mb-6">
    <div>
      <h1 class="text-2xl font-bold leading-6 text-gray-900">Communication</h1>
      <p class="mt-2 text-sm text-gray-700">
        Restez connecté avec l'ensemble de la communauté scolaire
      </p>
    </div>
    <div class="mt-4 sm:mt-0 flex space-x-3">
      {#if activeTab === 'messages'}
        <button 
          on:click={() => showNewMessageModal = true}
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        >
          <Icon icon="heroicons:envelope" class="-ml-1 mr-2 h-5 w-5" />
          Nouveau message
        </button>
      {:else if activeTab === 'annonces'}
        <button 
          on:click={() => showNewAnnouncementModal = true}
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        >
          <Icon icon="heroicons:megaphone" class="-ml-1 mr-2 h-5 w-5" />
          Nouvelle annonce
        </button>
      {/if}
    </div>
  </div>
  
  <!-- Onglets -->
  <CommunicationTabs bind:activeTab />
  
  <!-- Contenu des onglets -->
  <div class="mt-6">
    {#if activeTab === 'messages'}
      <MessageList {messages} />
    {:else if activeTab === 'annonces'}
      <AnnouncementList {announcements} />
    {:else}
      <NotificationCenter {notifications} />
    {/if}
  </div>
  
  <!-- Modales -->
  {#if showNewMessageModal}
    <NewMessageModal on:close={() => showNewMessageModal = false} />
  {/if}
  
  {#if showNewAnnouncementModal}
    <NewAnnouncementModal on:close={() => showNewAnnouncementModal = false} />
  {/if}
</div>