<script>
  import Icon from '@iconify/svelte';
  
  export let view;
  export let courses;
  
  const days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'];
  const hours = Array.from({ length: 10 }, (_, i) => 8 + i + ':00');
  
  function getCoursesForDayAndTime(day, time) {
    return courses.filter(course => course.day === day && course.start === time);
  }
</script>

<div class="overflow-auto">
  {#if view === 'day'}
    <!-- Vue Jour -->
    <div class="min-w-full divide-y divide-gray-200">
      <div class="bg-gray-50 flex">
        <div class="w-24 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
          Heure
        </div>
        <div class="flex-1 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
          Lundi 15 Mai
        </div>
      </div>
      
      {#each hours as hour}
        <div class="flex">
          <div class="w-24 py-4 text-center text-sm text-gray-500 border-r border-gray-200">
            {hour}
          </div>
          <div class="flex-1 py-4 px-2 min-h-20 border-b border-gray-200">
            {#each getCoursesForDayAndTime('Lundi', hour) as course}
              <div class={`${course.color} p-2 rounded-md mb-2 text-sm`}>
                <div class="font-medium">{course.title}</div>
                <div class="text-xs">{course.teacher} - {course.room}</div>
              </div>
            {/each}
          </div>
        </div>
      {/each}
    </div>
  
  {:else if view === 'week'}
    <!-- Vue Semaine -->
    <div class="min-w-full divide-y divide-gray-200">
      <div class="bg-gray-50 flex">
        <div class="w-24 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
          Heure
        </div>
        {#each days as day}
          <div class="flex-1 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
            {day}
          </div>
        {/each}
      </div>
      
      {#each hours as hour}
        <div class="flex">
          <div class="w-24 py-4 text-center text-sm text-gray-500 border-r border-gray-200">
            {hour}
          </div>
          {#each days as day}
            <div class="flex-1 py-4 px-2 min-h-20 border-b border-gray-200">
              {#each getCoursesForDayAndTime(day, hour) as course}
                <div class={`${course.color} p-2 rounded-md mb-2 text-sm`}>
                  <div class="font-medium">{course.title}</div>
                  <div class="text-xs">{course.class} - {course.room}</div>
                </div>
              {/each}
            </div>
          {/each}
        </div>
      {/each}
    </div>
  
  {:else}
    <!-- Vue Mois -->
    <div class="grid grid-cols-7 gap-px bg-gray-200">
      {#each ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'] as day}
        <div class="bg-gray-50 py-2 text-center text-xs font-semibold text-gray-500">
          {day}
        </div>
      {/each}
      
      {#each Array.from({ length: 35 }) as _, i}
        <div class="bg-white p-1 h-32 overflow-y-auto">
          <div class="text-right text-sm">{i + 1}</div>
          {#if i % 7 === 0}
            <div class="bg-green-50 text-green-800 p-1 rounded text-xs mt-1">
              Math - 08:00 (Salle 101)
            </div>
          {/if}
          {#if i % 5 === 0}
            <div class="bg-blue-50 text-blue-800 p-1 rounded text-xs mt-1">
              Physique - 10:00 (Labo)
            </div>
          {/if}
        </div>
      {/each}
    </div>
  {/if}
</div>