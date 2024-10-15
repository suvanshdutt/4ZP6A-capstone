<script>
    import { theme } from "../stores/theme";
</script>

<header style="--background: {$theme.background_color};">
    <nav>
    <div class="logo">AI For Chest X-ray Read</div>
    <ul class="nav-links">
    <li><a href="#">Home</a></li>
    <li><a href="#">Login</a></li>
    <li><a href="#">Contact</a></li>
    </ul>
    </nav>
    
</header>
<style>
header {
    
    padding: 1em;
    position: fixed;
    width: 100%;
    max-width: 240px;
    margin: 0 auto;
    background-color: var(--background);
    z-index: 100;

}
    nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 5px auto;
    padding: 0 20px;
}

.logo {
    font-size: 1.2rem;
    font-weight: bold;
}

.nav-links {
    list-style: none;
    display: flex;
}

.nav-links li {
    margin-right: 20px;
}

.nav-links a {
    
    padding: 10px;
    font-weight: bold;
    text-decoration: none;
    background-color: var(--background);
}

.nav-links a:hover {
    background-color: var(--background);
    border-radius: 4px;
    background-color: var(--background);
}
</style>
