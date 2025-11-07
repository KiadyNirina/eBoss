<script>
  import Icon from '@iconify/svelte';
  import { authApi } from '$lib/api';
  import { createEventDispatcher } from 'svelte';
  import { fade, fly } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';

  export let isOpen = false;
  export let student = null;
  export let classOptions = [];
  export let statusOptions = [];
  export let yearOptions = [];

  const dispatch = createEventDispatcher();

  let formData = {
    user: { first_name: '', last_name: '', email: '', telephone: '' },
    classe: null,
    statut: 'actif',
    annee_scolaire: ''
  };

  let errors = { user: {}, classe: '', annee_scolaire: '', general: '' };
  let selectedClassId = '';
  let isLoading = false;
  let isClosing = false;

  // Pré-remplir le formulaire quand student change
  $: if (student) {
    formData.user.first_name = student.prenom || '';
    formData.user.last_name = student.nom || '';
    formData.user.email = student.email || '';
    formData.user.telephone = student.telephone || '';
    formData.classe = student.classeId || null;
    selectedClassId = student.classeId || '';
    formData.statut = student.statut || 'actif';
    formData.annee_scolaire = student.annee_scolaire || '';
  }

  console.log('Editing student:', student);

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
        if(!value.trim()) return 'Le téléphone est obligatoire';
        if (value && !/^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$/.test(value.replace(/\s/g, ''))) {
          return 'Format de téléphone invalide (ex: 06 12 34 56 78)';
        }
        return '';
        
      case 'classe':
        if (!value) return 'La classe est obligatoire';
        return '';
        
      case 'annee_scolaire':
        if (!value) return 'L\'année scolaire est obligatoire';
        return '';
        
      default:
        return '';
    }
  }

  // Validation temps réel sur chaque frappe
  function handleFieldInput(field, value, category = 'user') {
    if (category === 'user') {
      errors.user[field] = validateField(field, value);
    } else {
      errors[field] = validateField(field, value);
    }
  }

  // Toujours garder blur pour marquer un champ "touché"
  function handleFieldBlur(field, value, category = 'user') {
    handleFieldInput(field, value, category);
  }

  function validateForm() {
    let isValid = true;
    
    // Valider les champs user
    Object.keys(formData.user).forEach(field => {
      const error = validateField(field, formData.user[field]);
      errors.user[field] = error;
      if (error) isValid = false;
    });
    
    // Valider les autres champs
    errors.classe = validateField('classe', selectedClassId);
    errors.annee_scolaire = validateField('annee_scolaire', formData.annee_scolaire);
    
    if (errors.classe || errors.annee_scolaire) isValid = false;
    
    return isValid;
  }

  async function handleSubmit() {
    if (isLoading) return;
    
    errors.general = '';

    if (!validateForm()) {
      errors.general = 'Veuillez corriger les erreurs dans le formulaire';
      return;
    }

    if (!selectedClassId) {
      errors.classe = 'Veuillez sélectionner une classe';
      return;
    }

    const selectedClass = classOptions.find(option => option.id === parseInt(selectedClassId));
    if (!selectedClass) {
      errors.classe = 'Classe sélectionnée invalide';
      return;
    }

    isLoading = true;
    try {
      const submitData = {
        id: student.id,
        user: {
          first_name: formData.user.first_name,
          last_name: formData.user.last_name,
          email: formData.user.email,
          telephone: formData.user.telephone,
          user_type: 'eleve'
        },
        classe: parseInt(selectedClassId),
        statut: formData.statut,
        annee_scolaire: formData.annee_scolaire
      };
      await authApi.updateEleve(submitData.id, submitData);
      dispatch('success', { message: 'Étudiant mis à jour avec succès' });
      await closeModalWithAnimation();
    } catch (err) {
      errors.general = err.message || 'Erreur lors de la mise à jour';
      console.error(err);
    } finally {
      isLoading = false;
    }
  }

  async function closeModalWithAnimation() {
    isClosing = true;
    await new Promise(resolve => setTimeout(resolve, 200));
    dispatch('close');
    isClosing = false;
  }

  function closeModal() {
    closeModalWithAnimation();
  }
</script>

{#if isOpen}
  <div 
    class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50"
    transition:fade={{ duration: 200 }}
  >
    <!-- Contenu du modal -->
    <div 
      class="bg-white rounded-lg shadow-xl p-6 w-full max-w-md max-h-[80vh] overflow-y-auto"
      in:fly="{{ y: -50, duration: 300, easing: quintOut }}"
      out:fly="{{ y: -50, duration: 200, easing: quintOut }}"
    >
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold text-gray-900">Éditer un étudiant</h2>
        <button 
          on:click={closeModal} 
          class="text-gray-500 hover:text-gray-700 transition-colors duration-200"
          disabled={isLoading}
        >
          <Icon icon="heroicons:x-mark" class="h-6 w-6" />
        </button>
      </div>

      <!-- Formulaire -->
      <form on:submit|preventDefault={handleSubmit}>
        <!-- Prénom -->
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
              bind:value={formData.user.first_name}
              on:input={() => handleFieldInput('first_name', formData.user.first_name)}
              on:blur={() => handleFieldBlur('first_name', formData.user.first_name)}
              class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm transition-colors duration-200"
              class:border-red-500={errors.user.first_name}
              class:border-gray-300={!errors.user.first_name}
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

        <!-- Nom -->
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
              bind:value={formData.user.last_name}
              on:input={() => handleFieldInput('last_name', formData.user.last_name)}
              on:blur={() => handleFieldBlur('last_name', formData.user.last_name)}
              class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm transition-colors duration-200"
              class:border-red-500={errors.user.last_name}
              class:border-gray-300={!errors.user.last_name}
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

        <!-- Email -->
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
              bind:value={formData.user.email}
              on:input={() => handleFieldInput('email', formData.user.email)}
              on:blur={() => handleFieldBlur('email', formData.user.email)}
              class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm transition-colors duration-200"
              class:border-red-500={errors.user.email}
              class:border-gray-300={!errors.user.email}
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

        <!-- Téléphone -->
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
              bind:value={formData.user.telephone}
              on:input={() => handleFieldInput('telephone', formData.user.telephone)}
              on:blur={() => handleFieldBlur('telephone', formData.user.telephone)}
              class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm transition-colors duration-200"
              class:border-red-500={errors.user.telephone}
              class:border-gray-300={!errors.user.telephone}
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

        <!-- Classe -->
        <div class="mb-4">
          <label for="classe" class="block text-sm font-medium text-gray-700">
            Classe
            {#if errors.classe}
              <span class="text-red-500 ml-1">*</span>
            {/if}
          </label>
          <div class="relative">
            <select
              id="classe"
              bind:value={selectedClassId}
              on:input={() => handleFieldInput('classe', selectedClassId)}
              on:blur={() => handleFieldBlur('classe', selectedClassId, 'other')}
              class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm transition-colors duration-200"
              class:border-red-500={errors.classe}
              class:border-gray-300={!errors.classe}
              disabled={isLoading}
            >
              <option value="">Sélectionner une classe</option>
              {#each classOptions as option}
                <option value={option.id}>{option.nom}</option>
              {/each}
            </select>
            {#if errors.classe}
              <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                <Icon icon="heroicons:exclamation-circle" class="h-5 w-5 text-red-500" />
              </div>
            {/if}
          </div>
          {#if errors.classe}
            <p class="mt-1 text-sm text-red-600">{errors.classe}</p>
          {/if}
        </div>

        <!-- Statut -->
        <div class="mb-4">
          <label for="statut" class="block text-sm font-medium text-gray-700">Statut</label>
          <select
            id="statut"
            bind:value={formData.statut}
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm transition-colors duration-200"
            disabled={isLoading}
          >
            {#each statusOptions as option}
              <option value={option.value}>{option.label}</option>
            {/each}
          </select>
        </div>

        <!-- Année scolaire -->
        <div class="mb-4">
          <label for="annee" class="block text-sm font-medium text-gray-700">
            Année scolaire
            {#if errors.annee_scolaire}
              <span class="text-red-500 ml-1">*</span>
            {/if}
          </label>
          <div class="relative">
            <select
              id="annee"
              bind:value={formData.annee_scolaire}
              on:input={() => handleFieldInput('annee_scolaire', formData.annee_scolaire)}
              on:blur={() => handleFieldBlur('annee_scolaire', formData.annee_scolaire, 'other')}
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

        {#if errors.general}
          <div class="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-red-600 text-sm flex items-center">
              <Icon icon="heroicons:exclamation-triangle" class="h-4 w-4 mr-2" />
              {errors.general}
            </p>
          </div>
        {/if}

        <!-- Boutons -->
        <div class="flex justify-end space-x-3">
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
              <!-- Animation de loading -->
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Mise à jour...
            {:else}
              Mettre à jour
            {/if}
          </button>
        </div>
      </form>
    </div>
  </div>
{/if}
