<!-- src/lib/components/AddressAutocomplete.svelte -->
<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import GeocodingService from '$lib/geocoding.js';
  import Icon from '@iconify/svelte';

  const dispatch = createEventDispatcher();

  export let value = '';
  export let placeholder = 'Saisissez une adresse...';
  export let label = 'Adresse';
  export let required = false;
  export let disabled = false;
  export let countryFilter = 'mg';
  export let language = 'fr';
  export let showMap = false;
  export let minChars = 3;

  let suggestions = [];
  let isSearching = false;
  let selectedSuggestion = null;
  let isFocused = false;
  let inputElement = null;
  let coordinates = null;
  let geocodeStatus = '';
  let searchTimeout = null;
  let hasSearched = false;

  export let geocodedData = null;
  export let isValid = false;

  async function handleInput(event) {
    const query = event.target.value;
    value = query;
    selectedSuggestion = null;
    isValid = false;
    hasSearched = false;

    if (query.length < minChars) {
      suggestions = [];
      return;
    }

    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(async () => {
      await searchAddress(query);
    }, 300);
  }

  async function searchAddress(query) {
    if (query.length < minChars) return;

    isSearching = true;
    hasSearched = true;
    try {
      const options = {
        limit: 5,
        language: language,
        countrycodes: countryFilter || undefined
      };

      const results = await GeocodingService.search(query, options);
      suggestions = results;

      // Si aucun résultat et que la recherche est terminée
      if (results.length === 0 && query.length >= minChars) {
        geocodeStatus = 'ℹ️ Aucune adresse trouvée. Vous pouvez utiliser le géocodage manuel.';
      } else {
        geocodeStatus = '';
      }

      dispatch('search', { query, results });
    } catch (error) {
      console.error('Erreur de recherche:', error);
      suggestions = [];
      geocodeStatus = '❌ Erreur de recherche. Veuillez réessayer ou utiliser le géocodage manuel.';
    } finally {
      isSearching = false;
    }
  }

  async function selectSuggestion(suggestion) {
    selectedSuggestion = suggestion;
    value = suggestion.display_name;
    suggestions = [];
    isValid = true;
    hasSearched = false;

    coordinates = {
      lat: suggestion.latitude,
      lng: suggestion.longitude
    };

    geocodedData = suggestion;
    geocodeStatus = '✅ Adresse géocodée';

    dispatch('select', {
      address: suggestion.display_name,
      latitude: suggestion.latitude,
      longitude: suggestion.longitude,
      fullData: suggestion
    });

    if (countryFilter && suggestion.address?.country_code !== countryFilter) {
      geocodeStatus = '⚠️ Adresse en dehors du pays sélectionné';
      isValid = false;
    }
  }

  function clearAddress() {
    value = '';
    suggestions = [];
    selectedSuggestion = null;
    coordinates = null;
    isValid = false;
    geocodedData = null;
    geocodeStatus = '';
    hasSearched = false;

    dispatch('clear');
  }

  export function getCoordinates() {
    return coordinates;
  }

  export function getGeocodedData() {
    return geocodedData;
  }

  export function isValidAddress() {
    return isValid;
  }

  onMount(() => {
    return () => {
      if (searchTimeout) {
        clearTimeout(searchTimeout);
      }
    };
  });
</script>

<div class="address-autocomplete">
  {#if label}
    <label for="address-input" class="block text-sm font-medium text-gray-700 mb-1">
      {label}
      {#if required}
        <span class="text-red-500">*</span>
      {/if}
    </label>
  {/if}

  <div class="relative">
    <div class="flex gap-1">
      <div class="relative flex-1" style="line-height: normal;">
        <input
          id="address-input"
          type="text"
          bind:this={inputElement}
          bind:value={value}
          on:input={handleInput}
          on:focus={() => isFocused = true}
          on:blur={() => setTimeout(() => isFocused = false, 200)}
          placeholder={placeholder}
          disabled={disabled}
          required={required}
          class={`
            w-full px-4 py-2.5 border rounded-lg
            ${isValid ? 'border-green-400 bg-green-50' : 'border-gray-300'}
            ${!isValid && value.length > 0 && !isSearching && hasSearched && suggestions.length === 0 ? 'border-yellow-300 bg-yellow-50' : ''}
            ${!isValid && value.length > 0 && !isSearching && !hasSearched ? 'border-gray-300' : ''}
            focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent
            transition-all
            pr-10
          `}
        />

        <div class="absolute right-3 top-1/2 -translate-y-1/2">
          {#if isSearching}
            <div class="animate-spin h-5 w-5 border-2 border-green-500 border-t-transparent rounded-full"></div>
          {:else if isValid}
            <Icon icon="heroicons:check-circle" class="h-5 w-5 text-green-500" />
          {:else if value && !isValid && !isSearching && hasSearched && suggestions.length === 0}
            <Icon icon="heroicons:exclamation-circle" class="h-5 w-5 text-yellow-500" />
          {:else if value && !isValid && !isSearching}
            <Icon icon="heroicons:exclamation-circle" class="h-5 w-5 text-yellow-500" />
          {/if}
        </div>

        {#if suggestions.length > 0 && isFocused}
          <div class="absolute z-50 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-60 overflow-y-auto">
            {#each suggestions as suggestion}
              <button
                on:click={() => selectSuggestion(suggestion)}
                class="w-full text-left px-4 py-2 hover:bg-gray-100 transition-colors border-b border-gray-100 last:border-0"
              >
                <div class="text-sm font-medium text-gray-900">
                  {suggestion.display_name}
                </div>
                {#if suggestion.address}
                  <div class="text-xs text-gray-500 mt-0.5">
                    {suggestion.address.city || suggestion.address.town || ''}
                    {#if suggestion.address.country}
                      - {suggestion.address.country}
                    {/if}
                  </div>
                {/if}
                {#if suggestion.importance}
                  <div class="text-xs text-gray-400 mt-0.5">
                    Pertinence: {Math.round(suggestion.importance * 100)}%
                  </div>
                {/if}
              </button>
            {/each}
          </div>
        {/if}
      </div>

      <div class="flex gap-2 shrink-0">
        {#if value}
          <button
            type="button"
            on:click={clearAddress}
            class="px-3 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors flex items-center gap-1"
            title="Effacer"
          >
            <Icon icon="heroicons:x-mark" class="h-4 w-4" />
          </button>
        {/if}
      </div>
    </div>
  </div>

  <!-- Message d'information quand aucune suggestion n'est trouvée -->
  {#if !isSearching && hasSearched && suggestions.length === 0 && value.length >= minChars && !isValid}
    <div class="z-50 w-full mt-1 bg-yellow-50 border border-yellow-200 rounded-lg p-3 text-sm text-yellow-800">
      <div class="flex items-start gap-2">
        <Icon icon="heroicons:information-circle" class="h-5 w-5 text-yellow-600 flex-shrink-0 mt-0.5" />
        <div>
          <p class="font-medium">Aucune adresse trouvée</p>
          <p class="text-xs text-yellow-700 mt-1">
            Vérifiez l'orthographe ou utilisez le bouton 
            <span class="font-semibold">"Géocodage manuel"</span> 
            pour saisir les coordonnées directement.
          </p>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .address-autocomplete {
    width: 100%;
  }

  .address-autocomplete .absolute {
    animation: slideDown 0.2s ease-out;
  }

  @keyframes slideDown {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
</style>