<script>
  import Icon from '@iconify/svelte';
  
  let title = '';
  let content = '';
  let targetGroups = [];
  let isPinned = false;
  let isUrgent = false;
  
  const groupOptions = [
    { id: 'all', name: 'Tous les utilisateurs' },
    { id: 'teachers', name: 'Professeurs' },
    { id: 'students', name: 'Étudiants' },
    { id: 'parents', name: 'Parents' },
    { id: 'class_3a', name: 'Classe 3ème A' },
    { id: 'class_4b', name: 'Classe 4ème B' }
  ];
  
  function handleSubmit() {
    const announcement = {
      title,
      content,
      targetGroups,
      isPinned,
      isUrgent,
      date: new Date().toLocaleDateString()
    };
    // Ici vous enverriez l'annonce au backend
    console.log('Nouvelle annonce:', announcement);
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
    <div class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full sm:p-6">
      <div>
        <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100">
          <Icon icon="heroicons:megaphone" class="h-6 w-6 text-green-600" />
        </div>
        <div class="mt-3 text-center sm:mt-5">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Nouvelle annonce
          </h3>
          <p class="mt-2 text-sm text-gray-500">
            Remplissez les détails de l'annonce à publier
          </p>
        </div>
      </div>
      
      <form class="mt-5 space-y-4" on:submit|preventDefault={handleSubmit}>
        <div>
          <label for="title" class="block text-sm font-medium text-gray-700">Titre de l'annonce</label>
          <input
            type="text"
            id="title"
            bind:value={title}
            required
            class="mt-1 block w-full shadow-sm sm:text-sm focus:ring-green-500 focus:border-green-500 border-gray-300 rounded-md"
            placeholder="Ex: Réunion parents-professeurs"
          />
        </div>
        
        <div>
          <label for="content" class="block text-sm font-medium text-gray-700">Contenu</label>
          <textarea
            id="content"
            rows={5}
            bind:value={content}
            required
            class="mt-1 block w-full shadow-sm sm:text-sm focus:ring-green-500 focus:border-green-500 border-gray-300 rounded-md"
            placeholder="Détails de l'annonce..."
          ></textarea>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700">Destinataires</label>
          <div class="mt-2 grid grid-cols-1 gap-4 sm:grid-cols-2">
            {#each groupOptions as group}
              <div class="relative flex items-start">
                <div class="flex items-center h-5">
                  <input
                    id={group.id}
                    name="targetGroups"
                    type="checkbox"
                    class="focus:ring-green-500 h-4 w-4 text-green-600 border-gray-300 rounded"
                    bind:group={targetGroups}
                    value={group.id}
                  />
                </div>
                <div class="ml-3 text-sm">
                  <label for={group.id} class="font-medium text-gray-700">{group.name}</label>
                </div>
              </div>
            {/each}
          </div>
        </div>
        
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input
              id="pinned"
              name="pinned"
              type="checkbox"
              bind:checked={isPinned}
              class="focus:ring-green-500 h-4 w-4 text-green-600 border-gray-300 rounded"
            />
            <label for="pinned" class="ml-2 block text-sm text-gray-700">
              Épingler cette annonce
            </label>
          </div>
          
          <div class="flex items-center">
            <input
              id="urgent"
              name="urgent"
              type="checkbox"
              bind:checked={isUrgent}
              class="focus:ring-green-500 h-4 w-4 text-green-600 border-gray-300 rounded"
            />
            <label for="urgent" class="ml-2 block text-sm text-gray-700">
              Annonce urgente
            </label>
          </div>
        </div>
        
        <div class="mt-6 flex items-center justify-end space-x-4">
          <button
            type="button"
            class="inline-flex justify-center items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
            on:click={() => dispatch('close')}
          >
            Annuler
          </button>
          <button
            type="submit"
            class="inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
          >
            Publier l'annonce
          </button>
        </div>
      </form>
    </div>
  </div>
</div>