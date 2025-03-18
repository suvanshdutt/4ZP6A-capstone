<script lang="ts">
  import type { IntegerType } from "mongodb";
    import { onMount } from "svelte";

    let AUROCCount: number = 0;
    let specificityCount: number = 0;
    let sensitivityCount: number = 0;

    function countUp(target: number, duration: number): void {
        const start: number = 0;
        const end: number = target;
        const increment: number = end / (duration / 1000 * 60);
        let current: number = start;

        const interval = setInterval(() => {
            current += increment;
            if (current >= end) {
                current = end;
                clearInterval(interval);
            }
            if (target === 92) AUROCCount = Math.round(current);
            if (target === 84) specificityCount = Math.round(current);
            if (target === 81) sensitivityCount = Math.round(current);
        }, 1000 / 60);
    }

    onMount(() => {
        countUp(92, 1500);
        countUp(84, 1500);  
        countUp(81, 1500);
    });
</script>

<main class="about-container">
    <div class="display">
        <h1 class="about-title">About Our Project</h1>
        <div class="content">
            <p class="about-description">
                Welcome to our Chest X-ray AI project, an innovative second opinion application 
                developed by students at McMaster University as part of their capstone project. 
                Our mission is to leverage cutting-edge artificial intelligence technology to 
                assist in the interpretation of chest X-rays, providing a valuable tool 
                for our users.
            </p>
            <h2 class="about-heading">Our Approach</h2>
            <p class="about-description">
                We have developed a sophisticated AI model using Convolutional Neural Networks (CNNs), 
                specifically employing the DenseNet201 architecture. This model has been fine-tuned 
                and optimized to achieve high performance in identifying various chest conditions from X-ray images.
            </p>
            <p class="about-description">
                Our AI was trained on the Stanford CheXpert dataset, which comprises a total of 224,316 
                chest radiographs of 65,240 patients. For more details on the dataset, please visit the 
                <a href="https://stanfordmlgroup.github.io/competitions/chexpert/" target="_blank" class="link">Stanford CheXpert website</a>
            </p>
            <h2 class="about-heading">Performance Metrics</h2>
            <p class="about-description">
                Our model was rigorously tested on over 33,000 images, 
                demonstrating strong performance with high values in key diagnostic metrics:
            </p>
            <div class="performance-metrics">
                <div class="metric">
                    <h3>{AUROCCount}%</h3>
                    <p>AUROC</p>
                </div>
                <div class="metric">
                    <h3>{specificityCount}%</h3>
                    <p>Specificity</p>
                </div>
                <div class="metric">
                    <h3>{sensitivityCount}%</h3>
                    <p>Sensitivity</p>
                </div>
            </div>
            <h2 class="about-heading">Additional Features</h2>
            <p class="about-description">
                Instead of binary "disease present" or "disease absent" outputs, our AI provides 
                probability-based predictions, displayed as percentage likelihoods using progress bars. 
                This allows users to assess the model's confidence in its diagnosis rather than 
                relying on a simple yes/no result.
            </p>
            <p class="about-description">
                To enhance clinical interpretation, our application features an advanced 
                visualization tool: a Grad-CAM-based heatmap. This heatmap visually highlights 
                regions of the X-ray that were most influential in the AI's prediction. 
                This visual guidance helps you focus on the most important areas of the X-ray, 
                making it easier to spot potential issues or confirm your observations.
                This visual guidance can be particularly valuable in identifying subtle abnormalities 
                or confirming the location of suspected pathologies, thereby supporting more informed 
                diagnostic decisions.
            </p>
            <h2 class="about-heading">Disclaimer</h2>
            <p class="about-description">
                While our AI model has been developed with cutting-edge techniques and 
                shows promising results, it is important to remember that AI is not infallible. 
                Its outputs are intended to support and not replace the clinical judgment of healthcare 
                professionals. We strongly advise consulting a qualified radiologist or medical doctor 
                before making any clinical decisions based solely on our tool.
            </p>
            <h2 class="about-heading">Open Source</h2>
            <p class="about-description">
                We believe in transparency and open science. Our project's code is available for exploration on our 
                <a href="https://github.com/suvanshdutt/4ZP6A-capstone" target="_blank" rel="noopener noreferrer" class="link">Github Repository.</a>
                We encourage interested individuals to review our work and gain insights into our development process.
            </p>
            <p class="about-description">
                By combining advanced AI techniques with a commitment to responsible and transparent development, 
                we aim to contribute to the field of medical imaging and support healthcare professionals in their 
                critical work. Our open-source approach allows for scrutiny and understanding of our methods, 
                fostering trust and advancement in AI-assisted medical imaging.
            </p>
            <div class="github-container">
                <a href="https://github.com/suvanshdutt/4ZP6A-capstone" target="_blank" rel="noopener noreferrer">
                    <img src="https://img.icons8.com/?size=100&id=62856&format=png&color=000000" alt="GitHub" class="github-icon" />
                </a>
                <span class="github-text">Follow us on GitHub</span>
            </div>
        </div>
    </div>
</main>

<style>
    :global(body) {
        background-color: var(--background_color);
        margin: 0;
    }

    .about-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 0px;
    }

    .display {
        text-align: center;
        background-color: var(--secondary_color);
        width: 80%;
        border-radius: 10px;
        padding: 30px;
        color: #333;
        font-family: Arial, sans-serif;
        box-shadow: 7px 10px 40px rgba(0,0,0,0.2);
    }

    .about-title {
        font-size: 55px;
        font-weight: bold;
        color: var(--heading_text);
        margin-bottom: 20px;
        margin-top: 20px;
    }

    .content {
        display: flex;
        flex-direction: column;
        justify-content: left;
        align-items: left;
        text-align: left;
        margin-left: 100px;
        margin-right: 100px;
    }

    .about-heading {
        font-size: 30px;
        font-weight: bold;
        color: var(--heading_text);
        margin-bottom: 0px;
    }

    .about-description {
        font-size: 1.2em;
        color: rgba(65,65,65,100%);
        margin-bottom: 0px;
    }

    .link {
        color: rgba(65,65,65,100%);
        text-decoration: underline;
    }

    .link:hover {
        text-decoration: none;
    }

    .performance-metrics {
        display: flex;
        justify-content: center;
        gap: 150px;
        margin-top: 20px;
    }

    .metric {
        text-align: center;
        background-color: var(--primary_color);
        border-radius: 50%;
        padding: 20px;
        box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.5);
        width: 100px;
        height: 100px;
    }

    .metric h3 {
        font-size: 2.2em;
        color: var(--background_color);
        margin-top: 15px;
        margin-bottom: 10px;
    }

    .metric p {
        font-size: 1.2em;
        color: var(--background_color);
        margin-top: 5px;
    }

    .github-container {
        display: flex; 
        align-items: center;
        justify-content: center;
        margin-top: 20px; 
    }

    .github-icon {
        width: 40px; 
        height: 40px; 
        margin-right: 10px; 
    }

    .github-text {
        font-size: 1.2em; 
    }
</style>