<script>
  const plans = [
    {
      name: 'Basique',
      price: '29€',
      period: '/mois',
      description: 'Parfait pour les petites écoles',
      features: [
        'Jusqu\'à 100 étudiants',
        'Gestion des cours et emplois du temps',
        'Gestion des notes',
        'Support par email'
      ],
      cta: 'Commencer',
      featured: false
    },
    {
      name: 'Standard',
      price: '79€',
      period: '/mois',
      description: 'Pour les établissements moyens',
      features: [
        'Jusqu\'à 500 étudiants',
        'Toutes les fonctionnalités Basique',
        'Gestion financière',
        'Communication intégrée',
        'Support prioritaire'
      ],
      cta: 'Commencer',
      featured: true
    },
    {
      name: 'Premium',
      price: '149€',
      period: '/mois',
      description: 'Pour les grandes institutions',
      features: [
        'Nombre illimité d\'étudiants',
        'Toutes les fonctionnalités Standard',
        'Gestion multi-établissements',
        'API d\'intégration',
        'Support 24/7',
        'Formation personnalisée'
      ],
      cta: 'Commencer',
      featured: false
    }
  ];
</script>

<section id="pricing" class="py-12 bg-gray-50">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="lg:text-center">
      <h2 class="text-base text-indigo-600 font-semibold tracking-wide uppercase">Tarifs</h2>
      <p class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
        Des forfaits adaptés à chaque établissement
      </p>
      <p class="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
        Essai gratuit de 30 jours sans engagement.
      </p>
    </div>

    <div class="mt-16 space-y-12 lg:space-y-0 lg:grid lg:grid-cols-3 lg:gap-x-8">
      {#each plans as plan}
        <div class={`relative p-8 bg-white border rounded-2xl shadow-sm ${plan.featured ? 'border-indigo-500 ring-2 ring-indigo-500' : 'border-gray-200'}`}>
          {#if plan.featured}
            <div class="absolute top-0 right-0 -mt-3 -mr-3 px-3 py-1 bg-indigo-600 text-white text-xs font-semibold rounded-full">
              Plus populaire
            </div>
          {/if}
          <div class="text-center">
            <h3 class="text-lg font-medium text-gray-900">{plan.name}</h3>
            <div class="mt-4 flex items-center justify-center">
              <span class="px-3 flex items-start text-6xl tracking-tight text-gray-900">
                <span class="mt-2 mr-1 text-4xl font-medium">€</span>
                <span class="font-extrabold">{plan.price}</span>
              </span>
              <span class="text-xl font-medium text-gray-500">{plan.period}</span>
            </div>
            <p class="mt-4 text-sm text-gray-500">
              {plan.description}
            </p>
          </div>
          
          <ul class="mt-6 space-y-4">
            {#each plan.features as feature}
              <li class="flex items-start">
                <svg class="h-6 w-6 flex-shrink-0 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <p class="ml-3 text-gray-700">{feature}</p>
              </li>
            {/each}
          </ul>
          
          <div class="mt-8">
            <a href="/register" class={`block w-full py-3 px-6 text-center rounded-md ${plan.featured ? 'bg-indigo-600 text-white hover:bg-indigo-700' : 'bg-indigo-50 text-indigo-700 hover:bg-indigo-100'} font-medium`}>
              {plan.cta}
            </a>
          </div>
        </div>
      {/each}
    </div>
  </div>
</section>