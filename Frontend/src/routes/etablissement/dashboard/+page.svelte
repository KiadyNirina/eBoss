<script>
  import StatsOverview from '../../../components/etablissement/StatsOverview.svelte';
  import RecentActivities from '../../../components/etablissement/RecentActivities.svelte';
  import CalendarOverview from '../../../components/etablissement/CalendarOverview.svelte';

  // Simuler des données
  const stats = {
    students: 1245,
    teachers: 78,
    classes: 36,
    pendingPayments: 12
  };
</script>

<h1 class="text-2xl font-bold">Tableau de bord</h1>

<StatsOverview {stats} />
<CalendarOverview />
<RecentActivities />