<!-- src/components/etablissement/map/EstablishmentCard.svelte -->
<script>
  import { createEventDispatcher } from 'svelte';
  import Icon from '@iconify/svelte';
  import { formatDistance, calculateDistance } from './mapUtils';

  export let establishment;
  export let userLocation = null;

  const dispatch = createEventDispatcher();
  const typeLabels = {
    ecole: 'École primaire',
    college: 'Collège',
    lycee: 'Lycée',
    universite: 'Université'
  };

  function getDistance() {
    if (!userLocation || !establishment.lat || !establishment.lng) return null;
    return calculateDistance(userLocation.lat, userLocation.lng, establishment.lat, establishment.lng);
  }
</script>

<div
  class="bg-white p-4 rounded-[2rem] border border-gray-200 hover:border-green-600 cursor-pointer transition-all duration-200 group relative overflow-hidden"
  on:click={() => dispatch('select', establishment.id)}
>
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
      <h3 class="font-medium text-gray-900 group-hover:text-[#20784d] transition-colors line-clamp-1">{establishment.name}</h3>
      <p class="text-xs text-gray-500 mt-1 flex items-start gap-1">
        <Icon icon="heroicons:map-pin" class="h-3.5 w-3.5 shrink-0 mt-0.5 text-gray-400" />
        <span class="line-clamp-2">{establishment.address}</span>
      </p>

      <div class="flex flex-wrap items-center mt-3 gap-2">
        <span class="text-[10px] font-semibold uppercase tracking-wider px-2 py-1 bg-gray-100 text-gray-600 rounded-full">
          {typeLabels[establishment.type] || establishment.type}
        </span>

        {#if userLocation}
          <span class="text-xs font-medium text-[#20784d] bg-green-50 px-2 py-1 rounded-full flex items-center gap-1">
            <Icon icon="heroicons:arrows-right-left" class="h-3 w-3" />
            {formatDistance(getDistance())}
          </span>
        {/if}
      </div>
    </div>

    <div class="shrink-0">
      <button
        class="h-8 w-8 rounded-full bg-gray-50 flex items-center justify-center text-gray-400 group-hover:bg-[#20784d] group-hover:text-white transition-all shadow-sm"
        on:click={(e) => {
          e.stopPropagation();
          dispatch('select', establishment.id);
        }}
        title="Voir sur la carte"
      >
        <Icon icon="heroicons:chevron-right" class="h-4 w-4" />
      </button>
    </div>
  </div>
</div>