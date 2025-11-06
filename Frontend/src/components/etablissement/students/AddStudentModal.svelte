<script>
  import Icon from '@iconify/svelte';
  import { authApi } from '$lib/api';
  import { createEventDispatcher } from 'svelte';
  import { user } from '$lib/stores';

  export let isOpen = false;
  export let classOptions = [];
  export let statusOptions = [];
  export let yearOptions = [];

  const dispatch = createEventDispatcher();

  let formData = {
    user: {
      first_name: '',
      last_name: '',
      email: '',
      telephone: '',
      password: '',
      password_confirm: '',
      user_type: 'eleve'
    },
    classe: null,
    statut: 'actif',
    annee_scolaire: '',
    etablissement: $user.profile.id
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
    classe: '',
    annee_scolaire: '',
    general: ''
  };
  
  let selectedClassId = '';

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

  function handleFieldBlur(field, value, category = 'user') {
    if (category === 'user') {
      errors.user[field] = validateField(field, value);
    } else {
      errors[field] = validateField(field, value);
    }
  }

  async function handleSubmit() {
    try {
      // Réinitialiser les erreurs
      errors.general = '';
      
      if (!validateForm()) {
        errors.general = 'Veuillez corriger les erreurs dans le formulaire';
        return;
      }

      if (!selectedClassId) {
        errors.classe = 'Veuillez sélectionner une classe';
        return;
      }

      // Trouver l'objet classe pour débogage
      const selectedClass = classOptions.find(option => option.id === parseInt(selectedClassId));
      if (!selectedClass) {
        errors.classe = 'Classe sélectionnée invalide';
        return;
      }

      console.log("Selected class object:", selectedClass);

      formData.classe = parseInt(selectedClassId);
      
      const submitData = {
        ...formData,
        classe: parseInt(selectedClassId)
      };

      console.log("Submit data:", submitData);
      await authApi.createEleve(submitData);
      dispatch('close');
      dispatch('success', { message: 'Étudiant ajouté avec succès' });
      resetForm();
      
    } catch (err) {
      errors.general = err.message || 'Une erreur est survenue lors de l\'ajout de l\'étudiant';
      console.error('Submission error:', err);
    }
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
      classe: '',
      annee_scolaire: '',
      general: ''
    };
    selectedClassId = '';
    formData = {
      user: {
        first_name: '',
        last_name: '',
        email: '',
        telephone: '',
        password: '',
        password_confirm: '',
        user_type: 'eleve'
      },
      classe: null,
      statut: 'actif',
      annee_scolaire: '',
      etablissement: $user.profile.id
    };
  }

  function closeModal() {
    dispatch('close');
    resetForm();
  }
</script>

{#if isOpen}
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
    <!-- Contenu du modal -->
    <div class="bg-white rounded-lg shadow-xl p-6 w-full max-w-md max-h-[80vh] overflow-y-auto">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold text-gray-900">Ajouter un étudiant</h2>
        <button on:click={closeModal} class="text-gray-500 hover:text-gray-700">
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
              on:blur={() => handleFieldBlur('first_name', formData.user.first_name)}
              class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm"
              class:border-red-500={errors.user.first_name}
              class:border-gray-300={!errors.user.first_name}
              placeholder="Prénom"
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
              on:blur={() => handleFieldBlur('last_name', formData.user.last_name)}
              class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm"
              class:border-red-500={errors.user.last_name}
              class:border-gray-300={!errors.user.last_name}
              placeholder="Nom"
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
              on:blur={() => handleFieldBlur('email', formData.user.email)}
              class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm"
              class:border-red-500={errors.user.email}
              class:border-gray-300={!errors.user.email}
              placeholder="Email"
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
              on:blur={() => handleFieldBlur('telephone', formData.user.telephone)}
              class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm"
              class:border-red-500={errors.user.telephone}
              class:border-gray-300={!errors.user.telephone}
              placeholder="06 12 34 56 78"
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
              on:blur={() => handleFieldBlur('classe', selectedClassId, 'other')}
              class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm"
              class:border-red-500={errors.classe}
              class:border-gray-300={!errors.classe}
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
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm"
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
              on:blur={() => handleFieldBlur('annee_scolaire', formData.annee_scolaire, 'other')}
              class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm"
              class:border-red-500={errors.annee_scolaire}
              class:border-gray-300={!errors.annee_scolaire}
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
              on:blur={() => handleFieldBlur('password', formData.user.password)}
              class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm"
              class:border-red-500={errors.user.password}
              class:border-gray-300={!errors.user.password}
              placeholder="Mot de passe"
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
              on:blur={() => handleFieldBlur('password_confirm', formData.user.password_confirm)}
              class="mt-1 block w-full px-3 py-2 border rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm"
              class:border-red-500={errors.user.password_confirm}
              class:border-gray-300={!errors.user.password_confirm}
              placeholder="Confirmer le mot de passe"
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
          <p class="text-red-600 text-sm mb-4">{errors.general}</p>
        {/if}

        <!-- Boutons -->
        <div class="flex justify-end space-x-3">
          <button
            type="button"
            on:click={closeModal}
            class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50"
          >
            Annuler
          </button>
          <button
            type="submit"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg shadow-sm text-white bg-green-600 hover:bg-green-700"
          >
            Ajouter
          </button>
        </div>
      </form>
    </div>
  </div>
{/if}