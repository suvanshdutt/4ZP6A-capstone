<script lang="ts">
    import Header from "../shared/Header.svelte";
    import Button from "../shared/Button.svelte";
    import {base} from '$app/paths';

</script>

<main>
    <div class="About">
        <h1>About</h1>
        <p>Our Project is based on AI chest read, Our website gives the patient a radiographed report of the chest xray
            provided. The report checks on the potential diseases.</p>
        <p>Project By : Suvansh Dutt, Ujjwal Raj, Yuvraj Singh Sandhu and Suhaas Parcha </p>
        <div class="buttons">
            <Button on:click={() => window.location.href = `${base}/login`}>Login</Button>
            <Button inverse={true} on:click={() => window.location.href = `${base}/signup`}>Sign Up</Button>
        </div>
    </div>
</main>

<style>
    main {
        margin-top: 15vh;
        margin-left: 15vw;
        margin-right: 15vw;
    }

    .About {
        margin-right: 40vw;
    }

    h1 {
        color: var(--heading_text);
        font-size: 80px;
        font-weight: 5;
    }

    p {
        color: var(--text_color);
        font-size: 20px;
        font-weight: 5;
        margin-left: 25px;
    }

    .buttons {
        margin-left: 100px;
        margin-top: 100px;
        display: flex;
        gap: 100px;
    }
</style>