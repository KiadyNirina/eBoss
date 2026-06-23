<script>
  import Icon from '@iconify/svelte';
  import { authApi } from '$lib/api';
  import { createEventDispatcher } from 'svelte';
  import { user } from '$lib/stores';
  import { fade, fly } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';
  import { browser } from '$app/environment';

  export let isOpen = false;
  export let teacher = null;
  export let classOptions = [];
  export let subjectOptions = [];
  export let yearOptions = [];

  const dispatch = createEventDispatcher();
  let etablissementId = $user?.profile?.id ?? null;
  let isLoading = false;
  let isClosing = false;

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
    user: {
      first_name: '',
      last_name: '',
      email: '',
      telephone: ''
    },
    annee_scolaire: '',
    matieres: '',
    classes: '',
    general: ''
  };

  // Pour la sélection des matières
  let selectedMatiereTemp = '';
  let selectedClasseTemp = '';

  // Fonctions de validation
  function validateField(field, value) {
    switch (field) {
      case 'first_name':
        if (!value.trim()) return 'Le prénom est obligatoire';
        if (value.length < 2) return 'Le prénom doit contenir au moins 2 caractères';
        if (!/^[a-zA-ZÀ-ÿ\s\-']+$/.test(value)) return 'Le prénom contient des caractères invalides';
        return '';
        
      case 'last_name':
        if (!value.trim()) return 'Le nom est obligatoire';
        if (value.length < 2) return 'Le nom doit contenir au moins 2 caractères';
        if (!/^[a-zA-ZÀ-ÿ\s\-']+$/.test(value)) return 'Le nom contient des caractères invalides';
        return '';
        
      case 'email':
        if (!value.trim()) return 'L\'email est obligatoire';
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return 'Format d\'email invalide';
        return '';
        
      case 'telephone':
        if (!value.trim()) return 'Le téléphone est obligatoire';
        if (value && !/^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$/.test(value.replace(/\s/g, ''))) {
          return 'Format de téléphone invalide (ex: 06 12 34 56 78)';
        }
        return '';
        
      case 'annee_scolaire':
        if (!value) return 'L\'année scolaire est obligatoire';
        return '';
        
      default:
        return '';
    }
  }

  // Validation temps réel
  function handleFieldInput(field, value) {
    if (field === 'annee_scolaire') {
      errors[field] = validateField(field, value);
    } else {
      errors.user[field] = validateField(field, value);
    }
  }

  function handleFieldBlur(field, value) {
    handleFieldInput(field, value);
  }

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

    // Réinitialiser les erreurs
    errors = {
      user: {
        first_name: '',
        last_name: '',
        email: '',
        telephone: ''
      },
      annee_scolaire: '',
      matieres: '',
      classes: '',
      general: ''
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
  }

  // Validation du formulaire
  function validateForm() {
    let isValid = true;
    
    // Valider les champs user
    Object.keys(formData).forEach(field => {
      if (field !== 'etablissement' && field !== 'matieres' && field !== 'classes' && field !== 'telephone' && field !== 'annee_scolaire') {
        const error = validateField(field, formData[field]);
        errors.user[field] = error;
        if (error) isValid = false;
      }
    });
    
    // Valider telephone
    const telephoneError = validateField('telephone', formData.telephone);
    errors.user.telephone = telephoneError;
    if (telephoneError) isValid = false;

    // Valider annee_scolaire
    const anneeError = validateField('annee_scolaire', formData.annee_scolaire);
    errors.annee_scolaire = anneeError;
    if (anneeError) isValid = false;

    // Valider matieres et classes
    if (formData.matieres.length === 0) {
      errors.matieres = 'Veuillez sélectionner au moins une matière';
      return;
    }
    if (formData.classes.length === 0) {
      errors.classes = 'Veuillez sélectionner au moins une classe';
      isValid = false;
    } else {
      errors.classes = '';
    }
    
    return isValid;
  }

  async function handleSubmit() {
    if (isLoading) return;
    
    errors.general = '';

    if (!validateForm()) {
      errors.general = 'Veuillez corriger les erreurs dans le formulaire';
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
      
      await closeModalWithAnimation();
      dispatch('success', { message: 'Professeur modifié avec succès' });
      
      closeModal();
    } catch (e) {
      console.error('Erreur lors de la mise à jour:', e);
      errors.general = e.message || "Une erreur s'est produite lors de la mise à jour";
    } finally {
      isLoading = false;
    }
  }

  async function closeModalWithAnimation() {
    isClosing = true;
    await new Promise(resolve => setTimeout(resolve, 300));
    dispatch('close');
    isClosing = false;
  }

  function closeModal() {
    closeModalWithAnimation();
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
    out:fly={{y:-50,duration:200,easing:quintOut}}
  >
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-bold text-gray-900">
        Modifier le professeur
      </h2>
      <button 
        on:click={closeModal}
        class="text-gray-500 hover:text-gray-700 transition-colors duration-200"
        disabled={isLoading}
      >
        <Icon icon="heroicons:x-mark" class="h-6 w-6" />
      </button>
    </div>

    <form on:submit|preventDefault={handleSubmit}>
      <!-- PRENOM -->
      <div class="mb-4">
        <label for="first_name" class="block text-sm font-medium text-gray-700">
          Prénom
          {#if errors.user.first_name}
            <span class="text-red-500 ml-1">*</span>
          {/if}
        </label>
        <div class="relative">
          <input
            type="text"
            id="first_name"
            class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm transition-colors duration-200"
            class:border-red-500={errors.user.first_name}
            class:border-gray-300={!errors.user.first_name}
            bind:value={formData.first_name}
            on:input={() => handleFieldInput('first_name', formData.first_name)}
            on:blur={() => handleFieldBlur('first_name', formData.first_name)}
            placeholder="Prénom"
            disabled={isLoading}
          />
          {#if errors.user.first_name}
            <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
              <Icon icon="heroicons:exclamation-circle" class="h-5 w-5 text-red-500" />
            </div>
          {/if}
        </div>
        {#if errors.user.first_name}
          <p class="mt-1 text-sm text-red-600">{errors.user.first_name}</p>
        {/if}
      </div>

      <!-- NOM -->
      <div class="mb-4">
        <label for="last_name" class="block text-sm font-medium text-gray-700">
          Nom
          {#if errors.user.last_name}
            <span class="text-red-500 ml-1">*</span>
          {/if}
        </label>
        <div class="relative">
          <input
            type="text"
            id="last_name"
            class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm transition-colors duration-200"
            class:border-red-500={errors.user.last_name}
            class:border-gray-300={!errors.user.last_name}
            bind:value={formData.last_name}
            on:input={() => handleFieldInput('last_name', formData.last_name)}
            on:blur={() => handleFieldBlur('last_name', formData.last_name)}
            placeholder="Nom"
            disabled={isLoading}
          />
          {#if errors.user.last_name}
            <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
              <Icon icon="heroicons:exclamation-circle" class="h-5 w-5 text-red-500" />
            </div>
          {/if}
        </div>
        {#if errors.user.last_name}
          <p class="mt-1 text-sm text-red-600">{errors.user.last_name}</p>
        {/if}
      </div>

      <!-- EMAIL -->
      <div class="mb-4">
        <label for="email" class="block text-sm font-medium text-gray-700">
          Email
          {#if errors.user.email}
            <span class="text-red-500 ml-1">*</span>
          {/if}
        </label>
        <div class="relative">
          <input
            type="email"
            id="email"
            class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm transition-colors duration-200"
            class:border-red-500={errors.user.email}
            class:border-gray-300={!errors.user.email}
            bind:value={formData.email}
            on:input={() => handleFieldInput('email', formData.email)}
            on:blur={() => handleFieldBlur('email', formData.email)}
            placeholder="Email"
            disabled={isLoading}
          />
          {#if errors.user.email}
            <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
              <Icon icon="heroicons:exclamation-circle" class="h-5 w-5 text-red-500" />
            </div>
          {/if}
        </div>
        {#if errors.user.email}
          <p class="mt-1 text-sm text-red-600">{errors.user.email}</p>
        {/if}
      </div>

      <!-- TELEPHONE -->
      <div class="mb-4">
        <label for="telephone" class="block text-sm font-medium text-gray-700">
          Téléphone
          {#if errors.user.telephone}
            <span class="text-red-500 ml-1">*</span>
          {/if}
        </label>
        <div class="relative">
          <input
            type="tel"
            id="telephone"
            class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm transition-colors duration-200"
            class:border-red-500={errors.user.telephone}
            class:border-gray-300={!errors.user.telephone}
            bind:value={formData.telephone}
            on:input={() => handleFieldInput('telephone', formData.telephone)}
            on:blur={() => handleFieldBlur('telephone', formData.telephone)}
            placeholder="06 12 34 56 78"
            disabled={isLoading}
          />
          {#if errors.user.telephone}
            <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
              <Icon icon="heroicons:exclamation-circle" class="h-5 w-5 text-red-500" />
            </div>
          {/if}
        </div>
        {#if errors.user.telephone}
          <p class="mt-1 text-sm text-red-600">{errors.user.telephone}</p>
        {/if}
      </div>

      <!-- ANNEE SCOLAIRE -->
      <div class="mb-4">
        <label for="annee_scolaire" class="block text-sm font-medium text-gray-700">
          Année scolaire
          {#if errors.annee_scolaire}
            <span class="text-red-500 ml-1">*</span>
          {/if}
        </label>
        <div class="relative">
          <select
            id="annee_scolaire"
            bind:value={formData.annee_scolaire}
            on:input={() => handleFieldInput('annee_scolaire', formData.annee_scolaire)}
            on:blur={() => handleFieldBlur('annee_scolaire', formData.annee_scolaire)}
            class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm transition-colors duration-200"
            class:border-red-500={errors.annee_scolaire}
            class:border-gray-300={!errors.annee_scolaire}
            disabled={isLoading}
          >
            <option value="">Sélectionner une année</option>
            {#each yearOptions as option}
              <option value={option.value}>{option.label}</option>
            {/each}
          </select>
          {#if errors.annee_scolaire}
            <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
              <Icon icon="heroicons:exclamation-circle" class="h-5 w-5 text-red-500" />
            </div>
          {/if}
        </div>
        {#if errors.annee_scolaire}
          <p class="mt-1 text-sm text-red-600">{errors.annee_scolaire}</p>
        {/if}
      </div>

      <!-- MATIERES -->
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700">
          Matières
          {#if errors.matieres}
            <span class="text-red-500 ml-1">*</span>
          {/if}
        </label>
        
        <div class="flex gap-2">
          <select
            bind:value={selectedMatiereTemp}
            class="flex-1 border rounded-lg p-2 focus:ring-green-500 focus:border-green-500 sm:text-sm transition-colors duration-200"
            disabled={isLoading || subjectOptions.length === 0}
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
            class="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={!selectedMatiereTemp || isLoading}
          >
            <Icon icon="heroicons:plus" class="h-5 w-5 mr-1" />
            Ajouter
          </button>
        </div>

        {#if subjectOptions.length === 0 && !isLoading}
          <p class="mt-1 text-sm text-amber-600">
            ⚠️ Aucune matière disponible. Veuillez d'abord créer des matières.
          </p>
        {/if}

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
                      class="hover:text-red-600 transition-colors duration-200 ml-1"
                      disabled={isLoading}
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
          Classes
          {#if errors.classes}
            <span class="text-red-500 ml-1">*</span>
          {/if}
        </label>
        
        <div class="flex gap-2">
          <select
            bind:value={selectedClasseTemp}
            class="flex-1 border rounded-lg p-2 focus:ring-green-500 focus:border-green-500 sm:text-sm transition-colors duration-200"
            disabled={isLoading || classOptions.length === 0}
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
            class="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={!selectedClasseTemp || isLoading}
          >
            <Icon icon="heroicons:plus" class="h-5 w-5 mr-1" />
            Ajouter
          </button>
        </div>

        {#if classOptions.length === 0 && !isLoading}
          <p class="mt-1 text-sm text-amber-600">
            ⚠️ Aucune classe disponible. Veuillez d'abord créer des classes.
          </p>
        {/if}

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
                      class="hover:text-red-600 transition-colors duration-200 ml-1"
                      disabled={isLoading}
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
        <div class="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-red-600 text-sm flex items-center">
            <Icon icon="heroicons:exclamation-triangle" class="h-4 w-4 mr-2" />
            {errors.general}
          </p>
        </div>
      {/if}

      <div class="flex justify-end space-x-3 mt-5">
        <button
          type="button"
          on:click={closeModal}
          class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={isLoading}
        >
          Annuler
        </button>
        <button
          type="submit"
          class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-green-600 hover:bg-green-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed min-w-20"
          disabled={isLoading || isClosing}
        >
          {#if isLoading}
            <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
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