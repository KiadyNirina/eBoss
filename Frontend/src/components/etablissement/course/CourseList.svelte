<script>
  import Icon from '@iconify/svelte';
  
  export let courses;
  
  let filters = {
    class: '',
    teacher: '',
    day: ''
  };
  
  let filteredCourses = courses;
  
  function applyFilters() {
    filteredCourses = courses.filter(course => {
      return (
        (filters.class === '' || course.class === filters.class) &&
        (filters.teacher === '' || course.teacher === filters.teacher) &&
        (filters.day === '' || course.day === filters.day)
      );
    });
  }
</script>

<div class="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
  <!-- Filtres -->
  <div class="p-4 border-b border-gray-200">
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
      <div>
        <label for="filter-class" class="block text-sm font-medium text-gray-700">Classe</label>
        <select
          id="filter-class"
          bind:value={filters.class}
          on:change={applyFilters}
          class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm rounded-md"
        >
          <option value="">Toutes les classes</option>
          <option value="3ème A">3ème A</option>
          <option value="4ème B">4ème B</option>
          <option value="5ème C">5ème C</option>
        </select>
      </div>
      
      <div>
        <label for="filter-teacher" class="block text-sm font-medium text-gray-700">Professeur</label>
        <select
          id="filter-teacher"
          bind:value={filters.teacher}
          on:change={applyFilters}
          class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm rounded-md"
        >
          <option value="">Tous les professeurs</option>
          <option value="M. Dupont">M. Dupont</option>
          <option value="Mme. Martin">Mme. Martin</option>
        </select>
      </div>
      
      <div>
        <label for="filter-day" class="block text-sm font-medium text-gray-700">Jour</label>
        <select
          id="filter-day"
          bind:value={filters.day}
          on:change={applyFilters}
          class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm rounded-md"
        >
          <option value="">Tous les jours</option>
          <option value="Lundi">Lundi</option>
          <option value="Mardi">Mardi</option>
          <option value="Mercredi">Mercredi</option>
          <option value="Jeudi">Jeudi</option>
          <option value="Vendredi">Vendredi</option>
        </select>
      </div>
    </div>
  </div>
  
  <!-- Tableau des cours -->
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Cours
          </th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Professeur
          </th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Classe
          </th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Jour/Horaire
          </th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Salle
          </th>
          <th scope="col" class="relative px-6 py-3">
            <span class="sr-only">Actions</span>
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        {#each filteredCourses as course}
          <tr class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">{course.title}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{course.teacher}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                {course.class}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{course.day} {course.start}-{course.end}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{course.room}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <div class="flex justify-end space-x-3">
                <a href="#" class="text-green-600 hover:text-green-900">
                  <Icon icon="heroicons:pencil-square" class="h-5 w-5" />
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
  
  <!-- Pagination -->
  <div class="bg-gray-50 px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
    <div class="flex-1 flex justify-between sm:hidden">
      <a href="#" class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
        Précédent
      </a>
      <a href="#" class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
        Suivant
      </a>
    </div>
    <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
      <div>
        <p class="text-sm text-gray-700">
          Affichage de <span class="font-medium">1</span> à <span class="font-medium">10</span> sur{' '}
          <span class="font-medium">{filteredCourses.length}</span> résultats
        </p>
      </div>
      <div>
        <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
          <a href="#" class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
            <span class="sr-only">Précédent</span>
            <Icon icon="heroicons:chevron-left" class="h-5 w-5" />
          </a>
          <a href="#" aria-current="page" class="z-10 bg-green-50 border-green-500 text-green-600 relative inline-flex items-center px-4 py-2 border text-sm font-medium">
            1
          </a>
          <a href="#" class="bg-white border-gray-300 text-gray-500 hover:bg-gray-50 relative inline-flex items-center px-4 py-2 border text-sm font-medium">
            2
          </a>
          <a href="#" class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
            <span class="sr-only">Suivant</span>
            <Icon icon="heroicons:chevron-right" class="h-5 w-5" />
          </a>
        </nav>
      </div>
    </div>
  </div>
</div>