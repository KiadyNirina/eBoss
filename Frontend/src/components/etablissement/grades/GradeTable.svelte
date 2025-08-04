<script>
  import Icon from '@iconify/svelte';
  
  export let selectedEvaluation;
  
  function getNoteColor(note) {
    if (note < 5) return 'text-red-600 bg-red-50';
    if (note < 10) return 'text-yellow-600 bg-yellow-50';
    if (note < 15) return 'text-green-600 bg-green-50';
    return 'text-blue-600 bg-blue-50';
  }
</script>

<div class="shadow-sm border border-gray-200 rounded-lg overflow-hidden">
  <table class="min-w-full divide-y divide-gray-200">
    <thead class="bg-gray-50">
      <tr>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          Étudiant
        </th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          Note
        </th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          Appréciation
        </th>
        <th scope="col" class="relative px-6 py-3">
          <span class="sr-only">Actions</span>
        </th>
      </tr>
    </thead>
    <tbody class="bg-white divide-y divide-gray-200">
      {#each selectedEvaluation.notes as note}
        <tr class="hover:bg-gray-50">
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="flex items-center">
              <div class="flex-shrink-0 h-10 w-10 bg-green-100 rounded-full flex items-center justify-center">
                <Icon icon="heroicons:user" class="h-6 w-6 text-green-600" />
              </div>
              <div class="ml-4">
                <div class="text-sm font-medium text-gray-900">{note.prenom} {note.nom}</div>
                <div class="text-sm text-gray-500">ID: {note.etudiantId}</div>
              </div>
            </div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            <span class={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getNoteColor(note.note)}`}>
              {note.note}/20
            </span>
          </td>
          <td class="px-6 py-4">
            <div class="text-sm text-gray-900">{note.appreciation}</div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
            <div class="flex justify-end space-x-3">
              <a href="#" class="text-green-600 hover:text-green-900">
                <Icon icon="heroicons:pencil-square" class="h-5 w-5" />
              </a>
              <a href="#" class="text-gray-600 hover:text-gray-900">
                <Icon icon="heroicons:document-text" class="h-5 w-5" />
              </a>
            </div>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>