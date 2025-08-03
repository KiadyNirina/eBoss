<script>
  import Icon from '@iconify/svelte';
  
  export let selectedEvaluation;
  
  // Calcul des statistiques
  $: average = selectedEvaluation.notes.reduce((acc, note) => acc + note.note, 0) / selectedEvaluation.notes.length;
  $: maxNote = Math.max(...selectedEvaluation.notes.map(note => note.note));
  $: minNote = Math.min(...selectedEvaluation.notes.map(note => note.note));
</script>

<div class="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-4">
  <!-- Note moyenne -->
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="px-4 py-5 sm:p-6">
      <div class="flex items-center">
        <div class="flex-shrink-0 bg-green-100 p-3 rounded-md">
          <Icon icon="heroicons:scale" class="h-6 w-6 text-green-600" />
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">Moyenne</dt>
            <dd>
              <div class="text-lg font-medium text-gray-900">{average.toFixed(2)}/20</div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Note max -->
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="px-4 py-5 sm:p-6">
      <div class="flex items-center">
        <div class="flex-shrink-0 bg-blue-100 p-3 rounded-md">
          <Icon icon="heroicons:arrow-trending-up" class="h-6 w-6 text-blue-600" />
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">Note max</dt>
            <dd>
              <div class="text-lg font-medium text-gray-900">{maxNote}/20</div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Note min -->
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="px-4 py-5 sm:p-6">
      <div class="flex items-center">
        <div class="flex-shrink-0 bg-yellow-100 p-3 rounded-md">
          <Icon icon="heroicons:arrow-trending-down" class="h-6 w-6 text-yellow-600" />
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">Note min</dt>
            <dd>
              <div class="text-lg font-medium text-gray-900">{minNote}/20</div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Coefficient -->
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="px-4 py-5 sm:p-6">
      <div class="flex items-center">
        <div class="flex-shrink-0 bg-purple-100 p-3 rounded-md">
          <Icon icon="heroicons:calculator" class="h-6 w-6 text-purple-600" />
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">Coefficient</dt>
            <dd>
              <div class="text-lg font-medium text-gray-900">{selectedEvaluation.coefficient}</div>
            </dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
</div>