<script>
  import Icon from '@iconify/svelte';
  export let stats;
</script>

<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-5 mb-6">
  <!-- Total -->
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="px-4 py-5 sm:p-6">
      <div class="flex items-center">
        <div class="flex-shrink-0 bg-green-100 p-3 rounded-md">
          <Icon icon="heroicons:users" class="h-6 w-6 text-green-600" />
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">Total candidatures</dt>
            <dd>
              <div class="text-lg font-medium text-gray-900">{stats.total}</div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Nouvelles -->
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="px-4 py-5 sm:p-6">
      <div class="flex items-center">
        <div class="flex-shrink-0 bg-blue-100 p-3 rounded-md">
          <Icon icon="heroicons:bell-alert" class="h-6 w-6 text-blue-600" />
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">Nouvelles</dt>
            <dd>
              <div class="text-lg font-medium text-gray-900">{stats.new}</div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
  
  <!-- En revue -->
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="px-4 py-5 sm:p-6">
      <div class="flex items-center">
        <div class="flex-shrink-0 bg-yellow-100 p-3 rounded-md">
          <Icon icon="heroicons:eye" class="h-6 w-6 text-yellow-600" />
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">En revue</dt>
            <dd>
              <div class="text-lg font-medium text-gray-900">{stats.inReview}</div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Acceptées -->
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="px-4 py-5 sm:p-6">
      <div class="flex items-center">
        <div class="flex-shrink-0 bg-green-100 p-3 rounded-md">
          <Icon icon="heroicons:check-badge" class="h-6 w-6 text-green-600" />
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">Acceptées</dt>
            <dd>
              <div class="text-lg font-medium text-gray-900">{stats.accepted}</div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Rejetées -->
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="px-4 py-5 sm:p-6">
      <div class="flex items-center">
        <div class="flex-shrink-0 bg-red-100 p-3 rounded-md">
          <Icon icon="heroicons:x-circle" class="h-6 w-6 text-red-600" />
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">Rejetées</dt>
            <dd>
              <div class="text-lg font-medium text-gray-900">{stats.rejected}</div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
</div>