<script>
  import Icon from '@iconify/svelte';
  import StudentTable from './StudentTable.svelte';
  import StudentFilters from './StudentFilters.svelte';
  import BulkActions from './BulkActions.svelte';
  import AddStudentModal from './AddStudentModal.svelte';
  import { authApi } from '$lib/api';
  import { user } from '$lib/stores';

  let students = [];
  let selectedStudents = [];
  let filters = {
    search: '',
    classe: '',
    statut: '',
    annee: '',
    etablissement: $user.profile.id
  };
  let classOptions = []; // Pour les filtres
  let classForStudent = []; // Pour le modal
  let statusOptions = [];
  let yearOptions = [];
  let showModal = false;
  let successMessage = '';

  // Charger les étudiants
  async function fetchStudents(page = 1) {
    try {
      const data = await authApi.getEleves({ ...filters, page });
      console.log('Fetched students:', data);
      students = data.map(student => ({
        id: student.id,
        nom: student.user.last_name,
        prenom: student.user.first_name,
        classe: student.classe.nom,
        email: student.user.email,
        telephone: student.user.telephone,
        statut: student.statut,
        derniereActivite: student.derniereActivite || 'N/A'
      }));
      totalCount = data.count || 1;
      nextPage = data.next;
      previousPage = data.previous;
      currentPage = page;
    } catch (error) {
      console.error('Erreur lors du chargement des étudiants:', error.message);
    }
  }

  // Charger les classes pour le modal
  async function fetchClasses() {
    try {
      const filtersForClasses = { etablissement: $user.profile.id };
      const classes = await authApi.getClasses(filtersForClasses);
      classForStudent = classes || [];
      console.log('Classes for modal:', classForStudent);
      return classForStudent;
    } catch (error) {
      console.error('Erreur lors de la récupération des classes:', error.message);
      classForStudent = [];
      return [];
    }
  }

  // Charger les options de filtrage
  async function fetchFilterOptions() {
    try {
      const data = await authApi.getFilterOptions();
      classOptions = data.classes || [];
      statusOptions = data.statuts || [];
      yearOptions = data.annees || [];
      console.log('Filter options:', { classOptions, statusOptions, yearOptions });
    } catch (error) {
      console.error('Erreur lors du chargement des options de filtrage:', error.message);
    }
  }

  // Appeler les fonctions au chargement
  $: if ($user.profile.id) {
    console.log('User profile ID:', $user.profile.id);
    filters.etablissement = $user.profile.id;
    fetchStudents();
    fetchFilterOptions();
    fetchClasses();
  }

  // Ouvre le modal et vérifie les classes
  async function openModal() {
    if (classForStudent.length === 0) {
      await fetchClasses(); // Recharge si classForStudent est vide
    }
    console.log('classForStudent before opening modal:', classForStudent);
    showModal = true;
  }

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

  function applyFilters(event) {
    filters = event.detail;
    fetchStudents();
  }

  async function handleBulkAction(event) {
    const action = event.detail.action;
    try {
      if (action === 'export') {
        const response = await authApi.bulkAction(action, selectedStudents);
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'etudiants.csv';
        a.click();
        window.URL.revokeObjectURL(url);
      } else {
        await authApi.bulkAction(action, selectedStudents);
        selectedStudents = [];
        fetchStudents();
      }
    } catch (error) {
      console.error('Erreur lors de l\'action groupée:', error.message);
    }
  }

  function handleModalSuccess() {
    fetchStudents();
    successMessage = 'Étudiant ajouté avec succès';
    setTimeout(() => (successMessage = ''), 3000);
  }

  let currentPage = 1;
  let totalCount = 0;
  let nextPage = null;
  let previousPage = null;

  function goToPage(page) {
    fetchStudents(page);
  }
</script>

<div>
  <!-- Message de succès -->
  {#if successMessage}
    <div class="bg-green-100 border-l-4 border-green-400 p-4 mb-4">
      <p class="text-green-700">{successMessage}</p>
    </div>
  {/if}

  <!-- En-tête -->
  <div class="sm:flex sm:items-center justify-between">
    <div class="mb-4 sm:mb-0">
      <h1 class="text-2xl font-bold text-gray-900">Gestion des Étudiants</h1>
      <p class="mt-2 text-sm text-gray-700">
        {students.length} étudiants au total
      </p>
    </div>
    <div class="flex space-x-3">
      <button
        on:click={openModal}
        disabled={classForStudent.length === 0}
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 disabled:opacity-50"
      >
        <Icon icon="heroicons:plus-sm" class="-ml-1 mr-2 h-5 w-5" />
        Ajouter un étudiant
      </button>
      <button
        on:click={() => handleBulkAction({ detail: { action: 'export' } })}
        class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50"
      >
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
      on:delete={handleBulkAction}
      on:export={handleBulkAction}
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
      <button
        on:click={() => goToPage(currentPage - 1)}
        disabled={!previousPage}
        class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
      >
        Précédent
      </button>
      <button
        on:click={() => goToPage(currentPage + 1)}
        disabled={!nextPage}
        class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
      >
        Suivant
      </button>
    </div>
    <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
      <div>
        <p class="text-sm text-gray-700">
          Affichage de <span class="font-medium">{(currentPage - 1) * 10 + 1}</span> à
          <span class="font-medium">{Math.min(currentPage * 10, totalCount)}</span> sur
          <span class="font-medium">{totalCount}</span> résultats
        </p>
      </div>
      <div>
        <nav
          class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
          aria-label="Pagination"
        >
          <button
            on:click={() => goToPage(currentPage - 1)}
            disabled={!previousPage}
            class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
          >
            <Icon icon="heroicons:chevron-left" class="h-5 w-5" />
          </button>
          {#each Array(Math.ceil(totalCount / 10)) as _, i}
            <button
              on:click={() => goToPage(i + 1)}
              class:bg-green-50={currentPage === i + 1}
              class:border-green-500={currentPage === i + 1}
              class:text-green-600={currentPage === i + 1}
              class="relative inline-flex items-center px-4 py-2 border text-sm font-medium"
            >
              {i + 1}
            </button>
          {/each}
          <button
            on:click={() => goToPage(currentPage + 1)}
            disabled={!nextPage}
            class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
          >
            <Icon icon="heroicons:chevron-right" class="h-5 w-5" />
          </button>
        </nav>
      </div>
    </div>
  </div>

  <!-- Modal -->
  <AddStudentModal
    isOpen={showModal}
    classOptions={classForStudent}
    {statusOptions}
    {yearOptions}
    on:close={() => (showModal = false)}
    on:success={handleModalSuccess}
  />
</div>