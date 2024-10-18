<script>
    import Header from "./shared/Header.svelte";
    import { theme } from "./stores/theme";
</script>

<main style="--background: {$theme.background_color};">
    <h1>Hello, world!</h1>

    <Header />
</main>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700&display=swap" rel="stylesheet">
</head>
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
