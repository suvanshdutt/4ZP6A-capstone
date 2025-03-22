<script lang="ts">
    import { light_theme, theme, dark_theme } from "../stores/theme";
    import { isLoggedIn } from "../stores/authStore";
    import Button from "../shared/Button.svelte";
    import { onMount } from "svelte";

    let loggedIn = false;
    let showLogoutDialog = false;
    type Theme = {
        text_color: string;
        background_color: string;
        primary_color: string;
        secondary_color: string;
        accent_color: string;
        grey_text: string;
        heading_text: string;
    };
    let currentTheme: Theme;

    const unsubscribe_theme = theme.subscribe(value => {
           currentTheme = value;
       });

    const unsubscribe_login = isLoggedIn.subscribe(value => {
        loggedIn = value;
    });

    onMount(() => {
        return () => {
            unsubscribe_theme(); 
            unsubscribe_login(); 
        };
    });

    let destination = "/";

    function handleLogout() {
        isLoggedIn.set(false);
        window.location.href = destination;
    }

    function confirmLogout(path = "/") {
        destination = path;
        showLogoutDialog = true;
    }

    function cancelLogout() {
        showLogoutDialog = false;
    }

    function toggleTheme() {
        theme.update(currentTheme => {
            const newTheme = currentTheme === light_theme ? dark_theme : light_theme;
            const newUrl = new URL(window.location.href);
            newUrl.searchParams.set('theme', newTheme === light_theme ? 'light' : 'dark');
            window.history.pushState({}, '', newUrl);
            return newTheme;
        });
    }
</script>

{#if showLogoutDialog}
    <div class="dialog-box-bg">
        <div class="dialog-box">
            <button class="close-button" on:click={cancelLogout} type="button">
                <img class="close-icon" src="https://img.icons8.com/?size=100&id=7FSknHLAHdnP&format=png&color=da3029" alt="close"/>
            </button>
            <h2 class="heading2">Are you sure you want to logout?</h2>
            <div class="logout-buttons">
                <Button inverse={true} on:click={cancelLogout} style="font-weight:normal; padding: 7px 15px; border-radius: 10px;">Cancel</Button>
                <Button on:click={handleLogout} style="font-weight:normal; padding: 7px 15px; border-radius: 10px;">Logout</Button>
            </div>
        </div>
    </div>
{/if}

<header>
    <nav>
        <div class="header">
            <button class="logo" on:click|preventDefault={toggleTheme}>
                {#if currentTheme === light_theme}
                    <img src="https://img.icons8.com/?size=100&id=q4yXFoEnYRH7&format=png&color=000000" alt="AI For Chest X-ray" class="logo-icon" />
                {:else}
                    <img src="https://img.icons8.com/?size=100&id=2ZR4nkc83eZe&format=png&color=ffffff" alt="AI For Chest X-ray" class="logo-icon" />
                {/if}
                </button>
            <div class="header-right">
                {#if loggedIn}
                    <button on:click={() => confirmLogout("/")}>Home</button>
                    <button on:click={() => confirmLogout("/about")}>About</button>
                    <button on:click={() => confirmLogout("/")}>Logout</button>
                    <button on:click={() => confirmLogout("/contact")}>Contact</button>
                {:else}
                    <a class="active" href="/">Home</a>
                    <a class="about" href="/about">About</a>
                    <a href="/login">Login</a>
                    <a href="/contact">Contact</a>
                {/if}
            </div>
        </div>
    </nav>
</header>
<style>
    header {
        position: flex;
        top: 0;
        left: 0;
        right: 0;
        z-index: 9999;
        background-color: var(--background_color);
    }

    .header {
        display: flex;
        overflow: hidden;
        font-family: 'Montserrat', sans-serif !important ;
        align-items: center;
        justify-content: space-between;
        background-color: var(--background_color);
        padding: 0px 10px;
    }

    .header a {
        float: left;
        text-align: center;
        padding: 10px;
        text-decoration: none;
        font-size: 20px;
        line-height: 25px;
        border-radius: 2px;
        color: var(--grey_text);
    }

    .header button.logo {
    font-size: 20px;
    font-weight: bold;
    }


    .header a:hover {
    background-color: var(--background_color);
    
    }


    .header a.active {
        background-color: var(--background_color);
    }

    /* Float the link section to the right */
    .header-right {
        float: right;
    }

    .header-right a {
    margin-left: 10px;
    }

    .header button {
        float: left;
        text-align: center;
        padding: 10px;
        text-decoration: none;
        font-size: 20px;
        line-height: 25px;
        border-radius: 2px;
        color: var(--grey_text);
    }

    .header button:hover {
        background-color: var(--background_color);
    }

    /* Add media queries for responsiveness - when the screen is 500px wide or less, stack the links on top of each other */
    @media screen and (max-width: 400px) {
    .header a {
        float: none;
        display: block;
        text-align: left;
    }
    .header-right {
        float: none;
    }
    }

    .logo-icon {
        width: 60px;
        height: auto; 
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

    .close-button {
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
    .header button {
        background: none;
        border: none;
        cursor: pointer;
        color: var(--grey_text);
        font-size: 20px;
        padding: 10px;
        font-family: 'Montserrat', sans-serif;
        text-decoration: none;
    }
</style>
