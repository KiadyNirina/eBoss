<script>
  import Icon from '@iconify/svelte';
  export let notifications;
  
  function getNotificationIcon(type) {
    const icons = {
      absence: 'heroicons:user-minus',
      grade: 'heroicons:clipboard-document-check',
      payment: 'heroicons:currency-dollar',
      event: 'heroicons:calendar'
    };
    return icons[type] || 'heroicons:bell';
  }
  
  function getNotificationColor(type) {
    const colors = {
      absence: 'bg-yellow-100 text-yellow-800',
      grade: 'bg-green-100 text-green-800',
      payment: 'bg-blue-100 text-blue-800',
      event: 'bg-purple-100 text-purple-800'
    };
    return colors[type] || 'bg-gray-100 text-gray-800';
  }
</script>

<div class="bg-white shadow-sm rounded-lg overflow-hidden border border-gray-200">
  <!-- En-tête -->
  <div class="bg-gray-50 px-4 py-3 flex items-center justify-between border-b border-gray-200">
    <h3 class="text-sm font-medium text-gray-900">
      Vos notifications récentes
    </h3>
    <button class="text-sm font-medium text-green-600 hover:text-green-500">
      Tout marquer comme lu
    </button>
  </div>
  
  <!-- Liste des notifications -->
  <ul class="divide-y divide-gray-200">
    {#each notifications as notification}
      <li class={!notification.read ? 'bg-green-50' : ''}>
        <div class="px-4 py-4 flex items-start">
          <div class={`flex-shrink-0 p-2 rounded-full ${getNotificationColor(notification.type)}`}>
            <Icon icon={getNotificationIcon(notification.type)} class="h-5 w-5" />
          </div>
          <div class="ml-3 flex-1">
            <p class="text-sm text-gray-700">
              {notification.content}
            </p>
            <p class="mt-1 text-xs text-gray-500">
              {notification.time}
            </p>
          </div>
          {#if !notification.read}
            <div class="ml-4 flex-shrink-0">
              <span class="h-2 w-2 rounded-full bg-green-500"></span>
            </div>
          {/if}
        </div>
      </li>
    {/each}
  </ul>
  
  <!-- Pied de page -->
  <div class="bg-gray-50 px-4 py-3 text-right">
    <button class="text-sm font-medium text-green-600 hover:text-green-500">
      Voir toutes les notifications
    </button>
  </div>
</div>