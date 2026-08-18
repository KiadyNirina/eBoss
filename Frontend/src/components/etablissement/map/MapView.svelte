<!-- src/components/etablissement/map/MapView.svelte -->
<script>
  import { onMount, tick } from 'svelte';
  import { calculateDistance, formatDistance } from './mapUtils';

  export let establishments = [];
  export let userLocation = null;

  let map = null;
  let L = null;
  let mapInitialized = false;
  let markers = [];
  let edgeMarkers = [];
  let userMarker = null;
  let userEdgeMarker = null;

  const typeColors = {
    ecole: '#3b82f6',
    college: '#f59e0b',
    lycee: '#ef4444',
    universite: '#8b5cf6'
  };

  const typeLabels = {
    ecole: 'École primaire',
    college: 'Collège',
    lycee: 'Lycée',
    universite: 'Université'
  };

  // Expose les méthodes au parent via bind:this
  export function selectEstablishment(id) {
    if (!mapInitialized || !L) return;
    const establishment = establishments.find(e => e.id === id);
    if (!establishment || !establishment.lat || !establishment.lng) return;
    map.setView([establishment.lat, establishment.lng], 16);
    markers.forEach(marker => {
      const latLng = marker.getLatLng();
      if (latLng.lat === establishment.lat && latLng.lng === establishment.lng) {
        marker.openPopup();
      }
    });
  }

  export function goToEstablishment(id) {
    if (!mapInitialized || !L) return;
    const establishment = establishments.find(e => e.id === id);
    if (!establishment || !establishment.lat || !establishment.lng) return;
    map.setView([establishment.lat, establishment.lng], 15, { animate: true, duration: 1 });
    markers.forEach(marker => {
      const latLng = marker.getLatLng();
      if (latLng.lat === establishment.lat && latLng.lng === establishment.lng) {
        setTimeout(() => marker.openPopup(), 500);
      }
    });
  }

  export function goToUserLocation() {
    if (!mapInitialized || !userLocation || !map) return;
    map.setView([userLocation.lat, userLocation.lng], 14, { animate: true, duration: 1 });
    if (userMarker) {
      setTimeout(() => userMarker.openPopup(), 500);
    }
  }

  // Met à jour les marqueurs quand les données ou la position changent
  $: if (mapInitialized) {
    void establishments;
    void userLocation;
    addEstablishmentMarkers(establishments, userLocation);
    updateEdgeMarkers(establishments, userLocation);
  }

  onMount(async () => {
    await initMap();
    if (map) {
      setTimeout(() => {
        map.invalidateSize();
        updateEdgeMarkers(establishments, userLocation);
      }, 300);
    }
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  });

  function handleResize() {
    if (map) {
      map.invalidateSize();
      updateEdgeMarkers();
      updateEdgeMarkers(establishments, userLocation);
    }
  }

  async function initMap() {
    if (mapInitialized) return;
    const leaflet = await import('leaflet');
    L = leaflet.default;
    await import('leaflet/dist/leaflet.css');

    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
      iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
      shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png'
    });

    map = L.map('map', {
      center: [-18.8792, 47.5079],
      zoom: 12,
      attributionControl: false,
      zoomControl: false
    });

    L.control.zoom({ position: 'topright' }).addTo(map);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '',
      maxZoom: 19
    }).addTo(map);

    mapInitialized = true;
    addLegend();
    setupMapEvents();
    addEstablishmentMarkers(establishments, userLocation);
    updateEdgeMarkers(establishments, userLocation);
  }

  function addEstablishmentMarkers(establishmentsList, userLocation) {
    if (!mapInitialized || !L) return;
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];

    establishmentsList.forEach((establishment, index) => {
      if (!establishment.lat || !establishment.lng) return;

      const color = typeColors[establishment.type] || '#6b7280';
      const typeLabel = typeLabels[establishment.type] || establishment.type;
      const delay = index * 0.2;
      const distance = establishment.distance || getEstablishmentDistance(establishment, userLocation);
      const distanceText = distance !== null ? formatDistance(distance) : 'Distance non disponible';

      let markerHtml = `
        <div style="
          background-color: ${color};
          width: 16px; height: 16px; border-radius: 50%;
          border: 3px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);
          cursor: pointer; transition: transform 0.3s ease;
          animation: markerPulse 2s ease-in-out ${delay}s infinite;
          position: relative;
        ">
          <div style="
            position: absolute; top: -8px; left: -8px;
            width: 32px; height: 32px; border-radius: 50%;
            background: ${color}; opacity: 0.2;
            animation: markerRipple 2s ease-out ${delay}s infinite;
          "></div>
      `;

      if (distance !== null && distance < 50) {
        markerHtml += `
          <div style="
            position: absolute; top: -24px; left: 50%;
            transform: translateX(-50%);
            background: rgba(32, 120, 77, 0.95);
            color: white; font-size: 9px;
            padding: 2px 8px; border-radius: 10px;
            white-space: nowrap; font-weight: bold;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            z-index: 10; pointer-events: none;
            border: 1px solid rgba(255,255,255,0.2);
          ">📏 ${distanceText}</div>
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
      }).addTo(map);

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
              <p class="text-sm font-medium text-[#20784d]">📏 Distance: ${distanceText}</p>
            </div>
          ` : `
            <div class="mt-2 p-2 bg-gray-50 rounded-md border border-gray-200">
              <p class="text-sm text-gray-500">📏 Activez la géolocalisation pour voir la distance</p>
            </div>
          `}
          <button onclick="window.openProfilePanel(${establishment.id})"
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

    setTimeout(() => updateEdgeMarkers(establishmentsList, userLocation), 100);
  }

  function getEstablishmentDistance(establishment, userLocation) {
    if (!userLocation) return null;
    if (!establishment.lat && !establishment.latitude) return null;
    const lat = establishment.lat || parseFloat(establishment.latitude);
    const lng = establishment.lng || parseFloat(establishment.longitude);
    if (!lat || !lng) return null;
    return calculateDistance(userLocation.lat, userLocation.lng, lat, lng);
  }

  function updateEdgeMarkers(establishmentsList, userLocation) {
    if (!mapInitialized || !L) return;
    edgeMarkers.forEach(marker => map.removeLayer(marker));
    edgeMarkers = [];
    if (userEdgeMarker) {
      map.removeLayer(userEdgeMarker);
      userEdgeMarker = null;
    }

    const bounds = map.getBounds();

    markers.forEach((marker, index) => {
      const latLng = marker.getLatLng();
      if (!bounds.contains(latLng)) {
        const edgePosition = getEdgePosition(latLng, bounds);
        const originalColor = marker.options.icon.options.html.match(/background-color: ([^;]+)/);
        const color = originalColor ? originalColor[1] : '#ef4444';

        const popupContent = marker.getPopup().getContent();
        const idMatch = popupContent.match(/selectEstablishment\((\d+)\)/);
        const establishmentId = idMatch ? parseInt(idMatch[1]) : null;
        const establishment = establishmentsList.find(e => e.id === establishmentId);
        const establishmentName = establishment?.name || 'Établissement';
        const distance = establishment ? getEstablishmentDistance(establishment, userLocation) : null;
        const distanceText = distance !== null ? formatDistance(distance) : 'N/A';

        const tooltipDirection = getTooltipDirection(edgePosition, bounds);
        let offsetX = 0, offsetY = 0;
        switch (tooltipDirection) {
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
            width: 32px; height: 32px; border-radius: 50%;
            border: 3px solid white; box-shadow: 0 2px 12px rgba(0,0,0,0.4);
            cursor: pointer; display: flex; align-items: center; justify-content: center;
            font-size: 12px; color: white; font-weight: bold;
            position: relative; transition: all 0.3s ease; z-index: 500;
          "
          onmouseover="this.style.transform='scale(1.3)'; this.style.boxShadow='0 4px 20px rgba(0,0,0,0.6)'"
          onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 2px 12px rgba(0,0,0,0.4)'"
          onclick="window.goToEstablishment(${establishmentId})"
          title="Cliquer pour voir ${establishmentName}">
            <div style="
              position: absolute; top: -4px; left: -4px; right: -4px; bottom: -4px;
              border-radius: 50%; border: 2px solid ${color};
              opacity: 0.4; animation: edgePulse 1.5s ease-in-out infinite;
            "></div>
            <span style="position: relative; z-index: 1; text-shadow: 0 1px 2px rgba(0,0,0,0.5);">${index + 1}</span>
        `;

        if (distance !== null && distance < 50) {
          edgeHtml += `
            <div style="
              position: absolute; top: -28px; left: 50%;
              transform: translateX(-50%);
              background: rgba(32, 120, 77, 0.95);
              color: white; font-size: 8px; padding: 2px 8px;
              border-radius: 10px; white-space: nowrap; font-weight: bold;
              box-shadow: 0 2px 4px rgba(0,0,0,0.2);
              z-index: 10; pointer-events: none;
              border: 1px solid rgba(255,255,255,0.2);
            ">📏 ${distanceText}</div>
          `;
        }

        edgeHtml += `</div>`;

        const edgeIcon = L.divIcon({
          className: 'edge-marker',
          html: edgeHtml,
          iconSize: [32, 32],
          iconAnchor: [16, 16]
        });

        const edgeMarker = L.marker(edgePosition, {
          icon: edgeIcon,
          riseOnHover: true,
          zIndexOffset: 500
        }).addTo(map);

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

    // Marqueur de bordure pour la position utilisateur
    if (userLocation && !bounds.contains([userLocation.lat, userLocation.lng])) {
      const edgePosition = getEdgePosition(
        { lat: userLocation.lat, lng: userLocation.lng },
        bounds
      );

      const userEdgeIcon = L.divIcon({
        className: 'user-edge-marker',
        html: `
          <div class="user-edge-container" style="
            width: 40px; height: 40px; border-radius: 50%;
            border: 3px solid white; box-shadow: 0 2px 12px rgba(32, 120, 77, 0.6);
            cursor: pointer; display: flex; align-items: center; justify-content: center;
            position: relative; background: #20784d;
            transition: all 0.3s ease; z-index: 1000;
          "
          onmouseover="this.style.transform='scale(1.3)'; this.style.boxShadow='0 4px 25px rgba(32, 120, 77, 0.8)'"
          onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 2px 12px rgba(32, 120, 77, 0.6)'"
          onclick="window.goToUserLocation()"
          title="Cliquer pour revenir à votre position">
            <div style="
              position: absolute; top: -6px; left: -6px; right: -6px; bottom: -6px;
              border-radius: 50%; border: 2px solid #20784d;
              opacity: 0.5; animation: userEdgePulse 1.5s ease-in-out infinite;
            "></div>
            <div style="
              position: absolute; top: -12px; left: -12px; right: -12px; bottom: -12px;
              border-radius: 50%; border: 2px solid #20784d;
              opacity: 0.2; animation: userEdgePulse 1.5s ease-in-out 0.5s infinite;
            "></div>
            <span style="position: relative; z-index: 1; font-size: 18px;">📍</span>
          </div>
        `,
        iconSize: [40, 40],
        iconAnchor: [20, 20]
      });

      userEdgeMarker = L.marker(edgePosition, {
        icon: userEdgeIcon,
        riseOnHover: true,
        zIndexOffset: 1000
      }).addTo(map);

      userEdgeMarker.bindPopup(`
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
    let edgeLat = Math.max(south, Math.min(north, position.lat));
    let edgeLng = Math.max(west, Math.min(east, position.lng));

    if (edgeLat === position.lat && edgeLng === position.lng) {
      const latDist = Math.max(position.lat - south, north - position.lat);
      const lngDist = Math.max(position.lng - west, east - position.lng);
      if (latDist > lngDist) {
        edgeLat = position.lat > (south + north) / 2 ? north : south;
      } else {
        edgeLng = position.lng > (west + east) / 2 ? east : west;
      }
    }
    return { lat: edgeLat, lng: edgeLng };
  }

  function getTooltipDirection(position, bounds) {
    const center = bounds.getCenter();
    const isTop = position.lat > center.lat;
    const isBottom = position.lat < center.lat;
    const isLeft = position.lng < center.lng;
    const isRight = position.lng > center.lng;

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

  function addUserLocationMarker() {
    if (!mapInitialized || !userLocation || !L) return;
    if (userMarker) map.removeLayer(userMarker);

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
      popupAnchor: [0, -34]
    });

    userMarker = L.marker([userLocation.lat, userLocation.lng], {
      icon: userIcon,
      zIndexOffset: 1000
    }).addTo(map);

    userMarker.bindPopup(`
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

  $: if (mapInitialized && userLocation) {
    addUserLocationMarker();
    // Recentrer éventuellement
    if (map) map.setView([userLocation.lat, userLocation.lng], 14);
  }

  function addLegend() {
    if (!mapInitialized || !L) return;
    const legend = L.control({ position: 'bottomright' });
    legend.onAdd = function () {
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

  function setupMapEvents() {
    if (!mapInitialized) return;
    map.on('moveend', () => updateEdgeMarkers(establishments, userLocation));
    map.on('zoomend', () => updateEdgeMarkers(establishments, userLocation));
  }
</script>

<div id="map" class="w-full h-full absolute inset-0"></div>

<style>
  :global(.leaflet-container) {
    font-family: "Fredoka", sans-serif !important;
  }

  :global(.leaflet-control-attribution) {
    display: none !important;
  }

  :global(.custom-marker),
  :global(.user-marker),
  :global(.edge-marker),
  :global(.user-edge-marker) {
    background: transparent !important;
    border: none !important;
  }

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

  :global(.user-marker-container) {
    position: relative;
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }

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