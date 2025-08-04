<script>
  import Icon from '@iconify/svelte';
  import GradeFilters from './GradeFilters.svelte';
  import GradeSummary from './GradeSummary.svelte';
  import GradeTable from './GradeTable.svelte';
  import GradeChart from './GradeChart.svelte';
  
  // Données simulées
  let evaluations = [
    {
      id: 1,
      nom: 'Contrôle de Mathématiques',
      matiere: 'Mathématiques',
      classe: '4ème B',
      date: '15/05/2023',
      coefficient: 2,
      type: 'Contrôle',
      statut: 'publié',
      notes: [
        { etudiantId: 1, nom: 'Dupont', prenom: 'Jean', note: 15, appreciation: 'Très bien' },
        { etudiantId: 2, nom: 'Martin', prenom: 'Sophie', note: 12, appreciation: 'Bien' },
      ]
    },
  ];
  
  let selectedEvaluation = evaluations[0];
  let filters = {
    classe: '',
    matiere: '',
    periode: ''
  };
  
  function applyFilters(newFilters) {
    filters = newFilters;
  }
  
  function selectEvaluation(eva) {
    selectedEvaluation = eva;
  }
</script>

<div>
  <!-- En-tête -->
  <div class="sm:flex sm:items-center justify-between">
    <div class="mb-4 sm:mb-0">
      <h1 class="text-2xl font-bold leading-6 text-gray-900">Notes & Évaluations</h1>
      <p class="mt-2 text-sm text-gray-700">
        Gestion des évaluations et des notes des étudiants
      </p>
    </div>
    <div class="flex space-x-3">
      <button class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
        <Icon icon="heroicons:plus-sm" class="-ml-1 mr-2 h-5 w-5" />
        Nouvelle évaluation
      </button>
      <button class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
        <Icon icon="heroicons:arrow-down-tray" class="-ml-1 mr-2 h-5 w-5" />
        Exporter le bulletin
      </button>
    </div>
  </div>
  
  <!-- Filtres -->
  <GradeFilters {filters} on:apply={applyFilters} />
  
  <!-- Résumé statistique -->
  <GradeSummary {selectedEvaluation} />
  
  <div class="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-3">
    <!-- Graphique -->
    <div class="lg:col-span-1">
      <GradeChart {selectedEvaluation} />
    </div>
    
    <!-- Liste des évaluations -->
    <div class="lg:col-span-2">
      <div class="bg-white shadow-sm border border-gray-200 rounded-lg overflow-hidden">
        <div class="border-b border-gray-200 bg-gray-50 px-4 py-3">
          <h3 class="text-sm font-medium text-gray-900">Évaluations récentes</h3>
        </div>
        <ul class="divide-y divide-gray-200">
          {#each evaluations as evalu}
            <li class="px-4 py-4 hover:bg-gray-50 cursor-pointer {selectedEvaluation.id === evalu.id ? 'bg-green-50' : ''}"
                on:click={() => selectEvaluation(evalu)}>
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-green-600">{evalu.nom}</p>
                  <p class="text-sm text-gray-500">{evalu.matiere} • {evalu.classe}</p>
                </div>
                <div class="flex items-center space-x-2">
                  <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                             {evalu.statut === 'publié' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}">
                    {evalu.statut === 'publié' ? 'Publié' : 'Brouillon'}
                  </span>
                  <p class="text-sm text-gray-500">{evalu.date}</p>
                  <Icon icon="heroicons:chevron-right" class="h-5 w-5 text-gray-400" />
                </div>
              </div>
            </li>
          {/each}
        </ul>
      </div>
    </div>
  </div>
  
  <!-- Tableau des notes -->
  <div class="mt-6">
    <h3 class="text-lg font-medium text-gray-900 mb-4">Notes - {selectedEvaluation.nom}</h3>
    <GradeTable {selectedEvaluation} />
  </div>
</div>