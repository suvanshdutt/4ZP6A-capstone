<script lang="ts">
    import { onMount } from "svelte";
    import Button from "../shared/Button.svelte";

    let reportId = "";
    let reportData: any = null;
    let errorMessage = "";

    function goBack() {
        window.location.href = "/dashboard";
    }

    async function fetchReport() {
        const params = new URLSearchParams(window.location.search);
        reportId = params.get("id") || "";
        if (reportId) {
            try {
                const res = await fetch(`/api/reports?id=${reportId}`);
                const data = await res.json();
                if (res.ok) {
                    reportData = data;
                } else {
                    errorMessage = data.error;
                }
            } catch (error) {
                errorMessage = "Error fetching report.";
                console.error("Fetch report error:", error);
            }
        } else {
            errorMessage = "No report identifier provided.";
        }
    }

    onMount(() => {
        fetchReport();
    });
</script>

<main>
    <div class="display">
        <Button inverse={true} on:click={goBack} style="align-self: flex-start;"> Back </Button>

        <div class="results">
            <div class="image">
                <p class="image-text">Chest X-ray Image</p>
                {#if errorMessage}
                    <p>{errorMessage}</p>
                {:else if reportData}
                    <img src="{reportData.imageUrl}" alt="chest x-ray" />
                {:else}
                    <p>Loading report...</p>
                {/if}
            </div>
            <div class="predictions">

            </div>
        </div>
    </div>
</main>

<style>
    :global(body) {
        background-color: var(--background_color);
        color: var(--text_color);
        font-family: 'Montserrat', sans-serif;
        margin: 0;
    }

    .display {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 40px;
        width: 90%;
        padding: 40px;
        margin: 0 auto;
    }

    .results {
        display: flex;
        width: 90%;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
    }

    .image{
        flex:1;
        padding: 10px;
    }

    .image-text {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
    }

    .predictions {
        width: 60%;
        padding: 10px;
    }

    img {
        max-width: 100%;
        height: auto;
    }

</style>