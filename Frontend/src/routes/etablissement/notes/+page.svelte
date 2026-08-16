<script>
  import GradesView from '../../../components/etablissement/grades/GradesView.svelte';
  import EvaluationForm from '../../../components/etablissement/grades/EvaluationForm.svelte';

  let showForm = false;
  let refreshKey = 0;

  function handleOpen() {
    showForm = true;
  }

  function handleCreated() {
    showForm = false;
    refreshKey++;
  }

  function handleCancel() {
    showForm = false;
  }
</script>

<GradesView key={refreshKey} on:open={handleOpen} />

{#if showForm}
  <!-- Modale -->
  <div class="fixed inset-0 z-50 overflow-y-auto bg-gray-500 bg-opacity-75 flex items-center justify-center p-4">
    <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full p-6">
      <EvaluationForm on:created={handleCreated} on:cancel={handleCancel} />
    </div>
  </div>
{/if}