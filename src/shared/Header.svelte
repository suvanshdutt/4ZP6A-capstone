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
    background-color: white;
    color: rgb(125, 122, 125);
    padding: 10px 0;
    position: fixed;
    width: 100%;
    z-index: 100;
    box-shadow: 0 2px 2px rgba(0, 0, 0, 0.2);
}

nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 5px auto;
    padding: 0 20px;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: #1f201f5a;
}

.nav-links {
    list-style: none;
    display: flex;
}

.nav-links li {
    margin-right: 20px;
}

.nav-links a {
    color: rgb(0, 0, 0);
    padding: 10px;
    font-weight: bold;
    text-decoration: none;
}

.nav-links a:hover {
    background-color: #444743;
    border-radius: 4px;
    color: white;
}
</style>
