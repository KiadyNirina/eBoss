<script>
  import Icon from '@iconify/svelte';
  import TeacherTable from './TeacherTable.svelte';
  import TeacherFilters from './TeacherFilters.svelte';
  import BulkActions from './BulkActions.svelte';
  import { authApi } from '$lib/api';
  import { onMount } from 'svelte';
  import AddTeacherModal from './AddTeacherModal.svelte';
  import EditTeacherModal from './EditTeacherModal.svelte';
  import { fade, scale } from 'svelte/transition';
  import { tick } from 'svelte';
  
  let pageTop;

  let teachers = [];
  let loading = false;
  
  let selectedTeachers = [];
  let searchTerm = '';
  let filters = {
    search: '',
    matiere: '',
    // statut: '',
    annee: ''
  };
  let matiereOptions = [];
  let classOptions = [];
  let yearOptions = [];
  let showAddTeacherModal = false;
  let showEditTeacherModal = false;
  let teacherToEdit = null;
  let successMessage = '';
  let errorMessage = '';

  // Variables pour le modal de suppression
  let deleteModalOpen = false;
  let teacherToDelete = null;
  let deleting = false;

  function openAddTeacherModal() {
    showAddTeacherModal = true;
  }

  function closeAddTeacherModal() {
    showAddTeacherModal = false;
  }

  function openEditTeacherModal(teacher) {
    teacherToEdit = teacher;
    showEditTeacherModal = true;
  }

  function closeEditTeacherModal() {
    showEditTeacherModal = false;
    teacherToEdit = null;
  }

  function handleTeacherSuccess(event) {
    console.log(event.detail.message);
    loadProfesseurs();
  }

  function handleTeacherUpdate(event) {
    console.log(event.detail.message);
    loadProfesseurs();
  }
    
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
  
  async function applyFilters(event) {
    filters = event.detail;
    await loadProfesseurs();
  }

  async function loadProfesseurs() {
    loading = true;
    try {
      const data = await authApi.getProfesseurs(filters);
      teachers = data.results || data;
    } catch (error) {
      console.error('Erreur lors du chargement des professeurs', error);
    } finally {
      loading = false;
    }
  }

  async function loadFilterOptions() {
    try {
      const data = await authApi.getProfesseurFilterOptions();
      matiereOptions = data.matieres || [];
      classOptions = data.classes || [];
      yearOptions = data.annees || [];
    } catch(error) {
      console.error("Erreur chargement options professeur", error);
    }
  }

  // Gestionnaire pour l'édition depuis le tableau
  function handleEditTeacher(event) {
    const teacherId = event.detail;
    const teacher = teachers.find(t => t.id === teacherId);
    if (teacher) {
      openEditTeacherModal(teacher);
    }
  }

  // Ouvre le modal de suppression
  function openDeleteModal(event) {
    const teacherId = event.detail;

    const teacher = teachers.find(t => t.id === teacherId);

    if (teacher) {
      teacherToDelete = teacher;
      deleteModalOpen = true;
    }
  }

  // Confirme la suppression
  async function confirmDelete() {
    deleting = true;

    try {
      await authApi.deleteProfesseur(teacherToDelete.id);

      teachers = teachers.filter(
        t => t.id !== teacherToDelete.id
      );

      deleteModalOpen = false;

      successMessage = '✅ Professeur supprimé avec succès';

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

      console.error('Erreur lors de la suppression', error);

    } finally {
      deleting = false;
    }
  }

  onMount(async () => {
    await loadProfesseurs();
    await loadFilterOptions();
  });
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
      <h1 class="text-2xl font-bold text-gray-900">Gestion des Professeurs</h1>
      <p class="mt-2 text-sm text-gray-700">
        {teachers.length} professeurs au total
      </p>
    </div>
    <div class="flex space-x-3">
      <button
        on:click={openAddTeacherModal}
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
      >
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
      on:edit={handleEditTeacher}
      on:delete={openDeleteModal}
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

<!-- Modal d'ajout -->
{#if showAddTeacherModal}
<AddTeacherModal
  isOpen={showAddTeacherModal}
  subjectOptions={matiereOptions}
  classOptions={classOptions}
  yearOptions={yearOptions}
  on:close={closeAddTeacherModal}
  on:success={handleTeacherSuccess}
/>
{/if}

<!-- Modal d'édition -->
{#if showEditTeacherModal && teacherToEdit}
<EditTeacherModal
  isOpen={showEditTeacherModal}
  teacher={teacherToEdit}
  subjectOptions={matiereOptions}
  classOptions={classOptions}
  yearOptions={yearOptions}
  on:close={closeEditTeacherModal}
  on:success={handleTeacherUpdate}
/>
{/if}

<!-- Modal de suppression -->
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
      Supprimer le professeur ?
    </h3>

    <p class="mt-3 text-center text-gray-600">
      Cette action est irréversible.
      <br>
      <span class="font-semibold">
        {teacherToDelete?.user?.first_name} {teacherToDelete?.user?.last_name}
      </span>
    </p>

    <div class="mt-6 flex justify-end gap-3">
      <button
        disabled={deleting}
        on:click={() => deleteModalOpen = false}
        class="px-4 py-2 border rounded-lg hover:bg-gray-50 disabled:opacity-50"
      >
        Annuler
      </button>

      <button
        disabled={deleting}
        on:click={confirmDelete}
        class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 flex items-center gap-2 disabled:opacity-50"
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