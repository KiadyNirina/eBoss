<script>
  import Icon from '@iconify/svelte';
  import StudentTable from './StudentTable.svelte';
  import StudentFilters from './StudentFilters.svelte';
  import BulkActions from './BulkActions.svelte';
  import AddStudentModal from './AddStudentModal.svelte';
  import EditStudentModal from './EditStudentModal.svelte';
  import { authApi } from '$lib/api';
  import { user } from '$lib/stores';
  import { fade, scale } from 'svelte/transition';
  import { tick } from 'svelte';

  let pageTop;

  let students = [];
  let selectedStudents = [];
  let filters = {
    search: '',
    classe: '',
    statut: '',
    annee: '',
    etablissement: null
  };
  let classOptions = []; // Pour les filtres
  let classForStudent = []; // Pour le modal
  let statusOptions = [];
  let yearOptions = [];
  let yearForStudent = [];
  let showModal = false;
  let successMessage = '';
  let errorMessage = '';

  let editModalOpen = false;
  let currentStudent = null;
  let selectedClassId = null;

  // Charger les étudiants
  async function fetchStudents(page = 1) {
    try {
      const data = await authApi.getEleves({ ...filters, page });
      console.log('Fetched students:', data);
      students = data.map(student => {
        const classeObj = classForStudent.find(c => c.id === student.classe);
        const classeNom = classeObj ? classeObj.nom : `Classe #${student.classe}`;
        const anneeScolaireObj = yearForStudent.find(y => y.id === student.annee_scolaire);
        const anneeScolaireNom = anneeScolaireObj ? anneeScolaireObj.nom : `Annee scolaire #${student.annee_scolaire}`;

        return {
          id: student.id,
          nom: student.user.last_name,
          prenom: student.user.first_name,
          classe: classeNom,
          classeId: student.classe || null, 
          email: student.user.email,
          telephone: student.user.telephone,
          statut: student.statut,
          annee_scolaire : anneeScolaireNom,
          annee_scolaire_id: student.annee_scolaire,
          derniereActivite: student.derniereActivite || 'N/A',
          date_joined: student.user.date_joined
        };
      });
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
      const filtersForClasses = { etablissement: $user?.profile?.id };
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

  async function fetchAnneeScolaire() {
    try {
      const annee_scolaires = await authApi.getAnneesScolaires();
      yearForStudent = annee_scolaires || [];
      console.log('Annee scolaire fetched :', yearForStudent);
      return yearForStudent; 
    } catch (err) {
      console.error('Erreur lors de la récupération des annees scolaires:', err.message);
      yearForStudent = [];
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
  $: if ($user?.profile?.id) {
    filters.etablissement = $user.profile.id;
    (async () => {
      await fetchAnneeScolaire();
      await fetchClasses();
      await fetchFilterOptions();
      await fetchStudents();
    })();
  }

  // Ouvre le modal et vérifie les classes
  async function openModal() {
    if (classForStudent.length === 0) {
      await fetchClasses(); // Recharge si classForStudent est vide
    }
    console.log('classForStudent before opening modal:', classForStudent);
    showModal = true;
  }

  function openEditModal(student) {
    currentStudent = student;
    editModalOpen = true;
    selectedClassId = student.classeId;
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
        if(selectedStudents.length === 0) {
          errorMessage = '⚠️ Aucun étudiant sélectionné pour l\'exportation';
          setTimeout(() => errorMessage = '', 3000);
          return;
        }
        const response = await authApi.bulkAction(action, selectedStudents);
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'etudiants.csv';
        a.click();
        window.URL.revokeObjectURL(url);
        successMessage = '📦 Exportation réussie';
      } else {
        await authApi.bulkAction(action, selectedStudents);
        selectedStudents = [];
        fetchStudents();
        successMessage = '✅ Étudiants supprimés avec succès';
      }
      setTimeout(() => successMessage = '', 3000);
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

  let deleteModalOpen = false;
  let studentToDelete = null;
  let deleting = false;

  function openDeleteModal(student) {
    studentToDelete = student;
    deleteModalOpen = true;
  }

  async function confirmDelete() {
    deleting = true;

    try {
      await authApi.deleteEleve(studentToDelete.id);

      students = students.filter(
        s => s.id !== studentToDelete.id
      );

      deleteModalOpen = false;

      successMessage = '✅ Étudiant supprimé avec succès';

      await tick();

      pageTop?.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });

      setTimeout(() => {
        successMessage = '';
      }, 4000);

    } catch (error) {
      errorMessage = '❌ Erreur lors de la suppression';

      await tick();

      pageTop?.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });

    } finally {
      deleting = false;
    }
  }
</script>

<div bind:this={pageTop}>
  <!-- Message de succès -->
  {#if successMessage}
    <div
      in:scale={{ duration: 250 }}
      out:fade
      class="bg-green-100 border-l-4 border-green-500 p-4 mb-4 shadow-md rounded-r-lg"
    >
      <p class="text-green-700">{successMessage}</p>
    </div>
  {/if}

  {#if errorMessage}
    <div in:fade out:fade class="bg-red-100 border-l-4 border-red-400 p-4 mb-4">
      <p class="text-red-700">{errorMessage}</p>
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
      {toggleSelectAll}
      toggleStudent={toggleStudentSelection}
      on:edit={(event) => openEditModal(event.detail.student)}
      on:delete={(event) => openDeleteModal(event.detail.student)}
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

  <EditStudentModal
    isOpen={editModalOpen}
    student={currentStudent}
    classOptions={classForStudent}
    {statusOptions}
    {yearOptions}
    on:close={() => (editModalOpen = false)}
    on:success={handleModalSuccess}
  />

  {#if deleteModalOpen}
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm"
    transition:fade
  >
    <div
      class="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-md"
      transition:scale={{ duration: 200 }}
    >
      <div class="flex justify-center mb-4">
        <div class="w-16 h-16 rounded-full bg-red-100 flex items-center justify-center">
          <Icon
            icon="heroicons:trash"
            class="h-8 w-8 text-red-600"
          />
        </div>
      </div>

      <h3 class="text-xl font-bold text-center text-gray-900">
        Supprimer l'étudiant ?
      </h3>

      <p class="mt-3 text-center text-gray-600">
        Cette action est irréversible.
        <br>
        <span class="font-semibold">
          {studentToDelete?.prenom} {studentToDelete?.nom}
        </span>
      </p>

      <div class="mt-6 flex justify-end gap-3">
        <button
          disabled={deleting}
          on:click={() => deleteModalOpen = false}
          class="px-4 py-2 border rounded-lg"
        >
          Annuler
        </button>

        <button
          disabled={deleting}
          on:click={confirmDelete}
          class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 flex items-center gap-2"
        >
          {#if deleting}
            <span
              class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"
            ></span>
            Suppression...
          {:else}
            Supprimer
          {/if}
        </button>
      </div>
    </div>
  </div>
  {/if}
</div>