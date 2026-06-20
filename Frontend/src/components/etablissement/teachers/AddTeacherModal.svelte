<script>
  import Icon from '@iconify/svelte';
  import { authApi } from '$lib/api';
  import { createEventDispatcher } from 'svelte';
  import { user } from '$lib/stores';
  import { fade, fly } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';

  export let isOpen = false;

  export let classOptions = [];
  export let subjectOptions = [];
  export let yearOptions = [];

  const dispatch = createEventDispatcher();
  let etablissementId = $user?.profile?.id ?? null;
  let isLoading = false;

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
    general: ''
  };

  async function handleSubmit(){
    if(isLoading) return;
    formData.etablissement = etablissementId;
    try {
      isLoading = true;
      await authApi.createProfesseur(formData);
      dispatch(
        'success',
        {
          message:'Professeur ajouté avec succès'
        }
      );
      closeModal();
    } catch(e){
      errors.general = e.message;
    } finally {
      isLoading=false;
    }
  }

  function closeModal(){
    dispatch('close');
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
                Ajouter un professeur
            </h2>
            <button
            on:click={closeModal}
            >
                <Icon icon="heroicons:x-mark" class="h-6 w-6"/>
            </button>
        </div>

        <form on:submit|preventDefault={handleSubmit}>
            <!-- PRENOM -->
            <div class="mb-4">
                <label class="block text-sm">
                    Prénom
                </label>

                <input
                    class="mt-1 w-full border rounded-lg p-2"
                    bind:value={formData.user.first_name}
                    placeholder="Prénom"
                />
            </div>

            <!-- NOM -->
            <div class="mb-4">
                <label class="block text-sm">
                    Nom
                </label>

                <input
                    class="mt-1 w-full border rounded-lg p-2"
                    bind:value={formData.user.last_name}
                    placeholder="Nom"
                />
            </div>

            <!-- EMAIL -->
            <div class="mb-4">
                <label class="block text-sm">
                    Email
                </label>

                <input
                    type="email"
                    class="mt-1 w-full border rounded-lg p-2"
                    bind:value={formData.user.email}
                    placeholder="Email"
                />
            </div>

            <!-- TELEPHONE -->
            <div class="mb-4">
                <label class="block text-sm">
                    Téléphone
                </label>

                <input
                    class="mt-1 w-full border rounded-lg p-2"
                    bind:value={formData.user.telephone}
                    placeholder="Téléphone"
                />
            </div>

            <!-- ANNEE SCOLAIRE -->
            <div class="mb-4">
                <label class="block text-sm">
                    Année scolaire
                </label>
                <select
                    class="mt-1 w-full border rounded-lg p-2"
                    bind:value={formData.annee_scolaire}
                >
                <option value="">
                    Sélectionner une année
                </option>
                    {#each yearOptions as option}
                        <option value={option.value}>
                            {option.label}
                        </option>
                    {/each}
                </select>
            </div>

            <!-- MATIERES -->
            <div class="mb-4">
                <label class="block text-sm">
                    Matières
                </label>
                <select
                    multiple
                    class="mt-1 w-full border rounded-lg p-2"
                    bind:value={formData.matieres}
                >
                {#each subjectOptions as option}
                    <option value={option.value}>
                        {option.label}
                    </option>
                {/each}
                </select>
            </div>

            <!-- CLASSES -->
            <div class="mb-4">
                <label class="block text-sm">
                        Classes
                </label>

                <select
                    multiple
                    class="mt-1 w-full border rounded-lg p-2"
                    bind:value={formData.classes}
                >
                {#each classOptions as option}
                    <option value={option.value}>
                    {option.label}
                    </option>
                {/each} 
                </select>
            </div>

            <!-- PASSWORD -->
            <div class="mb-4">
                <label class="block text-sm">
                    Mot de passe
                </label>

                <input
                    type="password"
                    class="mt-1 w-full border rounded-lg p-2"
                    bind:value={formData.user.password}
                />
            </div>

            <!-- CONFIRM PASSWORD -->
            <div class="mb-4">
                <label class="block text-sm">
                    Confirmation
                </label>

                <input
                    type="password"
                    class="mt-1 w-full border rounded-lg p-2"
                    bind:value={formData.user.password_confirm}
                />
            </div>

            {#if errors.general}
            <div class="bg-red-50 text-red-600 p-3 rounded">
                {errors.general}
            </div>
            {/if}

            <div class="flex justify-end gap-3 mt-5">
                <button
                    type="button"
                    on:click={closeModal}
                    class="px-4 py-2 border rounded-lg"
                >
                    Annuler
                </button>
                <button
                    class="px-4 py-2 bg-green-600 text-white rounded-lg"
                    disabled={isLoading}
                >
                    {#if isLoading}
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