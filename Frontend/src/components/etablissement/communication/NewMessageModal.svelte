<script>
  import Icon from '@iconify/svelte';
  
  let recipients = '';
  let subject = '';
  let message = '';
  
  function handleSubmit() {
    dispatch('close');
  }
</script>

<div class="fixed z-10 inset-0 overflow-y-auto">
  <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
    <!-- Fond -->
    <div class="fixed inset-0 transition-opacity" aria-hidden="true">
      <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
    </div>
    
    <!-- Contenu -->
    <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
      <div>
        <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
          <Icon icon="heroicons:envelope" class="h-6 w-6 text-green-600" />
        </div>
        <div class="mt-3 text-center sm:mt-5">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Nouveau message
          </h3>
        </div>
      </div>
      
      <form class="mt-5 space-y-4" on:submit|preventDefault={handleSubmit}>
        <div>
          <label for="recipients" class="block text-sm font-medium text-gray-700">Destinataires</label>
          <input
            type="text"
            id="recipients"
            bind:value={recipients}
            class="mt-1 block w-full shadow-sm sm:text-sm focus:ring-green-500 focus:border-green-500 border-gray-300 rounded-md"
            placeholder="Saisissez des noms ou groupes"
          />
        </div>
        
        <div>
          <label for="subject" class="block text-sm font-medium text-gray-700">Sujet</label>
          <input
            type="text"
            id="subject"
            bind:value={subject}
            class="mt-1 block w-full shadow-sm sm:text-sm focus:ring-green-500 focus:border-green-500 border-gray-300 rounded-md"
          />
        </div>
        
        <div>
          <label for="message" class="block text-sm font-medium text-gray-700">Message</label>
          <textarea
            id="message"
            rows={4}
            bind:value={message}
            class="mt-1 block w-full shadow-sm sm:text-sm focus:ring-green-500 focus:border-green-500 border-gray-300 rounded-md"
          ></textarea>
        </div>
        
        <div class="flex items-center space-x-4">
          <div class="flex-1">
            <button
              type="button"
              class="inline-flex justify-center items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              on:click={() => dispatch('close')}
            >
              Annuler
            </button>
          </div>
          <div class="flex-1">
            <button
              type="submit"
              class="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
            >
              Envoyer
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</div>