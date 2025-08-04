<script>
  import Icon from '@iconify/svelte';
  import FinanceStats from './FinanceStats.svelte';
  import PaymentTable from './PaymentTable.svelte';
  import InvoiceList from './InvoiceList.svelte';
  import FinancialChart from './FinancialChart.svelte';
  
  // Données simulées
  let activeTab = 'payments';
  let stats = {
    totalRevenue: 125430,
    pendingPayments: 23450,
    overduePayments: 8760,
    paymentRate: 82.5
  };
  
  let payments = [
    {
      id: 1,
      student: 'Jean Dupont',
      class: '3ème A',
      amount: 250,
      type: 'Frais de scolarité',
      dueDate: '15/06/2023',
      status: 'paid',
      paymentDate: '10/06/2023'
    },
  ];
  
  let invoices = [
    {
      id: 'FAC-2023-001',
      student: 'Sophie Martin',
      amount: 350,
      date: '01/09/2023',
      status: 'paid'
    },
  ];
</script>

<div>
  <!-- En-tête -->
  <div class="sm:flex sm:items-center justify-between">
    <div class="mb-4 sm:mb-0">
      <h1 class="text-2xl font-bold leading-6 text-gray-900">Gestion Financière</h1>
      <p class="mt-2 text-sm text-gray-700">
        Suivi des paiements, factures et statistiques financières
      </p>
    </div>
    <div class="flex space-x-3">
      <button class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
        <Icon icon="heroicons:plus-sm" class="-ml-1 mr-2 h-5 w-5" />
        Nouveau paiement
      </button>
      <button class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
        <Icon icon="heroicons:document-text" class="-ml-1 mr-2 h-5 w-5" />
        Générer rapport
      </button>
    </div>
  </div>
  
  <!-- Statistiques financières -->
  <FinanceStats {stats} />
  
  <!-- Graphique -->
  <div class="mt-6 bg-white shadow-sm rounded-lg p-4 border border-gray-200">
    <FinancialChart />
  </div>
  
  <!-- Navigation par onglets -->
  <div class="mt-8 border-b border-gray-200">
    <nav class="-mb-px flex space-x-8">
      <button
        on:click={() => activeTab = 'payments'}
        class={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'payments' ? 'border-green-500 text-green-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
      >
        Paiements
      </button>
      <button
        on:click={() => activeTab = 'invoices'}
        class={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'invoices' ? 'border-green-500 text-green-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
      >
        Factures
      </button>
      <button
        on:click={() => activeTab = 'reports'}
        class={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'reports' ? 'border-green-500 text-green-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
      >
        Rapports
      </button>
    </nav>
  </div>
  
  <!-- Contenu des onglets -->
  <div class="mt-6">
    {#if activeTab === 'payments'}
      <PaymentTable {payments} />
    {:else if activeTab === 'invoices'}
      <InvoiceList {invoices} />
    {:else if activeTab === 'reports'}
      <div class="bg-white shadow rounded-lg p-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Rapports Financiers</h2>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <!-- Rapport mensuel -->
          <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <div class="flex items-center">
              <div class="flex-shrink-0 bg-green-100 p-3 rounded-md">
                <Icon icon="heroicons:calendar" class="h-6 w-6 text-green-600" />
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-medium text-gray-900">Rapport Mensuel</h3>
                <p class="text-sm text-gray-500">Synthèse des revenus et paiements du mois</p>
              </div>
            </div>
            <div class="mt-4">
              <button class="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                <Icon icon="heroicons:arrow-down-tray" class="-ml-1 mr-2 h-5 w-5" />
                Télécharger
              </button>
            </div>
          </div>
          
          <!-- Rapport annuel -->
          <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <div class="flex items-center">
              <div class="flex-shrink-0 bg-green-100 p-3 rounded-md">
                <Icon icon="heroicons:chart-bar" class="h-6 w-6 text-green-600" />
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-medium text-gray-900">Rapport Annuel</h3>
                <p class="text-sm text-gray-500">Analyse des performances financières sur l'année</p>
              </div>
            </div>
            <div class="mt-4">
              <button class="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                <Icon icon="heroicons:arrow-down-tray" class="-ml-1 mr-2 h-5 w-5" />
                Télécharger
              </button>
            </div>
          </div>
          
          <!-- Rapport personnalisé -->
          <div class="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <div class="flex items-center">
              <div class="flex-shrink-0 bg-green-100 p-3 rounded-md">
                <Icon icon="heroicons:adjustments-horizontal" class="h-6 w-6 text-green-600" />
              </div>
              <div class="ml-4">
                <h3 class="text-lg font-medium text-gray-900">Rapport Personnalisé</h3>
                <p class="text-sm text-gray-500">Générez un rapport selon vos critères</p>
              </div>
            </div>
            <div class="mt-4">
              <button class="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                <Icon icon="heroicons:plus-sm" class="-ml-1 mr-2 h-5 w-5" />
                Créer
              </button>
            </div>
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>