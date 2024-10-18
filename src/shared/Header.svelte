<script>
    import { theme } from "../stores/theme";
</script>

<header style="--background: {$theme.background_color};">
    <nav>
        <div class="header">
            <a class="logo">AI For Chest X-ray read</a>
            <div class="header-right">
              <a class="active" href="#home">Home</a>
              <a href="contact">Login</a>
              <a href="about">Contact</a>
            </div>
          </div>
    </nav>
    
</header>
<style>
.header {
  overflow: hidden;
  background-color: var(--background);
  padding: 20px 10px;
}

.header a {
  float: left;
  text-align: center;
  padding: 12px;
  text-decoration: none;
  font-size: 18px;
  line-height: 25px;
  border-radius: 2px;
  color: grey;
  
}

.header a.logo {
  font-size: 20px;
  font-weight: bold;
}


.header a:hover {
  background-color: var(--background);
  
}


.header a.active {
    background-color: var(--background);
}

/* Float the link section to the right */
.header-right {
  float: right;
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
</style>
