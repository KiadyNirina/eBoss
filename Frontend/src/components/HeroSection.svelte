<script>
  import Icon from '@iconify/svelte';
</script>

<section class="relative bg-gradient-to-br from-green-50 to-emerald-50 overflow-hidden h-screen">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center">
    <!-- Two-column layout -->
    <div class="grid md:grid-cols-2 gap-8 items-center w-full">
      
      <!-- Left: text content -->
      <div class="text-center md:text-left">

        <h1 class="unbounded text-5xl font-extrabold tracking-tight text-gray-900 sm:text-6xl md:text-7xl">
          <span class="block">Révolutionnez votre</span>
          <span class="block bg-clip-text text-transparent bg-gradient-to-r from-[#20784d] to-emerald-600">gestion scolaire</span>
        </h1>
        
        <p class="mt-6 max-w-2xl text-xl text-gray-600">
          eBoss modernise votre établissement avec une plateforme intuitive, complète et conçue pour les besoins éducatifs d’aujourd’hui.
        </p>
        
        <div class="mt-8 flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
          <a href="/login" class="px-8 py-4 border border-transparent text-lg font-medium rounded-full text-white bg-[#20784d] hover:from-green-700 hover:to-emerald-600 transition-all duration-300 transform hover:-translate-y-1">
            Commencer maintenant
          </a>
          <a href="#features" class="px-8 py-4 border border-gray-300 text-lg font-medium rounded-full bg-white text-gray-700 hover:border-green-600 transition-all duration-300 flex items-center justify-center">
            <Icon icon="mdi:play-circle-outline" class="mr-2" />
            Voir les fonctionnalités
          </a>
        </div>
      </div>
      
      <!-- Right: the real image -->
      <div class="flex justify-center md:justify-end">
        <img 
          src="img/Learning-cuate.svg" 
          alt="Enseignant en classe" 
          class="w-full max-w-md lg:max-w-lg object-contain"
        />
      </div>
    </div>
  </div>
</section>