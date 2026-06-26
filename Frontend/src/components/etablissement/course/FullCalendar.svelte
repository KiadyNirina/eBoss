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
  
  // Générer les heures de 7h à 19h avec intervalles de 30min
  function generateHours() {
    const h = [];
    for (let i = 7; i <= 19; i++) {
      h.push(`${i.toString().padStart(2, '0')}:00`);
      if (i < 19) h.push(`${i.toString().padStart(2, '0')}:30`);
    }
    return h;
  }
  
  hours = generateHours();
  
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
  
  function getWeekStart(date) {
    const dayOfWeek = date.getDay();
    const mondayOffset = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
    const monday = new Date(date);
    monday.setDate(date.getDate() - mondayOffset);
    monday.setHours(0, 0, 0, 0);
    return monday;
  }
  
  function generateDayView() {
    const date = new Date(selectedDate);
    date.setHours(0, 0, 0, 0);
    
    const dayCourses = getCoursesForDate(date);
    const dateStr = formatDate(date);
    
    // Créer une structure pour chaque heure avec les cours
    calendarDays = [];
    hours.forEach((hour, index) => {
      const hourCourses = dayCourses.filter(c => {
        const courseStart = c.heure_debut;
        const courseEnd = c.heure_fin;
        return hour >= courseStart && hour < courseEnd;
      });
      
      calendarDays.push({
        date: date,
        dateStr: dateStr,
        hour: hour,
        hourIndex: index,
        courses: hourCourses
      });
    });
  }
  
  function generateWeekView() {
    const monday = getWeekStart(selectedDate);
    
    weekDays = [];
    for (let i = 0; i < 7; i++) {
      const day = new Date(monday);
      day.setDate(monday.getDate() + i);
      weekDays.push(day);
    }
    
    calendarDays = [];
    weekDays.forEach((day, dayIndex) => {
      const dayCourses = getCoursesForDate(day);
      const dateStr = formatDate(day);
      
      hours.forEach((hour, hourIndex) => {
        const hourCourses = dayCourses.filter(c => {
          const courseStart = c.heure_debut;
          const courseEnd = c.heure_fin;
          return hour >= courseStart && hour < courseEnd;
        });
        
        calendarDays.push({
          date: day,
          dateStr: dateStr,
          hour: hour,
          hourIndex: hourIndex,
          dayIndex: dayIndex,
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
    const startDayOfWeek = firstDay.getDay();
    
    const days = [];
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
      
      const monday = getWeekStart(date);
      const courseDate = new Date(monday);
      courseDate.setDate(monday.getDate() + jourIndex);
      
      return isSameDay(courseDate, date);
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
      { bg: 'bg-blue-100', border: 'border-blue-300', text: 'text-blue-800', hover: 'hover:bg-blue-200' },
      { bg: 'bg-green-100', border: 'border-green-300', text: 'text-green-800', hover: 'hover:bg-green-200' },
      { bg: 'bg-purple-100', border: 'border-purple-300', text: 'text-purple-800', hover: 'hover:bg-purple-200' },
      { bg: 'bg-yellow-100', border: 'border-yellow-300', text: 'text-yellow-800', hover: 'hover:bg-yellow-200' },
      { bg: 'bg-pink-100', border: 'border-pink-300', text: 'text-pink-800', hover: 'hover:bg-pink-200' },
      { bg: 'bg-indigo-100', border: 'border-indigo-300', text: 'text-indigo-800', hover: 'hover:bg-indigo-200' },
      { bg: 'bg-red-100', border: 'border-red-300', text: 'text-red-800', hover: 'hover:bg-red-200' },
      { bg: 'bg-teal-100', border: 'border-teal-300', text: 'text-teal-800', hover: 'hover:bg-teal-200' }
    ];
    return colors[index % colors.length];
  }
  
  function getCourseDuration(course) {
    const start = course.heure_debut;
    const end = course.heure_fin;
    return `${start} - ${end}`;
  }
  
  function getCourseDurationInMinutes(course) {
    const [startHour, startMin] = course.heure_debut.split(':').map(Number);
    const [endHour, endMin] = course.heure_fin.split(':').map(Number);
    return (endHour * 60 + endMin) - (startHour * 60 + startMin);
  }
  
  function getCourseHeight(course) {
    const minutes = getCourseDurationInMinutes(course);
    // 1 minute = 1.2px (60 minutes = 72px)
    return Math.max(minutes * 1.2, 30);
  }
  
  function getCoursePosition(course) {
    const [hour, min] = course.heure_debut.split(':').map(Number);
    const totalMinutes = hour * 60 + min;
    const startMinutes = 7 * 60; // 7h
    const offsetMinutes = totalMinutes - startMinutes;
    return offsetMinutes * 1.2; // 1 minute = 1.2px
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
  
  function isCurrentHour(hour) {
    const now = new Date();
    const currentHour = now.getHours();
    const currentMin = now.getMinutes();
    const [h, m] = hour.split(':').map(Number);
    return h === currentHour && Math.abs(currentMin - m) < 30;
  }
  
  function getCurrentTimePosition() {
    const now = new Date();
    const currentHour = now.getHours();
    const currentMin = now.getMinutes();
    const totalMinutes = currentHour * 60 + currentMin;
    const startMinutes = 7 * 60;
    const offsetMinutes = totalMinutes - startMinutes;
    return offsetMinutes * 1.2;
  }
  
  $: view, generateCalendar();
  $: courses, generateCalendar();
</script>

<div class="bg-white rounded-lg">
  <!-- En-tête du calendrier -->
  <div class="flex flex-wrap items-center justify-between mb-4 gap-2">
    <div class="flex items-center space-x-2">
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
    
    <div class="flex space-x-1">
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
        <div class="grid" style="grid-template-columns: 60px repeat({view === 'day' ? 1 : 7}, 1fr); gap: 2px;">
          <div class="text-xs font-medium text-gray-500 py-2 text-center"></div>
          {#if view === 'day'}
            <div class="text-xs font-medium text-gray-700 py-2 text-center">
              <div class="text-gray-500 text-xs">{selectedDate.toLocaleString('fr-FR', { weekday: 'short' })}</div>
              <div class={`text-lg font-bold ${isSameDay(selectedDate, new Date()) ? 'text-green-600' : 'text-gray-900'}`}>
                {getDayNumber(selectedDate)}
              </div>
            </div>
          {:else}
            {#each weekDays as day}
              <div class={`text-xs font-medium py-2 text-center ${
                isSameDay(day, new Date()) ? 'bg-green-50 rounded-lg' : ''
              }`}>
                <div class="text-gray-500 text-xs">{day.toLocaleString('fr-FR', { weekday: 'short' })}</div>
                <div class={`text-lg font-bold ${
                  isSameDay(day, new Date()) ? 'text-green-600' : 'text-gray-900'
                }`}>
                  {getDayNumber(day)}
                </div>
              </div>
            {/each}
          {/if}
        </div>
        
        <!-- Grille des cours avec hauteur fixe -->
        <div class="relative mt-2" style="height: 870px; overflow-y: auto;">
          <!-- Ligne de l'heure actuelle -->
          {#if view === 'day' || view === 'week'}
            <div 
              class="absolute left-0 right-0 z-10 pointer-events-none"
              style="top: {getCurrentTimePosition()}px;"
            >
              <div class="flex items-center">
                <div class="w-12 h-0.5 bg-red-500"></div>
                <div class="w-2 h-2 bg-red-500 rounded-full -ml-1"></div>
                <span class="ml-1 text-xs text-red-500 font-medium">
                  {new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
            </div>
          {/if}
          
          <!-- Grille des heures -->
          <div class="grid" style="grid-template-columns: 60px repeat({view === 'day' ? 1 : 7}, 1fr); gap: 2px;">
            <!-- Colonne des heures -->
            <div class="relative">
              {#each hours as hour}
                <div class="text-xs text-gray-400 pr-2 text-right" style="height: 36px; line-height: 36px;">
                  {hour}
                </div>
              {/each}
            </div>
            
            <!-- Colonnes des jours -->
            {#if view === 'day'}
              <div class="relative">
                <!-- Lignes de la grille -->
                {#each hours as hour}
                  <div class="border-t border-gray-100" style="height: 36px;"></div>
                {/each}
                
                <!-- Cours -->
                {#each calendarDays.filter(d => d.courses.length > 0) as dayData}
                  {#each dayData.courses as course}
                    <div 
                      class={`absolute left-1 right-1 rounded-md p-1.5 border-2 shadow-sm transition-all ${getColorForCourse(course, 0).bg} ${getColorForCourse(course, 0).border} ${getColorForCourse(course, 0).hover}`}
                      style="top: {getCoursePosition(course)}px; height: {getCourseHeight(course)}px; min-height: 30px;"
                    >
                      <div class="flex flex-col h-full">
                        <div class={`text-xs font-bold truncate ${getColorForCourse(course, 0).text}`}>
                          {course.matiere_nom}
                        </div>
                        <div class="text-xs text-gray-600 truncate">
                          {course.professeur_nom}
                        </div>
                        <div class="text-xs text-gray-500 truncate">
                          {course.classe_nom} • {getCourseDuration(course)}
                          {#if course.salle_nom}
                            • {course.salle_nom}
                          {/if}
                        </div>
                      </div>
                    </div>
                  {/each}
                {/each}
              </div>
            {:else}
              <!-- Vue semaine -->
              {#each weekDays as day, dayIndex}
                <div class="relative">
                  <!-- Lignes de la grille -->
                  {#each hours as hour}
                    <div class="border-t border-gray-100" style="height: 36px;"></div>
                  {/each}
                  
                  <!-- Cours -->
                  {#each calendarDays.filter(d => d.dayIndex === dayIndex && d.courses.length > 0) as dayData}
                    {#each dayData.courses as course, index}
                      <div 
                        class={`absolute left-1 right-1 rounded-md p-1.5 border-2 shadow-sm transition-all ${getColorForCourse(course, index).bg} ${getColorForCourse(course, index).border} ${getColorForCourse(course, index).hover}`}
                        style="top: {getCoursePosition(course)}px; height: {getCourseHeight(course)}px; min-height: 30px;"
                        title="{course.matiere_nom} - {course.classe_nom} - {course.professeur_nom} - {getCourseDuration(course)}"
                      >
                        <div class="flex flex-col h-full">
                          <div class={`text-xs font-bold truncate ${getColorForCourse(course, index).text}`}>
                            {course.matiere_nom}
                          </div>
                          <div class="text-xs text-gray-600 truncate">
                            {course.professeur_nom}
                          </div>
                          <div class="text-xs text-gray-500 truncate">
                            {course.classe_nom} • {getCourseDuration(course)}
                            {#if course.salle_nom}
                              • {course.salle_nom}
                            {/if}
                          </div>
                        </div>
                      </div>
                    {/each}
                  {/each}
                </div>
              {/each}
            {/if}
          </div>
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
          class={`min-h-[100px] p-1 border rounded-lg transition-colors cursor-pointer ${
            day.isCurrentMonth ? 'bg-white' : 'bg-gray-50'
          } ${
            day.isToday ? 'border-green-500 border-2' : 'border-gray-200'
          } hover:border-green-300 hover:shadow-md`}
          on:click={() => selectDate(day.date)}
        >
          <div class={`text-sm font-medium ${
            day.isCurrentMonth ? 'text-gray-900' : 'text-gray-400'
          } ${day.isToday ? 'text-green-600' : ''}`}>
            {getDayNumber(day.date)}
          </div>
          
          <div class="mt-1 space-y-1">
            {#each day.courses.slice(0, 3) as course, index}
              <div class={`${getColorForCourse(course, index).bg} ${getColorForCourse(course, index).text} border rounded text-xs p-1 truncate`}>
                <span class="font-medium">{course.matiere_nom}</span>
                <span class="text-gray-500 ml-1">{course.heure_debut}</span>
                <span class="text-gray-400 ml-1 text-[10px]">{course.classe_nom}</span>
              </div>
            {/each}
            {#if day.courses.length > 3}
              <div class="text-xs text-gray-500 font-medium">
                +{day.courses.length - 3} autres
              </div>
            {/if}
          </div>
        </div>
      {/each}
    </div>
  {/if}
  
  <!-- Légende et statistiques -->
  {#if courses.length > 0}
    <div class="mt-4 pt-4 border-t border-gray-200">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <div class="flex flex-wrap gap-3">
          {#each [...new Set(courses.map(c => c.matiere_nom))].slice(0, 6) as matiere, index}
            <div class="flex items-center space-x-1">
              <span class={`inline-block w-3 h-3 rounded ${getColorForCourse({ matiere_nom: matiere }, index).bg}`}></span>
              <span class="text-xs text-gray-600">{matiere}</span>
            </div>
          {/each}
          {#if [...new Set(courses.map(c => c.matiere_nom))].length > 6}
            <span class="text-xs text-gray-500">
              +{[...new Set(courses.map(c => c.matiere_nom))].length - 6} autres
            </span>
          {/if}
        </div>
        
        <div class="flex items-center gap-3 text-xs text-gray-500">
          <span><span class="font-medium">{courses.length}</span> cours</span>
          <span>•</span>
          <span><span class="font-medium">{new Set(courses.map(c => c.classe_nom)).size}</span> classes</span>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  /* Scroll personnalisé */
  .overflow-x-auto::-webkit-scrollbar {
    height: 8px;
  }
  
  .overflow-x-auto::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
  }
  
  .overflow-x-auto::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 4px;
  }
  
  .overflow-x-auto::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
  }
  
  /* Animation hover */
  .transition-all {
    transition: all 0.15s ease-in-out;
  }
  
  /* Effet de profondeur */
  .shadow-sm:hover {
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  }
</style>