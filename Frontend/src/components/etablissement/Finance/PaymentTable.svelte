<script>
  import Icon from '@iconify/svelte';
  export let payments;
  
  function getStatusBadge(status) {
    const statusClasses = {
      paid: 'bg-green-100 text-green-800',
      pending: 'bg-yellow-100 text-yellow-800',
      overdue: 'bg-red-100 text-red-800',
      cancelled: 'bg-gray-100 text-gray-800'
    };
    
    const statusLabels = {
      paid: 'Payé',
      pending: 'En attente',
      overdue: 'En retard',
      cancelled: 'Annulé'
    };
    
    return {
      class: statusClasses[status] || 'bg-gray-100 text-gray-800',
      label: statusLabels[status] || status
    };
  }
</script>

<div class="shadow-sm border border-gray-200 rounded-lg overflow-hidden">
  <table class="min-w-full divide-y divide-gray-200">
    <thead class="bg-gray-50">
      <tr>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          Étudiant
        </th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          Montant
        </th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          Type
        </th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          Date d'échéance
        </th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          Statut
        </th>
        <th scope="col" class="relative px-6 py-3">
          <span class="sr-only">Actions</span>
        </th>
      </tr>
    </thead>
    <tbody class="bg-white divide-y divide-gray-200">
      {#each payments as payment}
        <tr class="hover:bg-gray-50">
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="flex items-center">
              <div class="flex-shrink-0 h-10 w-10 bg-green-100 rounded-full flex items-center justify-center">
                <Icon icon="heroicons:user" class="h-6 w-6 text-green-600" />
              </div>
              <div class="ml-4">
                <div class="text-sm font-medium text-gray-900">{payment.student}</div>
                <div class="text-sm text-gray-500">{payment.class}</div>
              </div>
            </div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
            {new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(payment.amount)}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            {payment.type}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            {payment.dueDate}
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            {#if payment.statut}
              {@const status = getStatusBadge(payment.statut)}
              <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full {status.class}">
                {status.label}
              </span>
            {/if}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
            <div class="flex justify-end space-x-3">
              {#if payment.status !== 'paid'}
                <button class="text-green-600 hover:text-green-900">
                  <Icon icon="heroicons:credit-card" class="h-5 w-5" />
                </button>
              {/if}
              <button class="text-gray-600 hover:text-gray-900">
                <Icon icon="heroicons:printer" class="h-5 w-5" />
              </button>
              <button class="text-red-600 hover:text-red-900">
                <Icon icon="heroicons:trash" class="h-5 w-5" />
              </button>
            </div>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>