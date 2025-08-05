<script>
  import Icon from '@iconify/svelte';
  import DocumentBreadcrumb from './DocumentBreadcrumb.svelte';
  import DocumentGrid from './DocumentGrid.svelte';
  import DocumentPreviewModal from './DocumentPreviewModal.svelte';
  import UploadModal from './UploadModal.svelte';
  
  // Données simulées
  let currentFolder = {
    id: 'root',
    name: 'Documents',
    path: []
  };
  
  let folders = [
    { id: '1', name: 'Administratif', icon: 'folder', items: 12, lastModified: '2023-05-15' },
    { id: '2', name: 'Pédagogique', icon: 'folder', items: 8, lastModified: '2023-06-22' },
    { id: '3', name: 'Bulletins', icon: 'folder', items: 45, lastModified: '2023-07-10' }
  ];
  
  let files = [
    { id: 'f1', name: 'Règlement intérieur.pdf', icon: 'pdf', size: '2.4 MB', lastModified: '2023-01-10' },
    { id: 'f2', name: 'Calendrier scolaire.docx', icon: 'word', size: '1.2 MB', lastModified: '2023-06-30' },
    { id: 'f3', name: 'Liste des fournitures.xlsx', icon: 'excel', size: '0.8 MB', lastModified: '2023-07-05' }
  ];
  
  let selectedItems = [];
  let showUploadModal = false;
  let previewFile = null;
  
  // Fonctions de gestion
  function navigateToFolder(folder) {
    currentFolder = {
      id: folder.id,
      name: folder.name,
      path: [...currentFolder.path, { id: currentFolder.id, name: currentFolder.name }]
    };
  }
  
  function navigateUp() {
    if (currentFolder.path.length > 0) {
      const newPath = [...currentFolder.path];
      const parent = newPath.pop();
      currentFolder = {
        id: parent.id,
        name: parent.name,
        path: newPath
      };
    }
  }
  
  function toggleSelectItem(id) {
    if (selectedItems.includes(id)) {
      selectedItems = selectedItems.filter(itemId => itemId !== id);
    } else {
      selectedItems = [...selectedItems, id];
    }
  }
  
  function openPreview(file) {
    previewFile = file;
  }
</script>

<div>
  <!-- En-tête -->
  <div class="flex items-center justify-between mb-6">
    <div>
      <h1 class="text-2xl font-bold leading-6 text-gray-900">Gestion des Documents</h1>
      <p class="mt-2 text-sm text-gray-700">
        {folders.length + files.length} éléments dans ce dossier
      </p>
    </div>
    <div class="flex space-x-3">
      <button 
        on:click={() => showUploadModal = true}
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
      >
        <Icon icon="heroicons:arrow-up-tray" class="-ml-1 mr-2 h-5 w-5" />
        Téléverser
      </button>
      <button class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
        <Icon icon="heroicons:plus" class="-ml-1 mr-2 h-5 w-5" />
        Nouveau dossier
      </button>
    </div>
  </div>
  
  <!-- Barre de navigation et actions -->
  <div class="mb-6 flex items-center justify-between">
    <DocumentBreadcrumb 
      {currentFolder} 
      on:navigateUp={navigateUp}
    />
    
    <div class="flex space-x-3">
      <div class="relative rounded-md shadow-sm">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Icon icon="heroicons:magnifying-glass" class="h-5 w-5 text-gray-400" />
        </div>
        <input
          type="text"
          class="focus:ring-green-500 focus:border-green-500 block w-full pl-10 sm:text-sm border-gray-300 rounded-md"
          placeholder="Rechercher..."
        />
      </div>
      <button class="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100">
        <Icon icon="heroicons:list-bullet" class="h-5 w-5" />
      </button>
      <button class="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100">
        <Icon icon="heroicons:squares-2x2" class="h-5 w-5" />
      </button>
    </div>
  </div>
  
  <!-- Actions groupées -->
  {#if selectedItems.length > 0}
    <div class="bg-green-50 border-l-4 border-green-400 p-4 mb-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center">
          <Icon icon="heroicons:check-circle" class="h-5 w-5 text-green-400" />
          <p class="ml-3 text-sm text-green-700">
            <span class="font-medium">{selectedItems.length} éléments</span> sélectionnés
          </p>
        </div>
        <div class="flex space-x-3">
          <button class="inline-flex items-center px-3 py-1 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
            <Icon icon="heroicons:arrow-down-tray" class="-ml-1 mr-1 h-4 w-4" />
            Télécharger
          </button>
          <button class="inline-flex items-center px-3 py-1 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
            <Icon icon="heroicons:share" class="-ml-1 mr-1 h-4 w-4" />
            Partager
          </button>
          <button class="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
            <Icon icon="heroicons:trash" class="-ml-1 mr-1 h-4 w-4" />
            Supprimer
          </button>
        </div>
      </div>
    </div>
  {/if}
  
  <!-- Grille de documents -->
  <DocumentGrid
    {folders}
    {files}
    {selectedItems}
    on:toggleSelect={toggleSelectItem}
    on:openFolder={navigateToFolder}
    on:openFile={openPreview}
  />
</div>

<!-- Modals -->
{#if showUploadModal}
  <UploadModal on:close={() => showUploadModal = false} />
{/if}

{#if previewFile}
  <DocumentPreviewModal 
    file={previewFile} 
    on:close={() => previewFile = null} 
  />
{/if}