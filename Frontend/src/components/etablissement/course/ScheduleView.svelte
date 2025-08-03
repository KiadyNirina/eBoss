<script>
  import Icon from '@iconify/svelte';
  import FullCalendar from './FullCalendar.svelte';
  import CourseList from './CourseList.svelte';
  import RoomManagement from './RoomManagement.svelte';
  
  let activeTab = 'calendar';
  let view = 'week'; // 'day', 'week', 'month'
  
  // Données simulées
  const courses = [
    {
      id: 1,
      title: 'Mathématiques',
      teacher: 'M. Dupont',
      class: '3ème A',
      room: 'Salle 101',
      day: 'Lundi',
      start: '08:00',
      end: '09:30',
      color: 'bg-green-100 text-green-800'
    },
  ];
  
  const rooms = [
    { id: 1, name: 'Salle 101', capacity: 30, equipment: 'Projecteur, Tableau blanc' },
    { id: 2, name: 'Labo Sciences', capacity: 24, equipment: 'Paillasses, Matériel expériences' },
  ];
</script>

<div>
  <!-- En-tête avec onglets -->
  <div class="border-b border-gray-200">
    <div class="sm:flex sm:items-center sm:justify-between">
      <h1 class="text-2xl font-bold leading-6 text-gray-900">Cours & Emploi du Temps</h1>
      <div class="mt-4 sm:mt-0">
        <button class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
          <Icon icon="heroicons:plus-sm" class="-ml-1 mr-2 h-5 w-5" />
          Ajouter un cours
        </button>
      </div>
    </div>
    
    <nav class="-mb-px flex space-x-8 mt-6">
      <button
        on:click={() => activeTab = 'calendar'}
        class={`whitespace-nowrap pb-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'calendar' ? 'border-green-500 text-green-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
      >
        <Icon icon="heroicons:calendar" class="mr-2 h-5 w-5 inline" />
        Calendrier
      </button>
      <button
        on:click={() => activeTab = 'courses'}
        class={`whitespace-nowrap pb-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'courses' ? 'border-green-500 text-green-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
      >
        <Icon icon="heroicons:clipboard-document-list" class="mr-2 h-5 w-5 inline" />
        Liste des Cours
      </button>
      <button
        on:click={() => activeTab = 'rooms'}
        class={`whitespace-nowrap pb-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'rooms' ? 'border-green-500 text-green-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
      >
        <Icon icon="heroicons:building-office-2" class="mr-2 h-5 w-5 inline" />
        Gestion des Salles
      </button>
    </nav>
  </div>
  
  <!-- Contenu des onglets -->
  <div class="mt-6">
    {#if activeTab === 'calendar'}
      <!-- Vue Calendrier -->
      <div class="bg-white shadow-sm rounded-lg border border-gray-200 p-4">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-medium text-gray-900">Emploi du temps</h2>
          <div class="flex space-x-2">
            <button
              on:click={() => view = 'day'}
              class={`px-3 py-1 text-sm font-medium rounded-md ${view === 'day' ? 'bg-green-100 text-green-700' : 'text-gray-700 hover:bg-gray-100'}`}
            >
              Jour
            </button>
            <button
              on:click={() => view = 'week'}
              class={`px-3 py-1 text-sm font-medium rounded-md ${view === 'week' ? 'bg-green-100 text-green-700' : 'text-gray-700 hover:bg-gray-100'}`}
            >
              Semaine
            </button>
            <button
              on:click={() => view = 'month'}
              class={`px-3 py-1 text-sm font-medium rounded-md ${view === 'month' ? 'bg-green-100 text-green-700' : 'text-gray-700 hover:bg-gray-100'}`}
            >
              Mois
            </button>
          </div>
        </div>
        
        <FullCalendar {view} {courses} />
      </div>
    
    {:else if activeTab === 'courses'}
      <!-- Vue Liste des Cours -->
      <CourseList {courses} />
    
    {:else if activeTab === 'rooms'}
      <!-- Vue Gestion des Salles -->
      <RoomManagement {rooms} />
    {/if}
  </div>
</div>