<script>
    import { theme } from "../stores/theme";
</script>

<header>
    <nav>
        <div class="header">
            <a class="logo" href ="/">
              <img src="https://img.icons8.com/?size=100&id=q4yXFoEnYRH7&format=png&color=000000" alt="AI For Chest X-ray" class="logo-icon" />
            </a>
            <div class="header-right">
              <a class="active" href="/">Home</a>
              <a class="about" href="/about">About</a>
              <a href="/login">Login</a>
              <a href="/contact">Contact</a>
            </div>
          </div>
    </nav>
    
</header>
<style>
.header {
  overflow: hidden;
  font-family: 'Montserrat', sans-serif;
  background-color: var(--background_color);
  padding: 15px 10px;
}

.header a {
  float: left;
  text-align: center;
  padding: 12px;
  text-decoration: none;
  font-size: 20px;
  line-height: 25px;
  border-radius: 2px;
  color: var(--grey_text);
  
}

.header a.logo {
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
</style>
