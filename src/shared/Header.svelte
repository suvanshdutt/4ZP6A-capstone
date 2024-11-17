<script>
    import { theme } from "../stores/theme";
</script>

<header>
    <nav>
        <div class="header">
            <a class="logo" href ="/">AI For Chest X-ray read</a>
            <div class="header-right">
              <a class="active" href="/">Home</a>
              <a href="/login">Login</a>
              <a href="about">Contact</a>
            </div>
          </div>
    </nav>
    
</header>
<style>
.header {
  overflow: hidden;
  font-family: 'Montserrat', sans-serif;
  background-color: var(--background_color);
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
  background-color: var(--background_color);
  
}


.header a.active {
    background-color: var(--background_color);
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
