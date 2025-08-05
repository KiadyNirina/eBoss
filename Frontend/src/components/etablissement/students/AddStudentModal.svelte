<script>
  import Icon from '@iconify/svelte';
  import { authApi } from '$lib/api';
  import { createEventDispatcher } from 'svelte';

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
      telephone: ''
    },
    classe: '',
    statut: 'actif',
    annee_scolaire: ''
  };
  let error = '';

  async function handleSubmit() {
    try {
      await authApi.createEleve(formData);
      dispatch('close');
      dispatch('success', { message: 'Étudiant ajouté avec succès' });
      formData = {
        user: { first_name: '', last_name: '', email: '', telephone: '' },
        classe: '',
        statut: 'actif',
        annee_scolaire: ''
      };
      error = '';
    } catch (err) {
      error = err.message || 'Une erreur est survenue lors de l\'ajout de l\'étudiant';
    }
  }

  function closeModal() {
    dispatch('close');
    error = '';
  }
</script>

{#if isOpen}
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
    <!-- Contenu du modal -->
    <div class="bg-white rounded-lg shadow-xl p-6 w-full max-w-md">
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
          <label for="first_name" class="block text-sm font-medium text-gray-700">Prénom</label>
          <input
            type="text"
            id="first_name"
            bind:value={formData.user.first_name}
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm"
            placeholder="Prénom"
            required
          />
        </div>

        <!-- Nom -->
        <div class="mb-4">
          <label for="last_name" class="block text-sm font-medium text-gray-700">Nom</label>
          <input
            type="text"
            id="last_name"
            bind:value={formData.user.last_name}
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm"
            placeholder="Nom"
            required
          />
        </div>

        <!-- Email -->
        <div class="mb-4">
          <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
          <input
            type="email"
            id="email"
            bind:value={formData.user.email}
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm"
            placeholder="Email"
            required
          />
        </div>

        <!-- Téléphone -->
        <div class="mb-4">
          <label for="telephone" class="block text-sm font-medium text-gray-700">Téléphone</label>
          <input
            type="tel"
            id="telephone"
            bind:value={formData.user.telephone}
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm"
            placeholder="06 12 34 56 78"
          />
        </div>

        <!-- Classe -->
        <div class="mb-4">
          <label for="classe" class="block text-sm font-medium text-gray-700">Classe</label>
          <select
            id="classe"
            bind:value={formData.classe}
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm"
            required
          >
            <option value="">Sélectionner une classe</option>
            {#each classOptions as option}
              <option value={option.value}>{option.label}</option>
            {/each}
          </select>
        </div>

        <!-- Statut -->
        <div class="mb-4">
          <label for="statut" class="block text-sm font-medium text-gray-700">Statut</label>
          <select
            id="statut"
            bind:value={formData.statut}
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm"
            required
          >
            {#each statusOptions as option}
              <option value={option.value}>{option.label}</option>
            {/each}
          </select>
        </div>

        <!-- Année scolaire -->
        <div class="mb-4">
          <label for="annee" class="block text-sm font-medium text-gray-700">Année scolaire</label>
          <select
            id="annee"
            bind:value={formData.annee_scolaire}
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-green-500 focus:border-green-500 sm:text-sm"
            required
          >
            <option value="">Sélectionner une année</option>
            {#each yearOptions as option}
              <option value={option.value}>{option.label}</option>
            {/each}
          </select>
        </div>

        <!-- Message d'erreur -->
        {#if error}
          <p class="text-red-600 text-sm mb-4">{error}</p>
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