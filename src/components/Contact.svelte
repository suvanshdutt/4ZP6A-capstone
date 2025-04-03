<script lang="ts">

</script>

<main class="contact-container">
    <div class="display">
        <h1 class="contact-title">Contact Us</h1>
        <p class="contact-description">
            We appreciate your interest in our Chest X-ray project, a capstone endeavor by students of 
            McMaster University under the guidance of Dr. Mehdi Moradi. If you have any inquiries, 
            suggestions, or would like to collaborate, please feel free to reach out to us at
            <a href="mailto:chestxraygrpacc@gmail.com" class="email-link">chestxraygrpacc@gmail.com</a>
        </p>
        <p class="contact-github">
            For more information about our project, you can visit our GitHub repository. 
            We are committed to fostering a collaborative environment and welcome any feedback or contributions.
        </p>
        <div class="github-container">
            <a href="https://github.com/suvanshdutt/4ZP6A-capstone" target="_blank" rel="noopener noreferrer">
                <img src="https://img.icons8.com/?size=100&id=62856&format=png&color=000000" alt="GitHub" class="github-icon" />
            </a>
            <span class="github-text">Follow us on GitHub</span>
        </div>
    </div>
</main>

<style>
    :global(body) {
        background-color: var(--background_color);
        margin: 0;
    }

    .contact-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 70px;
    }

    .display {
        text-align: center;
        background-color: var(--secondary_color);
        width: 70%;
        border-radius: 10px;
        padding: 40px;
        color: #333;
        font-family: Arial, sans-serif;
        box-shadow: 7px 10px 40px rgba(0,0,0,0.2);
    }

    .contact-title {
        font-size: 60px;
        font-weight: bold;
        color: var(--heading_text);
        margin-bottom: 50px;
    }

    .contact-description,
    .contact-github {
        font-size: 1.4em;
        color: rgba(65,65,65,100%);
        margin-bottom: 30px;
        margin-left: 100px;
        margin-right: 100px;
    }

    .email-link {
        color: rgba(65,65,65,100%);
        text-decoration: underline;
    }

    .email-link:hover {
        text-decoration: none;
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

    @media only screen and (max-width:1200px) {
        .display {
            padding: 10px;
            width: 90%;
            margin-left: 20px;
            margin-right: 20px;
            box-shadow: 3px 5px 20px rgba(0,0,0,0.2);
        }

        .contact-description,
        .contact-github {
            margin-left: 20px;
            margin-right: 20px;
        }
    }
</style>