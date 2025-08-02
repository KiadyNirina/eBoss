<script>
  import Icon from '@iconify/svelte';
  export let activities;
  
  const activityIcons = {
    new_student: 'heroicons:user-plus',
    payment: 'heroicons:currency-dollar',
    grade: 'heroicons:clipboard-document-check',
    absence: 'heroicons:exclamation-triangle'
  };
  
  const activityColors = {
    new_student: 'text-green-500 bg-green-100',
    payment: 'text-blue-500 bg-blue-100',
    grade: 'text-purple-500 bg-purple-100',
    absence: 'text-yellow-500 bg-yellow-100'
  };
</script>

<div class="bg-white shadow rounded-lg overflow-hidden">
  <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
    <h3 class="text-lg leading-6 font-medium text-gray-900">Activités récentes</h3>
  </div>
  <div class="divide-y divide-gray-200">
    {#each activities as activity}
      <div class="px-4 py-4 sm:px-6">
        <div class="flex items-center">
          <div class={`flex-shrink-0 rounded-full p-2 ${activityColors[activity.type]}`}>
            <Icon icon={activityIcons[activity.type]} class="h-5 w-5" />
          </div>
          <div class="ml-3 flex-1">
            <div class="flex items-center justify-between">
              <p class="text-sm font-medium text-gray-900">
                {#if activity.type === 'new_student'}
                  Nouvel étudiant: {activity.name} ({activity.class})
                {:else if activity.type === 'payment'}
                  Paiement reçu: {activity.name} ({activity.amount})
                {:else if activity.type === 'grade'}
                  Notes ajoutées: {activity.name} ({activity.class})
                {:else if activity.type === 'absence'}
                  Absence signalée: {activity.name} ({activity.class})
                {/if}
              </p>
              <p class="text-sm text-gray-500">{activity.time}</p>
            </div>
          </div>
        </div>
      </div>
    {/each}
  </div>
  <div class="bg-gray-50 px-4 py-4 sm:px-6">
    <div class="text-sm">
      <a href="#" class="font-medium text-green-600 hover:text-green-500">
        Voir toutes les activités
      </a>
    </div>
  </div>
</div>