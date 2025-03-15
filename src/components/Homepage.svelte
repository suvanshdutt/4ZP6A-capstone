<script lang="ts">
    import Button from "../shared/Button.svelte";
    import Dropbox from "./Dropbox.svelte";

</script>

<main>
    <div class="main-body">
        <div class="About">
            <h1>About</h1>
            <p>Our Project is based on AI chest read, Our website gives the patient a radiographed report of the chest xray
                provided. The report checks on the potential disease/s.</p>
            <p>Project By : Suvansh Dutt, Ujjwal Raj, Yuvraj Singh Sandhu and Suhaas Parcha </p>
            <div class="buttons">
                <Button on:click={() => window.location.href = "/login"}>Login</Button>
                <Button inverse={true} on:click={() => window.location.href = "/signup"}>Sign Up</Button>
            </div>
        </div>
        <div class="dpb">
            <Dropbox/>
        </div>
    </div>
</main>

<style>
    :global(body) {
        background-color: var(--background_color);
        color: var(--text_color);
        margin: 0;
    }
    .main-body {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center; /* Vertically centers items */
    gap: 200px; /* Adjust spacing between the elements */
    flex-wrap: wrap; /* Allows items to wrap if the screen is smaller */
    }

    .dpb {
        flex: 1; 
        display: flex; 
        justify-content: center; 
        align-items: center; 
        margin-top: 20px; 
    }

    main {
        margin-top: 15vh;
        margin-left: 5vw; 
        margin-right: 5vw;
    }


    .About {
        margin-right: 5px;
        margin-left: 50px;
        width: 50%;
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
