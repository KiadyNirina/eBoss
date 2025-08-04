<script>
  import Icon from '@iconify/svelte';
  import TeacherTable from './TeacherTable.svelte';
  import TeacherFilters from './TeacherFilters.svelte';
  import BulkActions from './BulkActions.svelte';
  
  // Données simulées
  let teachers = [
    {
      id: 1,
      nom: 'Martin',
      prenom: 'Sophie',
      matieres: ['Mathématiques', 'Physique'],
      classes: ['4ème B', '3ème A'],
      email: 'sophie.martin@ecole.fr',
      telephone: '06 23 45 67 89',
      statut: 'actif',
      embauche: '15/08/2018'
    },
    {
      id: 2,
      nom: 'Bernard',
      prenom: 'Pierre',
      matieres: ['Histoire-Géographie'],
      classes: ['5ème C', '4ème A'],
      email: 'pierre.bernard@ecole.fr',
      telephone: '06 34 56 78 90',
      statut: 'actif',
      embauche: '01/09/2020'
    },
  ];
  
  let selectedTeachers = [];
  let searchTerm = '';
  let filters = {
    matiere: '',
    statut: '',
    annee: ''
  };
  
  // Fonctions de gestion
  function toggleSelectAll(event) {
    if (event.target.checked) {
      selectedTeachers = teachers.map(teacher => teacher.id);
    } else {
      selectedTeachers = [];
    }
  }
  
  function toggleTeacherSelection(id) {
    if (selectedTeachers.includes(id)) {
      selectedTeachers = selectedTeachers.filter(teacherId => teacherId !== id);
    } else {
      selectedTeachers = [...selectedTeachers, id];
    }
  }
  
  function applyFilters(newFilters) {
    filters = newFilters;
  }
</script>

<div class="">
  <!-- En-tête -->
  <div class="sm:flex sm:items-center justify-between">
    <div class="mb-4 sm:mb-0">
      <h1 class="text-2xl font-bold text-gray-900">Gestion des Professeurs</h1>
      <p class="mt-2 text-sm text-gray-700">
        {teachers.length} professeurs au total
      </p>
    </div>
    <div class="flex space-x-3">
      <button class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
        <Icon icon="heroicons:plus-sm" class="-ml-1 mr-2 h-5 w-5" />
        Ajouter un professeur
      </button>
      <button class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
        <Icon icon="heroicons:arrow-down-tray" class="-ml-1 mr-2 h-5 w-5" />
        Exporter
      </button>
    </div>
  </div>
  
  <!-- Filtres et recherche -->
  <TeacherFilters {filters} on:apply={applyFilters} />
  
  <!-- Actions groupées -->
  {#if selectedTeachers.length > 0}
    <BulkActions 
      count={selectedTeachers.length} 
      on:delete={() => console.log('Delete', selectedTeachers)}
      on:export={() => console.log('Export', selectedTeachers)}
      type="professeurs"
    />
  {/if}
  
  <!-- Tableau des professeurs -->
  <div class="mt-6 shadow-sm border border-gray-200 rounded-lg overflow-hidden">
    <TeacherTable 
      {teachers} 
      {selectedTeachers}
      on:toggleSelectAll={toggleSelectAll}
      on:toggleTeacher={toggleTeacherSelection}
    />
  </div>
  
  <!-- Pagination -->
  <div class="mt-6 flex items-center justify-between">
    <div class="flex-1 flex justify-between sm:hidden">
      <a href="#" class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
        Précédent
      </a>
      <a href="#" class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
        Suivant
      </a>
    </div>
    <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
      <div>
        <p class="text-sm text-gray-700">
          Affichage de <span class="font-medium">1</span> à <span class="font-medium">10</span> sur{' '}
          <span class="font-medium">{teachers.length}</span> résultats
        </p>
      </div>
      <div>
        <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
          <a href="#" class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
            <span class="sr-only">Précédent</span>
            <Icon icon="heroicons:chevron-left" class="h-5 w-5" />
          </a>
          <a href="#" aria-current="page" class="z-10 bg-green-50 border-green-500 text-green-600 relative inline-flex items-center px-4 py-2 border text-sm font-medium">
            1
          </a>
          <a href="#" class="bg-white border-gray-300 text-gray-500 hover:bg-gray-50 relative inline-flex items-center px-4 py-2 border text-sm font-medium">
            2
          </a>
          <a href="#" class="bg-white border-gray-300 text-gray-500 hover:bg-gray-50 relative inline-flex items-center px-4 py-2 border text-sm font-medium">
            3
          </a>
          <a href="#" class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
            <span class="sr-only">Suivant</span>
            <Icon icon="heroicons:chevron-right" class="h-5 w-5" />
          </a>
        </nav>
      </div>
    </div>
  </div>
</div>