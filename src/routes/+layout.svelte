<script lang="ts">
    import { theme } from "../stores/theme";
    import { onMount, onDestroy } from "svelte";
    import Header from "../shared/Header.svelte";

    let unsubscribe: () => void;

    onMount(() => {
        unsubscribe = theme.subscribe(($theme) => {
            for (const [key, val] of Object.entries($theme)) {
                document.documentElement.style.setProperty(`--${key}`, val);
            }
        });
    });

    onDestroy(() => {
        if (unsubscribe) unsubscribe();
    });
</script>

<Header />
<slot />

<style>
    /* Global styles can go here */
    :global(body) {
        background-color: var(--background_color);
        color: var(--text_color);
        font-family: 'Montserrat', sans-serif; /* Set a consistent global font */
        margin: 0;
    }
</style>