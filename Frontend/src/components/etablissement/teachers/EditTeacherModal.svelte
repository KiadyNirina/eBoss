<script>
  import Icon from '@iconify/svelte';
  import { authApi } from '$lib/api';
  import { createEventDispatcher } from 'svelte';
  import { user } from '$lib/stores';
  import { fade, fly } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';

  export let isOpen = false;
  export let teacher = null;
  export let classOptions = [];
  export let subjectOptions = [];
  export let yearOptions = [];

  const dispatch = createEventDispatcher();
  let etablissementId = $user?.profile?.id ?? null;
  let isLoading = false;

  let formData = {
    first_name: '',
    last_name: '',
    email: '',
    telephone: '',
    etablissement: etablissementId,
    annee_scolaire: null,
    matieres: [],
    classes: []
  };

  let errors = {
    general: '',
    annee_scolaire: '',
    matieres: '',
    classes: ''
  };

  // Pour la sélection des matières
  let selectedMatiereTemp = '';
  let selectedClasseTemp = '';

  // Initialiser les données du formulaire quand un professeur est fourni
  $: if (teacher?.id && isOpen) {

    const classes = teacher.classes_details?.map(
        c => Number(c.id)
    ) ?? [];

    const matieres = teacher.matieres_details?.map(
        m => Number(m.id)
    ) ?? [];

    formData = {
        first_name: teacher.user?.first_name || '',
        last_name: teacher.user?.last_name || '',
        email: teacher.user?.email || '',
        telephone: teacher.user?.telephone || '',

        etablissement: teacher.etablissement ?? etablissementId,

        annee_scolaire:
        teacher.annee_scolaire?.id ?? '',

        matieres,
        classes
    };

    selectedMatiereTemp = '';
    selectedClasseTemp = '';
  }

  // Fonctions pour ajouter/supprimer des matières
  function addMatiere() {
    console.log("Tentative d'ajout de matière:", selectedMatiereTemp);
    const matiereId = Number(selectedMatiereTemp);
    
    if (selectedMatiereTemp && !formData.matieres.includes(matiereId)) {
      formData.matieres = [...formData.matieres, matiereId];
      selectedMatiereTemp = '';
      errors.matieres = '';
      console.log("Matières après ajout:", formData.matieres);
    } else if (selectedMatiereTemp && formData.matieres.includes(matiereId)) {
      console.log("Cette matière est déjà sélectionnée");
    }
  }

  function removeMatiere(matiereId) {
    console.log("Suppression de la matière:", matiereId);
    formData.matieres = formData.matieres.filter(id => id !== matiereId);
    if (formData.matieres.length === 0) {
      errors.matieres = 'Veuillez sélectionner au moins une matière';
    } else {
      errors.matieres = '';
    }
    console.log("Matières après suppression:", formData.matieres);
  }

  // Fonctions pour ajouter/supprimer des classes
  function addClasse() {
    console.log("Tentative d'ajout de classe:", selectedClasseTemp);
    const classeId = Number(selectedClasseTemp);
    
    if (selectedClasseTemp && !formData.classes.includes(classeId)) {
      formData.classes = [...formData.classes, classeId];
      selectedClasseTemp = '';
      errors.classes = '';
      console.log("Classes après ajout:", formData.classes);
    } else if (selectedClasseTemp && formData.classes.includes(classeId)) {
      console.log("Cette classe est déjà sélectionnée");
    }
  }

  function removeClasse(classeId) {
    console.log("Suppression de la classe:", classeId);
    formData.classes = formData.classes.filter(id => id !== classeId);
    if (formData.classes.length === 0) {
      errors.classes = 'Veuillez sélectionner au moins une classe';
    } else {
      errors.classes = '';
    }
    console.log("Classes après suppression:", formData.classes);
  }

  async function handleSubmit() {
    if (isLoading) return;
    
    // Validation
    if (formData.matieres.length === 0) {
      errors.matieres = 'Veuillez sélectionner au moins une matière';
      return;
    }
    if (formData.classes.length === 0) {
      errors.classes = 'Veuillez sélectionner au moins une classe';
      return;
    }
    
    try {
      isLoading = true;
      errors.general = '';
      
      const updateData = {
        user: {
          first_name: formData.first_name,
          last_name: formData.last_name,
          email: formData.email,
          telephone: formData.telephone || '',
          user_type: "professeur"
        },
        etablissement: formData.etablissement,
        classes: formData.classes,
        matieres: formData.matieres
      };

      console.log('Données envoyées à l\'API:', JSON.stringify(updateData, null, 2));

      await authApi.updateProfesseur(teacher.id, updateData);
      
      dispatch('success', {
        message: 'Professeur modifié avec succès'
      });
      
      closeModal();
    } catch (e) {
      console.error('Erreur lors de la mise à jour:', e);
      errors.general = e.message || "Une erreur s'est produite lors de la mise à jour";
    } finally {
      isLoading = false;
    }
  }

  function closeModal() {
    dispatch('close');
  }

  $: if (isOpen) {
    errors.general = '';
  }
</script>

{#if isOpen}
<div
  class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50"
  transition:fade={{duration:200}}
>
  <div
    class="bg-white rounded-lg shadow-xl p-6 w-full max-w-md max-h-[80vh] overflow-y-auto"
    in:fly={{y:-50,duration:300,easing:quintOut}}
  >
    <div class="flex justify-between mb-4">
      <h2 class="text-xl font-bold">
        Modifier le professeur
      </h2>
      <button 
        on:click={closeModal}
        class="text-gray-400 hover:text-gray-600 transition-colors"
      >
        <Icon icon="heroicons:x-mark" class="h-6 w-6" />
      </button>
    </div>

    <form on:submit|preventDefault={handleSubmit}>
      <!-- PRENOM -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700">
          Prénom *
        </label>
        <input
          class="mt-1 w-full border rounded-lg p-2 focus:ring-green-500 focus:border-green-500"
          bind:value={formData.first_name}
          placeholder="Prénom"
          required
        />
      </div>

      <!-- NOM -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700">
          Nom *
        </label>
        <input
          class="mt-1 w-full border rounded-lg p-2 focus:ring-green-500 focus:border-green-500"
          bind:value={formData.last_name}
          placeholder="Nom"
          required
        />
      </div>

      <!-- EMAIL -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700">
          Email *
        </label>
        <input
          type="email"
          class="mt-1 w-full border rounded-lg p-2 focus:ring-green-500 focus:border-green-500"
          bind:value={formData.email}
          placeholder="Email"
          required
        />
      </div>

      <!-- TELEPHONE -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700">
          Téléphone
        </label>
        <input
          class="mt-1 w-full border rounded-lg p-2 focus:ring-green-500 focus:border-green-500"
          bind:value={formData.telephone}
          placeholder="Téléphone"
        />
      </div>

      <!-- ANNEE SCOLAIRE -->
      <div class="mb-4">
        <label for="annee_scolaire" class="block text-sm font-medium text-gray-700">
          Année scolaire
        </label>
        <div class="relative">
          <select
            id="annee_scolaire"
            bind:value={formData.annee_scolaire}
            class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm transition-colors duration-200"
            disabled={isLoading}
          >
            <option value="">Sélectionner une année</option>
            {#each yearOptions as option}
              <option value={option.value}>{option.label}</option>
            {/each}
          </select>
        </div>
      </div>

      <!-- MATIERES -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700">
          Matières *
        </label>
        
        <!-- Sélecteur + Bouton Ajouter -->
        <div class="flex gap-2">
          <select
            bind:value={selectedMatiereTemp}
            class="flex-1 border rounded-lg p-2 focus:ring-green-500 focus:border-green-500"
            disabled={isLoading}
          >
            <option value="">-- Sélectionner une matière --</option>
            {#each subjectOptions as option}
              <option value={String(option.value)}>
                {option.label}
              </option>
            {/each}
          </select>
          <button
            type="button"
            on:click={addMatiere}
            class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1"
            disabled={!selectedMatiereTemp || isLoading}
          >
            <Icon icon="heroicons:plus" class="h-5 w-5" />
            Ajouter
          </button>
        </div>

        <!-- Liste des matières sélectionnées -->
        <div class="mt-3">
          {#if formData.matieres.length === 0}
            <p class="text-sm text-gray-500 italic">Aucune matière sélectionnée</p>
          {:else}
            <div class="flex flex-wrap gap-2">
              {#each formData.matieres as matiereId}
                {@const matiere = subjectOptions.find(m => Number(m.value) === matiereId)}
                {#if matiere}
                  <span class="inline-flex items-center gap-1 bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                    {matiere.label}
                    <button
                      type="button"
                      on:click={() => removeMatiere(matiereId)}
                      class="hover:text-red-600 transition-colors ml-1"
                    >
                      <Icon icon="heroicons:x-mark" class="h-4 w-4" />
                    </button>
                  </span>
                {/if}
              {/each}
            </div>
          {/if}
        </div>

        {#if errors.matieres}
          <p class="mt-1 text-sm text-red-600">{errors.matieres}</p>
        {/if}
      </div>

      <!-- CLASSES -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700">
          Classes *
        </label>
        
        <!-- Sélecteur + Bouton Ajouter -->
        <div class="flex gap-2">
          <select
            bind:value={selectedClasseTemp}
            class="flex-1 border rounded-lg p-2 focus:ring-green-500 focus:border-green-500"
            disabled={isLoading}
          >
            <option value="">-- Sélectionner une classe --</option>
            {#each classOptions as option}
              <option value={String(option.value)}>
                {option.label}
              </option>
            {/each}
          </select>
          <button
            type="button"
            on:click={addClasse}
            class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1"
            disabled={!selectedClasseTemp || isLoading}
          >
            <Icon icon="heroicons:plus" class="h-5 w-5" />
            Ajouter
          </button>
        </div>

        <!-- Liste des classes sélectionnées -->
        <div class="mt-3">
          {#if formData.classes.length === 0}
            <p class="text-sm text-gray-500 italic">Aucune classe sélectionnée</p>
          {:else}
            <div class="flex flex-wrap gap-2">
              {#each formData.classes as classeId}
                {@const classe = classOptions.find(c => Number(c.value) === classeId)}
                {#if classe}
                  <span class="inline-flex items-center gap-1 bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                    {classe.label}
                    <button
                      type="button"
                      on:click={() => removeClasse(classeId)}
                      class="hover:text-red-600 transition-colors ml-1"
                    >
                      <Icon icon="heroicons:x-mark" class="h-4 w-4" />
                    </button>
                  </span>
                {/if}
              {/each}
            </div>
          {/if}
        </div>

        {#if errors.classes}
          <p class="mt-1 text-sm text-red-600">{errors.classes}</p>
        {/if}
      </div>

      {#if errors.general}
        <div class="bg-red-50 text-red-600 p-3 rounded mb-4 whitespace-pre-wrap text-sm">
          <strong>Erreur :</strong>
          {errors.general}
        </div>
      {/if}

      <div class="flex justify-end gap-3 mt-5">
        <button
          type="button"
          on:click={closeModal}
          class="px-4 py-2 border rounded-lg hover:bg-gray-50 transition-colors"
        >
          Annuler
        </button>
        <button
          type="submit"
          class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={isLoading || formData.classes.length === 0 || formData.matieres.length === 0}
        >
          {#if isLoading}
            Modification...
          {:else}
            Modifier
          {/if}
        </button>
      </div>
    </form>
  </div>
</div>
{/if}