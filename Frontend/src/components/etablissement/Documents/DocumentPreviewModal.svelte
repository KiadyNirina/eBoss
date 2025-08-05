<script>
  import Icon from '@iconify/svelte';
  
  export let file;
  
  function getFileIcon(type) {
    const icons = {
      pdf: 'vscode-icons:file-type-pdf2',
      word: 'vscode-icons:file-type-word2',
      excel: 'vscode-icons:file-type-excel2'
    };
    return icons[type] || 'heroicons:document';
  }
</script>

<div class="fixed z-50 inset-0 overflow-y-auto">
  <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
    <!-- Fond -->
    <div class="fixed inset-0 transition-opacity" aria-hidden="true">
      <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
    </div>
    
    <!-- Contenu -->
    <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
      <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
        <div class="sm:flex sm:items-start">
          <div class="mt-3 text-center sm:mt-0 sm:text-left w-full">
            <div class="flex justify-between items-center">
              <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                {file.name}
              </h3>
              <button 
                on:click={() => dispatch('close')}
                class="text-gray-400 hover:text-gray-500 focus:outline-none"
              >
                <Icon icon="heroicons:x-mark" class="h-6 w-6" />
              </button>
            </div>
            
            <div class="mt-6 border-t border-gray-200 pt-6">
              <div class="flex flex-col items-center justify-center py-12 bg-gray-50 rounded-lg">
                <Icon 
                  icon={getFileIcon(file.icon)} 
                  class="h-24 w-24 text-gray-400 mb-4" 
                />
                <p class="text-sm text-gray-500">
                  Prévisualisation non disponible pour ce type de fichier
                </p>
              </div>
              
              <div class="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div>
                  <p class="text-sm text-gray-500">Type</p>
                  <p class="mt-1 text-sm text-gray-900">
                    {#if file.icon === 'pdf'}
                      Document PDF
                    {:else if file.icon === 'word'}
                      Document Word
                    {:else if file.icon === 'excel'}
                      Document Excel
                    {:else}
                      Fichier
                    {/if}
                  </p>
                </div>
                <div>
                  <p class="text-sm text-gray-500">Taille</p>
                  <p class="mt-1 text-sm text-gray-900">{file.size}</p>
                </div>
                <div>
                  <p class="text-sm text-gray-500">Dernière modification</p>
                  <p class="mt-1 text-sm text-gray-900">{file.lastModified}</p>
                </div>
                <div>
                  <p class="text-sm text-gray-500">Emplacement</p>
                  <p class="mt-1 text-sm text-gray-900">Documents/Administratif</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
        <button
          type="button"
          class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-green-600 text-base font-medium text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 sm:ml-3 sm:w-auto sm:text-sm"
        >
          <Icon icon="heroicons:arrow-down-tray" class="-ml-1 mr-2 h-5 w-5" />
          Télécharger
        </button>
        <button
          type="button"
          class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
        >
          <Icon icon="heroicons:share" class="-ml-1 mr-2 h-5 w-5" />
          Partager
        </button>
      </div>
    </div>
  </div>
</div>