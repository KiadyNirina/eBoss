<script>
  import Icon from '@iconify/svelte';
  import StudentTable from './StudentTable.svelte';
  import StudentFilters from './StudentFilters.svelte';
  import BulkActions from './BulkActions.svelte';
  
  // Données simulées
  let students = [
    {
      id: 1,
      nom: 'Dupont',
      prenom: 'Jean',
      classe: '3ème A',
      email: 'jean.dupont@ecole.fr',
      telephone: '06 12 34 56 78',
      statut: 'actif',
      derniereActivite: 'Aujourd\'hui, 09:45'
    },
    {
      id: 2,
      nom: 'Martin',
      prenom: 'Sophie',
      classe: '4ème B',
      email: 'sophie.martin@ecole.fr',
      telephone: '06 23 45 67 89',
      statut: 'actif',
      derniereActivite: 'Hier, 14:30'
    },
  ];
  
  let selectedStudents = [];
  let searchTerm = '';
  let filters = {
    classe: '',
    statut: '',
    annee: ''
  };
  
  // Fonctions de gestion
  function toggleSelectAll(event) {
    if (event.target.checked) {
      selectedStudents = students.map(student => student.id);
    } else {
      selectedStudents = [];
    }
  }
  
  function toggleStudentSelection(id) {
    if (selectedStudents.includes(id)) {
      selectedStudents = selectedStudents.filter(studentId => studentId !== id);
    } else {
      selectedStudents = [...selectedStudents, id];
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
      <h1 class="text-2xl font-bold text-gray-900">Gestion des Étudiants</h1>
      <p class="mt-2 text-sm text-gray-700">
        {students.length} étudiants au total
      </p>
    </div>
    <div class="flex space-x-3">
      <button class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
        <Icon icon="heroicons:plus-sm" class="-ml-1 mr-2 h-5 w-5" />
        Ajouter un étudiant
      </button>
      <button class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
        <Icon icon="heroicons:arrow-down-tray" class="-ml-1 mr-2 h-5 w-5" />
        Exporter
      </button>
    </div>
  </div>
  
  <!-- Filtres et recherche -->
  <StudentFilters {filters} on:apply={applyFilters} />
  
  <!-- Actions groupées -->
  {#if selectedStudents.length > 0}
    <BulkActions 
      count={selectedStudents.length} 
      on:delete={() => console.log('Delete', selectedStudents)}
      on:export={() => console.log('Export', selectedStudents)}
    />
  {/if}
  
  <!-- Tableau des étudiants -->
  <div class="mt-6 shadow-sm border border-gray-200 rounded-lg overflow-hidden">
    <StudentTable 
      {students} 
      {selectedStudents}
      on:toggleSelectAll={toggleSelectAll}
      on:toggleStudent={toggleStudentSelection}
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
          <span class="font-medium">{students.length}</span> résultats
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