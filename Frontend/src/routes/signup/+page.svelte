<script>
  import Icon from '@iconify/svelte';
  
  let activeTab = 'etablissement';
  let isLoading = false;
  let errorMessage = '';
  
  const userTypes = [
    { id: 'etablissement', label: 'Établissement', icon: 'heroicons:building-office-2' },
    { id: 'professeur', label: 'Professeur', icon: 'heroicons:academic-cap' },
    { id: 'eleve', label: 'Élève', icon: 'heroicons:user' },
    { id: 'parent', label: 'Parent', icon: 'heroicons:users' }
  ];
  
  // Données des formulaires
  let etablissementData = {
    nom: '',
    email: '',
    telephone: '',
    adresse: '',
    typeEtablissement: '',
    password: '',
    confirmPassword: ''
  };
  
  let professeurData = {
    nom: '',
    prenom: '',
    email: '',
    telephone: '',
    matiere: '',
    etablissement: '',
    password: '',
    confirmPassword: ''
  };
  
  let eleveData = {
    nom: '',
    prenom: '',
    email: '',
    classe: '',
    etablissement: '',
    password: '',
    confirmPassword: ''
  };
  
  let parentData = {
    nom: '',
    prenom: '',
    email: '',
    telephone: '',
    enfants: [],
    password: '',
    confirmPassword: ''
  };

  $: enfantsText = parentData.enfants.join(', ');

  function updateEnfants(input) {
    parentData.enfants = input
      ? input.split(',').map(item => item.trim()).filter(item => item !== '')
      : [];
  }
  
  async function handleSubmit() {
    isLoading = true;
    errorMessage = '';
    
    try {
      let formData;
      
      switch (activeTab) {
        case 'etablissement':
          if (etablissementData.password !== etablissementData.confirmPassword) {
            throw new Error('Les mots de passe ne correspondent pas');
          }
          formData = etablissementData;
          break;
        case 'professeur':
          if (professeurData.password !== professeurData.confirmPassword) {
            throw new Error('Les mots de passe ne correspondent pas');
          }
          formData = professeurData;
          break;
        case 'eleve':
          if (eleveData.password !== eleveData.confirmPassword) {
            throw new Error('Les mots de passe ne correspondent pas');
          }
          formData = eleveData;
          break;
        case 'parent':
          if (parentData.password !== parentData.confirmPassword) {
            throw new Error('Les mots de passe ne correspondent pas');
          }
          formData = parentData;
          break;
      }
      
      // Ici vous ajouteriez votre logique d'inscription
      // await registerUser(formData, activeTab);
      // redirectToDashboard();
    } catch (error) {
      errorMessage = error.message || "Une erreur s'est produite lors de l'inscription";
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
  <div class="sm:mx-auto sm:w-full sm:max-w-md">
    <Icon icon="fluent:school-24-filled" class="mx-auto h-12 w-12 text-green-600" />
    <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
      Créez votre compte
    </h2>
    <p class="mt-2 text-center text-sm text-gray-600">
      Sélectionnez votre profil pour commencer
    </p>
  </div>

  <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-3xl">
    <div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
      <!-- Sélecteur de type d'utilisateur -->
      <div class="mb-6">
        <div class="flex space-x-4 overflow-x-auto pb-2">
          {#each userTypes as type}
            <button
              on:click={() => activeTab = type.id}
              class={`px-4 py-2 rounded-md flex items-center space-x-2 whitespace-nowrap ${activeTab === type.id ? 'bg-green-100 text-green-700' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              <Icon icon={type.icon} class="h-5 w-5" />
              <span>{type.label}</span>
            </button>
          {/each}
        </div>
      </div>
      
      {#if errorMessage}
        <div class="mb-4 bg-red-50 border-l-4 border-red-400 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <Icon icon="heroicons:exclamation-circle" class="h-5 w-5 text-red-400" />
            </div>
            <div class="ml-3">
              <p class="text-sm text-red-700">{errorMessage}</p>
            </div>
          </div>
        </div>
      {/if}
      
      <!-- Formulaire pour Établissement -->
      {#if activeTab === 'etablissement'}
        <form class="space-y-6" on:submit|preventDefault={handleSubmit}>
          <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label for="etab-nom" class="block text-sm font-medium text-gray-700">Nom de l'établissement</label>
              <input
                id="etab-nom"
                type="text"
                bind:value={etablissementData.nom}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div>
              <label for="etab-type" class="block text-sm font-medium text-gray-700">Type d'établissement</label>
              <select
                id="etab-type"
                bind:value={etablissementData.typeEtablissement}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              >
                <option value="">Sélectionnez...</option>
                <option value="ecole">École primaire</option>
                <option value="college">Collège</option>
                <option value="lycee">Lycée</option>
                <option value="universite">Université</option>
              </select>
            </div>
            
            <div>
              <label for="etab-email" class="block text-sm font-medium text-gray-700">Email</label>
              <input
                id="etab-email"
                type="email"
                bind:value={etablissementData.email}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div>
              <label for="etab-telephone" class="block text-sm font-medium text-gray-700">Téléphone</label>
              <input
                id="etab-telephone"
                type="tel"
                bind:value={etablissementData.telephone}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div class="sm:col-span-2">
              <label for="etab-adresse" class="block text-sm font-medium text-gray-700">Adresse</label>
              <input
                id="etab-adresse"
                type="text"
                bind:value={etablissementData.adresse}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div>
              <label for="etab-password" class="block text-sm font-medium text-gray-700">Mot de passe</label>
              <input
                id="etab-password"
                type="password"
                bind:value={etablissementData.password}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div>
              <label for="etab-confirm-password" class="block text-sm font-medium text-gray-700">Confirmer le mot de passe</label>
              <input
                id="etab-confirm-password"
                type="password"
                bind:value={etablissementData.confirmPassword}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
          </div>
          
          <div>
            <button
              type="submit"
              disabled={isLoading}
              class={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 ${isLoading ? 'opacity-70 cursor-not-allowed' : ''}`}
            >
              {#if isLoading}
                <Icon icon="heroicons:arrow-path" class="animate-spin h-5 w-5 mr-2" />
                Inscription en cours...
              {:else}
                S'inscrire en tant qu'établissement
              {/if}
            </button>
          </div>
        </form>
      
      <!-- Formulaire pour Professeur -->
      {:else if activeTab === 'professeur'}
        <form class="space-y-6" on:submit|preventDefault={handleSubmit}>
          <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label for="prof-nom" class="block text-sm font-medium text-gray-700">Nom</label>
              <input
                id="prof-nom"
                type="text"
                bind:value={professeurData.nom}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div>
              <label for="prof-prenom" class="block text-sm font-medium text-gray-700">Prénom</label>
              <input
                id="prof-prenom"
                type="text"
                bind:value={professeurData.prenom}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div>
              <label for="prof-email" class="block text-sm font-medium text-gray-700">Email</label>
              <input
                id="prof-email"
                type="email"
                bind:value={professeurData.email}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div>
              <label for="prof-telephone" class="block text-sm font-medium text-gray-700">Téléphone</label>
              <input
                id="prof-telephone"
                type="tel"
                bind:value={professeurData.telephone}
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div>
              <label for="prof-matiere" class="block text-sm font-medium text-gray-700">Matière enseignée</label>
              <input
                id="prof-matiere"
                type="text"
                bind:value={professeurData.matiere}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div>
              <label for="prof-etablissement" class="block text-sm font-medium text-gray-700">Établissement</label>
              <input
                id="prof-etablissement"
                type="text"
                bind:value={professeurData.etablissement}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div>
              <label for="prof-password" class="block text-sm font-medium text-gray-700">Mot de passe</label>
              <input
                id="prof-password"
                type="password"
                bind:value={professeurData.password}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div>
              <label for="prof-confirm-password" class="block text-sm font-medium text-gray-700">Confirmer le mot de passe</label>
              <input
                id="prof-confirm-password"
                type="password"
                bind:value={professeurData.confirmPassword}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
          </div>
          
          <div>
            <button
              type="submit"
              disabled={isLoading}
              class={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 ${isLoading ? 'opacity-70 cursor-not-allowed' : ''}`}
            >
              {#if isLoading}
                <Icon icon="heroicons:arrow-path" class="animate-spin h-5 w-5 mr-2" />
                Inscription en cours...
              {:else}
                S'inscrire en tant que professeur
              {/if}
            </button>
          </div>
        </form>
      
      <!-- Formulaire pour Élève -->
      {:else if activeTab === 'eleve'}
        <form class="space-y-6" on:submit|preventDefault={handleSubmit}>
          <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label for="eleve-nom" class="block text-sm font-medium text-gray-700">Nom</label>
              <input
                id="eleve-nom"
                type="text"
                bind:value={eleveData.nom}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div>
              <label for="eleve-prenom" class="block text-sm font-medium text-gray-700">Prénom</label>
              <input
                id="eleve-prenom"
                type="text"
                bind:value={eleveData.prenom}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div>
              <label for="eleve-email" class="block text-sm font-medium text-gray-700">Email</label>
              <input
                id="eleve-email"
                type="email"
                bind:value={eleveData.email}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div>
              <label for="eleve-classe" class="block text-sm font-medium text-gray-700">Classe</label>
              <input
                id="eleve-classe"
                type="text"
                bind:value={eleveData.classe}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div class="sm:col-span-2">
              <label for="eleve-etablissement" class="block text-sm font-medium text-gray-700">Établissement</label>
              <input
                id="eleve-etablissement"
                type="text"
                bind:value={eleveData.etablissement}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div>
              <label for="eleve-password" class="block text-sm font-medium text-gray-700">Mot de passe</label>
              <input
                id="eleve-password"
                type="password"
                bind:value={eleveData.password}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div>
              <label for="eleve-confirm-password" class="block text-sm font-medium text-gray-700">Confirmer le mot de passe</label>
              <input
                id="eleve-confirm-password"
                type="password"
                bind:value={eleveData.confirmPassword}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
          </div>
          
          <div>
            <button
              type="submit"
              disabled={isLoading}
              class={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 ${isLoading ? 'opacity-70 cursor-not-allowed' : ''}`}
            >
              {#if isLoading}
                <Icon icon="heroicons:arrow-path" class="animate-spin h-5 w-5 mr-2" />
                Inscription en cours...
              {:else}
                S'inscrire en tant qu'élève
              {/if}
            </button>
          </div>
        </form>
      
      <!-- Formulaire pour Parent -->
      {:else}
        <form class="space-y-6" on:submit|preventDefault={handleSubmit}>
          <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label for="parent-nom" class="block text-sm font-medium text-gray-700">Nom</label>
              <input
                id="parent-nom"
                type="text"
                bind:value={parentData.nom}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div>
              <label for="parent-prenom" class="block text-sm font-medium text-gray-700">Prénom</label>
              <input
                id="parent-prenom"
                type="text"
                bind:value={parentData.prenom}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div>
              <label for="parent-email" class="block text-sm font-medium text-gray-700">Email</label>
              <input
                id="parent-email"
                type="email"
                bind:value={parentData.email}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div>
              <label for="parent-telephone" class="block text-sm font-medium text-gray-700">Téléphone</label>
              <input
                id="parent-telephone"
                type="tel"
                bind:value={parentData.telephone}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div class="sm:col-span-2">
              <label for="parent-enfants" class="block text-sm font-medium text-gray-700">Enfants (noms et classes, séparés par des virgules)</label>
              <textarea
                id="parent-enfants"
                bind:value={enfantsText}
                on:input={(e) => updateEnfants(e.target.value)}
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                placeholder="Ex: Jean Dupont (3ème A), Marie Dupont (5ème B)"
              ></textarea>
            </div>
            
            <div>
              <label for="parent-password" class="block text-sm font-medium text-gray-700">Mot de passe</label>
              <input
                id="parent-password"
                type="password"
                bind:value={parentData.password}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
            
            <div>
              <label for="parent-confirm-password" class="block text-sm font-medium text-gray-700">Confirmer le mot de passe</label>
              <input
                id="parent-confirm-password"
                type="password"
                bind:value={parentData.confirmPassword}
                required
                class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
              />
            </div>
          </div>
          
          <div>
            <button
              type="submit"
              disabled={isLoading}
              class={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 ${isLoading ? 'opacity-70 cursor-not-allowed' : ''}`}
            >
              {#if isLoading}
                <Icon icon="heroicons:arrow-path" class="animate-spin h-5 w-5 mr-2" />
                Inscription en cours...
              {:else}
                S'inscrire en tant que parent
              {/if}
            </button>
          </div>
        </form>
      {/if}
      
      <div class="mt-6">
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white text-gray-500">
              Déjà un compte ?
            </span>
          </div>
        </div>

        <div class="mt-6">
          <a
            href="/login"
            class="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
          >
            Se connecter
          </a>
        </div>
      </div>
    </div>
  </div>
</div>