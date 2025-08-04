<script>
  import Icon from '@iconify/svelte';
  export let announcements;
</script>

<div class="bg-white shadow-sm rounded-lg overflow-hidden border border-gray-200">
  <!-- Liste des annonces -->
  <ul class="divide-y divide-gray-200">
    {#each announcements as announcement}
      <li class={announcement.pinned ? 'bg-green-50' : ''}>
        <div class="px-4 py-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              {#if announcement.pinned}
                <Icon icon="heroicons:map-pin" class="h-5 w-5 text-green-500 mr-2" />
              {/if}
              <p class="text-sm font-medium text-gray-900">
                {announcement.title}
              </p>
            </div>
            <p class="text-sm text-gray-500">
              {announcement.date}
            </p>
          </div>
          <p class="mt-2 text-sm text-gray-600">
            {announcement.content}
          </p>
          <div class="mt-3 flex items-center justify-between">
            <span class="text-xs font-medium text-gray-500">
              Par {announcement.author}
            </span>
            <div class="flex space-x-2">
              <button class="text-green-600 hover:text-green-800 text-sm font-medium">
                <Icon icon="heroicons:share" class="h-4 w-4 inline mr-1" />
                Partager
              </button>
            </div>
          </div>
        </div>
      </li>
    {/each}
  </ul>
</div>