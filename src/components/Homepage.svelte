<script lang="ts">
    import Button from "../shared/Button.svelte";

</script>

<main>
    <div class="main-body">
        <div class="About">
            <h2>AI-Powered</h2>
            <h1>Chest X-Ray Analysis</h1>
            <p>Our platform leverages deep learning to analyze chest X-rays, 
                providing probability-based predictions and disease localization 
                through heatmap visualizations</p>
            <p>
                By identifying potential abnormalities, the AI offers a reliable second opinion, 
                helping to refine assessments. This technology enhances efficiency in medical imaging, 
                offering valuable insights for improved analysis. </p>
            <div class="buttons">
                <Button on:click={() => window.location.href = "/login"}>Login</Button>
                <Button inverse={true} on:click={() => window.location.href = "/signup"}>Sign Up</Button>
            </div>
        </div>
        <div class="image">
            <img alt="sample" src="/Images/sample.png"/>
        </div>
    </div>
</main>
<div class="bg">
    <div class="bg-image">
        <img alt="bg-img" src="/Images/xray.jpg"/>
    </div>
    <div class="gradient"></div>
</div>

<style>
    :global(body) {
        background-color: var(--background_color);
        color: var(--text_color);
        margin: 0;
    }

    .main-body {
        display: flex;
        flex-direction: row;
        justify-content:space-evenly;
        align-items: center;
        gap: 20px; /* Adjust spacing between the elements */
        flex-wrap: wrap; /* Allows items to wrap if the screen is smaller */
        margin-top: 10vh;
        z-index: 100;
    }

    .image {
        display: flex;
        justify-content: center; 
        align-items: center; 
        background-color: var(--background_color);
        width: 35%;
        max-width: 1000px;
        margin-right: 50px;
        margin-top: 7vh; 
        padding: 25px;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); 
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        z-index: 100;
    }

    .image:hover {
        transform: scale(1.03); 
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3); 
    }

    .image img {
        width: 100%;
        height: auto;
    }

    .About {
        margin-right: 5px;
        margin-left: 120px;
        width: 45%;
        max-width: 1000px;
        margin-top: 0px;
        z-index: 100;
    }

    h1 {
        color: var(--heading_text);
        font-size: clamp(45px, 9.5vw, 75px);
        font-weight: 5;
        margin-top: 0px;
        margin-bottom: 10px;
    }

    h2 {
        color: #676f85;
        font-size: clamp(40px, 8vw, 50px);
        margin-bottom: 0px;
    }

    @media (max-width:1600px) {
        h1 {
            font-size: clamp(40px, 8.5vw, 60px);
        }

        h2 {
            font-size: clamp(35px, 7vw, 40px);
        }
    }

    p {
        color: var(--text_color);
        font-size: 20px;
        font-weight: 5;
        margin-left: 50px;
    }

    .buttons {
        margin-left: 100px;
        margin-top: 60px;
        display: flex;
        gap: 100px;
    }

    .bg{
        position: absolute;
        overflow: hidden;
        bottom: 0;
        left: 0;
        right: 0;
        top: 0;
        z-index: -1;
    }

    .bg-image {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: auto;
        margin-left: 2vw;
        z-index: -1;
    }

    .bg-image img {
        width: 89%;
        opacity: 0.5;
    }

    .gradient {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle at center, transparent 10%, var(--background_color) 50%);
        z-index: 11;
    }
</style>
