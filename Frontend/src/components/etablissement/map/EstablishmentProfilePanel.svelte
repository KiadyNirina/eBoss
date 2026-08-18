<!-- src/components/etablissement/map/EstablishmentProfilePanel.svelte -->
<script>
  import Icon from '@iconify/svelte';

  export let show = false;
  export let profileData = null;
  export let loading = false;
  export let error = null;

  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  const typeLabels = {
    ecole: 'École primaire',
    college: 'Collège',
    lycee: 'Lycée',
    universite: 'Université'
  };

  function formatDate(date) {
    if (!date) return 'N/A';
    return new Date(date).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  }
</script>

{#if show}
  <div class="w-full md:w-[450px] h-[50vh] md:h-full flex flex-col bg-white shadow-2xl z-20 shrink-0 overflow-hidden">
    <!-- En-tête -->
    <div class="p-4 border-b border-gray-100 flex items-center justify-between bg-white shrink-0">
      <h2 class="text-lg font-medium text-gray-900 truncate">
        {profileData?.nom || 'Profil'}
      </h2>
      <button on:click={() => dispatch('close')} class="p-2 rounded-full hover:bg-gray-100 text-gray-500 transition-colors">
        <Icon icon="heroicons:x-mark" class="h-5 w-5" />
      </button>
    </div>

    <!-- Contenu -->
    <div class="flex-1 overflow-y-auto p-4 sm:p-5 bg-gray-50">
      {#if loading}
        <div class="flex flex-col items-center justify-center py-20">
          <div class="animate-spin rounded-full h-12 w-12 border-4 border-gray-200 border-t-[#20784d]"></div>
          <p class="mt-4 text-gray-500">Chargement...</p>
        </div>
      {:else if error}
        <div class="text-center p-6">
          <Icon icon="heroicons:exclamation-triangle" class="h-8 w-8 text-red-500 mx-auto" />
          <p class="mt-2 text-red-600">{error}</p>
        </div>
      {:else if profileData}
        {@const etablissement = profileData}
        {@const user = profileData.user || {}}

        <div class="bg-white rounded-[2rem] overflow-hidden mb-4">
          <div class="p-5">
            <div class="flex flex-col sm:flex-row items-center gap-4">
              <div class="shrink-0">
                {#if user.profile_image}
                  <div class="h-28 w-28 rounded-full overflow-hidden border-2 border-gray-200">
                    <img src={user.profile_image} alt="Logo" class="h-full w-full object-cover" />
                  </div>
                {:else}
                  <div class="h-28 w-28 rounded-lg bg-gradient-to-br from-green-100 to-green-200 flex items-center justify-center border-2 border-gray-200">
                    <Icon icon="heroicons:building-office-2" class="w-12 h-12 text-green-600" />
                  </div>
                {/if}
              </div>

              <div class="flex-1 text-center sm:text-left">
                <h3 class="text-xl font-medium text-gray-900">{etablissement.nom || 'Non renseigné'}</h3>
                <p class="text-sm text-gray-500 mt-1">
                  {typeLabels[etablissement.type_etablissement] || etablissement.type_etablissement || 'Non renseigné'}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-[2rem] overflow-hidden mb-4">
          <div class="px-5 py-4 border-b border-gray-200 bg-gray-50">
            <h2 class="text-sm font-semibold text-gray-700">Présentation & Contact</h2>
          </div>
          <div class="p-5 space-y-4">
            {#if etablissement.description}
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Description</label>
                <p class="text-sm text-gray-900">{etablissement.description}</p>
              </div>
            {/if}

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Site web</label>
                {#if etablissement.site_web}
                  <a href={etablissement.site_web} target="_blank" class="text-sm text-green-600 hover:underline break-all">{etablissement.site_web}</a>
                {:else}
                  <p class="text-sm text-gray-400">Non renseigné</p>
                {/if}
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Téléphone</label>
                <p class="text-sm text-gray-900">{user.telephone || 'Non renseigné'}</p>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Adresse</label>
                <p class="text-sm text-gray-900">{etablissement.adresse || 'Non renseignée'}</p>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Email</label>
                {#if user.email}
                  <a href="mailto:{user.email}" class="text-sm text-green-600 hover:underline break-all">{user.email}</a>
                {:else}
                  <p class="text-sm text-gray-400">Non renseigné</p>
                {/if}
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4">
          <div class="bg-white rounded-[2rem] p-4 text-center">
            <p class="text-xl font-bold text-blue-600">{etablissement.stats?.total_eleves ?? 0}</p>
            <p class="text-xs text-gray-500">Élèves</p>
          </div>
          <div class="bg-white rounded-[2rem] p-4 text-center">
            <p class="text-xl font-bold text-green-600">{etablissement.stats?.total_professeurs ?? 0}</p>
            <p class="text-xs text-gray-500">Professeurs</p>
          </div>
          <div class="bg-white rounded-[2rem] p-4 text-center">
            <p class="text-xl font-bold text-purple-600">{etablissement.stats?.total_classes ?? 0}</p>
            <p class="text-xs text-gray-500">Classes</p>
          </div>
          <div class="bg-white rounded-[2rem] p-4 text-center">
            <p class="text-xl font-bold text-yellow-600">{etablissement.stats?.total_matieres ?? 0}</p>
            <p class="text-xs text-gray-500">Matières</p>
          </div>
        </div>

        {#if etablissement.annees_scolaires?.length}
          <div class="bg-white rounded-[2rem] overflow-hidden mb-4">
            <div class="px-5 py-4 border-b border-gray-200 bg-gray-50">
              <h2 class="text-sm font-semibold text-gray-700">Années scolaires</h2>
            </div>
            <div class="p-4">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {#each etablissement.annees_scolaires as annee}
                  <div class="p-3 border rounded-lg {annee.est_active ? 'bg-green-50 border-green-200' : 'border-gray-200'}">
                    <span class="font-medium text-sm">{annee.nom}</span>
                    {#if annee.est_active}
                      <span class="ml-2 px-2 py-0.5 text-xs bg-green-100 text-green-700 rounded-full">Active</span>
                    {/if}
                    <p class="text-xs text-gray-500 mt-1">{formatDate(annee.date_debut)} - {formatDate(annee.date_fin)}</p>
                  </div>
                {/each}
              </div>
            </div>
          </div>
        {/if}

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          {#if etablissement.classes?.length}
            <div class="bg-white rounded-[2rem] overflow-hidden">
              <div class="px-5 py-4 border-b border-gray-200 bg-gray-50">
                <h3 class="text-sm font-semibold text-gray-700">Classes</h3>
              </div>
              <ul class="divide-y divide-gray-100 p-4">
                {#each etablissement.classes.slice(0, 5) as classe}
                  <li class="py-2 flex justify-between text-sm">
                    <span>{classe.nom}</span>
                    {#if classe.niveau}<span class="text-gray-400">{classe.niveau}</span>{/if}
                  </li>
                {/each}
              </ul>
            </div>
          {/if}

          {#if etablissement.matieres?.length}
            <div class="bg-white rounded-[2rem] overflow-hidden">
              <div class="px-5 py-4 border-b border-gray-200 bg-gray-50">
                <h3 class="text-sm font-semibold text-gray-700">Matières</h3>
              </div>
              <ul class="divide-y divide-gray-100 p-4">
                {#each etablissement.matieres.slice(0, 5) as matiere}
                  <li class="py-2 text-sm">{matiere.nom}</li>
                {/each}
              </ul>
            </div>
          {/if}
        </div>
      {/if}
    </div>
  </div>
{/if}