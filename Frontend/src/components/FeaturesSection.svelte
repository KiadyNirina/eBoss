<script>
  import Icon from '@iconify/svelte';
  import { fade, fly } from 'svelte/transition';
  
  const features = [
    {
      name: 'Gestion des Établissements',
      description: 'Créez et gérez plusieurs établissements avec des paramètres personnalisés pour chaque entité.',
      longDescription: 'Notre module de gestion des établissements permet de créer des structures hiérarchiques complexes, de définir des paramètres spécifiques pour chaque entité et de gérer les accès de manière granulaire. Bénéficiez d\'une vue unifiée tout en conservant l\'autonomie de chaque établissement.',
      icon: 'heroicons:building-office-2',
      benefits: [
        'Gestion multi-établissements sécurisée',
        'Paramétrage personnalisable',
        'Tableaux de bord analytiques',
        'Hiérarchie configurable'
      ]
    },
    {
      name: 'Gestion des Utilisateurs',
      description: 'Administrez facilement les comptes des administrateurs, enseignants, étudiants et parents.',
      longDescription: 'Centralisez la gestion de tous les utilisateurs de votre écosystème éducatif. Créez des profils personnalisés, gérez les permissions et accédez à des outils de reporting avancés pour suivre l\'activité des utilisateurs.',
      icon: 'heroicons:users',
      benefits: [
        'Gestion des rôles et permissions',
        'Import massif via CSV/Excel',
        'Double authentification',
        'Historique des connexions'
      ]
    },
    {
      name: 'Gestion des Cours',
      description: 'Planifiez les cours, créez des emplois du temps et gérez les salles de classe intuitivement.',
      longDescription: 'Notre solution de gestion des cours vous permet de créer des emplois du temps complexes en quelques clics, avec gestion des conflits automatique et notification des changements en temps réel à tous les acteurs concernés.',
      icon: 'heroicons:calendar',
      benefits: [
        'Génération automatique des emplois du temps',
        'Gestion des salles et ressources',
        'Alertes de conflits',
        'Export vers calendriers externes'
      ]
    },
    {
      name: 'Évaluations & Résultats',
      description: 'Saisissez les notes, générez des bulletins et suivez les progrès des étudiants.',
      longDescription: 'Simplifiez le processus d\'évaluation avec des grilles de notation personnalisables, des outils d\'analyse des résultats et des bulletins automatisés disponibles en plusieurs formats (PDF, Excel, etc.).',
      icon: 'heroicons:academic-cap',
      benefits: [
        'Grilles de notation personnalisables',
        'Calcul automatique des moyennes',
        'Historique des résultats',
        'Alertes de performances'
      ]
    },
    {
      name: 'Inscriptions en Ligne',
      description: 'Automatisez le processus d\'inscription avec des formulaires personnalisables.',
      longDescription: 'Notre module d\'inscription en ligne permet aux familles de s\'inscrire 24h/24 depuis n\'importe quel appareil, avec suivi du processus, paiement en ligne et validation automatisée des documents.',
      icon: 'heroicons:clipboard-document-check',
      benefits: [
        'Formulaires personnalisables',
        'Paiement en ligne intégré',
        'Validation des documents',
        'Tableau de bord de suivi'
      ]
    },
    {
      name: 'Communication Unifiée',
      description: 'Messagerie, notifications et annonces pour une communication transparente.',
      longDescription: 'Notre plateforme intègre tous les outils de communication nécessaires : messagerie interne, notifications push, emails automatisés et portail parents avec traduction multilingue optionnelle.',
      icon: 'heroicons:chat-bubble-left-right',
      benefits: [
        'Messagerie sécurisée',
        'Modèles de communication',
        'Historique des échanges',
        'Traduction multilingue'
      ]
    },
    {
      name: 'Finance & Facturation',
      description: 'Suivez les frais de scolarité, paiements et générez des factures automatiques.',
      longDescription: 'Automatisez toute la gestion financière de votre établissement avec notre module intégré de facturation, gestion des frais, rappels automatiques et rapports financiers détaillés.',
      icon: 'heroicons:currency-dollar',
      benefits: [
        'Facturation automatisée',
        'Paiement en ligne',
        'Rappels automatiques',
        'Reporting financier'
      ]
    },
    {
      name: 'Portail Documentaire',
      description: 'Centralisez tous les documents scolaires de manière sécurisée et organisée.',
      longDescription: 'Stockez, organisez et partagez en toute sécurité tous les documents de votre établissement avec un système de gestion documentaire puissant et des workflows d\'approbation configurables.',
      icon: 'heroicons:folder',
      benefits: [
        'Stockage sécurisé',
        'Workflows d\'approbation',
        'Recherche avancée',
        'Versionning des documents'
      ]
    }
  ];

  let activeFeature = null;
  let showModal = false;

  function openModal(feature) {
    activeFeature = feature;
    showModal = true;
  }

  function closeModal() {
    showModal = false;
    activeFeature = null;
  }
</script>

<section id="features" class="py-20 bg-gradient-to-b from-white to-green-50">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="text-center mb-16">
      <span class="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-green-100 text-green-800 mb-4">
        <Icon icon="mdi:feature-search-outline" class="mr-2" />
        Fonctionnalités Clés
      </span>
      <h2 class="mt-2 text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl">
        Une suite complète <span class="text-green-600">d'outils intégrés</span>
      </h2>
      <p class="mt-6 max-w-3xl mx-auto text-xl text-gray-600">
        Découvrez comment eBoss transforme la gestion éducative avec des solutions modernes et intuitives.
      </p>
    </div>

    <div class="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
      {#each features as feature}
        <div class="relative group bg-white p-8 rounded-2xl shadow-sm hover:shadow-lg transition-all duration-300 border border-gray-100 hover:border-green-100">
          <div class="absolute -inset-0.5 bg-gradient-to-r from-green-100 to-emerald-100 rounded-2xl opacity-0 group-hover:opacity-100 blur-sm transition duration-300"></div>
          <div class="relative h-full flex flex-col">
            <div class="flex-shrink-0 mb-6">
              <span class="inline-flex items-center justify-center w-14 h-14 rounded-xl bg-green-50 text-green-600">
                <Icon icon={feature.icon} class="h-7 w-7" />
              </span>
            </div>
            <h3 class="text-xl font-semibold text-gray-900 mb-3">
              {feature.name}
            </h3>
            <p class="flex-grow text-gray-600">
              {feature.description}
            </p>
            <div class="mt-4 pt-4 border-t border-gray-100">
              <button 
                on:click={() => openModal(feature)}
                class="text-green-600 font-medium inline-flex items-center group-hover:text-green-700 transition-colors cursor-pointer"
              >
                En savoir plus
                <Icon icon="mdi:arrow-right" class="ml-2 transition-transform group-hover:translate-x-1" />
              </button>
            </div>
          </div>
        </div>
      {/each}
    </div>
  </div>

  <!-- Modal -->
  {#if showModal && activeFeature}
  <div transition:fade="{{ duration: 250 }}" class="fixed inset-0 bg-black bg-opacity-50 z-50 transition-opacity duration-300">
    <div class="fixed inset-0 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        <div class="sticky top-0 bg-white p-6 border-b border-gray-100 flex justify-between items-center">
          <h2 class="text-2xl font-bold text-gray-900">Détails de la fonctionnalité</h2>
          <button 
            on:click={closeModal}
            class="text-gray-400 hover:text-gray-500 transition-colors"
          >
            <Icon icon="mdi:close" class="w-6 h-6" />
          </button>
        </div>
        
        <div class="p-8">
          <div class="flex items-start mb-8">
            <span class="inline-flex items-center justify-center w-14 h-14 rounded-xl bg-green-50 text-green-600 mr-6 flex-shrink-0">
              <Icon icon={activeFeature.icon} class="h-7 w-7" />
            </span>
            <div>
              <h3 class="text-2xl font-bold text-gray-900">{activeFeature.name}</h3>
              <p class="text-gray-500 mt-2">{activeFeature.description}</p>
            </div>
          </div>
          
          <div class="prose prose-lg text-gray-600 max-w-none">
            <p class="text-lg leading-relaxed">{activeFeature.longDescription}</p>
            
            <div class="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="bg-green-50 p-6 rounded-xl border border-green-100">
                <h4 class="font-semibold text-lg text-green-800 flex items-center mb-4">
                  <Icon icon="mdi:check-circle" class="mr-2 text-green-600" />
                  Principaux avantages
                </h4>
                <ul class="space-y-3">
                  {#each activeFeature.benefits as benefit}
                    <li class="flex items-start">
                      <Icon icon="mdi:check" class="text-green-500 mr-2 mt-1 flex-shrink-0" />
                      <span class="text-gray-700">{benefit}</span>
                    </li>
                  {/each}
                </ul>
              </div>
              
              <div class="bg-blue-50 p-6 rounded-xl border border-blue-100">
                <h4 class="font-semibold text-lg text-blue-800 flex items-center mb-4">
                  <Icon icon="mdi:lightbulb-on" class="mr-2 text-blue-600" />
                  Intégration
                </h4>
                <p class="mb-4 text-gray-700">Ce module s'intègre parfaitement avec tous les autres composants de la plateforme eBoss pour une gestion unifiée de votre écosystème éducatif.</p>
                
                <div class="flex items-center mt-4">
                  <Icon icon="mdi:cog-sync" class="text-blue-500 mr-2" />
                  <span class="text-sm text-blue-600">Synchronisation en temps réel avec les autres modules</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="sticky bottom-0 bg-white p-6 border-t border-gray-100">
          <div class="flex flex-col sm:flex-row justify-end space-y-3 sm:space-y-0 sm:space-x-4">
            <button 
              on:click={closeModal}
              class="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors flex items-center justify-center"
            >
              <Icon icon="mdi:close" class="mr-2" />
              Fermer
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  {/if}
</section>