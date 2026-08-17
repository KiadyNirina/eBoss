<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';

  export let evaluation = null;

  let chart;
  let chartRef;

  $: notes = evaluation?.notes || [];
  $: validNotes = notes.filter(n => !n.absent && n.note != null);
  $: hasData = validNotes.length > 0;

  function updateChart() {
    if (!chartRef) return;

    if (!hasData) {
      if (chart) {
        chart.destroy();
        chart = null;
      }
      return;
    }

    if (chart) chart.destroy();

    const noteValues = validNotes.map(n => n.note);
    const noteGroups = {
      '0-5': noteValues.filter(n => n >= 0 && n < 5).length,
      '5-10': noteValues.filter(n => n >= 5 && n < 10).length,
      '10-15': noteValues.filter(n => n >= 10 && n < 15).length,
      '15-20': noteValues.filter(n => n >= 15 && n <= 20).length
    };
    const total = noteValues.length || 1;

    const ctx = chartRef.getContext('2d');
    chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['0-5', '5-10', '10-15', '15-20'],
        datasets: [{
          label: 'Répartition des notes',
          data: Object.values(noteGroups),
          backgroundColor: ['#ef4444', '#f59e0b', '#10b981', '#3b82f6'],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => `${ctx.parsed.y} étudiants (${Math.round(ctx.parsed.y / total * 100)}%)`
            }
          }
        },
        scales: {
          y: { beginAtZero: true, title: { display: true, text: "Nombre d'étudiants" } },
          x: { title: { display: true, text: "Intervalle de notes" } }
        }
      }
    });
  }

  onMount(() => {
    updateChart();
    return () => { if (chart) chart.destroy(); };
  });

  $: if (evaluation || hasData) {
    updateChart();
  }
</script>

<div class="bg-white p-4 shadow-sm border border-gray-200 rounded-lg">
  <h3 class="text-sm font-medium text-gray-900 mb-4">Répartition des notes</h3>

  <div class:hidden={!hasData}>
    <canvas bind:this={chartRef}></canvas>
  </div>

  {#if !hasData}
    <p class="text-gray-500 text-sm text-center py-8">
      Aucune note disponible
    </p>
  {/if}
</div>