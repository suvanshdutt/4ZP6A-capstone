<script lang="ts">
    import Button from "../shared/Button.svelte";
    import { onMount } from "svelte";
    import { isLoggedIn } from "../stores/authStore";
    
    isLoggedIn.set(true);
    let reportId = "";
    let reportData: any = null;
    let errorMessage = "";
    let showBanner = true;
    let showLogoutDialog = false;
    let showImageModal = false;
    let enlargedImageUrl = "";

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


    function getSortedPredictions(predictions: number[]) {
        if (!predictions) return [];
        
        // Create array of objects with all the information
        const combined = CLASSES.map((className, index) => ({
            className,
            prediction: predictions[index],
            auroc: auroc[index],
            originalIndex: index
        }));

        return combined.sort((a, b) => b.prediction - a.prediction);
    }

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

    function handleLogout() {
        window.location.href = "/about";
    }

    function confirmLogout() {
        showLogoutDialog = true;
    }

    function cancelLogout() {
        showLogoutDialog = false;
    }

    function openImageModal(imageUrl: string) {
        enlargedImageUrl = imageUrl; 
        showImageModal = true;
    }

    function closeImageModal() {
        showImageModal = false;
        enlargedImageUrl = ""; 
    }

    onMount(() => {
        fetchReport();
    });
</script>
<main>
<div class="result-container">
    {#if showLogoutDialog}
        <div class="dialog-box-bg">
            <div class="dialog-box">
                <button class="close-button-dialog" on:click={cancelLogout} type="button">
                    <img class="close-icon" src="https://img.icons8.com/?size=100&id=7FSknHLAHdnP&format=png&color=da3029" alt="close"/>
                </button>
                <h2 class="heading2">Are you sure you want to logout?</h2>
                <div class="logout-buttons">
                    <Button inverse={true} on:click={cancelLogout} style="font-weight:normal; padding: 7px 15px; border-radius: 10px">Cancel</Button>
                    <Button on:click={handleLogout} style="font-weight:normal; padding: 7px 15px; border-radius: 10px;">Logout</Button>
                </div>
            </div>
        </div>
    {/if}

    {#if showImageModal}
        <div 
        class="modal-bg"
        tabindex="0"
        role="button" 
        aria-label="Enlarge chest X-ray image"
        on:click={closeImageModal} 
        on:keydown={(e) => {
            if (e.key !== 'Enter' && e.key !== ' ') return;
            e.preventDefault();
            if (e.target instanceof HTMLElement) {
                e.target.click();
            }
        }}>
            <div 
            tabindex="0"
            role="button" 
            aria-label="Enlarge chest X-ray image"
            class="modal-content" 
            on:click|stopPropagation on:keydown={(e) => {
                if (e.key !== 'Enter' && e.key !== ' ') return;
                e.preventDefault();
                if (e.target instanceof HTMLElement) {
                    e.target.click();
                }
            }}>
                <img src={enlargedImageUrl} alt="Enlarged chest x-ray" class="enlarged-image" />
            </div>
        </div>
    {/if}
    <div class="display">
        <Button inverse={true} on:click={goBack} style="align-self: flex-start; font-size: 20px;"> Back </Button>
        {#if showBanner}
            <div class="banner">
                <span>This tool uses AI to predict potential findings in chest X-rays.
                    While we strive for accuracy, predictions may be incorrect.  
                    Do not rely solely on these predictions for medical decisions. 
                    Hover over labels to see model performance tested on 33,000+ images.
                    For more information on our AI model, visit the 
                    <button on:click={confirmLogout} class="about-link">About page</button>.
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
                        aria-label="Enlarge chest X-ray image"
                        on:click={() => openImageModal(reportData.imageUrl)}
                        on:keydown={(e) => {
                            if (e.key !== 'Enter' && e.key !== ' ') return;
                            e.preventDefault();
                            if (e.target instanceof HTMLElement) {
                                e.target.click();
                            }
                        }}>
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
                    aria-label="Enlarge chest X-ray image"
                    on:click={() => openImageModal(reportData.heatmapUrl)}
                    on:keydown={(e) => {
                        if (e.key !== 'Enter' && e.key !== ' ') return;
                        e.preventDefault();
                        if (e.target instanceof HTMLElement) {
                            e.target.click();
                        }
                    }}>
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
                    {#each getSortedPredictions(reportData.predictions) as {className, prediction, auroc: aurocValue}, index}
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
                                {className}:
                            </span>
                            {#if tooltipVisible && tooltipIndex === index}
                                <div class="tooltip">AUROC: {aurocValue}%</div>
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
</div>
</main>
<style>
    .result-container {
        width: 100%;
        min-height: calc(100vh - 60px);
        margin-top: 10px;
        padding-top: 20px;
        background-color: var(--background_color);
    }

    .display {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 40px;
        width: 90%;
        max-width: 2000px;
        padding: 40px;
        margin: 0 auto;
    }

    .results {
        display: flex;
        width: 95%;
        max-width: 1800px;
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
        background-color: var(--secondary_color);
        font-size: 24px;
        font-style: italic;
        font-family: Arial, Helvetica, sans-serif;
        color: var(--primary_color);
        text-decoration: none;
        border: none;
        cursor: pointer; 
        padding: 0;
        margin: 0;
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

    .dialog-box-bg {
        position: fixed;
        inset: 0;
        background-color: rgba(0,0,0,0.4); 
        backdrop-filter: blur(2px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 100;
    }

    .dialog-box {
        position: relative;
        background-color: var(--background_color);
        font-size: 22px;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.25);
        max-width: 400px;
        width: 90%;
        padding-top: 40px;
    }

    .close-button-dialog {
        background: none;
        border: none;
        cursor: pointer;
        font-size: 16px;
        position: absolute;
        top: 15px;
        right: 15px;
    }

    .close-icon {
        width: 24px;
        height: 24px;
    }

    .heading2 {
        font-size: 22px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        color: var(--heading_text);
    }

    .logout-buttons {
        display: flex;
        justify-content: center;
        gap: 50px;
    }

    .modal-bg {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0,0,0,0.6); 
        backdrop-filter: blur(5px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }

    .modal-content {
        border-radius: 15px;
        overflow: hidden;
        position: relative;
    }

    .enlarged-image {
        max-width: 100%;
        max-height: 80vh;
    }

</style>