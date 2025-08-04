<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';

  export let selectedEvaluation;

  let chart;
  let chartRef;

  onMount(() => {
    if (chartRef && selectedEvaluation) {
      updateChart();
    }

    return () => {
      if (chart) chart.destroy();
    };
  });

  function updateChart() {
    if (!chartRef) return;
    if (chart) chart.destroy();

    const notes = selectedEvaluation.notes.map(n => n.note);
    const noteGroups = {
      '0-5': notes.filter(n => n >= 0 && n < 5).length,
      '5-10': notes.filter(n => n >= 5 && n < 10).length,
      '10-15': notes.filter(n => n >= 10 && n < 15).length,
      '15-20': notes.filter(n => n >= 15 && n <= 20).length
    };

    const ctx = chartRef.getContext('2d');
    chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['0-5', '5-10', '10-15', '15-20'],
        datasets: [{
          label: 'Répartition des notes',
          data: Object.values(noteGroups),
          backgroundColor: [
            '#ef4444', // rouge
            '#f59e0b', // orange
            '#10b981', // vert
            '#3b82f6'  // bleu
          ],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: function(context) {
                return `${context.parsed.y} étudiants (${Math.round(context.parsed.y / notes.length * 100)}%)`;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: { display: true, text: "Nombre d'étudiants" }
          },
          x: {
            title: { display: true, text: "Intervalle de notes" }
          }
        }
      }
    });
  }

  $: if (selectedEvaluation && chartRef) updateChart();
</script>

<div class="bg-white p-4 shadow-sm border border-gray-200 rounded-lg">
  <h3 class="text-sm font-medium text-gray-900 mb-4">Répartition des notes</h3>
  <div class="">
    <canvas bind:this={chartRef}></canvas>
  </div>
</div>