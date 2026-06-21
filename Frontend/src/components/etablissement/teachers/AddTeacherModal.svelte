<script>
  import Icon from '@iconify/svelte';
  import { authApi } from '$lib/api';
  import { createEventDispatcher } from 'svelte';
  import { user } from '$lib/stores';
  import { fade, fly } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';
  import { browser } from '$app/environment';

  export let isOpen = false;
  export let classOptions = [];
  export let subjectOptions = [];
  export let yearOptions = [];

  const dispatch = createEventDispatcher();

  let etablissementId = $user?.profile?.id ?? null;

  let formData = {
    user: {
      first_name: '',
      last_name: '',
      email: '',
      telephone: '',
      password: '',
      password_confirm: '',
      user_type: 'professeur'
    },
    etablissement: etablissementId,
    annee_scolaire: '',
    matieres: [],
    classes: []
  };

  let errors = {
    user: {
      first_name: '',
      last_name: '',
      email: '',
      telephone: '',
      password: '',
      password_confirm: ''
    },
    matieres: '',
    classes: '',
    annee_scolaire: '',
    general: ''
  };

  let isLoading = false;
  let isClosing = false;

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
        
      case 'password':
        if (!value) return 'Le mot de passe est obligatoire';
        if (value.length < 8) return 'Le mot de passe doit contenir au moins 8 caractères';
        if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(value)) {
          return 'Le mot de passe doit contenir au moins une majuscule, une minuscule et un chiffre';
        }
        return '';
        
      case 'password_confirm':
        if (!value) return 'La confirmation du mot de passe est obligatoire';
        if (value !== formData.user.password) return 'Les mots de passe ne correspondent pas';
        return '';
        
      case 'matieres':
        if (!value || value.length === 0) return 'Sélectionnez au moins une matière';
        return '';
        
      case 'classes':
        if (!value || value.length === 0) return 'Sélectionnez au moins une classe';
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
    
    // Vérifier que l'ID établissement est disponible
    if (!etablissementId && browser) {
      errors.general = 'Impossible de déterminer l\'établissement. Veuillez rafraîchir la page.';
      return false;
    }
    
    // Valider les champs user
    Object.keys(formData.user).forEach(field => {
      const error = validateField(field, formData.user[field]);
      errors.user[field] = error;
      if (error) isValid = false;
    });
    
    // Valider les autres champs
    errors.matieres = validateField('matieres', formData.matieres);
    errors.classes = validateField('classes', formData.classes);
    errors.annee_scolaire = validateField('annee_scolaire', formData.annee_scolaire);
    
    if (errors.matieres || errors.classes || errors.annee_scolaire) isValid = false;
    
    return isValid;
  }

  async function handleSubmit() {
    if (isLoading) return;
    
    errors.general = '';

    // Vérifier l'établissement avant soumission
    if (!etablissementId) {
      errors.general = 'Établissement non trouvé. Veuillez vous reconnecter.';
      return;
    }

    // Mettre à jour l'ID établissement dans formData
    formData.etablissement = etablissementId;

    if (!validateForm()) {
      errors.general = 'Veuillez corriger les erreurs dans le formulaire';
      return;
    }

    const submitData = { ...formData };

    try {
      isLoading = true;
      await authApi.createProfesseur(submitData);
      await closeModalWithAnimation();
      dispatch('success', { message: 'Professeur ajouté avec succès' });
      
    } catch (err) {
      errors.general = err.message || 'Une erreur est survenue lors de l\'ajout du professeur';
      console.error('Submission error:', err);
    } finally {
      isLoading = false;
    }
  }

  async function closeModalWithAnimation() {
    isClosing = true;
    await new Promise(resolve => setTimeout(resolve, 300));
    dispatch('close');
    resetForm();
    isClosing = false;
  }

  function resetForm() {
    errors = {
      user: {
        first_name: '',
        last_name: '',
        email: '',
        telephone: '',
        password: '',
        password_confirm: ''
      },
      matieres: '',
      classes: '',
      annee_scolaire: '',
      general: ''
    };
    formData = {
      user: {
        first_name: '',
        last_name: '',
        email: '',
        telephone: '',
        password: '',
        password_confirm: '',
        user_type: 'professeur'
      },
      etablissement: etablissementId,
      annee_scolaire: '',
      matieres: [],
      classes: []
    };
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
        <h2 class="text-xl font-bold text-gray-900">Ajouter un professeur</h2>
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

        <!-- Matières -->
        <div class="mb-4">
          <label for="matieres" class="block text-sm font-medium text-gray-700">
            Matières
            {#if errors.matieres}
              <span class="text-red-500 ml-1">*</span>
            {/if}
          </label>
          <div class="relative">
            <select
              id="matieres"
              multiple
              bind:value={formData.matieres}
              on:input={() => handleFieldInput('matieres', formData.matieres, 'other')}
              on:blur={() => handleFieldBlur('matieres', formData.matieres, 'other')}
              class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm transition-colors duration-200 min-h-[100px]"
              class:border-red-500={errors.matieres}
              class:border-gray-300={!errors.matieres}
              disabled={isLoading || subjectOptions.length === 0}
            >
              {#each subjectOptions as option}
                <option value={option.value}>{option.label}</option>
              {/each}
            </select>
            {#if errors.matieres}
              <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                <Icon icon="heroicons:exclamation-circle" class="h-5 w-5 text-red-500" />
              </div>
            {/if}
          </div>
          {#if errors.matieres}
            <p class="mt-1 text-sm text-red-600">{errors.matieres}</p>
          {/if}
          {#if subjectOptions.length === 0 && !isLoading}
            <p class="mt-1 text-sm text-amber-600">
              ⚠️ Aucune matière disponible. Veuillez d'abord créer des matières.
            </p>
          {/if}
          <p class="mt-1 text-xs text-gray-500">Maintenez Ctrl/Cmd pour sélectionner plusieurs matières</p>
        </div>

        <!-- Classes -->
        <div class="mb-4">
          <label for="classes" class="block text-sm font-medium text-gray-700">
            Classes
            {#if errors.classes}
              <span class="text-red-500 ml-1">*</span>
            {/if}
          </label>
          <div class="relative">
            <select
              id="classes"
              multiple
              bind:value={formData.classes}
              on:input={() => handleFieldInput('classes', formData.classes, 'other')}
              on:blur={() => handleFieldBlur('classes', formData.classes, 'other')}
              class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm transition-colors duration-200 min-h-[100px]"
              class:border-red-500={errors.classes}
              class:border-gray-300={!errors.classes}
              disabled={isLoading || classOptions.length === 0}
            >
              {#each classOptions as option}
                <option value={option.value}>{option.label}</option>
              {/each}
            </select>
            {#if errors.classes}
              <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                <Icon icon="heroicons:exclamation-circle" class="h-5 w-5 text-red-500" />
              </div>
            {/if}
          </div>
          {#if errors.classes}
            <p class="mt-1 text-sm text-red-600">{errors.classes}</p>
          {/if}
          {#if classOptions.length === 0 && !isLoading}
            <p class="mt-1 text-sm text-amber-600">
              ⚠️ Aucune classe disponible. Veuillez d'abord créer des classes.
            </p>
          {/if}
          <p class="mt-1 text-xs text-gray-500">Maintenez Ctrl/Cmd pour sélectionner plusieurs classes</p>
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
              on:input={() => handleFieldInput('annee_scolaire', formData.annee_scolaire, 'other')}
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

        <!-- Mot de passe -->
        <div class="mb-4">
          <label for="password" class="block text-sm font-medium text-gray-700">
            Mot de passe
            {#if errors.user.password}
              <span class="text-red-500 ml-1">*</span>
            {/if}
          </label>
          <div class="relative">
            <input
              type="password"
              id="password"
              bind:value={formData.user.password}
              on:input={() => handleFieldInput('password', formData.user.password)}
              on:blur={() => handleFieldBlur('password', formData.user.password)}
              class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm transition-colors duration-200"
              class:border-red-500={errors.user.password}
              class:border-gray-300={!errors.user.password}
              placeholder="Mot de passe"
              disabled={isLoading}
            />
            {#if errors.user.password}
              <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                <Icon icon="heroicons:exclamation-circle" class="h-5 w-5 text-red-500" />
              </div>
            {/if}
          </div>
          {#if errors.user.password}
            <p class="mt-1 text-sm text-red-600">{errors.user.password}</p>
          {/if}
        </div>

        <!-- Confirmation mot de passe -->
        <div class="mb-4">
          <label for="password_confirm" class="block text-sm font-medium text-gray-700">
            Confirmer le mot de passe
            {#if errors.user.password_confirm}
              <span class="text-red-500 ml-1">*</span>
            {/if}
          </label>
          <div class="relative">
            <input
              type="password"
              id="password_confirm"
              bind:value={formData.user.password_confirm}
              on:input={() => handleFieldInput('password_confirm', formData.user.password_confirm)}
              on:blur={() => handleFieldBlur('password_confirm', formData.user.password_confirm)}
              class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm transition-colors duration-200"
              class:border-red-500={errors.user.password_confirm}
              class:border-gray-300={!errors.user.password_confirm}
              placeholder="Confirmer le mot de passe"
              disabled={isLoading}
            />
            {#if errors.user.password_confirm}
              <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                <Icon icon="heroicons:exclamation-circle" class="h-5 w-5 text-red-500" />
              </div>
            {/if}
          </div>
          {#if errors.user.password_confirm}
            <p class="mt-1 text-sm text-red-600">{errors.user.password_confirm}</p>
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
              Ajout...
            {:else}
              Ajouter
            {/if}
          </button>
        </div>
      </form>
    </div>
  </div>
{/if}