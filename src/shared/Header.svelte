<script>
    import { theme } from "../stores/theme";
</script>

<header style="--background: {$theme.background_color};">
    <nav>
    <div class="logo">AI For Chest X-ray Read</div>
    <ul class="nav-links">
    <li><a href="#">Home</a></li>
    <li><a href="../src/components/Login.svelte">Login</a></li>
    <li><a href="#">Contact</a></li>
    </ul>
    </nav>
    
</header>
<style>
header {
    display: flex;
  
    align-items: center;
  
    justify-content: space-between;
    width:100%;
    background-color: var(--background);

}


nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        float: right;
        background-color: var(--background);
        
}

.logo {
    display: flex;
    justify-content: space-between;
    align-items: right;
    font-size: 1.0rem;
    font-weight: bold;
    margin-left: 50px;
    float: right;
    width: auto;
    
}

.nav-links {
    list-style: none;
    display: flex;
    margin: 0px;
    padding: 0;
    width: auto;
    float: right;
    margin-right: 10;
    width: 50%;
    margin-right: -275%;
    margin-left: -50%;
    background-color: var(--background);

    
    
}

.nav-links li {
    margin-right: 0px;
    float: right;
    background-color: var(--background);
}

.nav-links a {
    
    padding: 5px;
    font-weight: bold;
    text-decoration: none;
    float: right;
    margin-right: 0px;
    background-color: var(--background);
}

.nav-links a:hover {
    background-color: var(--background);
    border-radius: 1px;

    
}
</style>
