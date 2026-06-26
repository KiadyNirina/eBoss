<script>
  import { onMount } from 'svelte';
  import Icon from '@iconify/svelte';
  import { authApi } from '$lib/api';
  import { createEventDispatcher } from 'svelte';
  
  export let courses = [];
  export let view = 'list';
  export let openForm = false; 

  const dispatch = createEventDispatcher();
  
  let loading = true;
  let error = null;
  let successMessage = null;
  
  // Options pour les selects
  let classesOptions = [];
  let professeursOptions = [];
  let matieresOptions = [];
  let sallesOptions = [];
  let anneesOptions = [];
  
  // Formulaire
  let isEditing = false;
  let currentCoursId = null;
  let newCours = {
    classe: '',
    professeur: '',
    matiere: '',
    salle: '',
    jour: 'lundi',
    heure_debut: '08:00',
    heure_fin: '09:30',
    annee_scolaire: ''
  };
  
  // Filtres
  let filters = {
    classe: '',
    professeur: '',
    matiere: '',
    annee: '',
    jour: ''
  };
  
  let searchTerm = '';
  let filteredCourses = [];
  
  const JOURS = [
    { value: 'lundi', label: 'Lundi' },
    { value: 'mardi', label: 'Mardi' },
    { value: 'mercredi', label: 'Mercredi' },
    { value: 'jeudi', label: 'Jeudi' },
    { value: 'vendredi', label: 'Vendredi' },
    { value: 'samedi', label: 'Samedi' }
  ];
  
  onMount(async () => {
    await loadFilterOptions();
    await loadCourses();
  });
  
  async function loadFilterOptions() {
    try {
      const [classes, professeurs, matieres, salles] = await Promise.all([
        authApi.getClasses(),
        authApi.getProfesseurs(),
        authApi.getMatieres(),
        authApi.getSalles()
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
      
      sallesOptions = (salles.results || salles).map(s => ({
        value: s.id,
        label: s.nom
      }));
      
      // Récupérer l'année scolaire active
      const annees = await authApi.getAnneesScolaires();
      const active = annees.find(a => a.est_active);
      if (active) {
        newCours.annee_scolaire = active.id;
        anneesOptions = annees.map(a => ({
          value: a.id,
          label: a.nom
        }));
      }
    } catch (err) {
      console.error('Erreur chargement options:', err);
    }
  }
  
  async function loadCourses() {
    loading = true;
    error = null;
    try {
      const data = await authApi.getCours(filters);
      courses = data.results || data;
      applyFilters();
    } catch (err) {
      error = err.message || 'Erreur lors du chargement des cours';
      console.error('Erreur:', err);
    } finally {
      loading = false;
    }
  }

  function openAddForm() {
    resetForm();
    openForm = true;
    dispatch('open');
  }
  
  function resetForm() {
    isEditing = false;
    currentCoursId = null;
    newCours = {
      classe: '',
      professeur: '',
      matiere: '',
      salle: '',
      jour: 'lundi',
      heure_debut: '08:00',
      heure_fin: '09:30',
      annee_scolaire: newCours.annee_scolaire || ''
    };
    openForm = false;
    dispatch('close');
  }
  
  function editCourse(cours) {
    isEditing = true;
    currentCoursId = cours.id;
    newCours = {
      classe: cours.classe,
      professeur: cours.professeur,
      matiere: cours.matiere,
      salle: cours.salle || '',
      jour: cours.jour,
      heure_debut: cours.heure_debut,
      heure_fin: cours.heure_fin,
      annee_scolaire: cours.annee_scolaire
    };
    openForm = true;
    dispatch('open'); 
  }
  
  async function saveCourse() {
    if (!newCours.classe || !newCours.professeur || !newCours.matiere || !newCours.jour) {
      error = 'Tous les champs obligatoires doivent être remplis';
      setTimeout(() => error = null, 3000);
      return;
    }
    
    if (newCours.heure_debut >= newCours.heure_fin) {
      error = 'L\'heure de début doit être avant l\'heure de fin';
      setTimeout(() => error = null, 3000);
      return;
    }
    
    loading = true;
    error = null;
    
    try {
      const profile = await authApi.getProfile();
      const etablissementId = profile.profile?.id || profile.etablissement?.id;
      
      if (!etablissementId) {
        throw new Error('Établissement non trouvé');
      }
      
      const coursData = {
        classe: parseInt(newCours.classe),
        professeur: parseInt(newCours.professeur),
        matiere: parseInt(newCours.matiere),
        salle: newCours.salle ? parseInt(newCours.salle) : null,
        jour: newCours.jour,
        heure_debut: newCours.heure_debut,
        heure_fin: newCours.heure_fin,
        annee_scolaire: parseInt(newCours.annee_scolaire),
        etablissement: etablissementId
      };
      
      if (isEditing && currentCoursId) {
        await authApi.updateCours(currentCoursId, coursData);
        successMessage = 'Cours modifié avec succès !';
      } else {
        await authApi.createCours(coursData);
        successMessage = 'Cours ajouté avec succès !';
      }
      
      setTimeout(() => successMessage = null, 3000);
      resetForm();
      await loadCourses();
    } catch (err) {
      error = err.message || 'Erreur lors de la sauvegarde';
      console.error('Erreur:', err);
      setTimeout(() => error = null, 3000);
    } finally {
      loading = false;
    }
  }
  
  async function deleteCourse(id) {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce cours ?')) return;
    
    loading = true;
    error = null;
    
    try {
      await authApi.deleteCours(id);
      successMessage = 'Cours supprimé avec succès !';
      setTimeout(() => successMessage = null, 3000);
      await loadCourses();
    } catch (err) {
      error = err.message || 'Erreur lors de la suppression';
      console.error('Erreur:', err);
      setTimeout(() => error = null, 3000);
    } finally {
      loading = false;
    }
  }
  
  function applyFilters() {
    if (!courses) return;
    
    let result = [...courses];
    
    // Filtres
    if (filters.classe) {
      result = result.filter(c => c.classe === parseInt(filters.classe));
    }
    if (filters.professeur) {
      result = result.filter(c => c.professeur === parseInt(filters.professeur));
    }
    if (filters.matiere) {
      result = result.filter(c => c.matiere === parseInt(filters.matiere));
    }
    if (filters.jour) {
      result = result.filter(c => c.jour === filters.jour);
    }
    
    // Recherche
    if (searchTerm) {
      const search = searchTerm.toLowerCase();
      result = result.filter(c => 
        c.matiere_nom?.toLowerCase().includes(search) ||
        c.professeur_nom?.toLowerCase().includes(search) ||
        c.classe_nom?.toLowerCase().includes(search) ||
        c.salle_nom?.toLowerCase().includes(search)
      );
    }
    
    filteredCourses = result;
  }
  
  function resetFilters() {
    filters = {
      classe: '',
      professeur: '',
      matiere: '',
      annee: '',
      jour: ''
    };
    searchTerm = '';
    loadCourses();
  }
  
  function getJourLabel(jour) {
    const found = JOURS.find(j => j.value === jour);
    return found ? found.label : jour;
  }
  
  $: applyFilters();
</script>

<div>
  <!-- Messages -->
  {#if successMessage}
    <div class="mb-4 p-4 bg-green-50 border border-green-200 rounded-md">
      <div class="flex items-center">
        <Icon icon="heroicons:check-circle" class="h-5 w-5 text-green-400 mr-2" />
        <p class="text-sm text-green-700">{successMessage}</p>
      </div>
    </div>
  {/if}
  
  {#if error}
    <div class="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
      <div class="flex items-center">
        <Icon icon="heroicons:x-circle" class="h-5 w-5 text-red-400 mr-2" />
        <p class="text-sm text-red-700">{error}</p>
      </div>
    </div>
  {/if}
  
  <!-- Formulaire d'ajout/modification -->
  {#if openForm}
  <div class="mb-6 p-4 border border-gray-200 rounded-lg bg-gray-50">
    <h4 class="text-sm font-medium text-gray-700 mb-4">
      {isEditing ? 'Modifier le cours' : 'Ajouter un nouveau cours'}
    </h4>
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <div>
        <label for="cours-classe" class="block text-xs font-medium text-gray-700">
          Classe <span class="text-red-500">*</span>
        </label>
        <select
          id="cours-classe"
          bind:value={newCours.classe}
          class="mt-1 block w-full pl-3 pr-10 py-1.5 text-sm border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 rounded-md"
        >
          <option value="">Sélectionner</option>
          {#each classesOptions as option}
            <option value={option.value}>{option.label}</option>
          {/each}
        </select>
      </div>
      
      <div>
        <label for="cours-professeur" class="block text-xs font-medium text-gray-700">
          Professeur <span class="text-red-500">*</span>
        </label>
        <select
          id="cours-professeur"
          bind:value={newCours.professeur}
          class="mt-1 block w-full pl-3 pr-10 py-1.5 text-sm border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 rounded-md"
        >
          <option value="">Sélectionner</option>
          {#each professeursOptions as option}
            <option value={option.value}>{option.label}</option>
          {/each}
        </select>
      </div>
      
      <div>
        <label for="cours-matiere" class="block text-xs font-medium text-gray-700">
          Matière <span class="text-red-500">*</span>
        </label>
        <select
          id="cours-matiere"
          bind:value={newCours.matiere}
          class="mt-1 block w-full pl-3 pr-10 py-1.5 text-sm border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 rounded-md"
        >
          <option value="">Sélectionner</option>
          {#each matieresOptions as option}
            <option value={option.value}>{option.label}</option>
          {/each}
        </select>
      </div>
      
      <div>
        <label for="cours-salle" class="block text-xs font-medium text-gray-700">
          Salle
        </label>
        <select
          id="cours-salle"
          bind:value={newCours.salle}
          class="mt-1 block w-full pl-3 pr-10 py-1.5 text-sm border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 rounded-md"
        >
          <option value="">Sélectionner</option>
          {#each sallesOptions as option}
            <option value={option.value}>{option.label}</option>
          {/each}
        </select>
      </div>
      
      <div>
        <label for="cours-jour" class="block text-xs font-medium text-gray-700">
          Jour <span class="text-red-500">*</span>
        </label>
        <select
          id="cours-jour"
          bind:value={newCours.jour}
          class="mt-1 block w-full pl-3 pr-10 py-1.5 text-sm border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 rounded-md"
        >
          {#each JOURS as jour}
            <option value={jour.value}>{jour.label}</option>
          {/each}
        </select>
      </div>
      
      <div>
        <label for="cours-heure-debut" class="block text-xs font-medium text-gray-700">
          Heure début <span class="text-red-500">*</span>
        </label>
        <input
          type="time"
          id="cours-heure-debut"
          bind:value={newCours.heure_debut}
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-1.5 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
        />
      </div>
      
      <div>
        <label for="cours-heure-fin" class="block text-xs font-medium text-gray-700">
          Heure fin <span class="text-red-500">*</span>
        </label>
        <input
          type="time"
          id="cours-heure-fin"
          bind:value={newCours.heure_fin}
          class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-1.5 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
        />
      </div>
      
      <div>
        <label for="cours-annee" class="block text-xs font-medium text-gray-700">
          Année <span class="text-red-500">*</span>
        </label>
        <select
          id="cours-annee"
          bind:value={newCours.annee_scolaire}
          class="mt-1 block w-full pl-3 pr-10 py-1.5 text-sm border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 rounded-md"
        >
          <option value="">Sélectionner</option>
          {#each anneesOptions as option}
            <option value={option.value}>{option.label}</option>
          {/each}
        </select>
      </div>
      
      <div class="flex items-end space-x-2">
        <button
          on:click={saveCourse}
          disabled={loading}
          class="inline-flex items-center px-4 py-1.5 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {#if loading}
            <Icon icon="heroicons:arrow-path" class="h-4 w-4 animate-spin mr-1" />
          {/if}
          {isEditing ? 'Modifier' : 'Ajouter'}
        </button>
        
        <button
          on:click={resetForm}
          class="inline-flex items-center px-4 py-1.5 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        >
          Annuler
        </button>
      </div>
    </div>
  </div>
  {/if}
  
  <!-- Filtres -->
  <div class="mb-4 p-4 border border-gray-200 rounded-lg bg-white">
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-5">
      <div>
        <label for="filter-classe" class="block text-xs font-medium text-gray-700">Classe</label>
        <select
          id="filter-classe"
          bind:value={filters.classe}
          on:change={applyFilters}
          class="mt-1 block w-full pl-3 pr-10 py-1.5 text-sm border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 rounded-md"
        >
          <option value="">Toutes</option>
          {#each classesOptions as option}
            <option value={option.value}>{option.label}</option>
          {/each}
        </select>
      </div>
      
      <div>
        <label for="filter-professeur" class="block text-xs font-medium text-gray-700">Professeur</label>
        <select
          id="filter-professeur"
          bind:value={filters.professeur}
          on:change={applyFilters}
          class="mt-1 block w-full pl-3 pr-10 py-1.5 text-sm border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 rounded-md"
        >
          <option value="">Tous</option>
          {#each professeursOptions as option}
            <option value={option.value}>{option.label}</option>
          {/each}
        </select>
      </div>
      
      <div>
        <label for="filter-matiere" class="block text-xs font-medium text-gray-700">Matière</label>
        <select
          id="filter-matiere"
          bind:value={filters.matiere}
          on:change={applyFilters}
          class="mt-1 block w-full pl-3 pr-10 py-1.5 text-sm border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 rounded-md"
        >
          <option value="">Toutes</option>
          {#each matieresOptions as option}
            <option value={option.value}>{option.label}</option>
          {/each}
        </select>
      </div>
      
      <div>
        <label for="filter-jour" class="block text-xs font-medium text-gray-700">Jour</label>
        <select
          id="filter-jour"
          bind:value={filters.jour}
          on:change={applyFilters}
          class="mt-1 block w-full pl-3 pr-10 py-1.5 text-sm border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 rounded-md"
        >
          <option value="">Tous</option>
          {#each JOURS as jour}
            <option value={jour.value}>{jour.label}</option>
          {/each}
        </select>
      </div>
      
      <div class="flex items-end space-x-2">
        <button
          on:click={resetFilters}
          class="inline-flex items-center px-3 py-1.5 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        >
          <Icon icon="heroicons:x-mark" class="h-4 w-4 mr-1" />
          Réinitialiser
        </button>
      </div>
    </div>
    
    <div class="mt-3 relative">
      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <Icon icon="heroicons:magnifying-glass" class="h-4 w-4 text-gray-400" />
      </div>
      <input
        type="text"
        bind:value={searchTerm}
        on:input={applyFilters}
        class="block w-full pl-9 pr-3 py-1.5 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-green-500 focus:border-green-500 sm:text-sm"
        placeholder="Rechercher un cours..."
      />
    </div>
  </div>
  
  <!-- Tableau des cours -->
  {#if loading && courses.length === 0}
    <div class="flex justify-center items-center py-12 bg-white rounded-lg border border-gray-200">
      <Icon icon="heroicons:arrow-path" class="h-8 w-8 animate-spin text-green-600" />
      <span class="ml-2 text-gray-600">Chargement...</span>
    </div>
  {:else if filteredCourses.length === 0}
    <div class="text-center py-12 bg-white rounded-lg border border-gray-200">
      <Icon icon="heroicons:book-open" class="h-12 w-12 text-gray-400 mx-auto mb-4" />
      <p class="text-gray-500 text-sm">
        {searchTerm || Object.values(filters).some(v => v) ? 'Aucun cours ne correspond à votre recherche' : 'Aucun cours trouvé'}
      </p>
      {#if !searchTerm && !Object.values(filters).some(v => v)}
        <button
          on:click={() => { resetForm(); }}
          class="mt-2 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-green-700 bg-green-100 hover:bg-green-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        >
          <Icon icon="heroicons:plus-sm" class="-ml-1 mr-2 h-5 w-5" />
          Ajouter un cours
        </button>
      {/if}
    </div>
  {:else}
    <div class="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Matière
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Professeur
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Classe
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Jour/Horaire
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Salle
              </th>
              <th scope="col" class="relative px-6 py-3">
                <span class="sr-only">Actions</span>
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            {#each filteredCourses as cours}
              <tr class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center">
                      <Icon icon="heroicons:book-open" class="h-5 w-5 text-blue-600" />
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900">{cours.matiere_nom}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">{cours.professeur_nom}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                    {cours.classe_nom}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">
                    <span class="font-medium">{getJourLabel(cours.jour)}</span>
                    <span class="text-gray-500 ml-1">{cours.heure_debut} - {cours.heure_fin}</span>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">{cours.salle_nom || 'N/A'}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div class="flex justify-end space-x-3">
                    <button
                      on:click={() => editCourse(cours)}
                      class="text-green-600 hover:text-green-900"
                    >
                      <Icon icon="heroicons:pencil-square" class="h-5 w-5" />
                    </button>
                    <button
                      on:click={() => deleteCourse(cours.id)}
                      class="text-red-600 hover:text-red-900"
                    >
                      <Icon icon="heroicons:trash" class="h-5 w-5" />
                    </button>
                  </div>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
      
      <!-- Statistiques -->
      <div class="bg-gray-50 px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
        <div class="text-sm text-gray-700">
          Affichage de <span class="font-medium">{filteredCourses.length}</span> cours
          {#if courses.length > filteredCourses.length}
            sur <span class="font-medium">{courses.length}</span> au total
          {/if}
        </div>
        <button
          on:click={loadCourses}
          disabled={loading}
          class="inline-flex items-center px-3 py-1 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
        >
          <Icon icon="heroicons:arrow-path" class={`h-4 w-4 mr-1 ${loading ? 'animate-spin' : ''}`} />
          Rafraîchir
        </button>
      </div>
    </div>
  {/if}
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