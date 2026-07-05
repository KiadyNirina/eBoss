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
  import { 
    validateAndFormatCoordinates, 
    formatCoordinatesDisplay,
    isValidCoordinates,
    cleanCoordinateString,
    formatCoordinate 
  } from '$lib/geocoding-helpers.js';
  
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
  
  // Variables pour le géocodage manuel
  let showManualGeocode = false;
  let manualLatitude = '';
  let manualLongitude = '';
  let manualGeocodeError = '';
  
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

    const formattedLat = formatCoordinate(latitude, 'lat');
    const formattedLng = formatCoordinate(longitude, 'lng');
    
    etablissementData.adresse = address;
    etablissementData.latitude = formattedLat;
    etablissementData.longitude = formattedLng;
    addressValid = true;
    geocodingSuccess = true;
    geocodingCoordinates = { lat: formattedLat, lng: formattedLng };
    geocodingStatus = `✅ Adresse géocodée: ${formatCoordinatesDisplay(formattedLat, formattedLng)}`;
    
    // Fermer le géocodage manuel si ouvert
    showManualGeocode = false;
    
    console.log('Adresse sélectionnée:', {
      address,
      latitude: formattedLat,
      longitude: formattedLng,
      fullData
    });
  }

  // Gestionnaire de géocodage automatique
  function handleGeocode(event) {
    const { latitude, longitude, address } = event.detail;

    const formattedLat = formatCoordinate(latitude, 'lat');
    const formattedLng = formatCoordinate(longitude, 'lng');
    
    etablissementData.latitude = formattedLat;
    etablissementData.longitude = formattedLng;
    if (address) {
      etablissementData.adresse = address;
    }
    addressValid = true;
    geocodingSuccess = true;
    geocodingCoordinates = { lat: formattedLat, lng: formattedLng };
    geocodingStatus = `✅ Coordonnées trouvées: ${formatCoordinatesDisplay(formattedLat, formattedLng)}`;
    
    // Fermer le géocodage manuel si ouvert
    showManualGeocode = false;
  }

  // Fonction pour ouvrir le géocodage manuel
  function openManualGeocode() {
    showManualGeocode = !showManualGeocode;
    if (showManualGeocode) {
      // Pré-remplir avec les coordonnées existantes si disponibles
      if (etablissementData.latitude) {
        manualLatitude = etablissementData.latitude.toString();
      }
      if (etablissementData.longitude) {
        manualLongitude = etablissementData.longitude.toString();
      }
      manualGeocodeError = '';
    }
  }

  // Fonction pour appliquer les coordonnées manuelles
  function applyManualCoordinates() {
    // Nettoyer les entrées
    const lat = cleanCoordinateString(manualLatitude);
    const lng = cleanCoordinateString(manualLongitude);
    
    // Valider et formater les coordonnées
    const result = validateAndFormatCoordinates(lat, lng);
    
    if (!result.valid) {
      manualGeocodeError = result.errors.join('. ');
      return;
    }
    
    // Appliquer les coordonnées formatées
    etablissementData.latitude = result.lat;
    etablissementData.longitude = result.lng;
    addressValid = true;
    geocodingSuccess = true;
    geocodingCoordinates = { lat: result.lat, lng: result.lng };
    geocodingStatus = `✅ Coordonnées saisies manuellement: ${formatCoordinatesDisplay(result.lat, result.lng)}`;
    manualGeocodeError = '';
    showManualGeocode = false;
    
    // if (!etablissementData.adresse) {
    //   etablissementData.adresse = `Coordonnées: ${formatCoordinatesDisplay(result.lat, result.lng)}`;
    // }
  }

  // Fonction pour ouvrir Google Maps avec un guide
  function openGoogleMapsGuide() {
    // Ouvrir Google Maps dans un nouvel onglet
    const url = 'https://www.google.com/maps';
    window.open(url, '_blank');
    
    // Afficher un message d'aide
    alert(
      '📌 Comment obtenir les coordonnées depuis Google Maps :\n\n' +
      '1. Ouvrez Google Maps\n' +
      '2. Recherchez votre adresse ou faites un clic droit sur le lieu souhaité\n' +
      '3. Cliquez sur les coordonnées affichées (Ex : -18.91249177910885, 47.53230029147827)\n' +
      '5. Copiez la latitude et la longitude dans les champs ci-dessous\n\n' +
      'Exemple de format :\n' +
      'Latitude: -18.8792\n' +
      'Longitude: 47.5079'
    );
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
      const result = await geocodingCache.geocode(etablissementData.adresse);
      
      if (result) {
        // Formater les coordonnées reçues
        const formattedLat = formatCoordinate(result.latitude, 'lat');
        const formattedLng = formatCoordinate(result.longitude, 'lng');

        etablissementData.latitude = formattedLat;
        etablissementData.longitude = formattedLng;
        addressValid = true;
        geocodingSuccess = true;
        geocodingCoordinates = {
          lat: formattedLat,
          lng: formattedLng
        };
        geocodingStatus = `✅ Coordonnées trouvées: ${formatCoordinatesDisplay(formattedLat, formattedLng)}`;
        
        if (result.display_name) {
          etablissementData.adresse = result.display_name;
        }
        
        // Fermer le géocodage manuel si ouvert
        showManualGeocode = false;
      } else {
        geocodingStatus = '❌ Adresse non trouvée. Vérifiez l\'adresse saisie ou Geocoder manuellement.'
        etablissementData.latitude = null;
        etablissementData.longitude = null;
        addressValid = false;
      }
    } catch (error) {
      geocodingStatus = `❌ Erreur de géocodage: ${error.message}`;
      console.error('Erreur de géocodage:', error);
    }
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
            // Formater les coordonnées
            const formattedLat = formatCoordinate(latitude, 'lat');
            const formattedLng = formatCoordinate(longitude, 'lng');

            etablissementData.adresse = result.display_name;
            etablissementData.latitude = formattedLat;
            etablissementData.longitude = formattedLng;
            addressValid = true;
            geocodingSuccess = true;
            geocodingCoordinates = { lat: formattedLat, lng: formattedLng };
            geocodingStatus = `✅ Position trouvée: ${formatCoordinatesDisplay(formattedLat, formattedLng)}`;
            showManualGeocode = false;
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

                if (etablissementData.latitude !== null && etablissementData.longitude !== null) {
                  const result = validateAndFormatCoordinates(
                    etablissementData.latitude,
                    etablissementData.longitude
                  );
                  
                  if (!result.valid) {
                    throw new Error(`Coordonnées invalides: ${result.errors.join('. ')}`);
                  }
                  
                  // Mettre à jour avec les coordonnées formatées
                  etablissementData.latitude = result.lat;
                  etablissementData.longitude = result.lng;
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
                  showManualGeocode = false;
                }}
              />
              
              <!-- Boutons d'action supplémentaires -->
              <div class="mt-2 flex flex-wrap gap-2">
                <button
                  type="button"
                  on:click={openManualGeocode}
                  class="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                >
                  <Icon icon="heroicons:adjustments-horizontal" class="h-4 w-4 mr-1" />
                  {showManualGeocode ? 'Fermer le géocodage manuel' : 'Géocodage manuel'}
                </button>
                <button
                  type="button"
                  on:click={geocodeAddressManually}
                  class="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                >
                  <Icon icon="heroicons:magnifying-glass" class="h-4 w-4 mr-1" />
                  Géocoder automatiquement
                </button>
                <button
                  type="button"
                  on:click={useCurrentLocation}
                  class="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                >
                  <Icon icon="heroicons:map-pin" class="h-4 w-4 mr-1" />
                  Ma position
                </button>
              </div>

              <!-- Section Géocodage Manuel -->
              {#if showManualGeocode}
                <div class="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <div class="flex items-start justify-between mb-3">
                    <div>
                      <h4 class="font-medium text-blue-800 flex items-center gap-2">
                        <Icon icon="heroicons:map" class="h-5 w-5" />
                        Saisie manuelle des coordonnées
                      </h4>
                      <p class="text-sm text-blue-600 mt-1">
                        Vous pouvez saisir directement les coordonnées GPS de l'établissement.
                      </p>
                    </div>
                    <button
                      type="button"
                      on:click={openGoogleMapsGuide}
                      class="inline-flex items-center px-3 py-1.5 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      <Icon icon="logos:google-maps" class="h-4 w-4 mr-1" />
                      Guide Google Maps
                    </button>
                  </div>

                  {#if manualGeocodeError}
                    <div class="mb-3 p-2 bg-red-50 border border-red-200 rounded text-red-700 text-sm">
                      {manualGeocodeError}
                    </div>
                  {/if}

                  <div class="grid grid-cols-2 gap-3">
                    <div>
                      <label class="block text-sm font-medium text-gray-700">Latitude</label>
                      <input
                        type="text"
                        bind:value={manualLatitude}
                        placeholder="Ex: -18.8792"
                        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                      />
                    </div>
                    <div>
                      <label class="block text-sm font-medium text-gray-700">Longitude</label>
                      <input
                        type="text"
                        bind:value={manualLongitude}
                        placeholder="Ex: 47.5079"
                        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                      />
                    </div>
                  </div>

                  <div class="mt-3 flex gap-2">
                    <button
                      type="button"
                      on:click={applyManualCoordinates}
                      class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm font-medium"
                    >
                      <Icon icon="heroicons:check" class="h-4 w-4 inline mr-1" />
                      Appliquer les coordonnées
                    </button>
                    <button
                      type="button"
                      on:click={() => {
                        showManualGeocode = false;
                        manualGeocodeError = '';
                      }}
                      class="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition-colors text-sm font-medium"
                    >
                      Annuler
                    </button>
                  </div>

                  <div class="mt-3 p-2 bg-blue-100 rounded text-xs text-blue-700">
                    <p class="font-medium">💡 Astuce :</p>
                    <p>Vous pouvez obtenir les coordonnées en cliquant sur le bouton "Guide Google Maps" ci-dessus.</p>
                  </div>
                </div>
              {/if}
              
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
                    <div class="flex gap-2">
                      <a
                        href={`https://www.openstreetmap.org/?mlat=${geocodingCoordinates.lat}&mlon=${geocodingCoordinates.lng}&zoom=15`}
                        target="_blank"
                        class="text-xs text-blue-500 hover:text-blue-700 underline"
                      >
                        Voir sur OpenStreetMap
                      </a>
                      <a
                        href={`https://www.google.com/maps?q=${geocodingCoordinates.lat},${geocodingCoordinates.lng}`}
                        target="_blank"
                        class="text-xs text-blue-500 hover:text-blue-700 underline"
                      >
                        Voir sur Google Maps
                      </a>
                    </div>
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
        <!-- ... (reste du code inchangé) ... -->
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