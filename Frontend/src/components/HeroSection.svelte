<script>
  import Icon from '@iconify/svelte';
</script>

<section class="relative bg-gradient-to-br from-green-50 to-emerald-50 flex items-center overflow-hidden">
  <div class="absolute top-0 left-0 w-full h-full opacity-10">
    <div class="absolute top-20 left-20 w-64 h-64 rounded-full bg-green-200 mix-blend-multiply filter blur-3xl"></div>
    <div class="absolute bottom-20 right-20 w-64 h-64 rounded-full bg-emerald-200 mix-blend-multiply filter blur-3xl"></div>
  </div>

  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 h-screen flex items-center">
    <div class="text-center">
      <span class="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium bg-green-100 text-green-800 mb-6">
        <Icon icon="mdi:school-outline" class="mr-2" />
        Solution innovante pour l'éducation
      </span>
      
      <h1 class="text-5xl font-extrabold tracking-tight text-gray-900 sm:text-6xl md:text-7xl">
        <span class="block">Révolutionnez votre</span>
        <span class="block bg-clip-text text-[#20784d]">gestion scolaire</span>
      </h1>
      
      <p class="mt-6 max-w-2xl mx-auto text-xl text-gray-600">
        eBoss modernise votre établissement avec une plateforme intuitive, complète et conçue pour les besoins éducatifs d'aujourd'hui.
      </p>
      
      <div class="mt-8 flex flex-col sm:flex-row justify-center gap-4">
        <a href="/login" class="px-8 py-4 border border-transparent text-lg font-medium rounded-xl text-white bg-[#20784d] hover:from-green-700 hover:to-emerald-600 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
          Commencer maintenant
        </a>
        <a href="#features" class="px-8 py-4 border border-gray-300 text-lg font-medium rounded-xl bg-white text-gray-700 hover:bg-gray-50 shadow hover:shadow-md transition-all duration-300 flex items-center justify-center">
          <Icon icon="mdi:play-circle-outline" class="mr-2" />
          Voir les fonctionnalités
        </a>
      </div>
      
      <div class="mt-12 flex items-center justify-center space-x-6 text-gray-500">
        <div class="flex items-center">
          <Icon icon="mdi:shield-check" class="text-[#20784d] mr-2" />
          <span>100% sécurisé</span>
        </div>
        <div class="flex items-center">
          <Icon icon="mdi:account-group" class="text-[#20784d] mr-2" />
          <span>10+ établissements</span>
        </div>
      </div>
    </div>
  </div>
</section>