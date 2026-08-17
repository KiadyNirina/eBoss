<!-- Frontend/src/components/etablissement/grades/NoteForm.svelte -->
<script>
  import { createEventDispatcher } from 'svelte';
  import Icon from '@iconify/svelte';

  const dispatch = createEventDispatcher();

  export let note = {
    eleve: null,
    note: null,
    appreciation: '',
    absent: false
  };

  let form = {
    note: note.note,
    appreciation: note.appreciation || '',
    absent: note.absent || false
  };

  let error = null;
  let submitting = false;

  $: if (form.absent) {
    form.note = null;
  }

  function handleSubmit() {
    if (!form.absent && (form.note === null || form.note === '')) {
      error = 'Veuillez saisir une note ou cocher "Absent".';
      return;
    }

    submitting = true;
    error = null;

    dispatch('save', {
      eleve: note.eleve,
      note: form.absent ? null : parseFloat(form.note),
      appreciation: form.appreciation,
      absent: form.absent
    });
  }
</script>

<form on:submit|preventDefault={handleSubmit} class="space-y-4">
  <div>
    <h3 class="text-lg font-medium text-gray-900">Modifier la note</h3>
    <p class="text-sm text-gray-500">
      Élève : {note.eleve_nom || 'ID ' + note.eleve}
    </p>
  </div>

  <div>
    <label class="block text-sm font-medium text-gray-700">Note sur 20</label>
    <input 
      type="number" 
      step="0.01" 
      min="0" 
      max="20" 
      bind:value={form.note}
      disabled={form.absent}
      class="p-2 mt-1 block w-full rounded-md border border-gray-300 focus:border-green-500 focus:ring-green-500 sm:text-sm disabled:bg-gray-100"
    >
  </div>

  <div>
    <label class="block text-sm font-medium text-gray-700">Appréciation</label>
    <textarea 
      rows="3" 
      bind:value={form.appreciation}
      class="p-2 mt-1 block w-full rounded-md border border-gray-300 focus:border-green-500 focus:ring-green-500 sm:text-sm"
    ></textarea>
  </div>

  <div class="flex items-center">
    <input 
      type="checkbox" 
      id="absent" 
      bind:checked={form.absent}
      class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
    >
    <label for="absent" class="ml-2 block text-sm text-gray-900">
      Absent
    </label>
  </div>

  {#if error}
    <div class="rounded-md bg-red-50 p-4">
      <div class="flex">
        <div class="flex-shrink-0">
          <Icon icon="heroicons:x-circle" class="h-5 w-5 text-red-400" />
        </div>
        <div class="ml-3">
          <p class="text-sm text-red-700">{error}</p>
        </div>
      </div>
    </div>
  {/if}

  <div class="flex justify-end space-x-3">
    <button 
      type="button" 
      on:click={() => dispatch('cancel')}
      class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
    >
      Annuler
    </button>
    <button 
      type="submit" 
      disabled={submitting}
      class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 disabled:opacity-50"
    >
      <Icon icon="heroicons:check" class="-ml-1 mr-2 h-5 w-5" />
      Enregistrer
    </button>
  </div>
</form>