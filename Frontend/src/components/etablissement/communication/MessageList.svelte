<script>
  import Icon from '@iconify/svelte';
  export let messages;
  
  let selectedMessages = [];
  
  function toggleSelectAll(event) {
    if (event.target.checked) {
      selectedMessages = messages.map(msg => msg.id);
    } else {
      selectedMessages = [];
    }
  }
</script>

<div class="bg-white shadow-sm rounded-lg overflow-hidden border border-gray-200">
  <!-- Actions -->
  <div class="bg-gray-50 px-4 py-3 flex items-center justify-between border-b border-gray-200">
    <div class="flex items-center">
      <input
        type="checkbox"
        class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
        checked={selectedMessages.length === messages.length}
        on:change={toggleSelectAll}
      />
      {#if selectedMessages.length > 0}
        <span class="ml-3 text-sm text-gray-700">
          {selectedMessages.length} sélectionnés
        </span>
      {/if}
    </div>
    <div class="flex space-x-3">
      <button class="text-gray-500 hover:text-gray-700">
        <Icon icon="heroicons:archive-box" class="h-5 w-5" />
      </button>
      <button class="text-gray-500 hover:text-gray-700">
        <Icon icon="heroicons:trash" class="h-5 w-5" />
      </button>
      <button class="text-gray-500 hover:text-gray-700">
        <Icon icon="heroicons:ellipsis-vertical" class="h-5 w-5" />
      </button>
    </div>
  </div>
  
  <!-- Liste des messages -->
  <ul class="divide-y divide-gray-200">
    {#each messages as message}
      <li class={!message.read ? 'bg-green-50' : ''}>
        <div class="px-4 py-4 flex items-center">
          <div class="flex items-center min-w-0 flex-1">
            <input
              type="checkbox"
              class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded mr-3"
              checked={selectedMessages.includes(message.id)}
              on:change={() => {
                if (selectedMessages.includes(message.id)) {
                  selectedMessages = selectedMessages.filter(id => id !== message.id);
                } else {
                  selectedMessages = [...selectedMessages, message.id];
                }
              }}
            />
            <div class="min-w-0 flex-1">
              <div class="flex justify-between">
                <p class={`text-sm font-medium ${message.important ? 'text-green-600' : 'text-gray-900'} truncate`}>
                  {message.sender}
                </p>
                <p class="text-sm text-gray-500 ml-2 whitespace-nowrap">
                  {message.time}
                </p>
              </div>
              <p class="text-sm text-gray-500 truncate">
                {message.subject}
              </p>
              <p class="text-sm text-gray-500 mt-1">
                {message.preview}
              </p>
            </div>
          </div>
          <div class="ml-4 flex-shrink-0">
            {#if message.important}
              <Icon icon="heroicons:exclamation-circle" class="h-5 w-5 text-yellow-500" />
            {/if}
          </div>
        </div>
      </li>
    {/each}
  </ul>
</div>