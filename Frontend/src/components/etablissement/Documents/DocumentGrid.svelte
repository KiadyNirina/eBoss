<script>
  import Icon from '@iconify/svelte';
  
  export let folders;
  export let files;
  export let selectedItems;
  
  export let toggleSelect;
  export let openFolder;
  export let openFile;
  
  function getFileIcon(type) {
    const icons = {
      pdf: 'vscode-icons:file-type-pdf2',
      word: 'vscode-icons:file-type-word2',
      excel: 'vscode-icons:file-type-excel2',
      folder: 'heroicons:folder'
    };
    return icons[type] || 'heroicons:document';
  }
  
  function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('fr-FR', options);
  }
</script>

<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
  <!-- Dossiers -->
  {#each folders as folder}
    <div 
      class={`bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm hover:shadow-md transition-shadow ${selectedItems.includes(folder.id) ? 'ring-2 ring-green-500' : ''}`}
      on:click|stopPropagation={() => openFolder(folder)}
    >
      <div class="p-4 flex flex-col items-center text-center">
        <div class="relative">
          <input
            type="checkbox"
            class="absolute top-2 left-2 focus:ring-green-500 h-4 w-4 text-green-600 border-gray-300 rounded"
            checked={selectedItems.includes(folder.id)}
            on:click|stopPropagation={(e) => { e.stopPropagation(); toggleSelect(folder.id); }}
          />
          <Icon 
            icon={getFileIcon(folder.icon)} 
            class="h-16 w-16 text-green-600" 
          />
        </div>
        <h3 class="mt-2 text-sm font-medium text-gray-900 truncate w-full">
          {folder.name}
        </h3>
        <p class="mt-1 text-xs text-gray-500">
          {folder.items} éléments • Modifié {formatDate(folder.lastModified)}
        </p>
      </div>
    </div>
  {/each}
  
  <!-- Fichiers -->
  {#each files as file}
    <div 
      class={`bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm hover:shadow-md transition-shadow ${selectedItems.includes(file.id) ? 'ring-2 ring-green-500' : ''}`}
      on:click|stopPropagation={() => openFile(file)}
    >
      <div class="p-4 flex flex-col items-center text-center">
        <div class="relative">
          <input
            type="checkbox"
            class="absolute top-2 left-2 focus:ring-green-500 h-4 w-4 text-green-600 border-gray-300 rounded"
            checked={selectedItems.includes(file.id)}
            on:click|stopPropagation={(e) => { e.stopPropagation(); toggleSelect(file.id); }}
          />
          <Icon 
            icon={getFileIcon(file.icon)} 
            class="h-16 w-16 text-gray-400" 
          />
        </div>
        <h3 class="mt-2 text-sm font-medium text-gray-900 truncate w-full">
          {file.name}
        </h3>
        <p class="mt-1 text-xs text-gray-500">
          {file.size} • Modifié {formatDate(file.lastModified)}
        </p>
      </div>
    </div>
  {/each}
</div>