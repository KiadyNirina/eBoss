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

  function handleFieldInput(field, value, category = 'user') {
    if (category === 'user') errors.user[field] = value.trim() ? '' : 'Champ requis';
    else errors[field] = value ? '' : 'Champ requis';
  }

  async function handleSubmit() {
    if (isLoading) return;
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
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50" transition:fade={{ duration: 200 }}>
    <div class="bg-white rounded-lg shadow-xl p-6 w-full max-w-md max-h-[80vh] overflow-y-auto"
         in:fly={{ y: -50, duration: 300, easing: quintOut }}
         out:fly={{ y: -50, duration: 200, easing: quintOut }}>
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold text-gray-900">Éditer un étudiant</h2>
        <button on:click={closeModal} class="text-gray-500 hover:text-gray-700" disabled={isLoading}>
          <Icon icon="heroicons:x-mark" class="h-6 w-6" />
        </button>
      </div>

      <form on:submit|preventDefault={handleSubmit}>
        <!-- Prénom -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700">Prénom</label>
          <input type="text" bind:value={formData.user.first_name}
                 on:input={() => handleFieldInput('first_name', formData.user.first_name)}
                 class="mt-1 block w-full px-3 py-2 border rounded-lg" />
        </div>

        <!-- Nom -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700">Nom</label>
          <input type="text" bind:value={formData.user.last_name}
                 on:input={() => handleFieldInput('last_name', formData.user.last_name)}
                 class="mt-1 block w-full px-3 py-2 border rounded-lg" />
        </div>

        <!-- Email -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700">Email</label>
          <input type="email" bind:value={formData.user.email}
                 on:input={() => handleFieldInput('email', formData.user.email)}
                 class="mt-1 block w-full px-3 py-2 border rounded-lg" />
        </div>

        <!-- Téléphone -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700">Téléphone</label>
          <input type="tel" bind:value={formData.user.telephone}
                 on:input={() => handleFieldInput('telephone', formData.user.telephone)}
                 class="mt-1 block w-full px-3 py-2 border rounded-lg" />
        </div>

        <!-- Classe -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700">Classe</label>
          <select bind:value={selectedClassId} class="mt-1 block w-full px-3 py-2 border rounded-lg">
            <option value="">Sélectionner une classe</option>
            {#each classOptions as option}
              <option value={option.id}>{option.nom}</option>
            {/each}
          </select>
        </div>

        <!-- Statut -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700">Statut</label>
          <select bind:value={formData.statut} class="mt-1 block w-full px-3 py-2 border rounded-lg">
            {#each statusOptions as option}
              <option value={option.value}>{option.label}</option>
            {/each}
          </select>
        </div>

        <!-- Année scolaire -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700">Année scolaire</label>
          <select bind:value={formData.annee_scolaire} class="mt-1 block w-full px-3 py-2 border rounded-lg">
            {#each yearOptions as option}
              <option value={option.value}>{option.label}</option>
            {/each}
          </select>
        </div>

        {#if errors.general}
          <div class="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-600">{errors.general}</div>
        {/if}

        <div class="flex justify-end space-x-3">
          <button type="button" on:click={closeModal} class="px-4 py-2 bg-gray-100 rounded-md">Annuler</button>
          <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-md" disabled={isLoading}>
            {isLoading ? 'Mise à jour...' : 'Mettre à jour'}
          </button>
        </div>
      </form>
    </div>
  </div>
{/if}
