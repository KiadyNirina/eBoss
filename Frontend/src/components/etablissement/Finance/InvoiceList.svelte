<script>
  import Icon from '@iconify/svelte';
  export let invoices;
  
  function getStatusBadge(status) {
    return status === 'paid' 
      ? 'bg-green-100 text-green-800' 
      : 'bg-yellow-100 text-yellow-800';
  }
</script>

<div class="bg-white shadow rounded-lg overflow-hidden">
  <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
    <h3 class="text-lg leading-6 font-medium text-gray-900">Factures</h3>
  </div>
  <ul class="divide-y divide-gray-200">
    {#each invoices as invoice}
      <li class="px-4 py-4 sm:px-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-green-100 p-3 rounded-md">
              <Icon icon="heroicons:document-text" class="h-6 w-6 text-green-600" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-900">
                Facture #{invoice.id} - {invoice.student}
              </p>
              <p class="text-sm text-gray-500">
                {new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(invoice.amount)} • Émise le {invoice.date}
              </p>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <span class={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusBadge(invoice.status)}`}>
              {invoice.status === 'paid' ? 'Payée' : 'En attente'}
            </span>
            <button class="text-gray-400 hover:text-gray-500">
              <Icon icon="heroicons:arrow-down-tray" class="h-5 w-5" />
            </button>
            <button class="text-gray-400 hover:text-gray-500">
              <Icon icon="heroicons:printer" class="h-5 w-5" />
            </button>
          </div>
        </div>
      </li>
    {/each}
  </ul>
  <div class="bg-gray-50 px-4 py-4 sm:px-6">
    <div class="text-sm">
      <a href="#" class="font-medium text-green-600 hover:text-green-500">
        Voir toutes les factures
      </a>
    </div>
  </div>
</div>