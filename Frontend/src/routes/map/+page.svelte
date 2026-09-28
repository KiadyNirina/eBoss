<!-- src/routes/map/+page.svelte -->
<script>
  import { onMount, tick } from 'svelte';
  import Icon from '@iconify/svelte';
  import { goto } from '$app/navigation';
  import { browser } from '$app/environment';
  import { authApi } from '$lib/api';
  import { distanceMeters, isDuplicate } from '$lib/utils/schools.js';

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
  let sourceFilter = 'all';
  let selectedId = null;
  let distanceFilter = 0;

  let loadingGoogle = false;

  const GOOGLE_CACHE_KEY = 'eboss_google_schools_cache';
  const GOOGLE_CACHE_TTL_MS = 24 * 60 * 60 * 1000; // 24 heures
  const GOOGLE_CACHE_RADIUS = 3000; // rayon utilisé pour la clé de cache

  // ---------------------------------------------------------------
  // 1. Chargement silencieux des écoles INSCRITES (ton API)
  // ---------------------------------------------------------------
  async function fetchRegistered(filters = {}) {
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
    let list = data.results || data || [];
    if (data.results) list = data.results;

    return list.map(est => ({
      id: est.id,
      name: est.nom,
      address: est.adresse,
      lat: parseFloat(est.latitude),
      lng: parseFloat(est.longitude),
      type: est.type_etablissement,
      phone: est.user?.telephone || 'Non disponible',
      email: est.user?.email || 'Non disponible',
      profileImage: est.user?.profile_image ? `${est.user.profile_image}` : null,
      source: 'registered',
      _raw: est,
    }));
  }

  // ---------------------------------------------------------------
  // Cache local pour les résultats Google Places (24h)
  // ---------------------------------------------------------------
  function getCacheKey(lat, lng, radius) {
    // Arrondi ~500m pour regrouper les positions proches
    const roundedLat = Math.round(lat * 200) / 200;
    const roundedLng = Math.round(lng * 200) / 200;
    return `${roundedLat.toFixed(3)}_${roundedLng.toFixed(3)}_${radius}`;
  }

  function readGoogleCache(lat, lng, radius) {
    if (!browser) return null;
    try {
      const raw = localStorage.getItem(GOOGLE_CACHE_KEY);
      if (!raw) return null;
      const store = JSON.parse(raw);
      const key = getCacheKey(lat, lng, radius);
      const entry = store[key];
      if (!entry) return null;
      if (Date.now() - entry.timestamp > GOOGLE_CACHE_TTL_MS) {
        // Expiré → on nettoie
        delete store[key];
        localStorage.setItem(GOOGLE_CACHE_KEY, JSON.stringify(store));
        return null;
      }
      return entry.data;
    } catch (e) {
      console.warn('Erreur lecture cache Google:', e);
      return null;
    }
  }

  function writeGoogleCache(lat, lng, radius, data) {
    if (!browser) return;
    try {
      const raw = localStorage.getItem(GOOGLE_CACHE_KEY);
      const store = raw ? JSON.parse(raw) : {};
      const key = getCacheKey(lat, lng, radius);
      store[key] = {
        timestamp: Date.now(),
        data,
      };

      // Nettoyage : on supprime les entrées expirées
      const now = Date.now();
      for (const k in store) {
        if (now - store[k].timestamp > GOOGLE_CACHE_TTL_MS) {
          delete store[k];
        }
      }

      // Limite à 20 entrées max (FIFO)
      const keys = Object.keys(store);
      if (keys.length > 20) {
        keys.sort((a, b) => store[a].timestamp - store[b].timestamp);
        const toDelete = keys.slice(0, keys.length - 20);
        for (const k of toDelete) delete store[k];
      }

      localStorage.setItem(GOOGLE_CACHE_KEY, JSON.stringify(store));
    } catch (e) {
      console.warn('Erreur écriture cache Google:', e);
    }
  }

  // ---------------------------------------------------------------
  // 2. Chargement des écoles GOOGLE PLACES (via ton proxy Django)
  // ---------------------------------------------------------------
  async function loadGoogleSchools() {
    try {
      const base = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      const res = await fetch(`${base}/school/api/nearby/`);
      if (!res.ok) return [];
      const data = await res.json();
      return data.results || [];
    } catch (e) {
      console.warn('OSM indisponible:', e);
      return [];
    }
  }

  function clearGoogleCache() {
    if (!browser) return;
    try {
      localStorage.removeItem(GOOGLE_CACHE_KEY);
      console.log('🗑️ Cache Google vidé');
    } catch (e) {}
  }

  // ---------------------------------------------------------------
  // 3. Fusion des deux sources + dédoublonnage
  // ---------------------------------------------------------------
  async function loadAllEstablishments(filters = {}) {
    loading = true;
    loadingGoogle = false;
    error = null;
    try {
      // 3.1 — Écoles inscrites
      const registered = await fetchRegistered(filters);
      // Dès que les inscrites sont là, on peut arrêter le "loading" global
      establishments = registered;
      filteredEstablishments = registered;
      loading = false;

      // 3.2 — Écoles Google (uniquement si on a la position)
      let googleSchools = [];
      loadingGoogle = true;
      const raw = await loadGoogleSchools();
      if (userLocation) {
        googleSchools = raw
          .filter(g => !isDuplicate(g, registered))
          .map(g => ({
            ...g,
            phone: 'Non disponible',
            email: 'Non disponible',
            profileImage: null,
            type: g.type || 'school',
            distance:
              distanceMeters(userLocation.lat, userLocation.lng, g.lat, g.lng) /
              1000,
          }));
      }
      loadingGoogle = false;

      // 3.3 — Fusion + tri par distance
      const all = [...registered, ...googleSchools];

      // Calcul de distance pour les inscrits s'il manque
      if (userLocation) {
        for (const e of all) {
          if (e.distance == null && e.lat && e.lng) {
            e.distance =
              distanceMeters(userLocation.lat, userLocation.lng, e.lat, e.lng) /
              1000;
          }
        }
      }

      all.sort((a, b) => (a.distance ?? Infinity) - (b.distance ?? Infinity));

      establishments = all;
      applySourceFilter();
    } catch (err) {
      console.error('Erreur de chargement des établissements:', err);
      error = err.message || 'Erreur lors du chargement';
      establishments = [];
      filteredEstablishments = [];
    } finally {
      loading = false;
      loadingGoogle = false;
    }
  }

  // ---------------------------------------------------------------
  // 4. Utilitaires
  // ---------------------------------------------------------------
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

  // ---------------------------------------------------------------
  // 5. Panneau profil (uniquement pour les inscrits)
  // ---------------------------------------------------------------
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

  // ---------------------------------------------------------------
  // 6. Handlers
  // ---------------------------------------------------------------
  function handleSearch(e) {
    searchQuery = e.detail;
    applySourceFilter();
  }

  function handleFilter(e) {
    filterType = e.detail;
    applySourceFilter();
  }

  function handleFilterSource(e) {
    sourceFilter = e.detail;
    applySourceFilter();
  }

  function handleFilterDistance(e) {
    distanceFilter = Number(e.detail) || 0;
    applySourceFilter();
  }

  function applySourceFilter() {
    let result = establishments;

    // 1. Filtre par source
    if (sourceFilter !== 'all') {
      result = result.filter(e => e.source === sourceFilter);
    }

    // 2. Filtre par distance
    if (distanceFilter > 0) {
      const maxKm = distanceFilter / 1000;
      result = result.filter(e => e.distance != null && e.distance <= maxKm);
    }

    // 3. Filtre par TYPE (mapping inscrit ↔ OSM)
    if (filterType !== 'all') {
      result = result.filter(e => {
        if (e.source === 'osm') {
          // Les OSM utilisent les tags OSM standards
          const osmType = (e.type || '').toLowerCase();
          const mapping = {
            'ecole': ['school', 'primary_school', 'kindergarten'],
            'college': ['college', 'secondary_school'],
            'lycee': ['school', 'secondary_school'],  // pas de tag lycée dédié dans OSM
            'universite': ['university', 'college'],
          };
          return (mapping[filterType] || []).includes(osmType);
        }
        // Pour les inscrits, comparaison directe
        return e.type === filterType;
      });
    }

    // 4. Filtre par texte (nom + adresse)
    if (searchQuery && searchQuery.trim().length > 0) {
      const q = searchQuery.trim().toLowerCase();
      result = result.filter(e => {
        const name = (e.name || '').toLowerCase();
        const address = (e.address || '').toLowerCase();
        return name.includes(q) || address.includes(q);
      });
    }

    filteredEstablishments = result;
  }

  function handleClear() {
    searchQuery = '';
    filterType = 'all';
    sourceFilter = 'all';
    distanceFilter = 0;
    loadAllEstablishments();
  }

  function handleSelectFromList(e) {
    selectedId = e.detail;
    mapView?.selectEstablishment(e.detail);
  }

  function handleGoToUserLocation() {
    mapView?.goToUserLocation();
  }

  function filterEstablishments() {
    loadAllEstablishments({ type: filterType, search: searchQuery });
  }

  // ---------------------------------------------------------------
  // 7. Fonctions globales pour les popups Leaflet
  // ---------------------------------------------------------------
  if (browser) {
    window.clearGoogleCache = clearGoogleCache;
    window.openProfilePanel = openProfilePanel;
    window.selectEstablishment = (id) => mapView?.selectEstablishment(id);
    window.goToEstablishment = (id) => mapView?.goToEstablishment(id);
    window.goToUserLocation = () => mapView?.goToUserLocation();
  }

  // ---------------------------------------------------------------
  // 8. Initialisation
  // ---------------------------------------------------------------
  onMount(async () => {
    await loadAllEstablishments();
    await tick();

    if (browser && navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          userLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };
          locationFound = true;
          setTimeout(() => loadAllEstablishments(), 200);
        },
        () => {
          console.log('Géolocalisation non disponible ou refusée');
          loadAllEstablishments();
        },
        { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
      );
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
      selectedId={selectedId}
      searchQuery={searchQuery}
      filterType={filterType}
      sourceFilter={sourceFilter}  
      distanceFilter={distanceFilter}
      loading={loading}
      loadingGoogle={loadingGoogle}
      on:search={handleSearch}
      on:filter={handleFilter}
      on:filterSource={handleFilterSource}
      on:filterDistance={handleFilterDistance}
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
      on:deselect={() => { selectedId = null; }}
    />

    {#if loading && filteredEstablishments.length === 0}
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