<script>
  import { onMount } from 'svelte';
  import StatsOverview from '../../../components/etablissement/StatsOverview.svelte';
  import RecentActivities from '../../../components/etablissement/RecentActivities.svelte';
  import CalendarOverview from '../../../components/etablissement/CalendarOverview.svelte';
  import { authApi } from '../../../lib/api'

  let stats = {
    students: 0,
    teachers: 0,
    classes: 0,
    pendingPayments: 0
  };
  
  let etablissementId = null;
  let loading = true;
  let error = null;

  async function loadStats() {
    loading = true;
    error = null;
    
    try {
      const profile = await authApi.getProfile();
      etablissementId = profile.profile?.id || profile.etablissement?.id;
      
      if (!etablissementId) {
        throw new Error('Établissement non trouvé');
      }
      
      const [eleves, professeurs, classes] = await Promise.all([
        authApi.getEleves({ etablissement: etablissementId, limit: 1 }), 
        authApi.getProfesseurs({ etablissement: etablissementId, limit: 1 }),
        authApi.getClasses({ etablissement: etablissementId, limit: 1 }),
      ]);
      
      const getCount = (data) => {
        if (!data) return 0;
        if (Array.isArray(data)) return data.length;
        if (data.count !== undefined) return data.count;
        if (data.results && Array.isArray(data.results)) return data.results.length;
        return 0;
      };
      
      stats = {
        students: getCount(eleves),
        teachers: getCount(professeurs),
        classes: getCount(classes),
        pendingPayments: 12
      };
    } catch (err) {
      console.error('Erreur lors du chargement des statistiques:', err);
      error = err.message || 'Impossible de charger les statistiques';
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    loadStats();
  });
</script>

<h1 class="text-2xl font-bold mb-6">Tableau de bord</h1>

{#if loading}
  <div class="flex justify-center items-center h-64">
    <div class="text-gray-500">Chargement des statistiques...</div>
  </div>
{:else if error}
  <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative" role="alert">
    <strong class="font-bold">Erreur : </strong>
    <span class="block sm:inline">{error}</span>
    <button 
      on:click={loadStats}
      class="ml-4 px-3 py-1 bg-red-100 hover:bg-red-200 rounded text-sm"
    >
      Réessayer
    </button>
  </div>
{:else}
  <StatsOverview {stats} />
  <div class="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
    <CalendarOverview />
    <RecentActivities />
  </div>
{/if}