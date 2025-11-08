<script>
  import Icon from '@iconify/svelte';
  import { createEventDispatcher } from 'svelte';

  export let students;
  export let selectedStudents;
  export let toggleSelectAll;
  export let toggleStudent;

  const dispatch = createEventDispatcher();

  let sortKey = null; // clé du tri (ex: 'nom', 'classe', ...)
  let sortOrder = 'asc';

  function sortBy(key) {
    if (sortKey === key) {
      sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
    } else {
      sortKey = key;
      sortOrder = 'asc';
    }

    students = [...students].sort((a, b) => {
      let aVal = a[key] ? a[key].toString().toLowerCase() : '';
      let bVal = b[key] ? b[key].toString().toLowerCase() : '';

      if (aVal < bVal) return sortOrder === 'asc' ? -1 : 1;
      if (aVal > bVal) return sortOrder === 'asc' ? 1 : -1;
      return 0;
    });
  }

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
        <th class="px-6 py-3">
          <input
            type="checkbox"
            class="focus:ring-green-500 h-4 w-4 text-green-600 border-gray-300 rounded"
            checked={selectedStudents.length === students.length}
            on:change={toggleSelectAll}
          />
        </th>

        <!-- Nom -->
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
            on:click={() => sortBy('nom')}>
          Nom
          {#if sortKey === 'nom'}
            <Icon icon={sortOrder === 'asc' ? 'mdi:arrow-up' : 'mdi:arrow-down'} class="inline-block w-4 h-4 ml-1" />
          {/if}
        </th>

        <!-- Classe -->
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
            on:click={() => sortBy('classe')}>
          Classe
          {#if sortKey === 'classe'}
            <Icon icon={sortOrder === 'asc' ? 'mdi:arrow-up' : 'mdi:arrow-down'} class="inline-block w-4 h-4 ml-1" />
          {/if}
        </th>

        <!-- Contact -->
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
            on:click={() => sortBy('telephone')}>
          Contact
          {#if sortKey === 'telephone'}
            <Icon icon={sortOrder === 'asc' ? 'mdi:arrow-up' : 'mdi:arrow-down'} class="inline-block w-4 h-4 ml-1" />
          {/if}
        </th>

        <!-- Statut -->
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
            on:click={() => sortBy('statut')}>
          Statut
          {#if sortKey === 'statut'}
            <Icon icon={sortOrder === 'asc' ? 'mdi:arrow-up' : 'mdi:arrow-down'} class="inline-block w-4 h-4 ml-1" />
          {/if}
        </th>

        <!-- Année scolaire -->
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
            on:click={() => sortBy('annee_scolaire')}>
          Année scolaire
          {#if sortKey === 'annee_scolaire'}
            <Icon icon={sortOrder === 'asc' ? 'mdi:arrow-up' : 'mdi:arrow-down'} class="inline-block w-4 h-4 ml-1" />
          {/if}
        </th>

        <!-- Date d inscription -->
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
            on:click={() => sortBy('date_joined')}>
          Date d'inscription
          {#if sortKey === 'date_joined'}
            <Icon icon={sortOrder === 'asc' ? 'mdi:arrow-up' : 'mdi:arrow-down'} class="inline-block w-4 h-4 ml-1" />
          {/if}
        </th>

        <!-- Dernière activité -->
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
            on:click={() => sortBy('derniereActivite')}>
          Dernière activité
          {#if sortKey === 'derniereActivite'}
            <Icon icon={sortOrder === 'asc' ? 'mdi:arrow-up' : 'mdi:arrow-down'} class="inline-block w-4 h-4 ml-1" />
          {/if}
        </th>

        <th class="px-6 py-3"></th>
      </tr>
    </thead>

    <tbody class="bg-white divide-y divide-gray-200">
      {#if students.length === 0}
        <tr>
          <td colspan="9" class="px-6 py-4 whitespace-nowrap text-center text-sm text-gray-500">
            Aucun étudiant trouvé.
          </td>
        </tr>
      {/if}
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
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{student.classe}</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{student.telephone}</td>
          <td class="px-6 py-4 whitespace-nowrap">
            {#if student.statut}
              <span class={"px-2 inline-flex text-xs leading-5 font-semibold rounded-full " + getStatusBadge(student.statut).class}>
                {getStatusBadge(student.statut).label}
              </span>
            {/if}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{student.annee_scolaire}</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{new Date(student.date_joined).toLocaleDateString('fr-FR')}</td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{student.derniereActivite}</td>
          <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
            <div class="flex justify-end space-x-3">
              <a href="#" class="text-green-600 hover:text-green-900" on:click={() => dispatch('edit', { student })}>
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