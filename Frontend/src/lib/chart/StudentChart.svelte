<script>
    import { Bar } from 'svelte-chartjs';
    import 'chart.js/auto'; // Importation des éléments nécessaires de Chart.js

    // Données pour le graphique
    let chartData = {
        labels: ['Classe A', 'Classe B', 'Classe C'], // Les catégories de classes ou niveaux
        datasets: [
            {
                label: 'Nombre d\'élèves',
                data: [30, 25, 40], // Nombre d'élèves dans chaque classe
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }
        ]
    };

    let chartOptions = {
        responsive: true,
        plugins: {
            legend: {
                display: true,
            },
            tooltip: {
                callbacks: {
                    label: function(tooltipItem) {
                        return `Nombre d'élèves: ${tooltipItem.raw}`;
                    }
                }
            }
        }
    };
</script>

<div class="chart-container">
    <Bar {chartData} {chartOptions} />
</div>

<style>
    .chart-container {
        width: 100%;
        max-width: 600px;
        margin: auto;
    }
</style>
