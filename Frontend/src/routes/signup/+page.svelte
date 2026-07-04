<!-- src/routes/register/+page.svelte -->
<script>
  import Icon from '@iconify/svelte';
  import { authApi } from '$lib/api';
  import { 
    getEtablissementFormData,
    getProfesseurFormData,
    getEleveFormData,
    getParentFormData 
  } from '$lib/formData';
  import AddressAutocomplete from '$lib/components/AddressAutocomplete.svelte';
  import GeocodingService from '$lib/geocoding.js';
  import geocodingCache from '$lib/geocoding-cache.js';
  
  let activeTab = 'etablissement';
  let isLoading = false;
  let errorMessage = '';
  let successMessage = '';
  
  // Statut du géocodage
  let geocodingStatus = '';
  let geocodingSuccess = false;
  let geocodingCoordinates = null;
  let addressValid = false;
  let addressData = null;
  
  // Liste des années scolaires et classes
  let anneesScolaires = [];
  let classes = [];
  
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
    latitude: null,
    longitude: null,
    typeEtablissement: '',
    password: '',
    confirmPassword: '',
    anneeScolaire: {
      nom: '',
      date_debut: '',
      date_fin: ''
    },
    classes: [{
      nom: '',
      niveau: '',
      section: ''
    }]
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

  // Fonction pour ajouter une nouvelle classe
  function addClasse() {
    etablissementData = {
      ...etablissementData,
      classes: [
        ...(etablissementData.classes || []),
        { nom: '', niveau: '', section: '' }
      ]
    };
  }
  
  // Fonction pour supprimer une classe
  function removeClasse(index) {
    etablissementData = {
      ...etablissementData,
      classes: etablissementData.classes.filter((_, i) => i !== index)
    };
  }

  function updateEnfants(input) {
    parentData.enfants = input
      ? input.split(',').map(item => item.trim()).filter(item => item !== '')
      : [];
  }

  function setDefaultClasses(type) {
    switch (type) {
      case 'ecole':
        etablissementData.classes = [
          { nom: 'CP', niveau: 'CP', section: '' },
          { nom: 'CE1', niveau: 'CE1', section: '' },
          { nom: 'CE2', niveau: 'CE2', section: '' },
          { nom: 'CM1', niveau: 'CM1', section: '' },
          { nom: 'CM2', niveau: 'CM2', section: '' }
        ];
        break;
      case 'college':
        etablissementData.classes = [
          { nom: '6ème', niveau: '6ème', section: '' },
          { nom: '5ème', niveau: '5ème', section: '' },
          { nom: '4ème', niveau: '4ème', section: '' },
          { nom: '3ème', niveau: '3ème', section: '' }
        ];
        break;
      case 'lycee':
        etablissementData.classes = [
          { nom: 'Seconde', niveau: 'Seconde', section: '' },
          { nom: 'Première', niveau: 'Première', section: '' },
          { nom: 'Terminale', niveau: 'Terminale', section: '' }
        ];
        break;
      case 'universite':
        etablissementData.classes = [
          { nom: 'Licence 1', niveau: 'L1', section: '' },
          { nom: 'Licence 2', niveau: 'L2', section: '' },
          { nom: 'Licence 3', niveau: 'L3', section: '' },
          { nom: 'Master 1', niveau: 'M1', section: '' },
          { nom: 'Master 2', niveau: 'M2', section: '' }
        ];
        break;
      default:
        etablissementData.classes = [{ nom: '', niveau: '', section: '' }];
    }
  }

  let lastTypeEtab = '';

  $: if (
    activeTab === 'etablissement' &&
    etablissementData.typeEtablissement &&
    etablissementData.typeEtablissement !== lastTypeEtab
  ) {
    lastTypeEtab = etablissementData.typeEtablissement;
    setDefaultClasses(etablissementData.typeEtablissement);
  }

  // Gestionnaire de sélection d'adresse
  function handleAddressSelect(event) {
    const { address, latitude, longitude, fullData } = event.detail;
    
    etablissementData.adresse = address;
    etablissementData.latitude = latitude;
    etablissementData.longitude = longitude;
    addressValid = true;
    geocodingSuccess = true;
    geocodingCoordinates = { lat: latitude, lng: longitude };
    geocodingStatus = `✅ Adresse géocodée: ${latitude}, ${longitude}`;
    
    console.log('Adresse sélectionnée:', {
      address,
      latitude,
      longitude,
      fullData
    });
  }

  // Gestionnaire de géocodage automatique
  function handleGeocode(event) {
    const { latitude, longitude, address } = event.detail;
    
    etablissementData.latitude = latitude;
    etablissementData.longitude = longitude;
    if (address) {
      etablissementData.adresse = address;
    }
    addressValid = true;
    geocodingSuccess = true;
    geocodingCoordinates = { lat: latitude, lng: longitude };
    geocodingStatus = `✅ Coordonnées trouvées: ${latitude}, ${longitude}`;
  }

  // Fonction pour géocoder l'adresse manuellement
  async function geocodeAddressManually() {
    if (!etablissementData.adresse) {
      geocodingStatus = '⚠️ Veuillez saisir une adresse d\'abord';
      return;
    }

    geocodingStatus = '🔍 Recherche des coordonnées en cours...';
    geocodingSuccess = false;
    addressValid = false;

    try {
      // Utiliser le service de géocodage avec cache
      const result = await geocodingCache.geocode(etablissementData.adresse);
      
      if (result) {
        etablissementData.latitude = result.latitude;
        etablissementData.longitude = result.longitude;
        addressValid = true;
        geocodingSuccess = true;
        geocodingCoordinates = {
          lat: result.latitude,
          lng: result.longitude
        };
        geocodingStatus = `✅ Coordonnées trouvées: ${result.latitude}, ${result.longitude}`;
        
        // Mettre à jour l'affichage avec le nom normalisé
        if (result.display_name) {
          etablissementData.adresse = result.display_name;
        }
      } else {
        geocodingStatus = '❌ Adresse non trouvée. Vérifiez l\'adresse saisie.';
        etablissementData.latitude = null;
        etablissementData.longitude = null;
        addressValid = false;
      }
    } catch (error) {
      geocodingStatus = `❌ Erreur de géocodage: ${error.message}`;
      console.error('Erreur de géocodage:', error);
    }
  }

  // Fonction pour ouvrir un lien Google Maps avec l'adresse
  function openGoogleMaps() {
    if (!etablissementData.adresse) return;
    const url = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(etablissementData.adresse)}`;
    window.open(url, '_blank');
  }

  // Fonction pour utiliser la position actuelle
  async function useCurrentLocation() {
    if (!navigator.geolocation) {
      geocodingStatus = '⚠️ La géolocalisation n\'est pas supportée par votre navigateur';
      return;
    }

    geocodingStatus = '📍 Obtention de votre position...';

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        try {
          const { latitude, longitude } = position.coords;
          
          // Géocodage inverse avec cache
          const result = await geocodingCache.reverseGeocode(latitude, longitude);
          
          if (result) {
            etablissementData.adresse = result.display_name;
            etablissementData.latitude = latitude;
            etablissementData.longitude = longitude;
            addressValid = true;
            geocodingSuccess = true;
            geocodingCoordinates = { lat: latitude, lng: longitude };
            geocodingStatus = `✅ Position trouvée: ${latitude}, ${longitude}`;
          } else {
            geocodingStatus = '❌ Impossible de récupérer l\'adresse depuis votre position';
          }
        } catch (error) {
          geocodingStatus = '❌ Erreur lors du géocodage inverse';
          console.error('Erreur:', error);
        }
      },
      (error) => {
        geocodingStatus = '❌ Impossible d\'obtenir votre position. Vérifiez les permissions.';
        console.error('Erreur de géolocalisation:', error);
      },
      { enableHighAccuracy: true, timeout: 10000 }
    );
  }
  
  async function handleSubmit() {
    isLoading = true;
    errorMessage = '';
    successMessage = '';
    geocodingStatus = '';
    
    try {
        let formData;
        let apiMethod;
        
        switch (activeTab) {
            case 'etablissement':
                if (etablissementData.password !== etablissementData.confirmPassword) {
                  throw new Error('Les mots de passe ne correspondent pas');
                }
                
                // Validation des données
                if (!etablissementData.anneeScolaire.nom || 
                    !etablissementData.anneeScolaire.date_debut || 
                    !etablissementData.anneeScolaire.date_fin) {
                  throw new Error('Veuillez remplir tous les champs de l\'année scolaire');
                }
                
                if (etablissementData.classes.length === 0) {
                  throw new Error('Veuillez ajouter au moins une classe');
                }
                
                for (const classe of etablissementData.classes) {
                  if (!classe.nom || !classe.niveau) {
                    throw new Error('Veuillez remplir tous les champs des classes');
                  }
                }

                // Vérifier si l'adresse a été géocodée
                if (!addressValid && etablissementData.adresse) {
                  geocodingStatus = '🌍 Géocodage de l\'adresse...';
                  try {
                    const result = await geocodingCache.geocode(etablissementData.adresse);
                    if (result) {
                      etablissementData.latitude = result.latitude;
                      etablissementData.longitude = result.longitude;
                      addressValid = true;
                      geocodingSuccess = true;
                      geocodingCoordinates = {
                        lat: result.latitude,
                        lng: result.longitude
                      };
                    } else {
                      throw new Error('Adresse non trouvée');
                    }
                  } catch (error) {
                    throw new Error(`Erreur de géocodage: ${error.message}`);
                  }
                }

                geocodingStatus = '🌍 Enregistrement de l\'établissement...';

                // Création de l'établissement avec les coordonnées déjà géocodées
                const etablissementFormData = getEtablissementFormData(etablissementData);
                // Ajouter les coordonnées manuellement si elles ne sont pas dans le formulaire
                if (!etablissementFormData.latitude && etablissementData.latitude) {
                  etablissementFormData.latitude = etablissementData.latitude;
                  etablissementFormData.longitude = etablissementData.longitude;
                }
                
                const etablissement = await authApi.registerEtablissement(etablissementFormData);

                console.log('Établissement créé:', etablissement);
                
                // Vérifier si l'établissement a des coordonnées
                if (etablissement.etablissement?.latitude && etablissement.etablissement?.longitude) {
                  geocodingStatus = '✅ Établissement enregistré et géocodé avec succès !';
                  geocodingSuccess = true;
                  geocodingCoordinates = {
                    lat: parseFloat(etablissement.etablissement.latitude),
                    lng: parseFloat(etablissement.etablissement.longitude)
                  };
                } else if (etablissementData.latitude && etablissementData.longitude) {
                  geocodingStatus = '✅ Établissement enregistré avec les coordonnées fournies';
                  geocodingSuccess = true;
                } else {
                  geocodingStatus = '⚠️ Établissement enregistré mais coordonnées non disponibles.';
                }
                
                // Création de l'année scolaire
                const anneeScolaire = await authApi.createAnneeScolaire({
                  ...etablissementData.anneeScolaire,
                  etablissement: etablissement.etablissement.id
                });
                
                // Création des classes
                for (const classe of etablissementData.classes) {
                  const classePayload = {
                    nom: classe.nom,
                    niveau: classe.niveau,
                    section: classe.section || null,
                    etablissement: etablissement.etablissement.id,
                    annee_scolaire_id: anneeScolaire.id,
                  };
                  
                  console.log("Envoi de la classe:", classePayload); 
                  
                  const createdClasse = await authApi.createClasse(classePayload);
                  
                  if (!createdClasse?.id) {
                    console.error("Échec création classe:", createdClasse);
                  }
                }
                
                successMessage = 'Établissement créé avec succès avec ses classes et année scolaire';
                break;
          
            case 'professeur':
                if (professeurData.password !== professeurData.confirmPassword) {
                    throw new Error('Les mots de passe ne correspondent pas');
                }
                formData = getProfesseurFormData(professeurData);
                apiMethod = authApi.registerProfesseur;
                break;

            case 'eleve':
                if (eleveData.password !== eleveData.confirmPassword) {
                    throw new Error('Les mots de passe ne correspondent pas');
                }
                formData = getEleveFormData(eleveData);
                apiMethod = authApi.registerEleve;
                break;

            case 'parent':
                if (parentData.password !== parentData.confirmPassword) {
                    throw new Error('Les mots de passe ne correspondent pas');
                }
                formData = getParentFormData(parentData);
                apiMethod = authApi.registerParent;
                break;
        }

        if (activeTab === 'etablissement') {
          setTimeout(() => {
            window.location.href = '/etablissement/dashboard';
          }, 2000);
        } else {
          window.location.href = '/etablissement/dashboard';
        }
        
    } catch (error) {
        errorMessage = error.message || "Une erreur s'est produite lors de l'inscription";
        geocodingStatus = '❌ Erreur : ' + errorMessage;
    } finally {
        isLoading = false;
    }
  }
</script>

<div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
  <div class="sm:mx-auto sm:w-full sm:max-w-md">
    <a href="/" class="flex justify-center h-12 mx-auto">
      <img src="/icons/favicon.png" class="h-12" alt="Logo">
    </a>
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
              <AddressAutocomplete
                bind:value={etablissementData.adresse}
                label="Adresse de l'établissement"
                placeholder="Ex: 123 Rue de l'Éducation, Antananarivo, Madagascar"
                countryFilter="mg"
                language="fr"
                showMap={true}
                required={true}
                on:select={handleAddressSelect}
                on:geocode={handleGeocode}
                on:clear={() => {
                  addressValid = false;
                  geocodingSuccess = false;
                  geocodingCoordinates = null;
                  etablissementData.latitude = null;
                  etablissementData.longitude = null;
                  geocodingStatus = '';
                }}
              />
              
              <!-- Boutons d'action supplémentaires -->
              <div class="mt-2 flex flex-wrap gap-2">
                <button
                  type="button"
                  on:click={geocodeAddressManually}
                  class="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                >
                  <Icon icon="heroicons:magnifying-glass" class="h-4 w-4 mr-1" />
                  Géocoder manuellement
                </button>
                <button
                  type="button"
                  on:click={useCurrentLocation}
                  class="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                >
                  <Icon icon="heroicons:map-pin" class="h-4 w-4 mr-1" />
                  Ma position
                </button>
                {#if etablissementData.adresse}
                  <button
                    type="button"
                    on:click={openGoogleMaps}
                    class="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                  >
                    <Icon icon="logos:google-maps" class="h-4 w-4 mr-1" />
                    Voir sur Maps
                  </button>
                {/if}
              </div>
              
              <!-- Affichage des coordonnées -->
              {#if geocodingCoordinates}
                <div class="mt-2 p-2 bg-green-50 border border-green-200 rounded-md">
                  <div class="flex items-center justify-between">
                    <div>
                      <span class="text-sm font-medium text-green-700">📍 Coordonnées trouvées</span>
                      <p class="text-xs text-gray-600 mt-0.5">
                        Latitude: {geocodingCoordinates.lat.toFixed(6)} 
                        | Longitude: {geocodingCoordinates.lng.toFixed(6)}
                      </p>
                    </div>
                    <a
                      href={`https://www.openstreetmap.org/?mlat=${geocodingCoordinates.lat}&mlon=${geocodingCoordinates.lng}&zoom=15`}
                      target="_blank"
                      class="text-xs text-blue-500 hover:text-blue-700 underline"
                    >
                      Voir sur OpenStreetMap
                    </a>
                  </div>
                </div>
              {/if}
              
              <!-- Statut du géocodage -->
              {#if geocodingStatus && !geocodingCoordinates}
                <div class="mt-2 p-2 rounded-md text-sm">
                  <span class={`
                    ${geocodingStatus.includes('✅') ? 'text-green-700' : ''}
                    ${geocodingStatus.includes('⚠️') ? 'text-yellow-700' : ''}
                    ${geocodingStatus.includes('❌') || geocodingStatus.includes('Erreur') ? 'text-red-700' : ''}
                    ${geocodingStatus.includes('🔍') || geocodingStatus.includes('📍') || geocodingStatus.includes('🌍') ? 'text-blue-700' : ''}
                  `}>
                    {geocodingStatus}
                  </span>
                </div>
              {/if}
            </div>
          </div>
          
          <!-- Section Année scolaire -->
          <div class="border-t border-gray-200 pt-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Année scolaire</h3>
            <div class="grid grid-cols-1 gap-6 sm:grid-cols-3">
              <div>
                <label for="annee-nom" class="block text-sm font-medium text-gray-700">Nom (ex: 2023-2024)</label>
                <input
                  id="annee-nom"
                  type="text"
                  bind:value={etablissementData.anneeScolaire.nom}
                  required
                  class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                />
              </div>
              
              <div>
                <label for="annee-debut" class="block text-sm font-medium text-gray-700">Date de début</label>
                <input
                  id="annee-debut"
                  type="date"
                  bind:value={etablissementData.anneeScolaire.date_debut}
                  required
                  class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                />
              </div>
              
              <div>
                <label for="annee-fin" class="block text-sm font-medium text-gray-700">Date de fin</label>
                <input
                  id="annee-fin"
                  type="date"
                  bind:value={etablissementData.anneeScolaire.date_fin}
                  required
                  class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                />
              </div>
            </div>
          </div>
          
          <!-- Section Classes -->
          <div class="border-t border-gray-200 pt-6">
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg font-medium text-gray-900">Classes</h3>
              <button
                type="button"
                on:click={addClasse}
                class="inline-flex items-center px-3 py-1 border border-transparent text-sm leading-4 font-medium rounded-md text-green-700 bg-green-100 hover:bg-green-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              >
                <Icon icon="heroicons:plus" class="h-4 w-4 mr-1" />
                Ajouter une classe
              </button>
            </div>
            
            {#each etablissementData.classes as classe, index (index)}
              <div class="grid grid-cols-1 gap-6 sm:grid-cols-3 mb-4 p-4 bg-gray-50 rounded-lg">
                <div>
                  <label for="classe-nom-{index}" class="block text-sm font-medium text-gray-700">Nom de la classe</label>
                  <input
                    id="classe-nom-{index}"
                    type="text"
                    bind:value={classe.nom}
                    required
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                    placeholder="Ex: CE1 A"
                  />
                </div>
                
                <div>
                  <label for="classe-niveau-{index}" class="block text-sm font-medium text-gray-700">Niveau</label>
                  <input
                    id="classe-niveau-{index}"
                    type="text"
                    bind:value={classe.niveau}
                    required
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                    placeholder="Ex: CE1, 6ème, Terminale"
                  />
                </div>
                
                <div class="flex items-end space-x-2">
                  <div class="flex-1">
                    <label for="classe-section-{index}" class="block text-sm font-medium text-gray-700">Section (optionnel)</label>
                    <input
                      id="classe-section-{index}"
                      type="text"
                      bind:value={classe.section}
                      class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                      placeholder="Ex: A, B, S, ES"
                    />
                  </div>
                  
                  {#if etablissementData.classes.length > 1}
                    <button
                      type="button"
                      on:click={() => removeClasse(index)}
                      class="mb-1 p-1 text-red-500 hover:text-red-700 focus:outline-none"
                      title="Supprimer cette classe"
                    >
                      <Icon icon="heroicons:trash" class="h-5 w-5" />
                    </button>
                  {/if}
                </div>
              </div>
            {/each}
          </div>
          
          <!-- Mot de passe -->
          <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
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
          
          {#if successMessage}
            <div class="bg-green-50 border-l-4 border-green-400 p-4">
              <div class="flex">
                <div class="flex-shrink-0">
                  <Icon icon="heroicons:check-circle" class="h-5 w-5 text-green-400" />
                </div>
                <div class="ml-3">
                  <p class="text-sm text-green-700">{successMessage}</p>
                  {#if geocodingCoordinates}
                    <p class="text-xs text-green-600 mt-1">
                      📍 Coordonnées: {geocodingCoordinates.lat.toFixed(6)}, {geocodingCoordinates.lng.toFixed(6)}
                    </p>
                  {/if}
                </div>
              </div>
            </div>
          {/if}
          
          <div>
            <button
              type="submit"
              disabled={isLoading}
              class={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 ${isLoading ? 'opacity-70 cursor-not-allowed' : ''}`}
            >
              {#if isLoading}
                <Icon icon="heroicons:arrow-path" class="animate-spin h-5 w-5 mr-2" />
                Création en cours...
              {:else}
                Créer l'établissement
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