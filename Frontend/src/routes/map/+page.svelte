<!-- src/routes/map/+page.svelte -->
<script>
  import { onMount, tick } from 'svelte';
  import Icon from '@iconify/svelte';
  import { goto } from '$app/navigation';
  import { browser } from '$app/environment';
  
  let map = null;
  let markers = [];
  let edgeMarkers = [];
  let establishments = [];
  let loading = true;
  let selectedEstablishment = null;
  let userLocation = null;
  let mapInitialized = false;
  let L = null;
  
  // Données des établissements
  const establishmentData = [
    {
      id: 1,
      name: "École Primaire Les Petits Génies",
      address: "123 Rue de l'Éducation, 75001 Paris",
      lat: 48.8566,
      lng: 2.3522,
      type: "Primaire",
      phone: "01 23 45 67 89",
      email: "contact@petitsgenies.fr"
    },
    {
      id: 2,
      name: "Collège Jean Jaurès",
      address: "45 Avenue de la République, 69002 Lyon",
      lat: 45.7640,
      lng: 4.8357,
      type: "Collège",
      phone: "04 56 78 90 12",
      email: "contact@jeanjaures.fr"
    },
    {
      id: 3,
      name: "Lycée Victor Hugo",
      address: "78 Boulevard Saint-Michel, 75005 Paris",
      lat: 48.8466,
      lng: 2.3389,
      type: "Lycée",
      phone: "01 98 76 54 32",
      email: "contact@victorhugo.fr"
    },
    {
      id: 4,
      name: "Université de Bordeaux",
      address: "351 Cours de la Libération, 33405 Talence",
      lat: 44.8052,
      lng: -0.6039,
      type: "Université",
      phone: "05 56 84 56 84",
      email: "contact@univ-bordeaux.fr"
    },
    {
      id: 5,
      name: "École Maternelle Le Jardin d'Enfants",
      address: "12 Rue des Fleurs, 31000 Toulouse",
      lat: 43.6047,
      lng: 1.4442,
      type: "Maternelle",
      phone: "05 61 23 45 67",
      email: "contact@jardinenfants.fr"
    }
  ];
  
  let searchQuery = '';
  let filterType = 'all';
  let filteredEstablishments = [];
  
  // Fonction pour sélectionner un établissement
  function selectEstablishment(id) {
    if (!browser) return;
    
    const establishment = establishments.find(e => e.id === id);
    if (establishment && mapInitialized && L) {
      selectedEstablishment = establishment;
      map.setView([establishment.lat, establishment.lng], 16);
      markers.forEach(marker => {
        const latLng = marker.getLatLng();
        if (latLng.lat === establishment.lat && 
            latLng.lng === establishment.lng) {
          marker.openPopup();
        }
      });
    }
  }
  
  // Fonction pour aller à un établissement depuis un marqueur de bordure
  function goToEstablishment(id) {
    if (!browser) return;
    
    const establishment = establishments.find(e => e.id === id);
    if (establishment && mapInitialized && L) {
      map.setView([establishment.lat, establishment.lng], 15, {
        animate: true,
        duration: 1
      });
      
      markers.forEach(marker => {
        const latLng = marker.getLatLng();
        if (latLng.lat === establishment.lat && 
            latLng.lng === establishment.lng) {
          setTimeout(() => {
            marker.openPopup();
          }, 500);
        }
      });
    }
  }
  
  onMount(async () => {
    establishments = establishmentData;
    filteredEstablishments = establishments;
    loading = false;
    
    await tick();
    
    if (browser) {
      await initMap();
    }
    
    if (browser && navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          userLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          addUserLocationMarker();
        },
        (error) => {
          console.log('Géolocalisation non disponible');
        }
      );
    }
  });
  
  async function initMap() {
    if (mapInitialized || !browser) return;
    
    const leaflet = await import('leaflet');
    L = leaflet.default;
    await import('leaflet/dist/leaflet.css');
    
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
      iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
      shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
    });
    
    map = L.map('map', {
      center: [46.603354, 1.888334],
      zoom: 6,
      attributionControl: false
    });
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '',
      maxZoom: 19
    }).addTo(map);
    
    mapInitialized = true;
    
    addEstablishmentMarkers();
    addLegend();
    setupMapEvents();
    
    setTimeout(() => {
      if (map) {
        map.invalidateSize();
        updateEdgeMarkers();
      }
    }, 300);
  }
  
  function addEstablishmentMarkers() {
    if (!mapInitialized || !L) return;
    
    markers.forEach(marker => {
      if (map) map.removeLayer(marker);
    });
    markers = [];
    
    const typeColors = {
      'Maternelle': '#3b82f6',
      'Primaire': '#22c55e',
      'Collège': '#f59e0b',
      'Lycée': '#ef4444',
      'Université': '#8b5cf6'
    };
    
    filteredEstablishments.forEach((establishment, index) => {
      const color = typeColors[establishment.type] || '#6b7280';
      const delay = index * 0.2;
      
      const customIcon = L.divIcon({
        className: 'custom-marker',
        html: `
          <div style="
            background-color: ${color};
            width: 16px;
            height: 16px;
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            cursor: pointer;
            transition: transform 0.3s ease;
            animation: markerPulse 2s ease-in-out ${delay}s infinite;
          ">
            <div style="
              position: absolute;
              top: -8px;
              left: -8px;
              width: 32px;
              height: 32px;
              border-radius: 50%;
              background: ${color};
              opacity: 0.2;
              animation: markerRipple 2s ease-out ${delay}s infinite;
            "></div>
          </div>
        `,
        iconSize: [16, 16],
        iconAnchor: [8, 8],
        popupAnchor: [0, -12]
      });
      
      const marker = L.marker([establishment.lat, establishment.lng], { 
        icon: customIcon,
        riseOnHover: true
      })
      .addTo(map)
      .bindPopup(`
        <div class="p-2 max-w-xs">
          <h3 class="font-bold text-[#20784d] text-lg">${establishment.name}</h3>
          <p class="text-sm text-gray-600 mt-1">📍 ${establishment.address}</p>
          <p class="text-sm text-gray-600">🏫 ${establishment.type}</p>
          <p class="text-sm text-gray-600">📞 ${establishment.phone}</p>
          <p class="text-sm text-gray-600">✉️ ${establishment.email}</p>
          <button onclick="window.selectEstablishment(${establishment.id})" 
                  class="mt-2 w-full bg-[#20784d] text-white px-3 py-1.5 rounded text-sm hover:bg-green-700 transition-colors">
            Voir détails
          </button>
        </div>
      `);
      
      markers.push(marker);
    });
    
    setTimeout(() => {
      updateEdgeMarkers();
    }, 100);
  }
  
  function updateEdgeMarkers() {
    if (!mapInitialized || !L || markers.length === 0) return;
    
    edgeMarkers.forEach(marker => {
      if (map) map.removeLayer(marker);
    });
    edgeMarkers = [];
    
    const bounds = map.getBounds();
    
    markers.forEach((marker, index) => {
      const latLng = marker.getLatLng();
      const position = latLng;
      
      if (!bounds.contains(position)) {
        const edgePosition = getEdgePosition(position, bounds);
        
        const originalColor = marker.options.icon.options.html.match(/background-color: ([^;]+)/);
        const color = originalColor ? originalColor[1] : '#ef4444';
        
        const popupContent = marker.getPopup().getContent();
        const idMatch = popupContent.match(/selectEstablishment\((\d+)\)/);
        const establishmentId = idMatch ? parseInt(idMatch[1]) : null;
        
        const edgeIcon = L.divIcon({
          className: 'edge-marker',
          html: `
            <div style="
              background-color: ${color};
              width: 18px;
              height: 18px;
              border-radius: 50%;
              border: 3px solid white;
              box-shadow: 0 2px 12px rgba(0,0,0,0.4);
              cursor: pointer;
              display: flex;
              align-items: center;
              justify-content: center;
              font-size: 10px;
              color: white;
              font-weight: bold;
              position: relative;
              transition: all 0.3s ease;
            "
            onmouseover="this.style.transform='scale(1.4)'; this.style.boxShadow='0 4px 20px rgba(0,0,0,0.5)'"
            onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 2px 12px rgba(0,0,0,0.4)'"
            onclick="window.goToEstablishment(${establishmentId})"
            title="Cliquer pour voir ${establishmentData.find(e => e.id === establishmentId)?.name || 'cet établissement'}"
            >
              <div style="
                position: absolute;
                top: -6px;
                left: -6px;
                right: -6px;
                bottom: -6px;
                border-radius: 50%;
                border: 2px solid ${color};
                opacity: 0.3;
                animation: edgePulse 1.5s ease-in-out infinite;
              "></div>
              <span style="position: relative; z-index: 1;">${index + 1}</span>
            </div>
          `,
          iconSize: [18, 18],
          iconAnchor: [9, 9]
        });
        
        const edgeMarker = L.marker(edgePosition, { 
          icon: edgeIcon,
          riseOnHover: true
        })
        .addTo(map)
        .bindPopup(`
          <div class="p-2 max-w-xs">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-bold text-gray-500">#${index + 1}</span>
              <span class="text-xs px-2 py-1 bg-[#20784d] text-white rounded-full">Cliquez pour voir</span>
            </div>
            ${popupContent}
          </div>
        `);
        
        edgeMarkers.push(edgeMarker);
      }
    });
  }
  
  function getEdgePosition(position, bounds) {
    const north = bounds.getNorth();
    const south = bounds.getSouth();
    const east = bounds.getEast();
    const west = bounds.getWest();
    
    const lat = position.lat;
    const lng = position.lng;
    
    let edgeLat = Math.max(south, Math.min(north, lat));
    let edgeLng = Math.max(west, Math.min(east, lng));
    
    if (edgeLat === lat && edgeLng === lng) {
      const latDist = Math.max(lat - south, north - lat);
      const lngDist = Math.max(lng - west, east - lng);
      
      if (latDist > lngDist) {
        edgeLat = (lat > (south + north) / 2) ? north : south;
      } else {
        edgeLng = (lng > (west + east) / 2) ? east : west;
      }
    }
    
    return { lat: edgeLat, lng: edgeLng };
  }
  
  function setupMapEvents() {
    if (!mapInitialized) return;
    
    map.on('moveend', () => {
      updateEdgeMarkers();
    });
    
    map.on('zoomend', () => {
      updateEdgeMarkers();
    });
  }
  
  function addUserLocationMarker() {
    if (!mapInitialized || !userLocation || !L) return;
    
    const userIcon = L.divIcon({
      className: 'user-marker',
      html: `<div style="
        background-color: #20784d;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        border: 3px solid white;
        box-shadow: 0 0 0 3px #20784d, 0 2px 8px rgba(0,0,0,0.3);
        animation: pulse 2s infinite;
      "></div>`,
      iconSize: [16, 16],
      iconAnchor: [8, 8]
    });
    
    L.marker([userLocation.lat, userLocation.lng], { icon: userIcon })
      .addTo(map)
      .bindPopup(`
        <div class="p-2">
          <p class="font-bold text-[#20784d]">📍 Vous êtes ici</p>
          <p class="text-sm text-gray-500">Lat: ${userLocation.lat.toFixed(4)}</p>
          <p class="text-sm text-gray-500">Lng: ${userLocation.lng.toFixed(4)}</p>
        </div>
      `);
  }
  
  function addLegend() {
    if (!mapInitialized || !L) return;
    
    const legend = L.control({ position: 'bottomright' });
    
    legend.onAdd = function() {
      const div = L.DomUtil.create('div', 'bg-white p-3 rounded-lg shadow-md text-sm min-w-[150px]');
      div.innerHTML = `
        <div class="font-bold text-gray-700 mb-2">Types d'établissements</div>
        <div class="space-y-1">
          <div><span class="inline-block w-3 h-3 rounded-full bg-blue-500 mr-2"></span>Maternelle</div>
          <div><span class="inline-block w-3 h-3 rounded-full bg-green-500 mr-2"></span>Primaire</div>
          <div><span class="inline-block w-3 h-3 rounded-full bg-orange-500 mr-2"></span>Collège</div>
          <div><span class="inline-block w-3 h-3 rounded-full bg-red-500 mr-2"></span>Lycée</div>
          <div><span class="inline-block w-3 h-3 rounded-full bg-purple-500 mr-2"></span>Université</div>
        </div>
      `;
      return div;
    };
    
    legend.addTo(map);
  }
  
  function filterEstablishments() {
    let filtered = establishments;
    
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase().trim();
      filtered = filtered.filter(e => 
        e.name.toLowerCase().includes(query) ||
        e.address.toLowerCase().includes(query) ||
        e.type.toLowerCase().includes(query)
      );
    }
    
    if (filterType !== 'all') {
      filtered = filtered.filter(e => e.type === filterType);
    }
    
    filteredEstablishments = filtered;
    addEstablishmentMarkers();
    
    setTimeout(() => {
      updateEdgeMarkers();
    }, 200);
  }
  
  function clearFilters() {
    searchQuery = '';
    filterType = 'all';
    filteredEstablishments = establishments;
    addEstablishmentMarkers();
    
    setTimeout(() => {
      updateEdgeMarkers();
    }, 200);
  }
  
  if (browser) {
    window.selectEstablishment = selectEstablishment;
    window.goToEstablishment = goToEstablishment;
  }
  
  function goBack() {
    goto('/');
  }
</script>

<svelte:head>
  <title>Rechercher des établissements - Carte interactive</title>
</svelte:head>

<div class="min-h-screen bg-gray-50">
  <!-- Header -->
  <div class="bg-white shadow-sm sticky top-0 z-10">
    <div class="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <button 
            on:click={goBack}
            class="text-gray-600 hover:text-[#20784d] transition-colors p-2 rounded-full hover:bg-green-50"
          >
            <Icon icon="heroicons:arrow-left" class="h-6 w-6" />
          </button>
          <h1 class="text-xl font-bold text-gray-900">Rechercher des établissements</h1>
        </div>
        <span class="text-sm text-gray-500">{filteredEstablishments.length} établissements trouvés</span>
      </div>
    </div>
  </div>
  
  <!-- Filtres -->
  <div class="bg-white border-b">
    <div class="max-w-7xl mx-auto px-4 py-3 sm:px-6 lg:px-8">
      <div class="flex flex-col sm:flex-row gap-3">
        <div class="flex-1 relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Icon icon="heroicons:magnifying-glass" class="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            placeholder="Rechercher un établissement..."
            bind:value={searchQuery}
            on:input={filterEstablishments}
            class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md text-sm placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-[#20784d] focus:border-transparent"
          />
        </div>
        
        <div class="sm:w-48">
          <select
            bind:value={filterType}
            on:change={filterEstablishments}
            class="block w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-[#20784d] focus:border-transparent"
          >
            <option value="all">Tous les types</option>
            <option value="Maternelle">Maternelle</option>
            <option value="Primaire">Primaire</option>
            <option value="Collège">Collège</option>
            <option value="Lycée">Lycée</option>
            <option value="Université">Université</option>
          </select>
        </div>
        
        <button
          on:click={clearFilters}
          class="px-4 py-2 text-sm text-gray-600 hover:text-[#20784d] border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
        >
          Réinitialiser
        </button>
      </div>
    </div>
  </div>
  
  <!-- Carte -->
  <div class="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
    {#if loading}
      <div class="flex items-center justify-center h-[500px] bg-white rounded-lg shadow">
        <div class="text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#20784d] mx-auto"></div>
          <p class="mt-4 text-gray-500">Chargement de la carte...</p>
        </div>
      </div>
    {:else}
      <div id="map" class="h-[500px] rounded-lg shadow-lg"></div>
    {/if}
  </div>
  
  <!-- Liste des établissements -->
  <div class="max-w-7xl mx-auto px-4 pb-8 sm:px-6 lg:px-8">
    <div class="bg-white rounded-lg shadow">
      <div class="p-4 border-b">
        <h2 class="font-semibold text-gray-900">Liste des établissements</h2>
      </div>
      <div class="divide-y divide-gray-200 max-h-60 overflow-y-auto">
        {#if filteredEstablishments.length === 0}
          <div class="p-8 text-center text-gray-500">
            <Icon icon="heroicons:map-pin" class="h-12 w-12 mx-auto text-gray-300 mb-2" />
            <p>Aucun établissement trouvé</p>
          </div>
        {:else}
          {#each filteredEstablishments as establishment}
            <div 
              class="p-4 hover:bg-gray-50 cursor-pointer transition-colors"
              on:click={() => selectEstablishment(establishment.id)}
            >
              <div class="flex items-start justify-between">
                <div>
                  <h3 class="font-medium text-gray-900">{establishment.name}</h3>
                  <p class="text-sm text-gray-500">{establishment.address}</p>
                  <div class="flex items-center mt-1 space-x-2">
                    <span class="text-xs px-2 py-1 bg-[#20784d] text-white rounded-full">
                      {establishment.type}
                    </span>
                    <span class="text-xs text-gray-400">{establishment.phone}</span>
                  </div>
                </div>
                <button 
                  class="text-[#20784d] hover:text-green-700 transition-colors"
                  on:click={(e) => {
                    e.stopPropagation();
                    selectEstablishment(establishment.id);
                  }}
                >
                  <Icon icon="heroicons:map-pin" class="h-5 w-5" />
                </button>
              </div>
            </div>
          {/each}
        {/if}
      </div>
    </div>
  </div>
</div>

<style>
  :global(.leaflet-control-attribution) {
    display: none !important;
  }

  :global(#map) {
    height: 500px;
    width: 100%;
    border-radius: 0.5rem;
  }
  
  :global(.custom-marker) {
    background: transparent !important;
    border: none !important;
  }
  
  :global(.user-marker) {
    background: transparent !important;
    border: none !important;
  }

  :global(.edge-marker) {
    background: transparent !important;
    border: none !important;
  }

  /* Animation des marqueurs */
  @keyframes markerPulse {
    0%, 100% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.2);
    }
  }
  
  @keyframes markerRipple {
    0% {
      transform: scale(0.8);
      opacity: 0.3;
    }
    100% {
      transform: scale(2);
      opacity: 0;
    }
  }
  
  @keyframes pulse {
    0% {
      transform: scale(1);
      opacity: 1;
    }
    50% {
      transform: scale(1.2);
      opacity: 0.8;
    }
    100% {
      transform: scale(1);
      opacity: 1;
    }
  }

  @keyframes edgePulse {
    0%, 100% {
      transform: scale(1);
      opacity: 1;
    }
    50% {
      transform: scale(1.3);
      opacity: 0.7;
    }
  }
  
  :global(.leaflet-popup-content) {
    min-width: 200px;
    max-width: 300px;
  }
  
  :global(.leaflet-popup-content-wrapper) {
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
  }
  
  :global(.leaflet-popup-tip) {
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
  }
  
  :global(.leaflet-control-zoom) {
    border: none !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    border-radius: 8px !important;
  }
  
  :global(.leaflet-control-zoom a) {
    color: #374151 !important;
    background: white !important;
  }
  
  :global(.leaflet-control-zoom a:hover) {
    background: #f3f4f6 !important;
    color: #20784d !important;
  }
</style>