<script>
  import { onMount } from 'svelte';
  import { Chart, registerables } from 'chart.js';
  import Icon from '@iconify/svelte';

  Chart.register(...registerables);
  
  let chart;
  let chartCanvas;
  
  // Données simulées
  const financialData = {
    year: {
      labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc'],
      revenues: [8500, 9200, 10500, 11200, 12500, 13400, 14200, 12800, 11500, 13200, 14800, 16200],
      payments: [7200, 8100, 9500, 10200, 11800, 12600, 13500, 12100, 10800, 12400, 13900, 15300]
    },
    quarter: {
      labels: ['Q1', 'Q2', 'Q3', 'Q4'],
      revenues: [28200, 37100, 38500, 44200],
      payments: [24800, 34600, 36400, 41600]
    },
    month: {
      labels: ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4'],
      revenues: [4000, 4200, 4500, 4800],
      payments: [3500, 3800, 4000, 4200]
    }
  };
  
  let selectedPeriod = 'year';
  
  // Fonction pour formatter les valeurs monétaires
  const formatMoney = (value) => {
    return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(value);
  };
  
  // Initialiser ou mettre à jour le graphique
  const updateChart = () => {
    const data = financialData[selectedPeriod];
    
    if (chart) {
      chart.data.labels = data.labels;
      chart.data.datasets[0].data = data.revenues;
      chart.data.datasets[1].data = data.payments;
      chart.update();
      return;
    }
    
    const ctx = chartCanvas.getContext('2d');
    
    chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.labels,
        datasets: [
          {
            label: 'Revenus',
            data: data.revenues,
            backgroundColor: '#16a34a', // Vert-600
            borderColor: '#16a34a',
            borderWidth: 1,
            borderRadius: 4,
            borderSkipped: false
          },
          {
            label: 'Paiements',
            data: data.payments,
            backgroundColor: '#2563eb', // Bleu-600
            borderColor: '#2563eb',
            borderWidth: 1,
            borderRadius: 4,
            borderSkipped: false
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: {
              boxWidth: 12,
              padding: 20,
              usePointStyle: true,
              pointStyle: 'circle'
            }
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                let label = context.dataset.label || '';
                if (label) {
                  label += ': ';
                }
                if (context.parsed.y !== null) {
                  label += formatMoney(context.parsed.y);
                }
                return label;
              }
            }
          }
        },
        scales: {
          x: {
            grid: {
              display: false
            }
          },
          y: {
            beginAtZero: true,
            grid: {
              color: '#e5e7eb' // Gris-200
            },
            ticks: {
              callback: (value) => formatMoney(value).replace('€', '') + '€'
            }
          }
        },
        interaction: {
          intersect: false,
          mode: 'index'
        }
      }
    });
  };
  
  onMount(() => {
    updateChart();
    return () => chart?.destroy();
  });
  
  $: if (chartCanvas) {
    updateChart();
  }
</script>

<div>
  <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-4 gap-3">
    <h3 class="text-lg font-medium text-gray-900">Activité Financière</h3>
    <div class="flex">
      <button 
        on:click={() => selectedPeriod = 'month'}
        class={`px-3 py-1 text-sm font-medium rounded-l-md ${selectedPeriod === 'month' ? 'bg-green-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-50'}`}
      >
        Mois
      </button>
      <button 
        on:click={() => selectedPeriod = 'quarter'}
        class={`px-3 py-1 text-sm font-medium border-l border-r border-gray-200 ${selectedPeriod === 'quarter' ? 'bg-green-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-50'}`}
      >
        Trimestre
      </button>
      <button 
        on:click={() => selectedPeriod = 'year'}
        class={`px-3 py-1 text-sm font-medium rounded-r-md ${selectedPeriod === 'year' ? 'bg-green-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-50'}`}
      >
        Année
      </button>
    </div>
  </div>
  
  <div class="bg-white p-4 rounded-lg border border-gray-200">
    <!-- Conteneur du graphique -->
    <div class="relative h-64 w-full">
      <canvas
        bind:this={chartCanvas}
        class="w-full h-full"
        aria-label="Graphique d'activité financière"
        role="img"
      ></canvas>
    </div>
    
    <!-- Légende simplifiée -->
    <div class="mt-4 flex flex-wrap justify-center gap-4 sm:gap-6">
      <div class="flex items-center">
        <div class="h-3 w-3 rounded-full bg-green-500 mr-2"></div>
        <span class="text-sm text-gray-500">Revenus</span>
      </div>
      <div class="flex items-center">
        <div class="h-3 w-3 rounded-full bg-blue-500 mr-2"></div>
        <span class="text-sm text-gray-500">Paiements</span>
      </div>
    </div>
  </div>
</div>