<!-- Frontend/src/components/etablissement/grades/NotesManager.svelte -->
<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import Icon from '@iconify/svelte';
  import { authApi } from '$lib/api';

  const dispatch = createEventDispatcher();

  export let evaluation;

  let eleves = []; 
  let notesForm = []; 
  let loading = true;
  let saving = false;
  let error = null;

  onMount(async () => {
    try {
      const response = await authApi.getEleves({ classe: evaluation.classe });
      console.log(response);
      eleves = response.results || response;

      const detail = await authApi.getEvaluationDetail(evaluation.id);
      const existingNotes = detail.notes || [];

      notesForm = eleves.map(eleve => {
        const existing = existingNotes.find(n => n.eleve === eleve.id);
        return {
          eleve: eleve.id,
          eleve_nom: eleve.user ? `${eleve.user.first_name} ${eleve.user.last_name}` : `Élève ${eleve.id}`,
          note: existing ? existing.note : null,
          appreciation: existing ? existing.appreciation : '',
          absent: existing ? existing.absent : false
        };
      });
    } catch (err) {
      error = 'Impossible de charger les élèves ou les notes existantes';
      console.error(err);
    } finally {
      loading = false;
    }
  });

  function handleSaveAll() {
    saving = true;
    error = null;

    const notesPayload = notesForm
      .filter(item => item.note !== null || item.absent || item.appreciation)
      .map(item => ({
        eleve: item.eleve,
        note: item.absent ? null : parseFloat(item.note),
        appreciation: item.appreciation,
        absent: item.absent
      }));

    authApi.manageNotes(evaluation.id, notesPayload)
      .then((result) => {
        dispatch('saved', result);
      })
      .catch((err) => {
        error = err.message || 'Erreur lors de l’enregistrement des notes';
      })
      .finally(() => {
        saving = false;
      });

    if (typeof window !== 'undefined') {
      window.location.reload();
    }
  }
</script>

<div class="space-y-6">
  <div>
    <h2 class="text-lg font-medium text-gray-900">Saisie des notes</h2>
    <p class="text-sm text-gray-500">
      {evaluation.nom} - {evaluation.classe_nom}
    </p>
  </div>

  {#if loading}
    <div class="text-center text-gray-500">Chargement des élèves...</div>
  {:else if error && eleves.length === 0}
    <div class="rounded-md bg-red-50 p-4">
      <p class="text-sm text-red-700">{error}</p>
    </div>
  {:else}
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">Élève</th>
            <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">Note /20</th>
            <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">Appréciation</th>
            <th class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase">Absent</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          {#each notesForm as item, index}
            <tr>
              <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-900">
                {item.eleve_nom}
              </td>
              <td class="px-3 py-2 whitespace-nowrap">
                <input 
                  type="number" 
                  step="0.01" 
                  min="0" 
                  max="20" 
                  bind:value={item.note}
                  disabled={item.absent}
                  class="p-2 block w-24 rounded-md border border-gray-300 focus:border-green-500 focus:ring-green-500 sm:text-sm disabled:bg-gray-100"
                >
              </td>
              <td class="px-3 py-2">
                <input 
                  type="text" 
                  bind:value={item.appreciation}
                  class="p-2 block w-full rounded-md border border-gray-300 focus:border-green-500 focus:ring-green-500 sm:text-sm"
                >
              </td>
              <td class="px-3 py-2 whitespace-nowrap text-center">
                <input 
                  type="checkbox" 
                  bind:checked={item.absent}
                  on:change={() => { if (item.absent) item.note = null; }}
                  class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                >
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>

    {#if error}
      <div class="rounded-md bg-red-50 p-4">
        <p class="text-sm text-red-700">{error}</p>
      </div>
    {/if}

    <div class="flex justify-end space-x-3">
      <button 
        type="button" 
        on:click={() => dispatch('cancel')}
        class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
      >
        Fermer
      </button>
      <button 
        type="button" 
        on:click={handleSaveAll}
        disabled={saving}
        class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 disabled:opacity-50"
      >
        {#if saving}
          <Icon icon="heroicons:arrow-path" class="animate-spin -ml-1 mr-2 h-5 w-5" />
          Enregistrement...
        {:else}
          <Icon icon="heroicons:check" class="-ml-1 mr-2 h-5 w-5" />
          Enregistrer les notes
        {/if}
      </button>
    </div>
  {/if}
</div>