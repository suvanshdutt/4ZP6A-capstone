<script>
    import Header from "./shared/Header.svelte";
    import { theme } from "./stores/theme";
</script>

<main style="--background: {$theme.background_color};">
    <h1>Hello, world!</h1>

    <Header />
</main>

<style>
    main {
        text-align: center;
        padding: 1em;
        max-width: 240px;
        margin: 0 auto;
        background-color: var(--background);
    }

    h1 {
        color: #333;
    }
</style>
