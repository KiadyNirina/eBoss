<script>
  import { onMount } from 'svelte';
  import Icon from '@iconify/svelte';
  import FullCalendar from './FullCalendar.svelte';
  import CourseList from './CourseList.svelte';
  import RoomManagement from './RoomManagement.svelte';
  import { authApi } from '$lib/api';
  
  let activeTab = 'courses';
  let view = 'week';
  let showCourseForm = false; 
  
  // Données réelles
  let courses = [];
  let rooms = [];
  let classesOptions = [];
  let matieresOptions = [];
  let professeursOptions = [];
  
  let loading = {
    courses: false,
    rooms: false,
    options: false
  };
  let error = {
    courses: null,
    rooms: null,
    options: null
  };
  
  onMount(async () => {
    await loadOptions();
    await loadCourses();
    await loadRooms();
  });
  
  async function loadOptions() {
    loading.options = true;
    try {
      const [classes, professeurs, matieres] = await Promise.all([
        authApi.getClasses(),
        authApi.getProfesseurs(),
        authApi.getMatieres()
      ]);
      
      classesOptions = (classes.results || classes).map(c => ({
        value: c.id,
        label: c.nom
      }));
      
      professeursOptions = (professeurs.results || professeurs).map(p => ({
        value: p.id,
        label: p.user?.first_name + ' ' + p.user?.last_name || 'Professeur'
      }));
      
      matieresOptions = (matieres.results || matieres).map(m => ({
        value: m.id,
        label: m.nom
      }));
    } catch (err) {
      error.options = err.message;
      console.error('Erreur chargement options:', err);
    } finally {
      loading.options = false;
    }
  }
  
  async function loadCourses() {
    loading.courses = true;
    error.courses = null;
    try {
      const data = await authApi.getCours();
      courses = data.results || data;
    } catch (err) {
      error.courses = err.message || 'Erreur lors du chargement des cours';
      console.error('Erreur chargement cours:', err);
    } finally {
      loading.courses = false;
    }
  }
  
  async function loadRooms() {
    loading.rooms = true;
    error.rooms = null;
    try {
      const data = await authApi.getSalles();
      rooms = data.results || data;
    } catch (err) {
      error.rooms = err.message || 'Erreur lors du chargement des salles';
      console.error('Erreur chargement salles:', err);
    } finally {
      loading.rooms = false;
    }
  }
  
  // Fonction pour ouvrir le modal d'ajout de cours
  function openAddCourse() {
    activeTab = 'courses';
    showCourseForm = true;
  }

  function handleCourseFormOpen() {
    showCourseForm = true;
  }
  
  function handleCourseFormClose() {
    showCourseForm = false;
  }
  
  function getCourseCount() {
    return courses.length;
  }
  
  function getRoomCount() {
    return rooms.length;
  }

  async function reloadCourses() {
    await loadCourses();
  }
</script>

<div>
  <!-- En-tête avec onglets -->
  <div class="border-b border-gray-200">
    <div class="sm:flex sm:items-center sm:justify-between">
      <div>
        <h1 class="text-2xl font-bold leading-6 text-gray-900">Cours & Emploi du Temps</h1>
        <p class="mt-1 text-sm text-gray-500">
          Gérez les cours, les emplois du temps et les salles
        </p>
      </div>
      <div class="mt-4 sm:mt-0 flex space-x-3">
        <button
          on:click={openAddCourse}
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        >
          <Icon icon="heroicons:plus-sm" class="-ml-1 mr-2 h-5 w-5" />
          Ajouter un cours
        </button>
      </div>
    </div>
    
    <nav class="-mb-px flex space-x-8 mt-6" aria-label="Tabs">
      <button
        on:click={() => activeTab = 'calendar'}
        class={`whitespace-nowrap pb-4 px-1 border-b-2 font-medium text-sm ${
          activeTab === 'calendar' 
            ? 'border-green-500 text-green-600' 
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
        }`}
      >
        <Icon icon="heroicons:calendar" class="mr-2 h-5 w-5 inline" />
        Calendrier
        {#if courses.length > 0}
          <span class="ml-1 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
            {courses.length}
          </span>
        {/if}
      </button>
      
      <button
        on:click={() => activeTab = 'courses'}
        class={`whitespace-nowrap pb-4 px-1 border-b-2 font-medium text-sm ${
          activeTab === 'courses' 
            ? 'border-green-500 text-green-600' 
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
        }`}
      >
        <Icon icon="heroicons:clipboard-document-list" class="mr-2 h-5 w-5 inline" />
        Liste des Cours
        {#if courses.length > 0}
          <span class="ml-1 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
            {courses.length}
          </span>
        {/if}
      </button>
      
      <button
        on:click={() => activeTab = 'rooms'}
        class={`whitespace-nowrap pb-4 px-1 border-b-2 font-medium text-sm ${
          activeTab === 'rooms' 
            ? 'border-green-500 text-green-600' 
            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
        }`}
      >
        <Icon icon="heroicons:building-office-2" class="mr-2 h-5 w-5 inline" />
        Gestion des Salles
        {#if rooms.length > 0}
          <span class="ml-1 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">
            {rooms.length}
          </span>
        {/if}
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
        </div>
        
        {#if loading.courses || loading.options}
          <div class="flex justify-center items-center py-12">
            <Icon icon="heroicons:arrow-path" class="h-8 w-8 animate-spin text-green-600" />
            <span class="ml-2 text-gray-600">Chargement du calendrier...</span>
          </div>
        {:else if error.courses}
          <div class="p-4 bg-red-50 border border-red-200 rounded-md">
            <div class="flex items-center">
              <Icon icon="heroicons:x-circle" class="h-5 w-5 text-red-400 mr-2" />
              <p class="text-sm text-red-700">{error.courses}</p>
            </div>
          </div>
        {:else}
          <FullCalendar 
            {view} 
            {courses}
            {classesOptions}
            {matieresOptions}
            {professeursOptions}
            loadCourses={reloadCourses}
          />
        {/if}
      </div>
    
    {:else if activeTab === 'courses'}
      <!-- Vue Liste des Cours -->
      {#if loading.courses}
        <div class="flex justify-center items-center py-12 bg-white rounded-lg border border-gray-200">
          <Icon icon="heroicons:arrow-path" class="h-8 w-8 animate-spin text-green-600" />
          <span class="ml-2 text-gray-600">Chargement des cours...</span>
        </div>
      {:else}
        <CourseList 
          {courses} 
          openForm={showCourseForm}
          on:open={handleCourseFormOpen}
          on:close={handleCourseFormClose}
        />
      {/if}
    
    {:else if activeTab === 'rooms'}
      <!-- Vue Gestion des Salles -->
      {#if loading.rooms}
        <div class="flex justify-center items-center py-12 bg-white rounded-lg border border-gray-200">
          <Icon icon="heroicons:arrow-path" class="h-8 w-8 animate-spin text-green-600" />
          <span class="ml-2 text-gray-600">Chargement des salles...</span>
        </div>
      {:else}
        <RoomManagement {rooms} />
      {/if}
    {/if}
  </div>
</div>

<style>
  .animate-spin {
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
</style>