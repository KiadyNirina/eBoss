<!-- src/lib/components/register/EtablissementForm.svelte -->
<script>
  import Icon from '@iconify/svelte';
  import { createEventDispatcher } from 'svelte';
  import { authApi } from '$lib/api';
  import { getEtablissementFormData } from '$lib/formData';
  import AddressAutocomplete from '$lib/components/AddressAutocomplete.svelte';
  import geocodingCache from '$lib/geocoding-cache.js';
  import {
    validateAndFormatCoordinates,
    formatCoordinatesDisplay,
    cleanCoordinateString,
    formatCoordinate
  } from '$lib/geocoding-helpers.js';
  import GoogleMapsGuidePopup from './GoogleMapsGuidePopup.svelte';

  const dispatch = createEventDispatcher();

  let isLoading = false;
  let errorMessage = '';
  let successMessage = '';

  let geocodingStatus = '';
  let geocodingSuccess = false;
  let geocodingCoordinates = null;
  let addressValid = false;

  let showManualGeocode = false;
  let manualLatitude = '';
  let manualLongitude = '';
  let manualGeocodeError = '';

  let showGoogleMapsPopup = false;

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
    anneeScolaire: { nom: '', date_debut: '', date_fin: '' },
    classes: [{ nom: '', niveau: '', section: '' }]
  };

  let lastTypeEtab = '';

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

  $: if (
    etablissementData.typeEtablissement &&
    etablissementData.typeEtablissement !== lastTypeEtab
  ) {
    lastTypeEtab = etablissementData.typeEtablissement;
    setDefaultClasses(etablissementData.typeEtablissement);
  }

  function addClasse() {
    etablissementData = {
      ...etablissementData,
      classes: [...(etablissementData.classes || []), { nom: '', niveau: '', section: '' }]
    };
  }

  function removeClasse(index) {
    etablissementData = {
      ...etablissementData,
      classes: etablissementData.classes.filter((_, i) => i !== index)
    };
  }

  function handleAddressSelect(event) {
    const { address, latitude, longitude } = event.detail;
    const formattedLat = formatCoordinate(latitude, 'lat');
    const formattedLng = formatCoordinate(longitude, 'lng');
    etablissementData.adresse = address;
    etablissementData.latitude = formattedLat;
    etablissementData.longitude = formattedLng;
    addressValid = true;
    geocodingSuccess = true;
    geocodingCoordinates = { lat: formattedLat, lng: formattedLng };
    geocodingStatus = `✅ Adresse géocodée: ${formatCoordinatesDisplay(formattedLat, formattedLng)}`;
    showManualGeocode = false;
  }

  function handleGeocode(event) {
    const { latitude, longitude, address } = event.detail;
    const formattedLat = formatCoordinate(latitude, 'lat');
    const formattedLng = formatCoordinate(longitude, 'lng');
    etablissementData.latitude = formattedLat;
    etablissementData.longitude = formattedLng;
    if (address) etablissementData.adresse = address;
    addressValid = true;
    geocodingSuccess = true;
    geocodingCoordinates = { lat: formattedLat, lng: formattedLng };
    geocodingStatus = `✅ Coordonnées trouvées: ${formatCoordinatesDisplay(formattedLat, formattedLng)}`;
    showManualGeocode = false;
  }

  function handleClearAddress() {
    addressValid = false;
    geocodingSuccess = false;
    geocodingCoordinates = null;
    etablissementData.latitude = null;
    etablissementData.longitude = null;
    geocodingStatus = '';
    showManualGeocode = false;
    manualLatitude = '';
    manualLongitude = '';
    manualGeocodeError = '';
  }

  function openManualGeocode() {
    showManualGeocode = !showManualGeocode;
    if (showManualGeocode) {
      if (etablissementData.latitude) manualLatitude = etablissementData.latitude.toString();
      if (etablissementData.longitude) manualLongitude = etablissementData.longitude.toString();
      manualGeocodeError = '';
    }
  }

  function applyManualCoordinates() {
    const lat = cleanCoordinateString(manualLatitude);
    const lng = cleanCoordinateString(manualLongitude);
    const result = validateAndFormatCoordinates(lat, lng);
    if (!result.valid) {
      manualGeocodeError = result.errors.join('. ');
      return;
    }
    etablissementData.latitude = result.lat;
    etablissementData.longitude = result.lng;
    addressValid = true;
    geocodingSuccess = true;
    geocodingCoordinates = { lat: result.lat, lng: result.lng };
    geocodingStatus = `✅ Coordonnées saisies manuellement: ${formatCoordinatesDisplay(result.lat, result.lng)}`;
    manualGeocodeError = '';
    showManualGeocode = false;
  }

  async function geocodeAddressManually() {
    if (addressValid && geocodingCoordinates) {
      geocodingStatus = 'ℹ️ Cette adresse est déjà géocodée.';
      geocodingSuccess = true;
      return;
    }
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
        const formattedLat = formatCoordinate(result.latitude, 'lat');
        const formattedLng = formatCoordinate(result.longitude, 'lng');
        etablissementData.latitude = formattedLat;
        etablissementData.longitude = formattedLng;
        addressValid = true;
        geocodingSuccess = true;
        geocodingCoordinates = { lat: formattedLat, lng: formattedLng };
        geocodingStatus = `✅ Coordonnées trouvées: ${formatCoordinatesDisplay(formattedLat, formattedLng)}`;
        if (result.display_name) etablissementData.adresse = result.display_name;
        showManualGeocode = false;
      } else {
        geocodingStatus = '❌ Adresse non trouvée. Vérifiez l\'adresse saisie ou Geocoder manuellement.';
        etablissementData.latitude = null;
        etablissementData.longitude = null;
        addressValid = false;
      }
    } catch (error) {
      geocodingStatus = `❌ Erreur de géocodage: ${error.message}`;
    }
  }

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
          const result = await geocodingCache.reverseGeocode(latitude, longitude);
          if (result) {
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
        }
      },
      () => {
        geocodingStatus = '❌ Impossible d\'obtenir votre position. Vérifiez les permissions.';
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
      if (etablissementData.password !== etablissementData.confirmPassword) {
        throw new Error('Les mots de passe ne correspondent pas');
      }

      if (etablissementData.latitude !== null && etablissementData.longitude !== null) {
        const result = validateAndFormatCoordinates(
          etablissementData.latitude,
          etablissementData.longitude
        );
        if (!result.valid) {
          throw new Error(`Coordonnées invalides: ${result.errors.join('. ')}`);
        }
        etablissementData.latitude = result.lat;
        etablissementData.longitude = result.lng;
      }

      if (!addressValid && etablissementData.adresse) {
        geocodingStatus = '🌍 Géocodage de l\'adresse...';
        try {
          const result = await geocodingCache.geocode(etablissementData.adresse);
          if (result) {
            etablissementData.latitude = result.latitude;
            etablissementData.longitude = result.longitude;
            addressValid = true;
            geocodingSuccess = true;
            geocodingCoordinates = { lat: result.latitude, lng: result.longitude };
          } else {
            throw new Error('Adresse non trouvée');
          }
        } catch (error) {
          throw new Error(`Erreur de géocodage: ${error.message}`);
        }
      }

      geocodingStatus = '🌍 Enregistrement de l\'établissement...';

      const etablissementFormData = getEtablissementFormData(etablissementData);
      if (!etablissementFormData.latitude && etablissementData.latitude) {
        etablissementFormData.latitude = etablissementData.latitude;
        etablissementFormData.longitude = etablissementData.longitude;
      }

      const etablissement = await authApi.registerEtablissement(etablissementFormData);

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

      // Année scolaire : OPTIONNEL
      const hasAnneeScolaire =
        etablissementData.anneeScolaire.nom ||
        etablissementData.anneeScolaire.date_debut ||
        etablissementData.anneeScolaire.date_fin;

      if (hasAnneeScolaire) {
        if (
          !etablissementData.anneeScolaire.nom ||
          !etablissementData.anneeScolaire.date_debut ||
          !etablissementData.anneeScolaire.date_fin
        ) {
          throw new Error('Veuillez remplir tous les champs de l\'année scolaire ou laisser vide');
        }

        const anneeScolaire = await authApi.createAnneeScolaire({
          ...etablissementData.anneeScolaire,
          etablissement: etablissement.etablissement.id
        });

        const classesValides = etablissementData.classes.filter((c) => c.nom && c.niveau);

        if (classesValides.length > 0) {
          for (const classe of classesValides) {
            const classePayload = {
              nom: classe.nom,
              niveau: classe.niveau,
              section: classe.section || null,
              etablissement: etablissement.etablissement.id,
              annee_scolaire_id: anneeScolaire.id
            };
            const createdClasse = await authApi.createClasse(classePayload);
            if (!createdClasse?.id) {
              console.error('Échec création classe:', createdClasse);
            }
          }
        }
      }

      successMessage = 'Établissement créé avec succès';
      setTimeout(() => dispatch('success'), 2000);
    } catch (error) {
      errorMessage = error.message || "Une erreur s'est produite lors de l'inscription";
      geocodingStatus = '❌ Erreur : ' + errorMessage;
    } finally {
      isLoading = false;
    }
  }
</script>

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

<form class="space-y-6" on:submit|preventDefault={handleSubmit}>
  <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
    <div>
      <label for="etab-nom" class="block text-sm font-medium text-gray-700">Nom de l'établissement</label>
      <input
        id="etab-nom"
        type="text"
        bind:value={etablissementData.nom}
        required
        class="mt-1 block w-full border border-gray-300 rounded-full py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
      />
    </div>

    <div>
      <label for="etab-type" class="block text-sm font-medium text-gray-700">Type d'établissement</label>
      <select
        id="etab-type"
        bind:value={etablissementData.typeEtablissement}
        required
        class="mt-1 block w-full border border-gray-300 rounded-full py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
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
        class="mt-1 block w-full border border-gray-300 rounded-full py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
      />
    </div>

    <div>
      <label for="etab-telephone" class="block text-sm font-medium text-gray-700">Téléphone</label>
      <input
        id="etab-telephone"
        type="tel"
        bind:value={etablissementData.telephone}
        required
        class="mt-1 block w-full border border-gray-300 rounded-full py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
      />
    </div>

    <div class="sm:col-span-2">
      <div class="flex gap-1 items-start">
        <div class="flex-1">
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
            on:clear={handleClearAddress}
          />
        </div>
        <div class="mt-6">
          <button
            type="button"
            on:click={useCurrentLocation}
            class="inline-flex items-center px-4 py-2.5 border border-gray-300 rounded-full text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors"
            title="Utiliser ma position"
          >
            <Icon icon="heroicons:map-pin" class="h-5 w-5 mr-1.5" />
            <span class="hidden sm:inline">Ma position</span>
            <span class="sm:hidden">Position</span>
          </button>
        </div>
      </div>

      {#if geocodingCoordinates}
        <div class="mt-2 p-2 bg-green-50 border border-green-200 rounded-3xl">
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

      {#if geocodingStatus}
        <div class="mt-2 p-2 rounded-md text-sm">
          <span class={`
            ${geocodingStatus.includes('✅') ? 'text-green-700' : ''}
            ${geocodingStatus.includes('⚠️') ? 'text-yellow-700' : ''}
            ${geocodingStatus.includes('❌') || geocodingStatus.includes('Erreur') ? 'text-red-700' : ''}
            ${geocodingStatus.includes('🔍') || geocodingStatus.includes('📍') || geocodingStatus.includes('🌍') ? 'text-blue-700' : ''}
            ${geocodingStatus.includes('ℹ️') ? 'text-blue-600' : ''}
          `}>
            {geocodingStatus}
          </span>
        </div>
      {/if}

      <div class="mt-2 flex flex-wrap gap-2">
        <button
          type="button"
          on:click={geocodeAddressManually}
          class="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-full text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        >
          <Icon icon="heroicons:magnifying-glass" class="h-4 w-4 mr-1" />
          Géocodage automatique
        </button>
        <button
          type="button"
          on:click={openManualGeocode}
          class="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-full text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        >
          <Icon icon="heroicons:adjustments-horizontal" class="h-4 w-4 mr-1" />
          {showManualGeocode ? 'Fermer le géocodage manuel' : 'Géocodage manuel'}
        </button>
      </div>

      {#if showManualGeocode}
        <div class="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-4xl">
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
              on:click={() => showGoogleMapsPopup = true}
              class="inline-flex items-center px-3 py-1.5 bg-blue-600 text-white text-sm rounded-full hover:bg-blue-700 transition-colors"
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
                class="mt-1 block w-full border border-gray-300 rounded-full py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Longitude</label>
              <input
                type="text"
                bind:value={manualLongitude}
                placeholder="Ex: 47.5079"
                class="mt-1 block w-full border border-gray-300 rounded-full py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
            </div>
          </div>

          <div class="mt-3 flex gap-2">
            <button
              type="button"
              on:click={applyManualCoordinates}
              class="px-4 py-2 bg-green-600 text-white rounded-full hover:bg-green-700 transition-colors text-sm font-medium"
            >
              <Icon icon="heroicons:check" class="h-4 w-4 inline mr-1" />
              Appliquer les coordonnées
            </button>
            <button
              type="button"
              on:click={() => { showManualGeocode = false; manualGeocodeError = ''; }}
              class="px-4 py-2 bg-gray-300 text-gray-700 rounded-full hover:bg-gray-400 transition-colors text-sm font-medium"
            >
              Annuler
            </button>
          </div>

          <div class="mt-3 p-2 bg-blue-100 rounded-3xl text-xs text-blue-700">
            <p class="font-medium">💡 Astuce :</p>
            <p>Vous pouvez obtenir les coordonnées en cliquant sur le bouton "Guide Google Maps" ci-dessus.</p>
          </div>
        </div>
      {/if}
    </div>
  </div>

  <!-- Section Année scolaire (OPTIONNEL) -->
  <div class="border-t border-gray-200 pt-6">
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-medium text-gray-900">Année scolaire</h3>
      <span class="text-xs text-gray-500 bg-gray-100 px-3 py-1 rounded-full">Optionnel</span>
    </div>
    <p class="text-sm text-gray-500 mb-4">
      Vous pourrez configurer l'année scolaire plus tard depuis votre tableau de bord.
    </p>
    <div class="grid grid-cols-1 gap-6 sm:grid-cols-3">
      <div>
        <label for="annee-nom" class="block text-sm font-medium text-gray-700">Nom (ex: 2023-2024)</label>
        <input
          id="annee-nom"
          type="text"
          bind:value={etablissementData.anneeScolaire.nom}
          class="mt-1 block w-full border border-gray-300 rounded-full py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
        />
      </div>
      <div>
        <label for="annee-debut" class="block text-sm font-medium text-gray-700">Date de début</label>
        <input
          id="annee-debut"
          type="date"
          bind:value={etablissementData.anneeScolaire.date_debut}
          class="mt-1 block w-full border border-gray-300 rounded-full py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
        />
      </div>
      <div>
        <label for="annee-fin" class="block text-sm font-medium text-gray-700">Date de fin</label>
        <input
          id="annee-fin"
          type="date"
          bind:value={etablissementData.anneeScolaire.date_fin}
          class="mt-1 block w-full border border-gray-300 rounded-full py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
        />
      </div>
    </div>
  </div>

  <!-- Section Classes (OPTIONNEL) -->
  <div class="border-t border-gray-200 pt-6">
    <div class="flex justify-between items-center mb-4">
      <div class="flex items-center gap-3">
        <h3 class="text-lg font-medium text-gray-900">Classes</h3>
        <span class="text-xs text-gray-500 bg-gray-100 px-3 py-1 rounded-full">Optionnel</span>
      </div>
      <button
        type="button"
        on:click={addClasse}
        class="inline-flex items-center px-3 py-1 border border-transparent text-sm leading-4 font-medium rounded-full text-green-700 bg-green-100 hover:bg-green-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
      >
        <Icon icon="heroicons:plus" class="h-4 w-4 mr-1" />
        Ajouter une classe
      </button>
    </div>
    <p class="text-sm text-gray-500 mb-4">
      Vous pourrez ajouter des classes plus tard depuis votre tableau de bord.
    </p>

    {#each etablissementData.classes as classe, index (index)}
      <div class="grid grid-cols-1 gap-6 sm:grid-cols-3 mb-4 p-4 bg-gray-50 rounded-2xl">
        <div>
          <label for="classe-nom-{index}" class="block text-sm font-medium text-gray-700">Nom de la classe</label>
          <input
            id="classe-nom-{index}"
            type="text"
            bind:value={classe.nom}
            class="mt-1 block w-full border border-gray-300 rounded-full py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
            placeholder="Ex: CE1 A"
          />
        </div>
        <div>
          <label for="classe-niveau-{index}" class="block text-sm font-medium text-gray-700">Niveau</label>
          <input
            id="classe-niveau-{index}"
            type="text"
            bind:value={classe.niveau}
            class="mt-1 block w-full border border-gray-300 rounded-full py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
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
              class="mt-1 block w-full border border-gray-300 rounded-full py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
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
        class="mt-1 block w-full border border-gray-300 rounded-full py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
      />
    </div>
    <div>
      <label for="etab-confirm-password" class="block text-sm font-medium text-gray-700">Confirmer le mot de passe</label>
      <input
        id="etab-confirm-password"
        type="password"
        bind:value={etablissementData.confirmPassword}
        required
        class="mt-1 block w-full border border-gray-300 rounded-full py-2 px-3 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
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
      class={`w-full flex justify-center py-2 px-4 border border-transparent rounded-full text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 ${isLoading ? 'opacity-70 cursor-not-allowed' : ''}`}
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

<GoogleMapsGuidePopup bind:show={showGoogleMapsPopup} />