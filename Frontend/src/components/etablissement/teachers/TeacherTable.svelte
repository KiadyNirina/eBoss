<script>
  import Icon from '@iconify/svelte';
  import { createEventDispatcher } from 'svelte';
  
  export let teachers;
  export let selectedTeachers;
  
  export let toggleSelectAll;
  export let toggleTeacher;

  const dispatch = createEventDispatcher();

  function getAnneesList(anneeData) {
    if (!anneeData) return [];
    
    if (Array.isArray(anneeData) && anneeData.length === 2 && typeof anneeData[1] === 'string') {
      return [{ id: anneeData[0], nom: anneeData[1] }];
    }
    
    if (Array.isArray(anneeData) && anneeData.length > 0 && Array.isArray(anneeData[0])) {
      return anneeData.map(item => ({
        id: item[0],
        nom: item[1]
      }));
    }
    
    if (typeof anneeData === 'object' && anneeData.id) {
      return [{ id: anneeData.id, nom: anneeData.nom || `Année ${anneeData.id}` }];
    }
    
    return [{ id: anneeData, nom: `Année ${anneeData}` }];
  }

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

  function handleEdit(teacherId) {
    dispatch('edit', teacherId);
  }

  function handleDelete(teacherId) {
    dispatch('delete', teacherId);
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
                Année Scolaire
            </th>
            <!-- <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Statut
            </th> -->
            <th scope="col" class="relative px-6 py-3">
                <span class="sr-only">Actions</span>
            </th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
            {#if teachers.length === 0}
                <tr>
                <td colspan="9" class="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-500">
                    Aucun professeur trouvé.
                </td>
                </tr>
            {/if}
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
                    <div class="text-sm font-medium text-gray-900">{teacher.user.first_name} {teacher.user.last_name}</div>
                    <div class="text-sm text-gray-500">{teacher.user.email}</div>
                    </div>
                </div>
                </td>
                <td class="px-6 py-4">
                <div class="flex flex-wrap gap-1">
                    {#each teacher.matieres_details ?? [] as matiere}
                    <span class="px-2 py-1 text-xs rounded bg-gray-100 text-gray-800">
                        {matiere.nom}
                    </span>
                    {/each}
                </div>
                </td>
                <td class="px-6 py-4">
                <div class="flex flex-wrap gap-1">
                    {#each teacher.classes_details ?? [] as classe}
                    <span class="px-2 py-1 text-xs rounded bg-blue-100 text-blue-800">
                        {classe.nom}
                    </span>
                    {/each}
                </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-500">{teacher.user.telephone}</div>
                </td>
                <td class="px-6 py-4">
                    <div class="flex flex-wrap gap-1">
                        {#if teacher.annee_scolaire}
                            {@const annees = getAnneesList(teacher.annee_scolaire)}
                            {#each annees as annee}
                                <span class="px-2 py-1 text-xs rounded bg-blue-100 text-blue-800">
                                    {annee.nom}
                                </span>
                            {/each}
                        {:else}
                            <span class="text-sm text-gray-400">Non assigné</span>
                        {/if}
                    </div>
                </td>
                <!-- <td class="px-6 py-4 whitespace-nowrap">
                {#if teacher.statut}
                    {@const status = getStatusBadge(teacher.statut)}
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full {status.class}">
                    {status.label}
                    </span>
                {/if}
                </td> -->
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex justify-end space-x-3">
                    <button 
                        on:click={() => handleEdit(teacher.id)}
                        class="text-green-600 hover:text-green-900 transition-colors"
                        title="Modifier"
                    >
                        <Icon icon="heroicons:pencil-square" class="h-5 w-5" />
                    </button>
                    <button 
                        on:click={() => handleDelete(teacher.id)}
                        class="text-red-600 hover:text-red-900 transition-colors"
                        title="Supprimer"
                    >
                        <Icon icon="heroicons:trash" class="h-5 w-5" />
                    </button>
                </div>
                </td>
            </tr>
            {/each}
        </tbody>
    </table>
</div>