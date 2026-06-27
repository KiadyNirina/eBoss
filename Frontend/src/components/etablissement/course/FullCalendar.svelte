<script>
  import { onMount } from 'svelte';
  import Icon from '@iconify/svelte';
  import { authApi } from '$lib/api';
  
  export let view = 'week';
  export let courses = [];
  export let classesOptions = [];
  export let matieresOptions = [];
  export let professeursOptions = [];
  
  let currentDate = new Date();
  let selectedDate = new Date();
  let calendarDays = [];
  let weekDays = [];
  let hours = [];
  let showFilters = false;
  
  // Filtres
  let filters = {
    classe: '',
    matiere: '',
    professeur: ''
  };

  // Modal de déplacement
  let showMoveModal = false;
  let selectedCourse = null;
  let moveDate = '';
  let moveHour = '';
  let moveAction = 'move'; 
  
  // Cours filtrés
  let filteredCourses = [];
  
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
    applyFilters();
    generateCalendar();
  });
  
  // Fonction pour appliquer les filtres
  function applyFilters() {
    filteredCourses = courses.filter(c => {
      let match = true;
      
      if (filters.classe) {
        match = match && c.classe === parseInt(filters.classe);
      }
      if (filters.matiere) {
        match = match && c.matiere === parseInt(filters.matiere);
      }
      if (filters.professeur) {
        match = match && c.professeur === parseInt(filters.professeur);
      }
      
      return match;
    });
    
    generateCalendar();
  }
  
  // Réinitialiser les filtres
  function resetFilters() {
    filters = {
      classe: '',
      matiere: '',
      professeur: ''
    };
    applyFilters();
  }
  
  // Vérifier si des filtres sont actifs
  function hasActiveFilters() {
    return filters.classe || filters.matiere || filters.professeur;
  }
  
  function getFilterCount() {
    let count = 0;
    if (filters.classe) count++;
    if (filters.matiere) count++;
    if (filters.professeur) count++;
    return count;
  }
  
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
    
    const prevMonthLastDay = new Date(year, month, 0).getDate();
    for (let i = startOffset - 1; i >= 0; i--) {
      const date = new Date(year, month - 1, prevMonthLastDay - i);
      days.push({
        date: date,
        isCurrentMonth: false,
        courses: getCoursesForDate(date)
      });
    }
    
    for (let i = 1; i <= daysInMonth; i++) {
      const date = new Date(year, month, i);
      days.push({
        date: date,
        isCurrentMonth: true,
        isToday: isSameDay(date, new Date()),
        courses: getCoursesForDate(date)
      });
    }
    
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
    return filteredCourses.filter(c => {
      // Si le cours a une date spécifique, on l'affiche uniquement ce jour-là
      if (c.date_specifique) {
        return c.date_specifique === dateStr;
      }
      
      // Sinon, on utilise le jour de la semaine
      const jourIndex = JOURS.findIndex(j => j.value === c.jour);
      if (jourIndex === -1) return false;
      
      const monday = getWeekStart(date);
      const courseDate = new Date(monday);
      courseDate.setDate(monday.getDate() + jourIndex);
      
      return isSameDay(courseDate, date);
    });
  }

  function getJourLabel(jour) {
    const found = JOURS.find(j => j.value === jour);
    return found ? found.label : jour;
  }

  function getCourseDisplayDate(course) {
    if (course.date_specifique) {
      const date = new Date(course.date_specifique + 'T00:00:00');
      return date.toLocaleString('fr-FR', { day: 'numeric', month: 'short' });
    }
    return getJourLabel(course.jour);
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
    return Math.max(minutes * 1.2, 30);
  }
  
  function getCoursePosition(course) {
    const [hour, min] = course.heure_debut.split(':').map(Number);
    const totalMinutes = hour * 60 + min;
    const startMinutes = 7 * 60;
    const offsetMinutes = totalMinutes - startMinutes;
    return offsetMinutes * 1.2;
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
  
  function toggleFilters() {
    showFilters = !showFilters;
  }

  function openMoveModal(course, event) {
    event.stopPropagation();
    selectedCourse = course;
    
    // Pré-remplir avec la date actuelle du cours
    const currentDate = getDateForCourse(course);
    if (currentDate) {
      const year = currentDate.getFullYear();
      const month = String(currentDate.getMonth() + 1).padStart(2, '0');
      const day = String(currentDate.getDate()).padStart(2, '0');
      moveDate = `${year}-${month}-${day}`;
    } else {
      moveDate = formatDate(new Date());
    }
    
    // Si le cours a une date spécifique, l'utiliser
    if (course.date_specifique) {
      moveDate = course.date_specifique;
    }
    
    moveHour = course.heure_debut;
    showMoveModal = true;
  }

  // Fonction pour obtenir la date d'un cours
  function getDateForCourse(course) {
    const jourIndex = JOURS.findIndex(j => j.value === course.jour);
    if (jourIndex === -1) return null;
    
    const monday = getWeekStart(selectedDate);
    const courseDate = new Date(monday);
    courseDate.setDate(monday.getDate() + jourIndex);
    return courseDate;
  }

  // Fonction pour déplacer/copier le cours
  async function moveCourse() {
    if (!selectedCourse || !moveDate || !moveHour) {
      alert('Veuillez sélectionner une date et une heure');
      return;
    }
    
    try {
      const dateObj = new Date(moveDate + 'T00:00:00');
      const dayIndex = dateObj.getDay();
      const jourMap = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];
      const newJour = jourMap[dayIndex === 0 ? 6 : dayIndex - 1];
      
      const duration = getCourseDurationInMinutes(selectedCourse);
      const [h, m] = moveHour.split(':').map(Number);
      const endMinutes = h * 60 + m + duration;
      const endH = Math.floor(endMinutes / 60);
      const endM = endMinutes % 60;
      const newEndHour = `${String(endH).padStart(2, '0')}:${String(endM).padStart(2, '0')}`;
      
      // Vérifier si la date est un jour spécifique ou régulier
      const isSpecificDate = moveDate !== formatDate(getDateForCourse(selectedCourse));
      
      const courseData = {
        classe: selectedCourse.classe,
        professeur: selectedCourse.professeur,
        matiere: selectedCourse.matiere,
        salle: selectedCourse.salle || null,
        jour: newJour,
        heure_debut: moveHour,
        heure_fin: newEndHour,
        annee_scolaire: selectedCourse.annee_scolaire,
        etablissement: selectedCourse.etablissement,
        date_specifique: isSpecificDate ? moveDate : null // Si la date change, on la rend spécifique
      };
      
      // Si c'est une copie, on garde la date spécifique
      if (moveAction === 'copy') {
        // Pour une copie, on garde la date spécifique si elle existe
        if (selectedCourse.date_specifique) {
          courseData.date_specifique = moveDate;
        }
        await createCourse(courseData);
        alert('Cours copié avec succès !');
      } else {
        // Pour un déplacement, on utilise la nouvelle date
        await updateCourse(selectedCourse.id, courseData);
        alert('Cours déplacé avec succès !');
      }
      
      showMoveModal = false;
      selectedCourse = null;
      
      const newCourses = await authApi.getCours();
      courses = newCourses.results || newCourses;
    } catch (err) {
      alert('Erreur: ' + (err.message || 'Impossible de déplacer le cours'));
      console.error('Erreur:', err);
    }
  }

  async function updateCourse(id, data) {
    try {
      await authApi.updateCours(id, data);
      await refreshCourses();
      return true;
    } catch (err) {
      console.error('Erreur mise à jour:', err);
      throw err;
    }
  }
  
  async function createCourse(data) {
    try {
      await authApi.createCours(data);
      await refreshCourses();
      return true;
    } catch (err) {
      console.error('Erreur création:', err);
      throw err;
    }
  }

  async function deleteCourse(id) {
    try {
      await authApi.deleteCours(id);
      await refreshCourses();
      return true;
    } catch (err) {
      console.error('Erreur suppression:', err);
      throw err;
    }
  }

  async function refreshCourses() {
    try {
      const data = await authApi.getCours();
      courses = data.results || data;
      applyFilters(); 
      generateCalendar();
    } catch (err) {
      console.error('Erreur rafraîchissement:', err);
    }
  }
  
  // Fonction pour supprimer un cours
  async function deleteCourseFromCalendar(course, event) {
    event.stopPropagation();
    if (!confirm(`Supprimer le cours "${course.matiere_nom}" du ${course.jour} ?`)) return;
    
    try {
      await deleteCourse(course.id);
      alert('Cours supprimé avec succès !');
    } catch (err) {
      alert('Erreur: ' + (err.message || 'Impossible de supprimer le cours'));
      console.error('Erreur:', err);
    }
  }
  
  // Fermer le modal
  function closeMoveModal() {
    showMoveModal = false;
    selectedCourse = null;
  }
  
  // Réagir aux changements
  $: view, generateCalendar();
  $: filteredCourses, generateCalendar();
  $: filters, applyFilters();
</script>

<div class="bg-white rounded-lg">
  <!-- En-tête du calendrier avec filtres -->
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
    
    <div class="flex items-center space-x-2">
      <!-- Bouton Filtres -->
      <button
        on:click={toggleFilters}
        class={`relative inline-flex items-center px-3 py-1 text-sm font-medium rounded-md transition-colors ${
          hasActiveFilters() 
            ? 'bg-green-100 text-green-700' 
            : 'text-gray-700 hover:bg-gray-100'
        }`}
      >
        <Icon icon="heroicons:funnel" class="h-4 w-4 mr-1" />
        Filtres
        {#if hasActiveFilters()}
          <span class="ml-1 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-600 text-white">
            {getFilterCount()}
          </span>
        {/if}
      </button>
      
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
  </div>
  
  <!-- Panneau des filtres -->
  {#if showFilters}
    <div class="mb-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
      <div class="flex items-center justify-between mb-3">
        <h4 class="text-sm font-medium text-gray-700">Filtrer les cours</h4>
        <button
          on:click={resetFilters}
          class="text-xs text-green-600 hover:text-green-800 font-medium"
        >
          Réinitialiser les filtres
        </button>
      </div>
      
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div>
          <label for="filter-classe-calendar" class="block text-xs font-medium text-gray-700">
            Classe
          </label>
          <select
            id="filter-classe-calendar"
            bind:value={filters.classe}
            on:change={applyFilters}
            class="mt-1 block w-full pl-3 pr-10 py-1.5 text-sm border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 rounded-md"
          >
            <option value="">Toutes les classes</option>
            {#each classesOptions as option}
              <option value={option.value}>{option.label}</option>
            {/each}
          </select>
        </div>
        
        <div>
          <label for="filter-matiere-calendar" class="block text-xs font-medium text-gray-700">
            Matière
          </label>
          <select
            id="filter-matiere-calendar"
            bind:value={filters.matiere}
            on:change={applyFilters}
            class="mt-1 block w-full pl-3 pr-10 py-1.5 text-sm border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 rounded-md"
          >
            <option value="">Toutes les matières</option>
            {#each matieresOptions as option}
              <option value={option.value}>{option.label}</option>
            {/each}
          </select>
        </div>
        
        <div>
          <label for="filter-professeur-calendar" class="block text-xs font-medium text-gray-700">
            Professeur
          </label>
          <select
            id="filter-professeur-calendar"
            bind:value={filters.professeur}
            on:change={applyFilters}
            class="mt-1 block w-full pl-3 pr-10 py-1.5 text-sm border-gray-300 focus:outline-none focus:ring-green-500 focus:border-green-500 rounded-md"
          >
            <option value="">Tous les professeurs</option>
            {#each professeursOptions as option}
              <option value={option.value}>{option.label}</option>
            {/each}
          </select>
        </div>
      </div>
      
      <!-- Indicateur de filtres actifs -->
      {#if hasActiveFilters()}
        <div class="mt-3 flex flex-wrap gap-2">
          {#if filters.classe}
            <span class="inline-flex items-center px-2 py-1 rounded-md text-xs bg-green-100 text-green-800">
              Classe: {classesOptions.find(o => o.value === parseInt(filters.classe))?.label}
              <button
                on:click={() => { filters.classe = ''; applyFilters(); }}
                class="ml-1 hover:text-green-600"
              >
                <Icon icon="heroicons:x-mark" class="h-3 w-3" />
              </button>
            </span>
          {/if}
          {#if filters.matiere}
            <span class="inline-flex items-center px-2 py-1 rounded-md text-xs bg-blue-100 text-blue-800">
              Matière: {matieresOptions.find(o => o.value === parseInt(filters.matiere))?.label}
              <button
                on:click={() => { filters.matiere = ''; applyFilters(); }}
                class="ml-1 hover:text-blue-600"
              >
                <Icon icon="heroicons:x-mark" class="h-3 w-3" />
              </button>
            </span>
          {/if}
          {#if filters.professeur}
            <span class="inline-flex items-center px-2 py-1 rounded-md text-xs bg-purple-100 text-purple-800">
              Professeur: {professeursOptions.find(o => o.value === parseInt(filters.professeur))?.label}
              <button
                on:click={() => { filters.professeur = ''; applyFilters(); }}
                class="ml-1 hover:text-purple-600"
              >
                <Icon icon="heroicons:x-mark" class="h-3 w-3" />
              </button>
            </span>
          {/if}
        </div>
      {/if}
    </div>
  {/if}
  
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
                
                <!-- Message si aucun cours -->
                {#if !calendarDays.some(d => d.courses.length > 0)}
                  <div class="absolute inset-0 no-course-pattern flex items-center justify-center">
                    <div class="backdrop-blur-sm px-4 py-2 rounded-lg">
                      <p class="text-sm font-medium text-gray-500">
                        Aucun cours pour cette journée
                      </p>
                    </div>
                  </div>
                {/if}
                
                <!-- Cours -->
                {#each calendarDays.filter(d => d.courses.length > 0) as dayData}
                  {#each dayData.courses as course, index}
                    <div 
                      class={`absolute left-1 right-1 rounded-md p-1.5 border-2 shadow-sm transition-all cursor-pointer group ${getColorForCourse(course, index).bg} ${getColorForCourse(course, index).border} ${getColorForCourse(course, index).hover}`}
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
                        <div class="text-xs text-gray-500 truncate flex items-center gap-1">
                          {#if course.date_specifique}
                            <span class="text-orange-500">📅</span>
                            <span class="text-orange-600 text-[10px]">{getCourseDisplayDate(course)}</span>
                            <span class="text-gray-400">•</span>
                          {/if}
                          {course.classe_nom} • {getCourseDuration(course)}
                          {#if course.salle_nom}
                            • {course.salle_nom}
                          {/if}
                        </div>
                      </div>
                      
                      <!-- Boutons d'action (hover) -->
                      <div class="absolute top-0 right-0 opacity-0 group-hover:opacity-100 transition-opacity flex space-x-0.5">
                        <button
                          on:click|stopPropagation={(e) => openMoveModal(course, e)}
                          class="p-0.5 bg-white rounded shadow-md hover:bg-gray-100 text-blue-600"
                          title="Déplacer/Copier"
                        >
                          <Icon icon="heroicons:arrows-pointing-out" class="h-3 w-3" />
                        </button>
                        <button
                          on:click|stopPropagation={(e) => deleteCourseFromCalendar(course, e)}
                          class="p-0.5 bg-white rounded shadow-md hover:bg-gray-100 text-red-600"
                          title="Supprimer"
                        >
                          <Icon icon="heroicons:trash" class="h-3 w-3" />
                        </button>
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
                  
                  <!-- Message si aucun cours -->
                  {#if !calendarDays.some(d => d.dayIndex === dayIndex && d.courses.length > 0)}
                    <div class="absolute inset-0 no-course-pattern flex items-center justify-center">
                      <span class="backdrop-blur-sm px-4 py-2 rounded-lg text-xs font-medium text-gray-500">
                        Aucun cours
                      </span>
                    </div>
                  {/if}
                  
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
              <div 
                class={`${getColorForCourse(course, index).bg} ${getColorForCourse(course, index).text} border rounded text-xs p-1 truncate cursor-pointer group relative ${course.date_specifique ? 'border-orange-200 border-2' : ''}`}
                on:click={() => selectDate(day.date)}
              >
                <span class="font-medium">{course.matiere_nom}</span>
                <span class="text-gray-500 ml-1">{course.heure_debut}</span>
                <span class="text-gray-400 ml-1 text-[10px]">{course.classe_nom}</span>
                {#if course.date_specifique}
                  <span class="text-orange-500 ml-1 text-[10px]">📅</span>
                {/if}
                
                <!-- Boutons d'action -->
                <div class="absolute top-0 right-0 opacity-0 group-hover:opacity-100 transition-opacity flex space-x-0.5">
                  <button
                    on:click|stopPropagation={(e) => openMoveModal(course, e)}
                    class="p-0.5 bg-white rounded shadow-md hover:bg-gray-100 text-blue-600 text-[10px]"
                  >
                    <Icon icon="heroicons:arrows-pointing-out" class="h-3 w-3" />
                  </button>
                </div>
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
  {#if filteredCourses.length > 0}
    <div class="mt-4 pt-4 border-t border-gray-200">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <div class="flex flex-wrap gap-3">
          {#each [...new Set(filteredCourses.map(c => c.matiere_nom))].slice(0, 6) as matiere, index}
            <div class="flex items-center space-x-1">
              <span class={`inline-block w-3 h-3 rounded ${getColorForCourse({ matiere_nom: matiere }, index).bg}`}></span>
              <span class="text-xs text-gray-600">{matiere}</span>
            </div>
          {/each}
          {#if [...new Set(filteredCourses.map(c => c.matiere_nom))].length > 6}
            <span class="text-xs text-gray-500">
              +{[...new Set(filteredCourses.map(c => c.matiere_nom))].length - 6} autres
            </span>
          {/if}
        </div>
        
        <div class="flex items-center gap-3 text-xs text-gray-500">
          <span><span class="font-medium">{filteredCourses.length}</span> cours</span>
          {#if hasActiveFilters()}
            <span class="text-green-600">
              ({courses.length - filteredCourses.length} filtrés)
            </span>
          {/if}
          <span>•</span>
          <span><span class="font-medium">{new Set(filteredCourses.map(c => c.classe_nom)).size}</span> classes</span>
        </div>
      </div>
    </div>
  {:else}
    <div class="mt-4 pt-4 border-t border-gray-200 text-center py-8">
      <Icon icon="heroicons:funnel" class="h-8 w-8 text-gray-300 mx-auto mb-2" />
      <p class="text-sm text-gray-500">
        {#if hasActiveFilters()}
          Aucun cours ne correspond aux filtres sélectionnés
        {:else}
          Aucun cours planifié
        {/if}
      </p>
      {#if hasActiveFilters()}
        <button
          on:click={resetFilters}
          class="mt-2 text-sm text-green-600 hover:text-green-800 font-medium"
        >
          Réinitialiser les filtres
        </button>
      {/if}
    </div>
  {/if}
</div>

<!-- Modal de déplacement/copie -->
{#if showMoveModal && selectedCourse}
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 p-6">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-medium text-gray-900">
          {moveAction === 'copy' ? 'Copier' : 'Déplacer'} le cours
        </h3>
        <button
          on:click={closeMoveModal}
          class="text-gray-400 hover:text-gray-600"
        >
          <Icon icon="heroicons:x-mark" class="h-6 w-6" />
        </button>
      </div>
      
      <div class="space-y-4">
        <!-- Informations du cours -->
        <div class="bg-gray-50 p-3 rounded-md">
          <p class="text-sm font-medium text-gray-700">{selectedCourse.matiere_nom}</p>
          <p class="text-sm text-gray-600">{selectedCourse.professeur_nom} • {selectedCourse.classe_nom}</p>
          <p class="text-sm text-gray-500">
            Actuellement: 
            {#if selectedCourse.date_specifique}
              <span class="text-orange-500 font-medium">
                📅 {new Date(selectedCourse.date_specifique + 'T00:00:00').toLocaleString('fr-FR', { 
                  day: 'numeric', 
                  month: 'short', 
                  year: 'numeric' 
                })}
              </span>
            {:else}
              {selectedCourse.jour}
            {/if}
            {selectedCourse.heure_debut} - {selectedCourse.heure_fin}
          </p>
          {#if selectedCourse.date_specifique}
            <p class="text-xs text-orange-600 mt-1">
              ⚠️ Cours exceptionnel (date spécifique)
            </p>
          {/if}
        </div>
        
        <!-- Nouvelle date -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Nouvelle date
            <span class="text-gray-400 text-xs font-normal">(sera marquée comme spécifique)</span>
          </label>
          <input
            type="date"
            bind:value={moveDate}
            class="w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
          />
        </div>
        
        <!-- Nouvelle heure -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Nouvelle heure de début
          </label>
          <input
            type="time"
            bind:value={moveHour}
            class="w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
          />
          <p class="mt-1 text-xs text-gray-500">
            Durée du cours: {getCourseDurationInMinutes(selectedCourse)} minutes
          </p>
        </div>
        
        <!-- Action -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Action
          </label>
          <div class="flex space-x-4">
            <label class="flex items-center">
              <input
                type="radio"
                bind:group={moveAction}
                value="move"
                checked
                class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300"
              />
              <span class="ml-2 text-sm text-gray-700">Déplacer</span>
            </label>
            <label class="flex items-center">
              <input
                type="radio"
                bind:group={moveAction}
                value="copy"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
              />
              <span class="ml-2 text-sm text-gray-700">Copier</span>
            </label>
          </div>
        </div>
        
        <!-- Boutons -->
        <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
          <button
            on:click={closeMoveModal}
            class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
          >
            Annuler
          </button>
          <button
            on:click={moveCourse}
            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
          >
            {moveAction === 'copy' ? 'Copier' : 'Déplacer'}
          </button>
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
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
  
  .transition-all {
    transition: all 0.15s ease-in-out;
  }
  
  .shadow-sm:hover {
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  }

  .no-course-pattern {
    background-image:
      repeating-linear-gradient(
        -45deg,
        transparent 0,
        transparent 12px,
        rgba(115, 118, 122, 0.612) 12px,
        rgba(209, 213, 219, 0.726) 13px
      );
  }
</style>