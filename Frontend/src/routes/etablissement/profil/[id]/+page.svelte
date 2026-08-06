<script>
  import { page } from '$app/stores';
  import ProfileView from '../../../../components/etablissement/profile/ProfileView.svelte';

  $: etablissementId = $page.params.id;
</script>

<ProfileView {etablissementId} />