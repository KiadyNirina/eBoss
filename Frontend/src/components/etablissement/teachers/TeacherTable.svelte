<script>
  import Icon from '@iconify/svelte';
  
  export let teachers;
  export let selectedTeachers;
  
  export let toggleSelectAll;
  export let toggleTeacher;
  
  function getStatusBadge(status) {
    const statusClasses = {
      actif: 'bg-green-100 text-green-800',
      inactif: 'bg-gray-100 text-gray-800',
      congé: 'bg-blue-100 text-blue-800'
    };
    
    const statusLabels = {
      actif: 'Actif',
      inactif: 'Inactif',
      congé: 'En congé'
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
                checked={selectedTeachers.length === teachers.length}
                on:change={toggleSelectAll}
                />
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Professeur
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Matières
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Classes
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Contact
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Statut
            </th>
            <th scope="col" class="relative px-6 py-3">
                <span class="sr-only">Actions</span>
            </th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
            {#each teachers as teacher}
            <tr class={selectedTeachers.includes(teacher.id) ? 'bg-green-50' : 'hover:bg-gray-50'}>
                <td class="px-6 py-4 whitespace-nowrap">
                <input
                    type="checkbox"
                    class="focus:ring-green-500 h-4 w-4 text-green-600 border-gray-300 rounded"
                    checked={selectedTeachers.includes(teacher.id)}
                    on:change={() => toggleTeacher(teacher.id)}
                />
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                    <div class="flex-shrink-0 h-10 w-10 bg-green-100 rounded-full flex items-center justify-center">
                    <Icon icon="heroicons:academic-cap" class="h-6 w-6 text-green-600" />
                    </div>
                    <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{teacher.prenom} {teacher.nom}</div>
                    <div class="text-sm text-gray-500">Embauché le {teacher.embauche}</div>
                    </div>
                </div>
                </td>
                <td class="px-6 py-4">
                <div class="flex flex-wrap gap-1">
                    {#each teacher.matieres as matiere}
                    <span class="px-2 py-1 text-xs rounded bg-gray-100 text-gray-800">
                        {matiere}
                    </span>
                    {/each}
                </div>
                </td>
                <td class="px-6 py-4">
                <div class="flex flex-wrap gap-1">
                    {#each teacher.classes as classe}
                    <span class="px-2 py-1 text-xs rounded bg-blue-100 text-blue-800">
                        {classe}
                    </span>
                    {/each}
                </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{teacher.email}</div>
                <div class="text-sm text-gray-500">{teacher.telephone}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                {#if teacher.statut}
                    {@const status = getStatusBadge(teacher.statut)}
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full {status.class}">
                    {status.label}
                    </span>
                {/if}
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