<script>
  import { onMount } from 'svelte';
  import Icon from '@iconify/svelte';
  import GradeFilters from './GradeFilters.svelte';
  import GradeSummary from './GradeSummary.svelte';
  import GradeTable from './GradeTable.svelte';
  import GradeChart from './GradeChart.svelte';
  import { authApi } from '$lib/api';
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();
  
  let evaluations = [];
  let selectedEvaluation = null;
  let loading = true;
  let error = null;
  let successMessage = null;

  // Options pour les filtres (chargées depuis l'API)
  let classOptions = [];
  let subjectOptions = [];
  let periodOptions = [];
  
  let filters = {
    classe: '',
    matiere: '',
    periode: ''
  };

  // Chargement initial
  onMount(async () => {
    await loadFilterOptions();
    await loadEvaluations();
  });

  async function loadFilterOptions() {
    try {
      // Récupérer les classes, matières et périodes pour l'établissement connecté
      const [classesRes, matieresRes, periodesRes] = await Promise.all([
        authApi.getClasses(),
        authApi.getMatieres(),
        authApi.getPeriodes()
      ]);
      
      classOptions = (classesRes.results || classesRes).map(c => ({
        value: c.id,
        label: c.nom
      }));
      
      subjectOptions = (matieresRes.results || matieresRes).map(m => ({
        value: m.id,
        label: m.nom
      }));
      
      periodOptions = (periodesRes.results || periodesRes).map(p => ({
        value: p.id,
        label: p.nom
      }));
    } catch (err) {
      console.error('Erreur chargement options filtres:', err);
    }
  }

  async function loadEvaluations() {
    loading = true;
    error = null;
    try {
      // Construire les paramètres de filtres pour l'API
      const params = {};
      if (filters.classe) params.classe = filters.classe;
      if (filters.matiere) params.matiere = filters.matiere;
      if (filters.periode) params.periode = filters.periode;
      
      const data = await authApi.getEvaluations(params);
      evaluations = data.results || data;
      
      // Sélectionner la première évaluation par défaut si aucune sélectionnée
      if (evaluations.length > 0 && (!selectedEvaluation || !evaluations.find(e => e.id === selectedEvaluation.id))) {
        selectedEvaluation = evaluations[0];
      }
    } catch (err) {
      error = err.message || 'Erreur lors du chargement des évaluations';
      console.error(err);
    } finally {
      loading = false;
    }
  }

  function applyFilters(newFilters) {
    filters = newFilters;
    loadEvaluations();
  }

  function selectEvaluation(eva) {
    selectedEvaluation = eva;
  }

  function openForm() {
    dispatch('open');
  }

  // Supprimer une évaluation
  async function deleteEvaluation(id) {
    if (!confirm('Supprimer cette évaluation ?')) return;
    try {
      await authApi.deleteEvaluation(id);
      successMessage = 'Évaluation supprimée';
      setTimeout(() => successMessage = null, 3000);
      await loadEvaluations();
      if (selectedEvaluation?.id === id) selectedEvaluation = null;
    } catch (err) {
      error = err.message;
      setTimeout(() => error = null, 5000);
    }
  }

  // Publier / dépublier
  async function togglePublish(evaluation) {
    try {
      if (evaluation.statut === 'publie') {
        await authApi.unpublishEvaluation(evaluation.id);
      } else {
        await authApi.publishEvaluation(evaluation.id);
      }
      await loadEvaluations();
    } catch (err) {
      error = err.message;
      setTimeout(() => error = null, 5000);
    }
  }
</script>

<div>
  <!-- Messages -->
  {#if successMessage}
    <div class="mb-4 p-4 bg-green-50 border border-green-200 rounded-md flex items-center">
      <Icon icon="heroicons:check-circle" class="h-5 w-5 text-green-400 mr-2" />
      <p class="text-sm text-green-700">{successMessage}</p>
    </div>
  {/if}
  {#if error}
    <div class="mb-4 p-4 bg-red-50 border border-red-200 rounded-md flex items-center">
      <Icon icon="heroicons:x-circle" class="h-5 w-5 text-red-400 mr-2" />
      <p class="text-sm text-red-700">{error}</p>
    </div>
  {/if}

  <!-- En-tête -->
  <div class="sm:flex sm:items-center justify-between">
    <div class="mb-4 sm:mb-0">
      <h1 class="text-2xl font-bold leading-6 text-gray-900">Notes & Évaluations</h1>
      <p class="mt-2 text-sm text-gray-700">
        Gestion des évaluations et des notes des étudiants
      </p>
    </div>
    <div class="flex space-x-3">
      <button 
        on:click={openForm}
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700">
        <Icon icon="heroicons:plus-sm" class="-ml-1 mr-2 h-5 w-5" />
        Nouvelle évaluation
      </button>
      <button class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50">
        <Icon icon="heroicons:arrow-down-tray" class="-ml-1 mr-2 h-5 w-5" />
        Exporter le bulletin
      </button>
    </div>
  </div>
  
  <!-- Filtres -->
  <GradeFilters 
    bind:filters={filters}
    {classOptions}
    {subjectOptions}
    {periodOptions}
    on:apply={(e) => applyFilters(e.detail)} 
  />
  
  <!-- Résumé statistique (à adapter avec les données de selectedEvaluation) -->
  {#if selectedEvaluation}
    <GradeSummary evaluation={selectedEvaluation} />
  {/if}
  
  <div class="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-3">
    <!-- Graphique -->
    <div class="lg:col-span-1">
      {#if selectedEvaluation}
        <GradeChart evaluation={selectedEvaluation} />
      {:else}
        <p class="text-gray-500 text-sm">Sélectionnez une évaluation</p>
      {/if}
    </div>
    
    <!-- Liste des évaluations -->
    <div class="lg:col-span-2">
      <div class="bg-white shadow-sm border border-gray-200 rounded-lg overflow-hidden">
        <div class="border-b border-gray-200 bg-gray-50 px-4 py-3">
          <h3 class="text-sm font-medium text-gray-900">Évaluations récentes</h3>
        </div>
        {#if loading}
          <div class="p-4 text-center text-gray-500">Chargement...</div>
        {:else if evaluations.length === 0}
          <div class="p-4 text-center text-gray-500">Aucune évaluation trouvée</div>
        {:else}
          <ul class="divide-y divide-gray-200">
            {#each evaluations as evalu}
              <li 
                class="px-4 py-4 hover:bg-gray-50 cursor-pointer {selectedEvaluation?.id === evalu.id ? 'bg-green-50' : ''}"
                on:click={() => selectEvaluation(evalu)}>
                <div class="flex items-center justify-between">
                  <div>
                    <p class="text-sm font-medium text-green-600">{evalu.nom}</p>
                    <p class="text-sm text-gray-500">{evalu.matiere_nom} • {evalu.classe_nom}</p>
                  </div>
                  <div class="flex items-center space-x-2">
                    <button 
                      on:click|stopPropagation={() => togglePublish(evalu)}
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                             {evalu.statut === 'publie' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}">
                      {evalu.statut === 'publie' ? 'Publié' : 'Brouillon'}
                    </button>
                    <p class="text-sm text-gray-500">{evalu.date}</p>
                    <button 
                      on:click|stopPropagation={() => deleteEvaluation(evalu.id)}
                      class="text-red-400 hover:text-red-600">
                      <Icon icon="heroicons:trash" class="h-4 w-4" />
                    </button>
                    <Icon icon="heroicons:chevron-right" class="h-5 w-5 text-gray-400" />
                  </div>
                </div>
              </li>
            {/each}
          </ul>
        {/if}
      </div>
    </div>
  </div>
  
  <!-- Tableau des notes -->
  <div class="mt-6">
    {#if selectedEvaluation}
      <h3 class="text-lg font-medium text-gray-900 mb-4">Notes - {selectedEvaluation.nom}</h3>
      <GradeTable evaluation={selectedEvaluation} />
    {:else}
      <p class="text-gray-500">Sélectionnez une évaluation pour voir les notes</p>
    {/if}
  </div>
</div>