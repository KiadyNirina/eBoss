<script>
  import Icon from '@iconify/svelte';
  
  export let applications;
  export let activeTab;
  
  function getStatusBadge(status) {
    const statusMap = {
      nouveau: { class: 'bg-blue-100 text-blue-800', label: 'Nouveau' },
      en_revue: { class: 'bg-yellow-100 text-yellow-800', label: 'En revue' },
      accepte: { class: 'bg-green-100 text-green-800', label: 'Accepté' },
      rejete: { class: 'bg-red-100 text-red-800', label: 'Rejeté' }
    };
    return statusMap[status] || { class: 'bg-gray-100 text-gray-800', label: status };
  }
  
  function getActionButton(status) {
    switch (status) {
      case 'nouveau':
        return { color: 'green', icon: 'heroicons:eye', text: 'Examiner' };
      case 'en_revue':
        return { color: 'green', icon: 'heroicons:check', text: 'Accepter' };
      default:
        return { color: 'gray', icon: 'heroicons:eye', text: 'Voir' };
    }
  }
</script>

<div class="bg-white shadow overflow-hidden sm:rounded-lg">
  <ul class="divide-y divide-gray-200">
    {#each applications as app}
      <li class="px-6 py-4 hover:bg-gray-50">
        <div class="flex items-center justify-between">
          <!-- Info candidat -->
          <div class="flex items-center min-w-0">
            <div class="flex-shrink-0 bg-green-100 rounded-md p-2">
              <Icon icon="heroicons:user-circle" class="h-6 w-6 text-green-600" />
            </div>
            <div class="ml-4 min-w-0">
              <div class="flex items-center">
                <p class="text-sm font-medium text-green-600 truncate">
                  {app.prenom} {app.nom}
                </p>
                <span class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                  {app.niveau}
                </span>
              </div>
              <div class="flex items-center mt-1 text-sm text-gray-500">
                <Icon icon="heroicons:calendar" class="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
                <span>Déposé le {app.date}</span>
                <span class="mx-1">·</span>
                <Icon icon="heroicons:document-text" class="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
                <span>{app.documents} documents</span>
              </div>
            </div>
          </div>
          
          <!-- Statut et actions -->
          <div class="flex items-center space-x-4">
            <span class="px-3 py-1 rounded-full text-xs font-medium {getStatusBadge(app.statut).class}">
              {getStatusBadge(app.statut).label}
            </span>
            
            {#if activeTab === 'en_cours'}
              <button
                class="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-{getActionButton(app.statut).color}-600 hover:bg-{getActionButton(app.statut).color}-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-{getActionButton(app.statut).color}-500"
              >
                <Icon icon={getActionButton(app.statut).icon} class="-ml-1 mr-1 h-4 w-4" />
                {getActionButton(app.statut).text}
              </button>
            {:else}
              <button
                class="inline-flex items-center px-3 py-1 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              >
                <Icon icon="heroicons:eye" class="-ml-1 mr-1 h-4 w-4" />
                Voir
              </button>
            {/if}
          </div>
        </div>
      </li>
    {/each}
  </ul>
</div>