<script>
  import Icon from '@iconify/svelte';
  export let stats;
  
  $: {
    if (!stats) {
      stats = {
        students: 0,
        teachers: 0,
        classes: 0,
        pendingPayments: 0
      };
    }
  }
</script>

<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
  <!-- Étudiants -->
  <div class="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow duration-200">
    <div class="p-5">
      <div class="flex items-center">
        <div class="flex-shrink-0 bg-green-100 p-3 rounded-md">
          <Icon icon="heroicons:user-group" class="h-6 w-6 text-green-600" />
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">Étudiants</dt>
            <dd>
              <div class="text-lg font-medium text-gray-900">
                {stats.students || 0}
              </div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
    <div class="bg-gray-50 px-5 py-3">
      <div class="text-sm">
        <a href="/etablissement/etudiants" class="font-medium text-green-600 hover:text-green-500">
          Voir tous
        </a>
      </div>
    </div>
  </div>
  
  <!-- Professeurs -->
  <div class="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow duration-200">
    <div class="p-5">
      <div class="flex items-center">
        <div class="flex-shrink-0 bg-green-100 p-3 rounded-md">
          <Icon icon="heroicons:academic-cap" class="h-6 w-6 text-green-600" />
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">Professeurs</dt>
            <dd>
              <div class="text-lg font-medium text-gray-900">
                {stats.teachers || 0}
              </div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
    <div class="bg-gray-50 px-5 py-3">
      <div class="text-sm">
        <a href="/etablissement/professeurs" class="font-medium text-green-600 hover:text-green-500">
          Voir tous
        </a>
      </div>
    </div>
  </div>
  
  <!-- Classes -->
  <div class="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow duration-200">
    <div class="p-5">
      <div class="flex items-center">
        <div class="flex-shrink-0 bg-green-100 p-3 rounded-md">
          <Icon icon="heroicons:rectangle-group" class="h-6 w-6 text-green-600" />
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">Classes</dt>
            <dd>
              <div class="text-lg font-medium text-gray-900">
                {stats.classes || 0}
              </div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
    <div class="bg-gray-50 px-5 py-3">
      <div class="text-sm">
        <a href="/etablissement/classes" class="font-medium text-green-600 hover:text-green-500">
          Voir toutes
        </a>
      </div>
    </div>
  </div>
  
  <!-- Paiements en attente -->
  <div class="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow duration-200">
    <div class="p-5">
      <div class="flex items-center">
        <div class="flex-shrink-0 bg-green-100 p-3 rounded-md">
          <Icon icon="heroicons:currency-dollar" class="h-6 w-6 text-green-600" />
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">Paiements en attente</dt>
            <dd>
              <div class="text-lg font-medium text-gray-900">
                {stats.pendingPayments || 0}
              </div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
    <div class="bg-gray-50 px-5 py-3">
      <div class="text-sm">
        <a href="/etablissement/paiements" class="font-medium text-green-600 hover:text-green-500">
          Gérer
        </a>
      </div>
    </div>
  </div>
</div>