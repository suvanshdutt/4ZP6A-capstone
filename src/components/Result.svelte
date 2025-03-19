<script lang="ts">
    import { onMount } from "svelte";
    import Button from "../shared/Button.svelte";
    
    let reportId = "";
    let reportData: any = null;
    let errorMessage = "";
    let showBanner = true;

    let auroc = ["93", "91", "94", "89", "91", "91", "87", "92", "92", "91", "90", "88", "94", "96"];

    const CLASSES = [
        "Enlarged Cardiomediastinum",
        "Cardiomegaly",
        "Lung Opacity",
        "Lung Lesion",
        "Edema",
        "Consolidation",
        "Pneumonia",
        "Atelectasis",
        "Pneumothorax",
        "Pleural Effusion",
        "Pleural Other",
        "Fracture",
        "Support Devices",
        "No Finding",
    ];

    let tooltipVisible = false;
    let tooltipIndex = -1;

    function showTooltip(index:any) {
        tooltipVisible = true;
        tooltipIndex = index;
    }

    function hideTooltip() {
        tooltipVisible = false;
        tooltipIndex = -1;
    }

    function goBack() {
        window.location.href = "/dashboard";
    }

    function dismissBanner() {
        showBanner = false; 
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
    <head>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap">
    </head>
    <div class="display">
        <Button inverse={true} on:click={goBack} style="align-self: flex-start; font-size: 20px;"> Back </Button>
        {#if showBanner}
            <div class="banner">
                <span>This tool uses AI to predict potential findings in chest X-rays.
                    While we strive for accuracy, predictions may be incorrect.  
                    Do not rely solely on these predictions for medical decisions. 
                    Hover over labels to see model performance tested on 33,000+ images.
                    For more information on our AI model, visit the 
                    <a href="/about" class="about-link"> About page</a>.
                </span>
                <button class="close-button" on:click={dismissBanner}>✖</button>
            </div>
        {/if}
        <div class="results">
            <div class="image-contains">
                <div class="image">
                    <p class="image-text">Chest X-ray Image</p>
                    {#if errorMessage}
                        <p>{errorMessage}</p>
                    {:else if reportData}
                        <div 
                        class="Real-Image" 
                        role="button"
                        tabindex="0"
                        aria-label="Enlarge chest X-ray image">
                            <img src="{reportData.imageUrl}" alt="chest x-ray" />
                        </div>
                    {:else}
                        <p>Loading report...</p>
                    {/if}
                </div>
            
                <div class="image-heatmap">
                    <p class="image-text">Heatmap</p>
                    {#if errorMessage}
                        <p>{errorMessage}</p>
                    {:else if reportData}
                    <div 
                    class="Real-Image"
                    role="button"
                    tabindex="0"
                    aria-label="Enlarge chest X-ray image">
                        <img src="{reportData.heatmapUrl}" alt="chest x-ray" />
                    </div>
                {:else}
                    <p>Loading report...</p>
                {/if}
            </div>
            </div>
            <div class="predictions">
        
                <p class="image-text">Predictions</p>
                {#if reportData && reportData.predictions && reportData.predictions.length > 0}
                <div class="prediction-list">
                    {#each reportData.predictions as prediction, index}
                        <div 
                            class="prediction-item"
                            role="button" 
                            tabindex="0" 
                            on:mouseover={() => showTooltip(index)} 
                            on:mouseleave={hideTooltip}
                            on:focus={() => showTooltip(index)} 
                            on:blur={hideTooltip}>
                            <span 
                                class="disease-label" 
                                role="button" 
                                tabindex="0" 
                                on:mouseover={() => showTooltip(index)} 
                                on:mouseleave={hideTooltip}
                                on:focus={() => showTooltip(index)} 
                                on:blur={hideTooltip}
                            >
                                {CLASSES[index]}:
                            </span>
                            {#if tooltipVisible && tooltipIndex === index}
                                <div class="tooltip">AUROC: {auroc[index]}%</div>
                            {/if}
                            <div class="bar-and-value">
                                <div class="progress-bar">
                                    <div class="progress" style="width: {prediction * 100}%;"></div>
                                </div>
                                <span class="prediction-value">{(prediction * 100).toFixed(1)}%</span>
                            </div>
                        </div>
                    {/each}
                </div>
                {:else if reportData}
                    <p>No predictions available.</p>
                {/if}
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
        max-width: 1600px;
        padding: 40px;
        margin: 0 auto;
    }

    .results {
        display: flex;
        width: 95%;
        max-width: 1500px;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 7px 10px 40px rgba(0, 0, 0, 0.3);
    }

    .banner {
        background-color: var(--secondary_color);
        color: var(--heading_text);
        border: 1px solid var(--primary_color);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 60%; 
        font-size: 24px;
        font-style: italic;
        font-family: Arial, Helvetica, sans-serif;
        box-shadow: 3px 5px 20px rgba(0,0,0,0.15);
    }

    .close-button {
        background: none;
        border: none;
        color: var(--primary_color);
        cursor: pointer;
        font-size: 22px;
    }

    .about-link {
        color: var(--primary_color);
        text-decoration: none;
        cursor: pointer; 
    }

    .about-link:hover {
        text-decoration: underline;
    }

    .image{
        flex:1;
        padding: 10px;
        padding-bottom: 0px;
        margin-bottom: 50px;
    }

    .image-heatmap{
        flex:1;
        padding: 10px;
        padding-bottom: 0px;
        margin-bottom: 50px;
        margin-top: -50px;
    }

    .image-text {
        font-family: 'Roboto', sans-serif;
        color: var(--heading_text);
        text-align: center;
        font-size: 28px;
        font-weight: 500;
    }

    .predictions {
        width: 50%;
        padding: 10px;
    }

    .prediction-list {
        margin-top: 20px;
    }

    .prediction-item {
        margin-bottom: 15px;
        position: relative;
    }

    .disease-label {
        color: var(--grey_text);
        font-size: 22px; 
        position: relative;
    }

    .bar-and-value {
        display: flex;
        align-items: center;
        flex-grow: 1;
        margin-top: 10px;
        gap: 20px;
    }

    .progress-bar {
        background-color: var(--secondary_color);
        border: var(--primary_color) solid 1px;
        border-radius: 6px;
        overflow: hidden;
        height: 25px;
        width: 87%;
        box-shadow: 0 8px 10px rgba(0, 0, 0, 0.1);
    }

    .progress {
        background-color: var(--primary_color); 
        height: 100%;
        transition: width 0.3s ease;
    }

    .prediction-value {
        color: var(--grey_text);
        font-size: 18px; 
    }

    .tooltip {
        position: absolute;
        background-color: var(--primary_color);
        color: var(--secondary_color);
        border: 1px solid var(--primary_color);
        border-radius: 10px;
        padding: 5px 10px;
        margin-top: 25px;
        box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
        z-index: 10;
        white-space: nowrap;
        display: inline;
        transform: translateY(-30px);
        margin-left: 15px;
    }

    img {
        width: 800px;
        height: auto;
    }

    .image-contains {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align : center;
        flex: 1;
        margin-left: -25px;
    }

    .Real-Image {
        border-radius: 12px;
        width: 600px;
        overflow: hidden;
        cursor: zoom-in;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); 
        transition: transform 0.3s ease, box-shadow 0.3s ease; 
    }

    .Real-Image img {
        width: 100%; 
        height: auto;
        display: flex; 
    }

    .Real-Image:hover {
        transform: scale(1.03); 
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3); 
    }
</style>