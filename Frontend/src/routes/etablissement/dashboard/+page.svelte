<script>
  import Icon from '@iconify/svelte';
  import Sidebar from '../../../components/etablissement/Sidebar.svelte';
  import Header from '../../../components/etablissement/Header.svelte';
  import StatsOverview from '../../../components/etablissement/StatsOverview.svelte';
  import RecentActivities from '../../../components/etablissement/RecentActivities.svelte';
  import CalendarOverview from '../../../components/etablissement/CalendarOverview.svelte';
  import StudentsView from '../../../components/etablissement/students/StudentsView.svelte';
  import TeachersView from '../../../components/etablissement/teachers/TeachersView.svelte';
  import ScheduleView from '../../../components/etablissement/course/ScheduleView.svelte';
  import GradesView from '../../../components/etablissement/grades/GradesView.svelte';
  import AdmissionsView from '../../../components/etablissement/admissions/AdmissionsView.svelte';
  import CommunicationView from '../../../components/etablissement/communication/CommunicationView.svelte';
  import FinanceView from '../../../components/etablissement/Finance/FinanceView.svelte';
  import { currentView } from '$lib/stores';

  let sidebarOpen = false;

  // Simuler des données
  const stats = {
    students: 1245,
    teachers: 78,
    classes: 36,
    pendingPayments: 12
  };

  const activities = [
    { type: 'new_student', name: 'Jean Dupont', class: '3ème A', time: '10 min ago' },
    { type: 'payment', name: 'Sophie Martin', amount: '€250', time: '1h ago' },
    { type: 'grade', name: 'Mathématiques', class: '4ème B', time: '2h ago' },
    { type: 'absence', name: 'Lucas Bernard', class: '5ème C', time: '5h ago' }
  ];
</script>

<div class="flex h-screen bg-gray-50">
  <!-- Sidebar Mobile -->
  <div class={`fixed inset-0 z-40 md:hidden ${sidebarOpen ? 'block' : 'hidden'}`}>
    <div class="fixed inset-0 bg-gray-600 bg-opacity-75" on:click={() => sidebarOpen = false}></div>
    <div class="relative flex flex-col w-72 max-w-xs bg-white">
      <Sidebar on:close={() => sidebarOpen = false} />
    </div>
  </div>
  
  <!-- Sidebar Desktop -->
  <div class="hidden md:flex md:flex-shrink-0">
    <div class="flex flex-col w-72 border-r border-gray-200 bg-white">
      <Sidebar />
    </div>
  </div>
  
  <div class="flex flex-col flex-1 overflow-hidden">
    <!-- Header -->
    <Header on:toggleSidebar={() => sidebarOpen = !sidebarOpen} />
    
    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto p-4 md:p-6 bg-gray-50">
      {#if $currentView === 'dashboard'}
        <div class="space-y-6">
          <div class="flex justify-between items-center">
            <h1 class="text-2xl font-bold text-gray-900">Tableau de bord</h1>
            <div class="flex space-x-3">
              <button class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500">
                <Icon icon="heroicons:plus-sm" class="-ml-1 mr-2 h-5 w-5" />
                Nouvelle action
              </button>
            </div>
          </div>
          
          <StatsOverview {stats} />
          
          <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
            <div class="lg:col-span-2">
              <CalendarOverview />
            </div>
            
            <div>
              <RecentActivities {activities} />
            </div>
          </div>
        </div>
      
      {:else if $currentView === 'etudiants'}
        <StudentsView />
      
      {:else if $currentView === 'professeurs'}
        <TeachersView />
      
      {:else if $currentView === 'cours'}
        <ScheduleView />
      
      {:else if $currentView === 'notes'}
        <GradesView />
      
      {:else if $currentView === 'inscriptions'}
        <AdmissionsView />
      
      {:else if $currentView === 'communication'}
        <CommunicationView />
      
      {:else if $currentView === 'finances'}
        <FinanceView />
      
      {:else if $currentView === 'documents'}
        <div class="bg-white shadow rounded-lg p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Documents</h2>
        </div>
      
      {:else if $currentView === 'parametres'}
        <div class="bg-white shadow rounded-lg p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Paramètres</h2>
        </div>
      
      {/if}
    </main>
  </div>
</div>