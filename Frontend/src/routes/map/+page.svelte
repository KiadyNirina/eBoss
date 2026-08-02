<!-- src/routes/map/+page.svelte -->
<script>
  import { onMount, tick } from 'svelte';
  import Icon from '@iconify/svelte';
  import { goto } from '$app/navigation';
  import { browser } from '$app/environment';
  import { authApi } from '$lib/api';
  
  let map = null;
  let markers = [];
  let edgeMarkers = [];
  let establishments = [];
  let loading = true;
  let selectedEstablishment = null;
  let userLocation = null;
  let mapInitialized = false;
  let L = null;
  let userMarker = null;
  let locationFound = false;
  let userEdgeMarker = null;
  let error = null;
  
  let searchQuery = '';
  let filterType = 'all';
  let filteredEstablishments = [];
  
  // Mapping des types
  const typeColors = {
    'ecole': '#3b82f6',
    'college': '#f59e0b',
    'lycee': '#ef4444',
    'universite': '#8b5cf6'
  };
  
  const typeLabels = {
    'ecole': 'École primaire',
    'college': 'Collège',
    'lycee': 'Lycée',
    'universite': 'Université'
  };
  
  // Fonction pour calculer la distance entre deux points en kilomètres
  function calculateDistance(lat1, lng1, lat2, lng2) {
    if (!lat1 || !lng1 || !lat2 || !lng2) return null;
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLng = (lng2 - lng1) * Math.PI / 180;
    const a = 
      Math.sin(dLat/2) * Math.sin(dLat/2) +
      Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
      Math.sin(dLng/2) * Math.sin(dLng/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
  }
  
  // Fonction pour formater la distance
  function formatDistance(distance) {
    if (distance === null || distance === undefined) return 'N/A';
    if (distance < 1) {
      return `${Math.round(distance * 1000)} m`;
    } else if (distance < 10) {
      return `${distance.toFixed(1)} km`;
    } else {
      return `${Math.round(distance)} km`;
    }
  }
  
  // Fonction pour obtenir la distance d'un établissement
  function getEstablishmentDistance(establishment) {
    if (!userLocation) return null;
    if (!establishment.lat && !establishment.latitude) return null;
    
    const lat = establishment.lat || parseFloat(establishment.latitude);
    const lng = establishment.lng || parseFloat(establishment.longitude);
    
    if (!lat || !lng) return null;
    
    return calculateDistance(
      userLocation.lat, userLocation.lng,
      lat, lng
    );
  }

  // Fonction pour charger les établissements depuis l'API
  async function loadEstablishments(filters = {}) {
    try {
      loading = true;
      error = null;
      
      // Préparer les filtres
      const apiFilters = {
        type: filters.type || filterType,
        search: filters.search || searchQuery,
      };
      
      // Ajouter la position pour la recherche par proximité
      if (userLocation) {
        apiFilters.lat = userLocation.lat;
        apiFilters.lng = userLocation.lng;
        apiFilters.radius = 50;
        apiFilters.with_coords = true;
      }
      
      // Appel API
      const data = await authApi.getEtablissements(apiFilters);
      
      // Traiter les données
      let establishmentsData = data.results || data || [];
      
      // Si c'est un objet avec des résultats paginés
      if (data.results) {
        establishmentsData = data.results;
      }
      
      // Mapper les données si présentes, sinon garder une liste vide
      if (establishmentsData.length > 0) {
        establishments = establishmentsData.map(est => ({
          id: est.id,
          name: est.nom,
          address: est.adresse,
          lat: parseFloat(est.latitude),
          lng: parseFloat(est.longitude),
          type: est.type_etablissement,
          phone: est.user?.telephone || 'Non disponible',
          email: est.user?.email || 'Non disponible',
          profileImage: est.user?.profile_image 
          ? `${est.user.profile_image}` 
          : null, 
          _raw: est
        }));
      } else {
        // Aucune donnée de l'API, on garde une liste vide – pas de fallback
        console.warn('Aucun établissement trouvé via l\'API.');
        establishments = [];
      }
      
      // Calculer les distances si position utilisateur disponible
      if (userLocation) {
        establishments = establishments.map(est => ({
          ...est,
          distance: getEstablishmentDistance(est)
        }));
        
        // Trier par distance
        establishments.sort((a, b) => (a.distance || Infinity) - (b.distance || Infinity));
      }
      
      filteredEstablishments = establishments;
      
      // Mettre à jour les marqueurs si la carte est initialisée
      if (mapInitialized) {
        addEstablishmentMarkers();
        updateEdgeMarkers();
      }
      
    } catch (err) {
      console.error('Erreur de chargement des établissements:', err);
      error = err.message || 'Erreur lors du chargement';
      
      // En cas d'erreur, on laisse également la liste vide – pas de données de secours
      establishments = [];
      filteredEstablishments = [];
      
      // Mettre à jour les marqueurs (ils seront vides)
      if (mapInitialized) {
        addEstablishmentMarkers();
        updateEdgeMarkers();
      }
      
    } finally {
      loading = false;
    }
  }
  
  // Fonction pour sélectionner un établissement
  function selectEstablishment(id) {
    if (!browser) return;
    
    const establishment = establishments.find(e => e.id === id);
    if (establishment && mapInitialized && L && establishment.lat && establishment.lng) {
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
    if (establishment && mapInitialized && L && establishment.lat && establishment.lng) {
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
  
  function goToUserLocation() {
    if (!browser || !userLocation || !map) return;
    
    map.setView([userLocation.lat, userLocation.lng], 14, {
      animate: true,
      duration: 1
    });
    
    if (userMarker) {
      setTimeout(() => {
        userMarker.openPopup();
      }, 500);
    }
  }
  
  onMount(async () => {
    // Charger les établissements
    await loadEstablishments();
    await tick();
    
    if (browser) {
      await initMap();
      
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            userLocation = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };
            locationFound = true;
            addUserLocationMarker();
            if (map) {
              map.setView([userLocation.lat, userLocation.lng], 14);
            }
            setTimeout(() => {
              loadEstablishments({
                lat: userLocation.lat,
                lng: userLocation.lng,
                radius: 50
              });
            }, 200);
          },
          (error) => {
            console.log('Géolocalisation non disponible ou refusée');
            if (map) {
              map.setView([-18.8792, 47.5079], 12); // Centre sur Madagascar
            }
            loadEstablishments();
          },
          {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
          }
        );
      } else {
        if (map) {
          map.setView([-18.8792, 47.5079], 12); // Centre sur Madagascar
        }
        loadEstablishments();
      }
    }
    
    // Resize map when window resizes to avoid grey areas in split view
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  });
  
  function handleResize() {
    if (map) {
      map.invalidateSize();
      updateEdgeMarkers();
    }
  }
  
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
      center: [-18.8792, 47.5079], // Centre sur Madagascar
      zoom: 12,
      attributionControl: false,
      zoomControl: false
    });
    
    // Repositionner les contrôles de zoom
    L.control.zoom({
      position: 'topright'
    }).addTo(map);
    
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
    
    filteredEstablishments.forEach((establishment, index) => {
      // Vérifier que l'établissement a des coordonnées
      if (!establishment.lat || !establishment.lng) {
        console.warn(`Établissement ${establishment.name} sans coordonnées`);
        return;
      }

      const color = typeColors[establishment.type] || '#6b7280';
      const typeLabel = typeLabels[establishment.type] || establishment.type;
      const delay = index * 0.2;
      const distance = establishment.distance || getEstablishmentDistance(establishment);
      const distanceText = distance !== null ? formatDistance(distance) : 'Distance non disponible';
      
      let markerHtml = `
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
          position: relative;
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
      `;
      
      if (distance !== null && distance < 50) {
        markerHtml += `
          <div style="
            position: absolute;
            top: -24px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(32, 120, 77, 0.95);
            color: white;
            font-size: 9px;
            padding: 2px 8px;
            border-radius: 10px;
            white-space: nowrap;
            font-weight: bold;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            z-index: 10;
            pointer-events: none;
            border: 1px solid rgba(255,255,255,0.2);
          ">
            📏 ${distanceText}
          </div>
        `;
      }
      
      markerHtml += `</div>`;
      
      const customIcon = L.divIcon({
        className: 'custom-marker',
        html: markerHtml,
        iconSize: [16, 16],
        iconAnchor: [8, 8],
        popupAnchor: [0, -12]
      });
      
      const tooltipContent = `
        <div class="distance-tooltip">
          <div class="font-bold text-[#20784d]">${establishment.name}</div>
          <div class="text-sm text-gray-600">📍 ${establishment.address}</div>
          ${distance !== null ? `
            <div class="flex items-center gap-1 mt-1 text-sm">
              <span class="text-gray-500">📏 Distance:</span>
              <span class="font-semibold text-[#20784d]">${distanceText}</span>
              <span class="text-gray-400 text-xs">de vous</span>
            </div>
          ` : `
            <div class="text-xs text-gray-400 mt-1">📍 Localisez-vous pour voir la distance</div>
          `}
          <div class="text-xs text-gray-400 mt-1">🏫 ${typeLabel}</div>
        </div>
      `;
      
      const marker = L.marker([establishment.lat, establishment.lng], { 
        icon: customIcon,
        riseOnHover: true
      })
      .addTo(map);
      
      marker.bindTooltip(tooltipContent, {
        permanent: false,
        direction: 'top',
        offset: [0, -10],
        className: 'custom-tooltip',
        sticky: true,
        interactive: true
      });
      
      marker.bindPopup(`
        <div class="p-2 max-w-xs">
          <h3 class="font-bold text-[#20784d] text-lg">${establishment.name}</h3>
          <p class="text-sm text-gray-600 mt-1">📍 ${establishment.address}</p>
          <p class="text-sm text-gray-600">🏫 ${typeLabel}</p>
          <p class="text-sm text-gray-600">📞 ${establishment.phone}</p>
          <p class="text-sm text-gray-600">✉️ ${establishment.email}</p>
          ${distance !== null ? `
            <div class="mt-2 p-2 bg-green-50 rounded-md border border-green-200">
              <p class="text-sm font-medium text-[#20784d]">
                📏 Distance: ${distanceText}
              </p>
            </div>
          ` : `
            <div class="mt-2 p-2 bg-gray-50 rounded-md border border-gray-200">
              <p class="text-sm text-gray-500">
                📏 Activez la géolocalisation pour voir la distance
              </p>
            </div>
          `}
          <button onclick="window.viewProfile(${establishment.id})" 
                  class="mt-2 w-full bg-white border border-[#20784d] text-[#20784d] px-3 py-2 rounded-lg text-sm font-medium hover:bg-green-50 transition-colors shadow-sm">
            Voir le profil
          </button>
          <button onclick="window.selectEstablishment(${establishment.id})" 
                  class="mt-3 w-full bg-[#20784d] text-white px-3 py-2 rounded-lg text-sm font-medium hover:bg-green-700 transition-colors shadow-sm">
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

  function getTooltipDirection(position, bounds) {
    const center = bounds.getCenter();
    const lat = position.lat;
    const lng = position.lng;
    
    const isTop = lat > center.lat;
    const isBottom = lat < center.lat;
    const isLeft = lng < center.lng;
    const isRight = lng > center.lng;
    
    if (isTop && !isLeft && !isRight) return 'bottom';
    if (isBottom && !isLeft && !isRight) return 'top';
    if (isLeft && !isTop && !isBottom) return 'right';
    if (isRight && !isTop && !isBottom) return 'left';
    
    if (isTop && isLeft) return 'bottomright';
    if (isTop && isRight) return 'bottomleft';
    if (isBottom && isLeft) return 'topright';
    if (isBottom && isRight) return 'topleft';
    
    return 'top';
  }
  
  function updateEdgeMarkers() {
    if (!mapInitialized || !L) return;
    
    edgeMarkers.forEach(marker => {
      if (map) map.removeLayer(marker);
    });
    edgeMarkers = [];
    
    if (userEdgeMarker) {
      map.removeLayer(userEdgeMarker);
      userEdgeMarker = null;
    }
    
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
        const establishment = establishments.find(e => e.id === establishmentId);
        const establishmentName = establishment?.name || 'Établissement';
        const distance = establishment ? getEstablishmentDistance(establishment) : null;
        const distanceText = distance !== null ? formatDistance(distance) : 'N/A';
        
        const tooltipDirection = getTooltipDirection(edgePosition, bounds);
        
        let offsetX = 0;
        let offsetY = 0;
        
        switch(tooltipDirection) {
            case 'top': offsetY = -15; break;
            case 'bottom': offsetY = 15; break;
            case 'left': offsetX = -15; break;
            case 'right': offsetX = 15; break;
            case 'topright': offsetX = 15; offsetY = -15; break;
            case 'topleft': offsetX = -15; offsetY = -15; break;
            case 'bottomright': offsetX = 15; offsetY = 15; break;
            case 'bottomleft': offsetX = -15; offsetY = 15; break;
            default: offsetY = -15;
        }
        
        const edgeTooltipContent = `
          <div class="distance-tooltip">
            <div class="font-bold text-[#20784d]">${establishmentName}</div>
            ${distance !== null ? `
              <div class="flex items-center gap-1 mt-1 text-sm">
                <span class="text-gray-500">📏 Distance:</span>
                <span class="font-semibold text-[#20784d]">${distanceText}</span>
                <span class="text-gray-400 text-xs">de vous</span>
              </div>
            ` : `
              <div class="text-xs text-gray-400 mt-1">📍 Localisez-vous pour voir la distance</div>
            `}
            <div class="text-xs text-gray-400 mt-1">#${index + 1} - Cliquez pour voir</div>
          </div>
        `;
        
        let edgeHtml = `
          <div class="edge-marker-container" style="
            background-color: ${color};
            width: 32px;
            height: 32px;
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 2px 12px rgba(0,0,0,0.4);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            color: white;
            font-weight: bold;
            position: relative;
            transition: all 0.3s ease;
            z-index: 500;
          "
          onmouseover="this.style.transform='scale(1.3)'; this.style.boxShadow='0 4px 20px rgba(0,0,0,0.6)'"
          onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 2px 12px rgba(0,0,0,0.4)'"
          onclick="window.goToEstablishment(${establishmentId})"
          title="Cliquer pour voir ${establishmentName}"
          >
            <div style="
              position: absolute;
              top: -4px;
              left: -4px;
              right: -4px;
              bottom: -4px;
              border-radius: 50%;
              border: 2px solid ${color};
              opacity: 0.4;
              animation: edgePulse 1.5s ease-in-out infinite;
            "></div>
            <span style="position: relative; z-index: 1; text-shadow: 0 1px 2px rgba(0,0,0,0.5);">${index + 1}</span>
        `;
        
        if (distance !== null && distance < 50) {
          edgeHtml += `
            <div style="
              position: absolute;
              top: -28px;
              left: 50%;
              transform: translateX(-50%);
              background: rgba(32, 120, 77, 0.95);
              color: white;
              font-size: 8px;
              padding: 2px 8px;
              border-radius: 10px;
              white-space: nowrap;
              font-weight: bold;
              box-shadow: 0 2px 4px rgba(0,0,0,0.2);
              z-index: 10;
              pointer-events: none;
              border: 1px solid rgba(255,255,255,0.2);
            ">
              📏 ${distanceText}
            </div>
          `;
        }
        
        edgeHtml += `</div>`;
        
        const edgeIcon = L.divIcon({
          className: 'edge-marker',
          html: edgeHtml,
          iconSize: [32, 32],
          iconAnchor: [16, 16],
          className: 'edge-marker-wrapper'
        });
        
        const edgeMarker = L.marker(edgePosition, { 
          icon: edgeIcon,
          riseOnHover: true,
          zIndexOffset: 500
        })
        .addTo(map);
        
        edgeMarker.bindTooltip(edgeTooltipContent, {
          permanent: false,
          direction: tooltipDirection,
          offset: [offsetX, offsetY],
          className: 'custom-tooltip',
          sticky: true,
          interactive: true
        });
        
        edgeMarker.bindPopup(`
          <div class="p-3 max-w-xs">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-bold text-gray-500 bg-gray-100 px-2 py-1 rounded">#${index + 1}</span>
              <span class="text-xs px-2 py-1 bg-[#20784d] text-white rounded-full">Cliquez pour voir</span>
            </div>
            ${popupContent}
          </div>
        `);
        
        edgeMarkers.push(edgeMarker);
      }
    });
    
    if (userLocation && !bounds.contains([userLocation.lat, userLocation.lng])) {
      const edgePosition = getEdgePosition(
          { lat: userLocation.lat, lng: userLocation.lng }, 
          bounds
      );
      
      const userEdgeIcon = L.divIcon({
        className: 'user-edge-marker',
        html: `
          <div class="user-edge-container" style="
            width: 40px;
            height: 40px;
            border-radius: 50%;
            border: 3px solid white;
            box-shadow: 0 2px 12px rgba(32, 120, 77, 0.6);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            background: #20784d;
            transition: all 0.3s ease;
            z-index: 1000;
          "
          onmouseover="this.style.transform='scale(1.3)'; this.style.boxShadow='0 4px 25px rgba(32, 120, 77, 0.8)'"
          onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 2px 12px rgba(32, 120, 77, 0.6)'"
          onclick="window.goToUserLocation()"
          title="Cliquer pour revenir à votre position"
          >
            <div style="
              position: absolute;
              top: -6px;
              left: -6px;
              right: -6px;
              bottom: -6px;
              border-radius: 50%;
              border: 2px solid #20784d;
              opacity: 0.5;
              animation: userEdgePulse 1.5s ease-in-out infinite;
            "></div>
            <div style="
              position: absolute;
              top: -12px;
              left: -12px;
              right: -12px;
              bottom: -12px;
              border-radius: 50%;
              border: 2px solid #20784d;
              opacity: 0.2;
              animation: userEdgePulse 1.5s ease-in-out 0.5s infinite;
            "></div>
            <span style="position: relative; z-index: 1; font-size: 18px;">📍</span>
          </div>
        `,
        iconSize: [40, 40],
        iconAnchor: [20, 20],
        className: 'user-edge-wrapper'
      });
      
      userEdgeMarker = L.marker(edgePosition, { 
        icon: userEdgeIcon,
        riseOnHover: true,
        zIndexOffset: 1000
      })
      .addTo(map)
      .bindPopup(`
        <div class="p-3">
          <div class="flex items-center gap-2 mb-2">
            <span class="text-lg">📍</span>
            <span class="font-bold text-[#20784d]">Votre position</span>
          </div>
          <p class="text-sm text-gray-600">Cliquez sur le marqueur pour revenir à votre position</p>
          <button onclick="window.goToUserLocation()" 
                  class="mt-3 w-full bg-[#20784d] text-white px-3 py-2 rounded-lg text-sm font-medium hover:bg-green-700 transition-colors shadow-sm">
            Revenir à ma position
          </button>
        </div>
      `);
    }
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
    
    if (userMarker) {
      map.removeLayer(userMarker);
    }
    
    const userIcon = L.divIcon({
      className: 'user-marker',
      html: `
        <div class="user-marker-container" onclick="window.goToUserLocation()" style="cursor: pointer;">
          <div class="pulse-ring-outer"></div>
          <div class="pulse-ring-inner"></div>
          <div class="user-marker-dot">
            <div class="user-marker-center"></div>
          </div>
          <div class="user-marker-icon">📍</div>
        </div>
      `,
      iconSize: [60, 60],
      iconAnchor: [30, 30],
      popupAnchor: [0, -34],
      className: 'user-marker-wrapper'
    });
    
    userMarker = L.marker([userLocation.lat, userLocation.lng], { 
      icon: userIcon,
      zIndexOffset: 1000
    })
    .addTo(map)
    .bindPopup(`
      <div class="p-3">
        <div class="flex items-center gap-2 mb-2">
          <span class="text-xl">📍</span>
          <p class="font-bold text-[#20784d]">Vous êtes ici</p>
        </div>
        <p class="text-sm text-gray-500">Lat: ${userLocation.lat.toFixed(6)}</p>
        <p class="text-sm text-gray-500">Lng: ${userLocation.lng.toFixed(6)}</p>
        <button onclick="window.goToUserLocation()" 
                class="mt-3 w-full bg-[#20784d] text-white px-3 py-2 rounded-lg text-sm font-medium hover:bg-green-700 transition-colors shadow-sm">
          Centrer sur ma position
        </button>
      </div>
    `);
  }
  
  function addLegend() {
    if (!mapInitialized || !L) return;
    
    const legend = L.control({ position: 'bottomright' });
    
    legend.onAdd = function() {
      const div = L.DomUtil.create('div', 'bg-white/95 backdrop-blur-sm p-4 rounded-xl shadow-lg border border-gray-100 text-sm min-w-[160px] m-4');
      div.innerHTML = `
        <div class="font-bold text-gray-800 mb-3 flex items-center gap-2">
          <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          Légende
        </div>
        <div class="space-y-2">
          <div class="flex items-center"><span class="inline-block w-3 h-3 rounded-full bg-blue-500 mr-3 shadow-sm"></span><span class="text-gray-600">École primaire</span></div>
          <div class="flex items-center"><span class="inline-block w-3 h-3 rounded-full bg-orange-500 mr-3 shadow-sm"></span><span class="text-gray-600">Collège</span></div>
          <div class="flex items-center"><span class="inline-block w-3 h-3 rounded-full bg-red-500 mr-3 shadow-sm"></span><span class="text-gray-600">Lycée</span></div>
          <div class="flex items-center"><span class="inline-block w-3 h-3 rounded-full bg-purple-500 mr-3 shadow-sm"></span><span class="text-gray-600">Université</span></div>
        </div>
        <div class="mt-3 pt-3 border-t border-gray-100 space-y-2">
          <div class="flex items-center justify-between group">
            <div class="flex items-center">
              <div class="w-3 h-3 rounded-full bg-[#20784d] mr-3 ring-4 ring-[#20784d]/20 animate-pulse"></div>
              <span class="text-xs text-gray-600">Votre position</span>
            </div>
          </div>
          <div class="flex items-center">
            <div class="w-3 h-3 rounded-full bg-[#20784d] mr-3 border-2 border-white shadow-md"></div>
            <span class="text-xs text-gray-500">Marqueur bordure</span>
          </div>
        </div>
      `;
      return div;
    };
    
    legend.addTo(map);
  }
  
  async function filterEstablishments() {
    await loadEstablishments({
      type: filterType,
      search: searchQuery
    });
  }
  
  function clearFilters() {
    searchQuery = '';
    filterType = 'all';
    loadEstablishments();
  }
  
  if (browser) {
    window.selectEstablishment = selectEstablishment;
    window.goToEstablishment = goToEstablishment;
    window.goToUserLocation = goToUserLocation;
    window.viewProfile = (id) => { goto('/etablissement/profil/' + id); };
  }
  
  function goBack() {
    goto('/');
  }
</script>

<svelte:head>
  <title>Rechercher des établissements - Carte interactive</title>
</svelte:head>

<!-- Layout divisé: Sidebar (gauche/bas) + Carte (droite/haut) -->
<div class="flex flex-col-reverse md:flex-row h-screen bg-gray-50 overflow-hidden">
  
  <!-- Panneau latéral (Liste & Filtres) -->
  <div class="w-full md:w-[400px] lg:w-[450px] h-[50vh] md:h-full flex flex-col bg-white shadow-2xl z-20 shrink-0">
    
    <!-- En-tête -->
    <div class="p-4 sm:p-5 border-b border-gray-100 flex items-center justify-between bg-white shrink-0">
      <div class="flex items-center space-x-3">
        <button 
          on:click={goBack}
          class="text-gray-500 hover:text-[#20784d] transition-colors p-2 rounded-full hover:bg-green-50 focus:outline-none focus:ring-2 focus:ring-[#20784d]/50"
        >
          <Icon icon="heroicons:arrow-left" class="h-5 w-5" />
        </button>
        <h1 class="text-lg font-bold text-gray-900 leading-tight">Recherche</h1>
      </div>
      
      {#if userLocation}
        <button 
          on:click={goToUserLocation}
          class="flex items-center gap-1.5 text-xs font-medium bg-green-50 text-[#20784d] px-3 py-1.5 rounded-full hover:bg-[#20784d] hover:text-white transition-all shadow-sm border border-green-100"
        >
          <Icon icon="heroicons:map-pin" class="h-4 w-4" />
          Ma position
        </button>
      {/if}
    </div>
    
    <!-- Section Filtres -->
    <div class="p-4 sm:px-5 bg-gray-50/50 border-b border-gray-100 shrink-0 space-y-3">
      <div class="relative">
        <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
          <Icon icon="heroicons:magnifying-glass" class="h-4 w-4 text-gray-400" />
        </div>
        <input
          type="text"
          placeholder="Nom, adresse, type..."
          bind:value={searchQuery}
          on:input={filterEstablishments}
          class="block w-full pl-10 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#20784d]/50 focus:border-[#20784d] transition-all shadow-sm"
        />
      </div>
      
      <div class="flex gap-2">
        <div class="relative flex-1">
          <select
            bind:value={filterType}
            on:change={filterEstablishments}
            class="block w-full pl-3 pr-8 py-2 bg-white border border-gray-200 rounded-lg text-sm text-gray-700 appearance-none focus:outline-none focus:ring-2 focus:ring-[#20784d]/50 focus:border-[#20784d] transition-all shadow-sm"
          >
            <option value="all">Tous les types</option>
            <option value="ecole">École primaire</option>
            <option value="college">Collège</option>
            <option value="lycee">Lycée</option>
            <option value="universite">Université</option>
          </select>
          <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
             <Icon icon="heroicons:chevron-down" class="h-4 w-4 text-gray-400" />
          </div>
        </div>
        
        <button
          on:click={clearFilters}
          class="px-4 py-2 text-sm font-medium text-gray-600 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-200 transition-all shadow-sm flex items-center gap-1"
          title="Réinitialiser"
        >
          <Icon icon="heroicons:arrow-path" class="h-4 w-4" />
        </button>
      </div>
      
      <div class="text-xs text-gray-500 pt-1 font-medium">
        {filteredEstablishments.length} établissement{filteredEstablishments.length > 1 ? 's' : ''} trouvé{filteredEstablishments.length > 1 ? 's' : ''}
      </div>
    </div>
    
    <!-- Liste des résultats -->
    <div class="flex-1 overflow-y-auto p-4 sm:p-5 bg-gray-50 space-y-3">
      {#if filteredEstablishments.length === 0}
        <div class="flex flex-col items-center justify-center h-full text-center p-6 text-gray-500">
          <div class="bg-gray-100 p-4 rounded-full mb-3">
            <Icon icon="heroicons:building-library" class="h-8 w-8 text-gray-400" />
          </div>
          <p class="font-medium text-gray-700">Aucun résultat</p>
          <p class="text-sm mt-1 text-gray-400">Essayez de modifier vos filtres de recherche.</p>
        </div>
      {:else}
        {#each filteredEstablishments as establishment}
          <!-- Carte d'établissement moderne -->
          <div 
            class="bg-white p-4 rounded-xl border border-gray-100 shadow-sm hover:shadow-md hover:border-green-200 cursor-pointer transition-all duration-200 group relative overflow-hidden"
            on:click={() => selectEstablishment(establishment.id)}
          >
            <!-- Liseré de couleur décoratif au survol -->
            <div class="absolute left-0 top-0 bottom-0 w-1 bg-transparent group-hover:bg-[#20784d] transition-colors"></div>
            
            <div class="flex items-start gap-3">

              {#if establishment.profileImage}
                <img 
                  src={establishment.profileImage} 
                  alt={establishment.name}
                  class="w-10 h-10 rounded-full object-cover border-2 border-white shadow-sm shrink-0"
                />
              {:else}
                <div class="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center shrink-0">
                  <Icon icon="heroicons:building-office-2" class="h-5 w-5 text-green-600" />
                </div>
              {/if}

              <div class="min-w-0 flex-1">
                <h3 class="font-bold text-gray-900 group-hover:text-[#20784d] transition-colors line-clamp-1">{establishment.name}</h3>
                <p class="text-xs text-gray-500 mt-1 flex items-start gap-1">
                  <Icon icon="heroicons:map-pin" class="h-3.5 w-3.5 shrink-0 mt-0.5 text-gray-400" />
                  <span class="line-clamp-2">{establishment.address}</span>
                </p>
                
                <div class="flex flex-wrap items-center mt-3 gap-2">
                  <span class="text-[10px] font-semibold uppercase tracking-wider px-2 py-1 bg-gray-100 text-gray-600 rounded-md">
                    {typeLabels[establishment.type] || establishment.type}
                  </span>
                  
                  {#if userLocation}
                    <span class="text-xs font-medium text-[#20784d] bg-green-50 px-2 py-1 rounded-md flex items-center gap-1">
                       <Icon icon="heroicons:arrows-right-left" class="h-3 w-3" />
                      {formatDistance(getEstablishmentDistance(establishment))}
                    </span>
                  {/if}
                </div>
              </div>
              
              <div class="shrink-0">
                <button 
                  class="h-8 w-8 rounded-full bg-gray-50 flex items-center justify-center text-gray-400 group-hover:bg-[#20784d] group-hover:text-white transition-all shadow-sm"
                  on:click={(e) => {
                    e.stopPropagation();
                    selectEstablishment(establishment.id);
                  }}
                  title="Voir sur la carte"
                >
                  <Icon icon="heroicons:chevron-right" class="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        {/each}
      {/if}
    </div>
  </div>
  
  <!-- Zone de la Carte (Prend tout le reste de l'espace) -->
  <div class="flex-1 h-[50vh] md:h-full relative z-10 bg-gray-200 overflow-hidden">
      <div id="map" class="w-full h-full absolute inset-0"></div>

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
  
</div>

<style>
  :global(.leaflet-container) {
    font-family: "Fredoka", sans-serif !important;
  }

  :global(.leaflet-control-attribution) {
    display: none !important;
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

  :global(.user-edge-marker) {
    background: transparent !important;
    border: none !important;
  }

  /* Style des tooltips de distance */
  :global(.custom-tooltip) {
    background: rgba(255, 255, 255, 0.95) !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1) !important;
    padding: 10px 14px !important;
    max-width: 280px !important;
    backdrop-filter: blur(12px) !important;
    font-size: 13px !important;
  }

  :global(.custom-tooltip::before) {
    border-top-color: rgba(255, 255, 255, 0.95) !important;
  }

  :global(.distance-tooltip) {
    font-size: 13px;
    line-height: 1.5;
  }

  :global(.distance-tooltip .font-bold) {
    font-size: 14px;
    margin-bottom: 2px;
  }

  /* Conteneur du marqueur utilisateur */
  :global(.user-marker-container) {
    position: relative;
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }

  /* Anneaux */
  :global(.pulse-ring-outer) {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: rgba(32, 120, 77, 0.15);
    animation: pulseRing 2s ease-in-out infinite;
  }

  :global(.pulse-ring-inner) {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 35px;
    height: 35px;
    border-radius: 50%;
    background: rgba(32, 120, 77, 0.25);
    animation: pulseRing 2s ease-in-out 0.6s infinite;
  }

  :global(.user-marker-dot) {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 26px;
    height: 26px;
    background: #20784d;
    border-radius: 50%;
    border: 3px solid white;
    box-shadow: 0 0 0 3px rgba(32, 120, 77, 0.3), 0 4px 12px rgba(0, 0, 0, 0.2);
    animation: popIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    z-index: 2;
  }

  :global(.user-marker-center) {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 8px;
    height: 8px;
    background: white;
    border-radius: 50%;
    animation: pulse 2s ease-in-out 0.6s infinite;
  }

  :global(.user-marker-icon) {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 14px;
    color: white;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    pointer-events: none;
    z-index: 3;
    animation: popIn 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  }

  @keyframes popIn {
    0% { transform: translate(-50%, -50%) scale(0); opacity: 0; }
    70% { transform: translate(-50%, -50%) scale(1.2); opacity: 1; }
    100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
  }

  @keyframes pulse {
    0%, 100% { transform: translate(-50%, -50%) scale(1); }
    50% { transform: translate(-50%, -50%) scale(1.3); }
  }

  @keyframes pulseRing {
    0% { transform: translate(-50%, -50%) scale(0.6); opacity: 1; }
    100% { transform: translate(-50%, -50%) scale(1.6); opacity: 0; }
  }

  @keyframes markerPulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.2); }
  }
  
  @keyframes markerRipple {
    0% { transform: scale(0.8); opacity: 0.3; }
    100% { transform: scale(2.2); opacity: 0; }
  }

  @keyframes edgePulse {
    0%, 100% { transform: scale(1); opacity: 0.4; }
    50% { transform: scale(1.4); opacity: 0.8; }
  }

  @keyframes userEdgePulse {
    0%, 100% { transform: scale(1); opacity: 0.5; }
    50% { transform: scale(1.5); opacity: 0.8; }
  }
  
  :global(.leaflet-popup-content) {
    min-width: 220px;
    max-width: 320px;
    margin: 16px !important;
  }
  
  :global(.leaflet-popup-content-wrapper) {
    border-radius: 16px !important;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1) !important;
    padding: 0 !important;
  }
  
  :global(.leaflet-popup-tip) {
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1) !important;
  }
  
  :global(.leaflet-control-zoom) {
    border: none !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
    border-radius: 8px !important;
    margin-top: 20px !important;
    margin-right: 20px !important;
    overflow: hidden;
  }
  
  :global(.leaflet-control-zoom a) {
    color: #4b5563 !important;
    background: white !important;
    transition: all 0.2s ease !important;
    width: 36px !important;
    height: 36px !important;
    line-height: 36px !important;
  }
  
  :global(.leaflet-control-zoom a:hover) {
    background: #f9fafb !important;
    color: #20784d !important;
  }

  :global(.edge-marker-container:hover) {
    transform: scale(1.3) !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.6) !important;
  }

  :global(.user-edge-container:hover) {
    transform: scale(1.3) !important;
    box-shadow: 0 10px 25px rgba(32, 120, 77, 0.8) !important;
  }

  :global(.leaflet-tooltip-pane) {
    z-index: 1000 !important;
  }
</style>