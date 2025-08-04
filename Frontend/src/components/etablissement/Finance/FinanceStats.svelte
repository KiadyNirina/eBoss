<script>
  import Icon from '@iconify/svelte';
  export let stats;
</script>

<div class="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
  <!-- Revenu total -->
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="p-5">
      <div class="flex items-center">
        <div class="flex-shrink-0 bg-green-100 p-3 rounded-md">
          <Icon icon="heroicons:banknotes" class="h-6 w-6 text-green-600" />
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">Revenu total</dt>
            <dd>
              <div class="text-lg font-medium text-gray-900">{new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(stats.totalRevenue)}</div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Paiements en attente -->
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="p-5">
      <div class="flex items-center">
        <div class="flex-shrink-0 bg-yellow-100 p-3 rounded-md">
          <Icon icon="heroicons:clock" class="h-6 w-6 text-yellow-600" />
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">Paiements en attente</dt>
            <dd>
              <div class="text-lg font-medium text-gray-900">{new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(stats.pendingPayments)}</div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Retards de paiement -->
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="p-5">
      <div class="flex items-center">
        <div class="flex-shrink-0 bg-red-100 p-3 rounded-md">
          <Icon icon="heroicons:exclamation-triangle" class="h-6 w-6 text-red-600" />
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">Retards de paiement</dt>
            <dd>
              <div class="text-lg font-medium text-gray-900">{new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(stats.overduePayments)}</div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Taux de paiement -->
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="p-5">
      <div class="flex items-center">
        <div class="flex-shrink-0 bg-blue-100 p-3 rounded-md">
          <Icon icon="heroicons:chart-pie" class="h-6 w-6 text-blue-600" />
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">Taux de paiement</dt>
            <dd>
              <div class="text-lg font-medium text-gray-900">{stats.paymentRate}%</div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
</div>