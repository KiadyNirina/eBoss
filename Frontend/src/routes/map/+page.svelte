<!-- src/routes/map/+page.svelte -->
<script>
  import { onMount, tick } from 'svelte';
  import Icon from '@iconify/svelte';
  import { goto } from '$app/navigation';
  import { browser } from '$app/environment';
  import { authApi } from '$lib/api';

  import MapView from '../../components/etablissement/map/MapView.svelte';
  import EstablishmentList from '../../components/etablissement/map/EstablishmentList.svelte';
  import EstablishmentProfilePanel from '../../components/etablissement/map/EstablishmentProfilePanel.svelte';

  let mapView; // référence au composant MapView
  let establishments = [];
  let filteredEstablishments = [];
  let loading = true;
  let selectedEstablishment = null;
  let userLocation = null;
  let locationFound = false;
  let error = null;

  let showProfilePanel = false;
  let selectedProfileId = null;
  let profileData = null;
  let loadingProfile = false;
  let profileError = null;

  let searchQuery = '';
  let filterType = 'all';

  // Fonctions de chargement
  async function loadEstablishments(filters = {}) {
    try {
      loading = true;
      error = null;

      const apiFilters = {
        type: filters.type || filterType,
        search: filters.search || searchQuery,
      };

      if (userLocation) {
        apiFilters.lat = userLocation.lat;
        apiFilters.lng = userLocation.lng;
        apiFilters.radius = 50;
        apiFilters.with_coords = true;
      }

      const data = await authApi.getEtablissements(apiFilters);
      let establishmentsData = data.results || data || [];
      if (data.results) establishmentsData = data.results;

      establishments = establishmentsData.map(est => ({
        id: est.id,
        name: est.nom,
        address: est.adresse,
        lat: parseFloat(est.latitude),
        lng: parseFloat(est.longitude),
        type: est.type_etablissement,
        phone: est.user?.telephone || 'Non disponible',
        email: est.user?.email || 'Non disponible',
        profileImage: est.user?.profile_image ? `${est.user.profile_image}` : null,
        _raw: est
      }));

      if (userLocation) {
        establishments = establishments.map(est => ({
          ...est,
          distance: calculateDistance(userLocation.lat, userLocation.lng, est.lat, est.lng)
        }));
        establishments.sort((a, b) => (a.distance || Infinity) - (b.distance || Infinity));
      }

      filteredEstablishments = establishments;
    } catch (err) {
      console.error('Erreur de chargement des établissements:', err);
      error = err.message || 'Erreur lors du chargement';
      establishments = [];
      filteredEstablishments = [];
    } finally {
      loading = false;
    }
  }

  function calculateDistance(lat1, lng1, lat2, lng2) {
    if (!lat1 || !lng1 || !lat2 || !lng2) return null;
    const R = 6371;
    const dLat = ((lat2 - lat1) * Math.PI) / 180;
    const dLng = ((lng2 - lng1) * Math.PI) / 180;
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos((lat1 * Math.PI) / 180) *
        Math.cos((lat2 * Math.PI) / 180) *
        Math.sin(dLng / 2) *
        Math.sin(dLng / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  }

  async function openProfilePanel(id) {
    selectedProfileId = id;
    showProfilePanel = true;
    loadingProfile = true;
    profileError = null;
    profileData = null;

    try {
      profileData = await authApi.getPublicEtablissement(id);
    } catch (err) {
      profileError = err.message || 'Impossible de charger le profil';
    } finally {
      loadingProfile = false;
    }
  }

  function closeProfilePanel() {
    showProfilePanel = false;
    selectedProfileId = null;
    profileData = null;
    profileError = null;
  }

  function goBack() {
    goto('/');
  }

  // Handlers pour les événements des composants enfants
  function handleSearch(e) {
    searchQuery = e.detail;
    filterEstablishments();
  }

  function handleFilter(e) {
    filterType = e.detail;
    filterEstablishments();
  }

  function handleClear() {
    searchQuery = '';
    filterType = 'all';
    loadEstablishments();
  }

  function handleSelectFromList(e) {
    mapView?.selectEstablishment(e.detail);
  }

  function handleGoToUserLocation() {
    mapView?.goToUserLocation();
  }

  function filterEstablishments() {
    loadEstablishments({ type: filterType, search: searchQuery });
  }

  // Attribution des fonctions globales pour les popups Leaflet
  if (browser) {
    window.openProfilePanel = openProfilePanel;
    window.selectEstablishment = (id) => mapView?.selectEstablishment(id);
    window.goToEstablishment = (id) => mapView?.goToEstablishment(id);
    window.goToUserLocation = () => mapView?.goToUserLocation();
  }

  // Initialisation
  onMount(async () => {
    await loadEstablishments();
    await tick();

    if (browser) {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            userLocation = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };
            locationFound = true;
            setTimeout(() => {
              loadEstablishments({
                lat: userLocation.lat,
                lng: userLocation.lng,
                radius: 50
              });
            }, 200);
          },
          () => {
            console.log('Géolocalisation non disponible ou refusée');
            loadEstablishments();
          },
          { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
        );
      } else {
        loadEstablishments();
      }
    }
  });
</script>

<svelte:head>
  <title>Rechercher des établissements - Carte interactive</title>
</svelte:head>

<div class="flex flex-col-reverse md:flex-row h-screen bg-gray-50 overflow-hidden">
  <!-- Sidebar (Liste) -->
  <div class="w-full md:w-[400px] lg:w-[450px] h-[50vh] md:h-full flex flex-col bg-white shadow-2xl z-20 shrink-0">
    <EstablishmentList
      establishments={filteredEstablishments}
      userLocation={userLocation}
      searchQuery={searchQuery}
      filterType={filterType}
      loading={loading}
      on:search={handleSearch}
      on:filter={handleFilter}
      on:clear={handleClear}
      on:select={handleSelectFromList}
      on:goToUserLocation={handleGoToUserLocation}
      on:back={goBack}
    />
  </div>

  <!-- Zone de la Carte -->
  <div class="flex-1 h-[50vh] md:h-full relative z-10 bg-gray-200 overflow-hidden">
    <MapView
      bind:this={mapView}
      establishments={filteredEstablishments}
      userLocation={userLocation}
    />

    {#if loading}
      <div class="absolute inset-0 flex flex-col items-center justify-center bg-white/90 backdrop-blur-sm z-10">
        <div class="relative">
          <div class="animate-spin rounded-full h-14 w-14 border-4 border-gray-100 border-t-[#20784d]"></div>
          <Icon icon="heroicons:map" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 h-5 w-5 text-[#20784d]" />
        </div>
        <p class="mt-4 font-medium text-gray-500 animate-pulse">Initialisation de la carte...</p>
      </div>
    {/if}
  </div>

  <!-- Panneau Profil -->
  <EstablishmentProfilePanel
    show={showProfilePanel}
    profileData={profileData}
    loading={loadingProfile}
    error={profileError}
    on:close={closeProfilePanel}
  />
</div>