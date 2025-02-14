<script lang="ts">
    import Button from "../shared/Button.svelte";

    let email = "";
    let password = "";

    async function login() {
        const payload = {
            action: "login",
            _username: email,
            user_pass: password
        };

        try {
            const response = await fetch("/api/auth", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok) {
                alert("Login successful! Redirecting to dashboard...");
                window.location.href = "/dashboard"; // Redirect user after login
            } else {
                alert(`Error: ${data.error}`);
            }
        } catch (error) {
            console.error("Login failed:", error);
            alert("Something went wrong. Please try again.");
        }
    }
</script>

<main>
    <div class="login-form">
        <div class="form-left">
            <h1>Email</h1>
            <input type="email" placeholder="Johnsmith@gmail.com" bind:value={email} />

            <h1>Password</h1>
            <input type="password" placeholder="Password" bind:value={password} />

            <div class="forgot-password">
                <a href="/">Forgot password?</a>
            </div>

            <button class="login-btn" on:click|preventDefault={login}>Login</button>
        </div>

        <!-- Divider Line -->
        <div class="divider-line"></div>

        <div class="form-right">
            <h2>Rules for password</h2>
            <ul>
                <li>8 characters or longer</li>
                <li>Must contain 1 special character</li>
                <li>Must contain at least 6 letters</li>
                <li>Must contain at least 1 number</li>
            </ul>
        </div>
    </div>
</main>

<style>
    :global(body) {
        background-color: var(--background_color); /* Pinkish background */
        color: var(--text_color);
        font-family: 'Montserrat', sans-serif;
        margin: 0;
    }

    main {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin-top: -10vh;
    }

    .login-form {
        display: flex;
        justify-content: space-between;
        width: 100%;
        max-width: 1200px;
        background-color: var(--background_color); /* Pinkish background */
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }

    .form-left, .form-right {
        width: 48%;
    }

    h1, h2 {
        font-size: 24px;
        margin-bottom: 10px;
        color: #333;
        font-weight: 700;
    }

    input {
        width: 100%;
        padding: 10px;
        font-size: 16px;
        margin-bottom: 20px;
        border: 1px solid #333; 
        border-radius: 5px;
        outline: none;
    }

    .forgot-password {
        text-align: right;
        margin-bottom: 20px;
    }

    .forgot-password a {
        color: red;
        text-decoration: none;
    }

    .login-btn {
        display: block;
        width: 100%;
        background-color: #f03e3e;
        color: white;
        padding: 15px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .login-btn:hover {
        background-color: #d33d3d;
    }

    /* Divider Line Styling */
    .divider-line {
        width: 50px;
        height: 100%; 
        background-color: #333; 
        margin: 0 40px;  
    }

    .form-right {
        background-color: #fceceb; 
        padding-left: 80px; 
    }

    ul {
        list-style-type: disc; /* Bullet points */
        padding-left: 20px;
    }

    ul li {
        font-size: 18px;
        margin-bottom: 10px;
    }
</style>
