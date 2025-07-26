<script>
  import Icon from '@iconify/svelte';
  
  const features = [
    {
      name: 'Gestion des Établissements',
      description: 'Créez et gérez plusieurs établissements avec des paramètres personnalisés pour chaque entité.',
      icon: 'heroicons:building-office-2'
    },
    {
      name: 'Gestion des Utilisateurs',
      description: 'Administrez facilement les comptes des administrateurs, enseignants, étudiants et parents.',
      icon: 'heroicons:users'
    },
    {
      name: 'Gestion des Cours et Emplois du Temps',
      description: 'Planifiez les cours, créez des emplois du temps et gérez les salles de classe en toute simplicité.',
      icon: 'heroicons:calendar'
    },
    {
      name: 'Gestion des Notes et Évaluations',
      description: 'Saisissez les notes, générez des bulletins et suivez les progrès des étudiants.',
      icon: 'heroicons:academic-cap'
    },
    {
      name: 'Inscription et Admission',
      description: 'Automatisez le processus d\'inscription et de admission des nouveaux étudiants.',
      icon: 'heroicons:clipboard-document-check'
    },
    {
      name: 'Communication',
      description: 'Messagerie intégrée, notifications et annonces pour une communication fluide.',
      icon: 'heroicons:chat-bubble-left-right'
    },
    {
      name: 'Gestion Financière',
      description: 'Suivez les frais de scolarité, les paiements et générez des factures automatiques.',
      icon: 'heroicons:currency-dollar'
    },
    {
      name: 'Gestion des Documents',
      description: 'Stockez et organisez tous les documents scolaires de manière sécurisée.',
      icon: 'heroicons:folder'
    }
  ];
</script>

<section id="features" class="py-12 bg-gray-50">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="lg:text-center">
      <h2 class="text-base text-indigo-600 font-semibold tracking-wide uppercase">Fonctionnalités</h2>
      <p class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
        Tout ce dont votre établissement a besoin
      </p>
      <p class="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
        Une plateforme complète pour simplifier la gestion quotidienne de votre école ou université.
      </p>
    </div>

    <div class="mt-10">
      <div class="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-4">
        {#each features as feature}
          <div class="group relative bg-white p-6 focus-within:ring-2 focus-within:ring-indigo-500 rounded-lg shadow-sm hover:shadow-md transition-shadow">
            <div>
              <span class="rounded-lg inline-flex p-3 bg-indigo-50 text-indigo-700 ring-4 ring-white">
                <Icon icon={feature.icon} class="h-6 w-6" />
              </span>
            </div>
            <div class="mt-8">
              <h3 class="text-lg font-medium">
                <a href="#" class="focus:outline-none">
                  <span class="absolute inset-0" aria-hidden="true"></span>
                  {feature.name}
                </a>
              </h3>
              <p class="mt-2 text-sm text-gray-500">
                {feature.description}
              </p>
            </div>
          </div>
        {/each}
      </div>
    </div>
  </div>
</section>