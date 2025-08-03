<script>
  import Icon from '@iconify/svelte';
  import AdmissionsTabs from './AdmissionsTabs.svelte';
  import AdmissionsStats from './AdmissionsStats.svelte';
  import ApplicationList from './ApplicationList.svelte';
  import ProcessStepper from './ProcessStepper.svelte';
  
  // Données simulées
  const stats = {
    total: 245,
    new: 32,
    inReview: 56,
    accepted: 124,
    rejected: 33
  };
  
  const applications = [
    {
      id: 1001,
      nom: 'Dupont',
      prenom: 'Lucas',
      niveau: '3ème',
      date: '15/05/2023',
      statut: 'en_revue',
      etape: 2,
      documents: 3
    },
    {
      id: 1002,
      nom: 'Martin',
      prenom: 'Emma',
      niveau: 'CP',
      date: '12/05/2023',
      statut: 'nouveau',
      etape: 1,
      documents: 2
    },
  ];
  
  const processSteps = [
    { id: 1, name: 'Dépôt de dossier', status: 'complete' },
    { id: 2, name: 'Examen administratif', status: 'current' },
    { id: 3, name: 'Entretien', status: 'upcoming' },
    { id: 4, name: 'Décision', status: 'upcoming' },
    { id: 5, name: 'Inscription finale', status: 'upcoming' }
  ];
  
  let activeTab = 'en_cours';
</script>

<div>
  <!-- En-tête avec boutons -->
  <div class="sm:flex sm:items-center justify-between mb-8">
    <div>
      <h1 class="text-2xl font-bold leading-6 text-gray-900">Gestion des Inscriptions</h1>
      <p class="mt-2 text-sm text-gray-700">
        Processus d'admission et inscriptions pour l'année scolaire 2023-2024
      </p>
    </div>
    <div class="mt-4 sm:mt-0 flex space-x-3">
      <button class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
        <Icon icon="heroicons:plus-sm" class="-ml-1 mr-2 h-5 w-5" />
        Nouvelle inscription
      </button>
      <button class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
        <Icon icon="heroicons:cog" class="-ml-1 mr-2 h-5 w-5" />
        Configurer
      </button>
    </div>
  </div>
  
  <!-- Statistiques -->
  <AdmissionsStats {stats} />
  
  <!-- Onglets -->
  <AdmissionsTabs bind:activeTab />
  
  <!-- Processus d'admission -->
  <div class="mt-6 bg-white shadow rounded-lg p-6">
    <h2 class="text-lg font-medium text-gray-900 mb-4">Processus d'admission</h2>
    <ProcessStepper steps={processSteps} />
  </div>
  
  <!-- Liste des candidatures -->
  <div class="mt-6">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-medium text-gray-900">
        {#if activeTab === 'en_cours'}
          Candidatures en cours
        {:else if activeTab === 'acceptees'}
          Candidatures acceptées
        {:else if activeTab === 'rejetees'}
          Candidatures rejetées
        {/if}
      </h2>
      <div class="flex items-center space-x-2">
        <div class="relative">
          <button class="inline-flex items-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
            <Icon icon="heroicons:funnel" class="mr-2 h-4 w-4" />
            Filtrer
          </button>
        </div>
        <button class="inline-flex items-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
          <Icon icon="heroicons:arrow-down-tray" class="mr-2 h-4 w-4" />
          Exporter
        </button>
      </div>
    </div>
    
    <ApplicationList applications={applications} {activeTab} />
  </div>
</div>