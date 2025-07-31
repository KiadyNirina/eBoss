<script>
  import Icon from '@iconify/svelte';
</script>

<section class="relative bg-gradient-to-br from-green-50 to-emerald-50 flex items-center overflow-hidden">
  <div class="absolute top-0 left-0 w-full h-full opacity-10">
    <div class="absolute top-20 left-20 w-64 h-64 rounded-full bg-green-200 mix-blend-multiply filter blur-3xl"></div>
    <div class="absolute bottom-20 right-20 w-64 h-64 rounded-full bg-emerald-200 mix-blend-multiply filter blur-3xl"></div>
  </div>

  <div class="max-w-7xl mx-auto py-16 px-4 sm:py-24 sm:px-6 lg:px-8 relative z-10">
    <div class="text-center">
      <span class="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-green-100 text-green-800 mb-6">
        <Icon icon="mdi:school-outline" class="mr-2" />
        Solution innovante pour l'éducation
      </span>
      
      <h1 class="text-5xl font-extrabold tracking-tight text-gray-900 sm:text-6xl md:text-7xl">
        <span class="block">Révolutionnez votre</span>
        <span class="block bg-clip-text text-transparent bg-gradient-to-r from-green-600 to-emerald-500">gestion scolaire</span>
      </h1>
      
      <p class="mt-6 max-w-2xl mx-auto text-xl text-gray-600">
        eBoss modernise votre établissement avec une plateforme intuitive, complète et conçue pour les besoins éducatifs d'aujourd'hui.
      </p>
      
      <div class="mt-8 flex flex-col sm:flex-row justify-center gap-4">
        <a href="/login" class="px-8 py-4 border border-transparent text-lg font-medium rounded-xl text-white bg-gradient-to-r from-green-600 to-emerald-500 hover:from-green-700 hover:to-emerald-600 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
          Commencer maintenant
        </a>
        <a href="#features" class="px-8 py-4 border border-gray-300 text-lg font-medium rounded-xl bg-white text-gray-700 hover:bg-gray-50 shadow hover:shadow-md transition-all duration-300 flex items-center justify-center">
          <Icon icon="mdi:play-circle-outline" class="mr-2" />
          Voir les fonctionnalités
        </a>
      </div>
      
      <div class="mt-12 flex items-center justify-center space-x-6 text-gray-500">
        <div class="flex items-center">
          <Icon icon="mdi:shield-check" class="text-green-500 mr-2" />
          <span>100% sécurisé</span>
        </div>
        <div class="flex items-center">
          <Icon icon="mdi:account-group" class="text-emerald-500 mr-2" />
          <span>10+ établissements</span>
        </div>
      </div>
    </div>
    
    <div class="mt-20 max-w-5xl mx-auto">
      <div class="relative rounded-2xl overflow-hidden shadow-2xl border border-gray-200/50 bg-white">
        <div class="absolute top-0 left-0 right-0 h-10 bg-gray-50 flex items-center px-4 border-b">
          <div class="flex space-x-2 mr-4">
            <div class="w-3 h-3 rounded-full bg-red-500"></div>
            <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
            <div class="w-3 h-3 rounded-full bg-green-500"></div>
          </div>
          <div class="flex-1 bg-gray-100 rounded-full h-5 mx-4"></div>
          <Icon icon="mdi:dots-horizontal" class="text-gray-400" />
        </div>
        <div class="h-96 bg-gradient-to-br from-white to-gray-50 flex items-center justify-center">
          <Icon icon="mdi:monitor-dashboard" class="w-24 h-24 text-gray-300" />
        </div>
      </div>
    </div>
  </div>
</section>