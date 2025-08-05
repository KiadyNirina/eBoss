<script>
  import Icon from '@iconify/svelte';
  
  let files = [];
  let isDragging = false;
  
  function handleDragOver(e) {
    e.preventDefault();
    isDragging = true;
  }
  
  function handleDragLeave() {
    isDragging = false;
  }
  
  function handleDrop(e) {
    e.preventDefault();
    isDragging = false;
    files = [...files, ...Array.from(e.dataTransfer.files)];
  }
  
  function handleFileSelect(e) {
    files = [...files, ...Array.from(e.target.files)];
  }
  
  function removeFile(index) {
    files = files.filter((_, i) => i !== index);
  }
</script>

<div class="fixed z-50 inset-0 overflow-y-auto">
  <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
    <!-- Fond -->
    <div class="fixed inset-0 transition-opacity" aria-hidden="true">
      <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
    </div>
    
    <!-- Contenu -->
    <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
      <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
        <div class="sm:flex sm:items-start">
          <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
            <div class="flex justify-between items-center">
              <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                Téléverser des fichiers
              </h3>
              <button 
                on:click={() => dispatch('close')}
                class="text-gray-400 hover:text-gray-500 focus:outline-none"
              >
                <Icon icon="heroicons:x-mark" class="h-6 w-6" />
              </button>
            </div>
            
            <div class="mt-6">
              <div 
                class={`mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-dashed rounded-md ${isDragging ? 'border-green-500 bg-green-50' : 'border-gray-300'}`}
                on:dragover={handleDragOver}
                on:dragleave={handleDragLeave}
                on:drop={handleDrop}
              >
                <div class="space-y-1 text-center">
                  <Icon icon="heroicons:arrow-up-tray" class="mx-auto h-12 w-12 text-gray-400" />
                  <div class="flex text-sm text-gray-600">
                    <label for="file-upload" class="relative cursor-pointer bg-white rounded-md font-medium text-green-600 hover:text-green-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-green-500">
                      <span>Téléversez un fichier</span>
                      <input id="file-upload" name="file-upload" type="file" class="sr-only" multiple on:change={handleFileSelect}>
                    </label>
                    <p class="pl-1">ou glissez-déposez</p>
                  </div>
                  <p class="text-xs text-gray-500">
                    PDF, DOCX, XLSX jusqu'à 10MB
                  </p>
                </div>
              </div>
              
              {#if files.length > 0}
                <div class="mt-6 space-y-4">
                  <h4 class="text-sm font-medium text-gray-900">Fichiers sélectionnés ({files.length})</h4>
                  <ul class="border border-gray-200 rounded-md divide-y divide-gray-200">
                    {#each files as file, index}
                      <li class="pl-3 pr-4 py-3 flex items-center justify-between text-sm">
                        <div class="w-0 flex-1 flex items-center">
                          <Icon icon="heroicons:document" class="flex-shrink-0 h-5 w-5 text-gray-400" />
                          <span class="ml-2 flex-1 w-0 truncate">{file.name}</span>
                        </div>
                        <div class="ml-4 flex-shrink-0 flex space-x-4">
                          <span class="text-gray-500">{Math.round(file.size / 1024)} KB</span>
                          <button 
                            on:click={() => removeFile(index)}
                            class="bg-white rounded-md text-gray-400 hover:text-gray-500 focus:outline-none"
                          >
                            <Icon icon="heroicons:x-mark" class="h-5 w-5" />
                          </button>
                        </div>
                      </li>
                    {/each}
                  </ul>
                </div>
              {/if}
            </div>
          </div>
        </div>
      </div>
      
      <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
        <button
          type="button"
          class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-green-600 text-base font-medium text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 sm:ml-3 sm:w-auto sm:text-sm"
          disabled={files.length === 0}
          class:opacity-50={files.length === 0}
          class:cursor-not-allowed={files.length === 0}
        >
          Téléverser
        </button>
        <button
          type="button"
          class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
          on:click={() => dispatch('close')}
        >
          Annuler
        </button>
      </div>
    </div>
  </div>
</div>