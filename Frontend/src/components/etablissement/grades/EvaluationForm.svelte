<!-- Frontend/src/components/etablissement/grades/EvaluationForm.svelte -->
<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import Icon from '@iconify/svelte';
  import { authApi } from '$lib/api';

  const dispatch = createEventDispatcher();

  // Options chargées depuis l'API
  let classOptions = [];
  let subjectOptions = [];
  let periodOptions = [];
  let professeurOptions = [];

  let loadingOptions = true;
  let submitting = false;
  let error = null;

  // Formulaire initial
  let form = {
    nom: '',
    matiere: '',
    classe: '',
    professeur: '',
    periode: '',
    date: '',
    coefficient: 1.0,
    type: 'controle',
    description: '',
    bareme: 20
  };

  onMount(async () => {
    try {
      const [classesRes, matieresRes, periodesRes, professeursRes] = await Promise.all([
        authApi.getClasses(),
        authApi.getMatieres(),
        authApi.getPeriodes(),
        authApi.getProfesseurs()
      ]);

      classOptions = (classesRes.results || classesRes).map(c => ({ value: c.id, label: c.nom }));
      subjectOptions = (matieresRes.results || matieresRes).map(m => ({ value: m.id, label: m.nom }));
      periodOptions = (periodesRes.results || periodesRes).map(p => ({ value: p.id, label: p.nom }));
      professeurOptions = (professeursRes.results || professeursRes).map(p => ({
        value: p.id,
        label: `${p.user.first_name} ${p.user.last_name}`.trim() || 'Professeur sans nom'
      }));
    } catch (err) {
      error = 'Impossible de charger les options du formulaire';
      console.error(err);
    } finally {
      loadingOptions = false;
    }
  });

  async function handleSubmit() {
    submitting = true;
    error = null;
    try {
      const payload = {
        ...form,
        coefficient: parseFloat(form.coefficient),
        bareme: parseFloat(form.bareme) || null,
        classe: parseInt(form.classe),
        matiere: parseInt(form.matiere),
        professeur: parseInt(form.professeur),
        periode: form.periode ? parseInt(form.periode) : null
      };

      const result = await authApi.createEvaluation(payload);
      dispatch('created', result);
    } catch (err) {
      error = err.message || 'Erreur lors de la création de l’évaluation';
    } finally {
      submitting = false;
    }
  }
</script>

<form on:submit|preventDefault={handleSubmit} class="space-y-6">
  <div>
    <h2 class="text-lg font-medium text-gray-900">Nouvelle évaluation</h2>
    <p class="text-sm text-gray-500">Remplissez les informations de l’évaluation</p>
  </div>

  {#if loadingOptions}
    <div class="text-center text-gray-500">Chargement des options...</div>
  {:else}
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
      <!-- Nom -->
      <div class="sm:col-span-2">
        <label class="block text-sm font-medium text-gray-700">Nom de l'évaluation *</label>
        <input type="text" bind:value={form.nom} required
               class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm">
      </div>

      <!-- Matière -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Matière *</label>
        <select bind:value={form.matiere} required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm">
          <option value="">Sélectionner</option>
          {#each subjectOptions as option}
            <option value={option.value}>{option.label}</option>
          {/each}
        </select>
      </div>

      <!-- Classe -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Classe *</label>
        <select bind:value={form.classe} required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm">
          <option value="">Sélectionner</option>
          {#each classOptions as option}
            <option value={option.value}>{option.label}</option>
          {/each}
        </select>
      </div>

      <!-- Professeur -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Professeur *</label>
        <select bind:value={form.professeur} required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm">
          <option value="">Sélectionner</option>
          {#each professeurOptions as option}
            <option value={option.value}>{option.label}</option>
          {/each}
        </select>
      </div>

      <!-- Période -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Période</label>
        <select bind:value={form.periode}
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm">
          <option value="">Aucune</option>
          {#each periodOptions as option}
            <option value={option.value}>{option.label}</option>
          {/each}
        </select>
      </div>

      <!-- Date -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Date *</label>
        <input type="date" bind:value={form.date} required
               class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm">
      </div>

      <!-- Coefficient -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Coefficient</label>
        <input type="number" step="0.1" min="0" bind:value={form.coefficient}
               class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm">
      </div>

      <!-- Type -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Type</label>
        <select bind:value={form.type}
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm">
          <option value="controle">Contrôle</option>
          <option value="examen">Examen</option>
          <option value="devoir">Devoir maison</option>
          <option value="projet">Projet</option>
          <option value="autre">Autre</option>
        </select>
      </div>

      <!-- Barème -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Barème</label>
        <input type="number" step="0.01" min="0" bind:value={form.bareme}
               class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm">
      </div>

      <!-- Description -->
      <div class="sm:col-span-2">
        <label class="block text-sm font-medium text-gray-700">Description</label>
        <textarea rows="3" bind:value={form.description}
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm"></textarea>
      </div>
    </div>
  {/if}

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
    <button type="button" on:click={() => dispatch('cancel')}
            class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
      Annuler
    </button>
    <button type="submit" disabled={submitting || loadingOptions}
            class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 disabled:opacity-50">
      {#if submitting}
        <Icon icon="heroicons:arrow-path" class="animate-spin -ml-1 mr-2 h-5 w-5" />
        Création...
      {:else}
        <Icon icon="heroicons:check" class="-ml-1 mr-2 h-5 w-5" />
        Créer l'évaluation
      {/if}
    </button>
  </div>
</form>