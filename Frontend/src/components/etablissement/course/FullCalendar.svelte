<script>
  import { onMount } from 'svelte';
  import Icon from '@iconify/svelte';
  
  export let view = 'week';
  export let courses = [];
  
  let currentDate = new Date();
  let selectedDate = new Date();
  let calendarDays = [];
  let weekDays = [];
  let hours = [];
  
  const JOURS = [
    { value: 'lundi', label: 'Lundi' },
    { value: 'mardi', label: 'Mardi' },
    { value: 'mercredi', label: 'Mercredi' },
    { value: 'jeudi', label: 'Jeudi' },
    { value: 'vendredi', label: 'Vendredi' },
    { value: 'samedi', label: 'Samedi' }
  ];
  
  const JOURS_ABBR = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'];
  
  // Générer les heures de 8h à 18h
  for (let i = 8; i <= 18; i++) {
    hours.push(`${i.toString().padStart(2, '0')}:00`);
  }
  
  onMount(() => {
    generateCalendar();
  });
  
  function generateCalendar() {
    if (view === 'day') {
      generateDayView();
    } else if (view === 'week') {
      generateWeekView();
    } else {
      generateMonthView();
    }
  }
  
  function generateDayView() {
    const date = new Date(selectedDate);
    const dayOfWeek = date.getDay(); // 0 = dimanche, 1 = lundi, ...
    const mondayOffset = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
    const monday = new Date(date);
    monday.setDate(date.getDate() - mondayOffset);
    
    weekDays = [];
    for (let i = 0; i < 7; i++) {
      const day = new Date(monday);
      day.setDate(monday.getDate() + i);
      weekDays.push(day);
    }
    
    calendarDays = [];
    const dayCourses = getCoursesForDate(selectedDate);
    const dateStr = formatDate(selectedDate);
    
    // Créer une structure pour chaque heure
    hours.forEach(hour => {
      const hourCourses = dayCourses.filter(c => {
        const courseHour = parseInt(c.heure_debut.split(':')[0]);
        return courseHour === parseInt(hour.split(':')[0]);
      });
      
      calendarDays.push({
        date: selectedDate,
        dateStr: dateStr,
        hour: hour,
        courses: hourCourses
      });
    });
  }
  
  function generateWeekView() {
    const date = new Date(selectedDate);
    const dayOfWeek = date.getDay();
    const mondayOffset = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
    const monday = new Date(date);
    monday.setDate(date.getDate() - mondayOffset);
    
    weekDays = [];
    for (let i = 0; i < 7; i++) {
      const day = new Date(monday);
      day.setDate(monday.getDate() + i);
      weekDays.push(day);
    }
    
    calendarDays = [];
    weekDays.forEach((day, index) => {
      const dayCourses = getCoursesForDate(day);
      const dateStr = formatDate(day);
      
      // Créer une structure pour chaque heure
      hours.forEach(hour => {
        const hourCourses = dayCourses.filter(c => {
          const courseHour = parseInt(c.heure_debut.split(':')[0]);
          return courseHour === parseInt(hour.split(':')[0]);
        });
        
        calendarDays.push({
          date: day,
          dateStr: dateStr,
          hour: hour,
          dayIndex: index,
          courses: hourCourses
        });
      });
    });
  }
  
  function generateMonthView() {
    const year = selectedDate.getFullYear();
    const month = selectedDate.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startDayOfWeek = firstDay.getDay(); // 0 = dimanche
    
    const days = [];
    // Ajuster pour commencer par lundi
    const startOffset = startDayOfWeek === 0 ? 6 : startDayOfWeek - 1;
    
    // Jours du mois précédent
    const prevMonthLastDay = new Date(year, month, 0).getDate();
    for (let i = startOffset - 1; i >= 0; i--) {
      const date = new Date(year, month - 1, prevMonthLastDay - i);
      days.push({
        date: date,
        isCurrentMonth: false,
        courses: getCoursesForDate(date)
      });
    }
    
    // Jours du mois courant
    for (let i = 1; i <= daysInMonth; i++) {
      const date = new Date(year, month, i);
      days.push({
        date: date,
        isCurrentMonth: true,
        isToday: isSameDay(date, new Date()),
        courses: getCoursesForDate(date)
      });
    }
    
    // Jours du mois suivant
    const remainingDays = (7 - (days.length % 7)) % 7;
    for (let i = 1; i <= remainingDays; i++) {
      const date = new Date(year, month + 1, i);
      days.push({
        date: date,
        isCurrentMonth: false,
        courses: getCoursesForDate(date)
      });
    }
    
    calendarDays = days;
  }
  
  function getCoursesForDate(date) {
    const dateStr = formatDate(date);
    return courses.filter(c => {
      const jourIndex = JOURS.findIndex(j => j.value === c.jour);
      if (jourIndex === -1) return false;
      
      // Calculer la date du cours dans la semaine
      const courseDate = new Date(date);
      const currentDayOfWeek = date.getDay(); // 0 = dimanche
      const mondayOffset = currentDayOfWeek === 0 ? 6 : currentDayOfWeek - 1;
      const monday = new Date(date);
      monday.setDate(date.getDate() - mondayOffset);
      const courseDateObj = new Date(monday);
      courseDateObj.setDate(monday.getDate() + jourIndex);
      
      return isSameDay(courseDateObj, date);
    });
  }
  
  function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }
  
  function isSameDay(date1, date2) {
    return date1.getFullYear() === date2.getFullYear() &&
           date1.getMonth() === date2.getMonth() &&
           date1.getDate() === date2.getDate();
  }
  
  function getDayName(date) {
    const dayIndex = date.getDay();
    return JOURS_ABBR[dayIndex === 0 ? 6 : dayIndex - 1];
  }
  
  function getDayNumber(date) {
    return date.getDate();
  }
  
  function getMonthName(date) {
    return date.toLocaleString('fr-FR', { month: 'long' });
  }
  
  function getFullDateLabel(date) {
    return date.toLocaleString('fr-FR', { 
      weekday: 'long', 
      day: 'numeric', 
      month: 'long', 
      year: 'numeric' 
    });
  }
  
  function getColorForCourse(course, index) {
    const colors = [
      'bg-blue-100 text-blue-800 border-blue-200',
      'bg-green-100 text-green-800 border-green-200',
      'bg-purple-100 text-purple-800 border-purple-200',
      'bg-yellow-100 text-yellow-800 border-yellow-200',
      'bg-pink-100 text-pink-800 border-pink-200',
      'bg-indigo-100 text-indigo-800 border-indigo-200',
      'bg-red-100 text-red-800 border-red-200',
      'bg-teal-100 text-teal-800 border-teal-200'
    ];
    return colors[index % colors.length];
  }
  
  function navigateDays(direction) {
    const newDate = new Date(selectedDate);
    if (view === 'day') {
      newDate.setDate(selectedDate.getDate() + direction);
    } else if (view === 'week') {
      newDate.setDate(selectedDate.getDate() + (direction * 7));
    } else {
      newDate.setMonth(selectedDate.getMonth() + direction);
    }
    selectedDate = newDate;
    generateCalendar();
  }
  
  function goToToday() {
    selectedDate = new Date();
    generateCalendar();
  }
  
  function selectDate(date) {
    selectedDate = date;
    if (view === 'month') {
      view = 'day';
    }
    generateCalendar();
  }
  
  function getWeekRange() {
    if (weekDays.length === 0) return '';
    const start = weekDays[0];
    const end = weekDays[6];
    return `${start.getDate()} ${start.toLocaleString('fr-FR', { month: 'short' })} - ${end.getDate()} ${end.toLocaleString('fr-FR', { month: 'short', year: 'numeric' })}`;
  }
  
  function getCourseDuration(course) {
    const start = course.heure_debut;
    const end = course.heure_fin;
    return `${start} - ${end}`;
  }
  
  // Réagir aux changements de view
  $: view, generateCalendar();
  $: courses, generateCalendar();
</script>

<div class="bg-white rounded-lg">
  <!-- En-tête du calendrier -->
  <div class="flex items-center justify-between mb-4">
    <div class="flex items-center space-x-4">
      <button
        on:click={() => navigateDays(-1)}
        class="p-2 hover:bg-gray-100 rounded-full transition-colors"
      >
        <Icon icon="heroicons:chevron-left" class="h-5 w-5 text-gray-600" />
      </button>
      
      <button
        on:click={goToToday}
        class="px-3 py-1 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-md transition-colors"
      >
        Aujourd'hui
      </button>
      
      <button
        on:click={() => navigateDays(1)}
        class="p-2 hover:bg-gray-100 rounded-full transition-colors"
      >
        <Icon icon="heroicons:chevron-right" class="h-5 w-5 text-gray-600" />
      </button>
    </div>
    
    <h3 class="text-lg font-semibold text-gray-900">
      {#if view === 'day'}
        {getFullDateLabel(selectedDate)}
      {:else if view === 'week'}
        {getWeekRange()}
      {:else}
        {getMonthName(selectedDate)} {selectedDate.getFullYear()}
      {/if}
    </h3>
    
    <div class="flex space-x-2">
      <button
        on:click={() => { view = 'day'; generateCalendar(); }}
        class={`px-3 py-1 text-sm font-medium rounded-md transition-colors ${
          view === 'day' ? 'bg-green-100 text-green-700' : 'text-gray-700 hover:bg-gray-100'
        }`}
      >
        Jour
      </button>
      <button
        on:click={() => { view = 'week'; generateCalendar(); }}
        class={`px-3 py-1 text-sm font-medium rounded-md transition-colors ${
          view === 'week' ? 'bg-green-100 text-green-700' : 'text-gray-700 hover:bg-gray-100'
        }`}
      >
        Semaine
      </button>
      <button
        on:click={() => { view = 'month'; generateCalendar(); }}
        class={`px-3 py-1 text-sm font-medium rounded-md transition-colors ${
          view === 'month' ? 'bg-green-100 text-green-700' : 'text-gray-700 hover:bg-gray-100'
        }`}
      >
        Mois
      </button>
    </div>
  </div>
  
  <!-- Vue Jour ou Semaine -->
  {#if view === 'day' || view === 'week'}
    <div class="overflow-x-auto">
      <div class="min-w-[800px]">
        <!-- En-tête des jours -->
        <div class="grid grid-cols-8 gap-1 mb-2">
          <div class="text-xs font-medium text-gray-500 uppercase py-2 text-center">Heure</div>
          {#if view === 'day'}
            <div class="text-xs font-medium text-gray-700 py-2 text-center">
              {getFullDateLabel(selectedDate)}
            </div>
          {:else}
            {#each weekDays as day}
              <div class={`text-xs font-medium py-2 text-center ${
                isSameDay(day, new Date()) ? 'bg-green-50 rounded-lg' : ''
              }`}>
                <div class="text-gray-500">{getDayName(day)}</div>
                <div class={`text-lg font-bold ${
                  isSameDay(day, new Date()) ? 'text-green-600' : 'text-gray-900'
                }`}>
                  {getDayNumber(day)}
                </div>
              </div>
            {/each}
          {/if}
        </div>
        
        <!-- Grille des cours -->
        <div class="grid grid-cols-8 gap-1">
          {#each hours as hour}
            <div class="text-xs text-gray-500 py-2 text-right pr-2 border-t border-gray-100">
              {hour}
            </div>
            
            {#if view === 'day'}
              <!-- Vue jour -->
              <div class="border-t border-gray-100 min-h-[60px] p-1">
                {#each calendarDays.filter(d => d.hour === hour) as dayData}
                  {#each dayData.courses as course, index}
                    <div class={`${getColorForCourse(course, index)} border rounded-md p-1 mb-1 text-xs`}>
                      <div class="font-medium truncate">{course.matiere_nom}</div>
                      <div class="truncate text-gray-600">{course.professeur_nom}</div>
                      <div class="truncate text-gray-500">{course.salle_nom || 'N/A'}</div>
                    </div>
                  {/each}
                {/each}
              </div>
            {:else}
              <!-- Vue semaine -->
              {#each weekDays as day, dayIndex}
                <div class="border-t border-gray-100 min-h-[60px] p-1">
                  {#each calendarDays.filter(d => d.dayIndex === dayIndex && d.hour === hour) as dayData}
                    {#each dayData.courses as course, index}
                      <div class={`${getColorForCourse(course, index)} border rounded-md p-1 mb-1 text-xs`}>
                        <div class="font-medium truncate">{course.matiere_nom}</div>
                        <div class="truncate text-gray-600">{course.professeur_nom}</div>
                        <div class="truncate text-gray-500">{course.salle_nom || 'N/A'}</div>
                      </div>
                    {/each}
                  {/each}
                </div>
              {/each}
            {/if}
          {/each}
        </div>
      </div>
    </div>
  
  <!-- Vue Mois -->
  {:else}
    <div class="grid grid-cols-7 gap-1">
      <!-- En-tête des jours -->
      {#each ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'] as dayName}
        <div class="text-xs font-medium text-gray-500 uppercase py-2 text-center">
          {dayName}
        </div>
      {/each}
      
      <!-- Jours du mois -->
      {#each calendarDays as day}
        <div
          class={`min-h-[100px] p-1 border rounded-lg transition-colors ${
            day.isCurrentMonth ? 'bg-white' : 'bg-gray-50'
          } ${
            day.isToday ? 'border-green-500 border-2' : 'border-gray-200'
          } hover:border-green-300 cursor-pointer`}
          on:click={() => selectDate(day.date)}
        >
          <div class={`text-sm font-medium ${
            day.isCurrentMonth ? 'text-gray-900' : 'text-gray-400'
          } ${day.isToday ? 'text-green-600' : ''}`}>
            {getDayNumber(day.date)}
          </div>
          
          <div class="mt-1 space-y-1">
            {#each day.courses.slice(0, 3) as course, index}
              <div class={`${getColorForCourse(course, index)} border rounded text-xs p-1 truncate`}>
                {course.matiere_nom}
              </div>
            {/each}
            {#if day.courses.length > 3}
              <div class="text-xs text-gray-500">
                +{day.courses.length - 3} autres
              </div>
            {/if}
          </div>
        </div>
      {/each}
    </div>
  {/if}
  
  <!-- Légende -->
  {#if courses.length > 0}
    <div class="mt-4 pt-4 border-t border-gray-200">
      <div class="flex flex-wrap gap-3">
        {#each courses.slice(0, 5) as course, index}
          <div class="flex items-center space-x-1">
            <span class={`inline-block w-3 h-3 rounded ${getColorForCourse(course, index).split(' ')[0]}`}></span>
            <span class="text-xs text-gray-600">{course.matiere_nom}</span>
          </div>
        {/each}
        {#if courses.length > 5}
          <span class="text-xs text-gray-500">+{courses.length - 5} autres</span>
        {/if}
      </div>
    </div>
  {/if}
</div>

<style>
  .min-h-100 {
    min-height: 100px;
  }
</style>