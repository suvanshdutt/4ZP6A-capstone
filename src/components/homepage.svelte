<script lang="ts">
    import { theme } from "../stores/theme";
    import Header from "../shared/Header.svelte";


    // using css variables
    $: {
        for (const [key, val] of Object.entries($theme)) {
            document.documentElement.style.setProperty(`--${key}`, val);
        }
    }
</script>

<Header />
<main>
    <div class="About">
        <h1>About</h1>
        <p>Our Project is based on AI chest read, Our website gives the patient a radiographed report of the chest xray provided. The report checks on the potential diseases.</p>
        <p>Project By : Suvansh Dutt, Ujjwal Raj, Yuvraj Singh Sandhu and Suhaas Parcha </p>
        <div class="buttons">
            <button>Login</button>
            <button>Sign Up</button>
        </div>
    </div>
</main>

<style>
    :global(body) {
        background-color: var(--background_color);
        color: var(--text_color);
        margin: 0;
        font-family: 'Alumni Sans';
    }
    main {
        padding-top: 250px;
        margin-left: 200px;
        margin-right: 200px;
    }
    .About {
        margin-right: 750px;
    }

    h1 {
        color: #1e1e1e;
        font-size: 80px;
        font-family: 'Alumni Sans';
        font-weight: 5;
    }
    p {
        color: rgba(24,23,24,0.8);
        font-size: 20px;
        font-family: 'Alumni Sans';
        font-weight: 5;
        margin-left: 25px;
    }
    .buttons {
        margin-left: 100px;
        margin-top: 100px;
        display: flex;
        gap: 100px;
    }
    button {
        background-color: var(--primary_color);
        color: #fdddd7;
        font-size: 22px;
        font-weight: 5;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        width: 120px;
        height: 48px;
    }
</style>