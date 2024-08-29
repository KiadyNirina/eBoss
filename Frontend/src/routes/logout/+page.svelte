<script>
    import { logout } from "../../lib/auth";
    import { onMount } from "svelte";
    import { goto } from '$app/navigation';

    onMount( async () => {
        logout();
        goto('/login');
    })
</script>