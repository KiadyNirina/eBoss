<script>
  import Icon from '@iconify/svelte';
  
  export let students;
  export let selectedStudents;
  export let toggleSelectAll;
  export let toggleStudent;
  
  function getStatusBadge(status) {
    const statusClasses = {
      actif: 'bg-green-100 text-green-800',
      inactif: 'bg-gray-100 text-gray-800',
      suspendu: 'bg-yellow-100 text-yellow-800'
    };
    
    const statusLabels = {
      actif: 'Actif',
      inactif: 'Inactif',
      suspendu: 'Suspendu'
    };
    
    return {
      class: statusClasses[status] || 'bg-gray-100 text-gray-800',
      label: statusLabels[status] || status
    };
  }
</script>

<div class="overflow-x-auto">
  <table class="min-w-full divide-y divide-gray-200">
    <thead class="bg-gray-50">
      <tr>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          <input
            type="checkbox"
            class="focus:ring-green-500 h-4 w-4 text-green-600 border-gray-300 rounded"
            checked={selectedStudents.length === students.length}
            on:change={toggleSelectAll}
          />
        </th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          Nom
        </th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          Classe
        </th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          Contact
        </th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          Statut
        </th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          Dernière activité
        </th>
        <th scope="col" class="relative px-6 py-3">
          <span class="sr-only">Actions</span>
        </th>
      </tr>
    </thead>
    <tbody class="bg-white divide-y divide-gray-200">
      {#each students as student}
        <tr class={selectedStudents.includes(student.id) ? 'bg-green-50' : 'hover:bg-gray-50'}>
          <td class="px-6 py-4 whitespace-nowrap">
            <input
              type="checkbox"
              class="focus:ring-green-500 h-4 w-4 text-green-600 border-gray-300 rounded"
              checked={selectedStudents.includes(student.id)}
              on:change={() => toggleStudent(student.id)}
            />
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="flex items-center">
              <div class="flex-shrink-0 h-10 w-10 bg-green-100 rounded-full flex items-center justify-center">
                <Icon icon="heroicons:user" class="h-6 w-6 text-green-600" />
              </div>
              <div class="ml-4">
                <div class="text-sm font-medium text-gray-900">{student.prenom} {student.nom}</div>
                <div class="text-sm text-gray-500">{student.email}</div>
              </div>
            </div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="text-sm text-gray-900">{student.classe}</div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="text-sm text-gray-900">{student.telephone}</div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            {#if student.statut}
              {@const status = getStatusBadge(student.statut)}
              <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full {status.class}">
                {status.label}
              </span>
            {/if}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            {student.derniereActivite}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
            <div class="flex justify-end space-x-3">
              <a href="#" class="text-green-600 hover:text-green-900">
                <Icon icon="heroicons:pencil-square" class="h-5 w-5" />
              </a>
              <a href="#" class="text-gray-600 hover:text-gray-900">
                <Icon icon="heroicons:eye" class="h-5 w-5" />
              </a>
              <a href="#" class="text-red-600 hover:text-red-900">
                <Icon icon="heroicons:trash" class="h-5 w-5" />
              </a>
            </div>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>