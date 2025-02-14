<script>
    let fullName = "";
    let email = "";
    let password = "";

    async function signup() {
        const payload = {
            _username: email, // Using email as the username
            user_pass: password,
            fullName: fullName // Optional
        };

        try {
            // Call SvelteKit's backend API
            const response = await fetch("/api/signup", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const data = await response.json();

            if (response.ok) {
                alert("Sign-up successful! Redirecting to login...");
                window.location.href = "/login"; // Redirect user to login page
            } else {
                alert(`Error: ${data.error}`);
            }
        } catch (error) {
            console.error("Signup failed:", error);
            alert("Something went wrong. Please try again.");
        }
    }
</script>

<main>
    <div class="signup-form">
        <div class="form-left">
            <h1>Sign Up</h1>

            <h2>Full Name</h2>
            <input placeholder="John Smith" type="text" bind:value={fullName} />

            <h2>Email</h2>
            <input placeholder="Johnsmith@gmail.com" type="email" bind:value={email} />

            <h2>Password</h2>
            <input placeholder="Password" type="password" bind:value={password} />

            <button class="signup-btn" on:click|preventDefault={signup}>Sign Up</button>

            <div class="or-divider">
                <span></span>
                <p>or sign up with</p>
                <span></span>
            </div>

            <div class="social-login">
                <button class="social-btn">
                    <img alt="Google" src="/Images/google.png" />
                </button>
                <button class="social-btn">
                    <img alt="Facebook" src="/Images/Facebook.png" />
                </button>
                <button class="social-btn">
                    <img alt="Linkedin" src="/Images/Linkedin.png" />
                </button>
            </div>

            <p class="login-link">
                Already have an account? <a href="/login">Login</a>
            </p>
        </div>
    </div>
</main>
<style>
    :global(body) {
        background-color: #fceceb;
        color: var(--text_color, #1e1e1e);
        font-family: 'Montserrat', sans-serif;
        margin: 0;
    }

    main {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 90vh;
        padding: 0 20px;
        background-color: #fceceb;
        margin-top: 0;
    }

    .signup-form {
        background-color: #fceceb;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3); /* Drop shadow */
        width: 100%;
        max-width: 600px;
    }

    .form-left {
        text-align: center;
    }

    h1 {
        font-size: 28px;
        color: #333;
        font-weight: 700;
        margin-bottom: 20px;
    }

    h2 {
        font-size: 18px;
        color: #333;
        font-weight: 600;
        text-align: left;
        margin-bottom: 10px;
    }

    input {
        width: 100%;
        padding: 12px;
        font-size: 16px;
        margin-bottom: 20px;
        border: 1px solid #333;
        border-radius: 5px;
        outline: none;
    }

    .signup-btn {
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

    .signup-btn:hover {
        background-color: #d33d3d;
    }

    .or-divider {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 20px 0;
        color: #333;
    }

    .or-divider span {
        width: 40px;
        height: 1px;
        background-color: #333;
        margin: 0 10px;
    }

    .social-login {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-bottom: 20px;
    }

    .social-btn {
        background-color: transparent;
        border: none;
        cursor: pointer;
    }

    .social-btn img {
        width: 40px;
        height: 40px;
    }

    .login-link {
        font-size: 16px;
        color: #333;
    }

    .login-link a {
        color: #f03e3e;
        text-decoration: none;
    }
</style>
