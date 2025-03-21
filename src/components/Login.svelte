<script lang="ts">
    import Button from "../shared/Button.svelte";

    let email = "";
    let password = "";
    let showPassword = false;

    function togglePassword(){
        showPassword = !showPassword;
    }

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
                window.location.href = "/dashboard"; // Redirect user after login
            } else {
                alert(`Error: ${data.error}`);
            }
        } catch (error) {
            console.error("Login failed:", error);
            alert("Something went wrong. Please try again.");
        }
    }

    function handleEmailInput(event: any) {
        email = event.target.value.toLowerCase();
    }
</script>

<main>
    <div class="login-form">
        <div class="form-left">
            <h1>Login</h1>
            <h2>Email</h2>
            <input type="email" placeholder="johnsmith@gmail.com" bind:value={email} on:input={handleEmailInput}/>

            <h2>Password</h2>
            <div class="password">
                {#if showPassword}
                    <input
                        type="text"
                        placeholder="Password"
                        bind:value={password}
                    />
                {:else}
                    <input
                        type="password"
                        placeholder="Password"
                        bind:value={password}
                    />
                {/if}

                <button type="button" class="eye-icon" on:click={togglePassword}>
                    <svg class="shrink-0 size-3.5" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        {#if showPassword}
                            <!-- Eye open icon -->
                            <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path>
                            <circle cx="12" cy="12" r="3"></circle>
                        {:else}
                            <!-- Eye closed icon -->
                            <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path>
                            <circle cx="12" cy="12" r="3"></circle>
                            <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"></path>
                            <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"></path>
                            <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"></path>
                            <line x1="2" x2="22" y1="2" y2="22"></line>
                        {/if}
                    </svg>
                </button>
            </div>
            <div class="forgot-password">
                <a href="/">Forgot password?</a>
            </div>

            <Button on:click={login} style="display:block; width: 60%; font-size: 24px; padding: 15px; margin: auto">Login</Button>
            
            <div class="or-divider">
                <span></span>
                <p>or login with</p>
                <span></span>
            </div>
            
            <div class="social-login">
                <button class="social-btn">
                    <img alt="Google" style="width: 60px; height: 60px" src="/Images/google.png" />
                </button>
                <button class="social-btn">
                    <img alt="Facebook" src="/Images/Facebook.png" />
                </button>
                <button class="social-btn">
                    <img alt="Linkedin" style="width: 53px; height: 53px" src="/Images/Linkedin.png" />
                </button>
            </div>
        </div>
    </div>
</main>

<style>
    :global(body) {
        background-color: var(--background_color);
        color: var(--text_color);
        font-family: 'Montserrat', sans-serif;
        margin: 0;
    }

    main {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 90vh;
        padding: 0 20px;
        background-color: var(--background_color);
        margin-top: 0;
    }

    .login-form {
        display: flex;
        background-color: var(--secondary_color);
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3); /* Drop shadow */
        width: 100%;
        max-width: 600px;
    }

    .form-left {
        text-align: center;
        width: 100%;
        margin: 20px 20px 20px 20px;
        background-color: var(--secondary_color);
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
        padding: 10px;
        font-size: 16px;
        margin-bottom: 20px;
        border: 1px solid #333; 
        border-radius: 5px;
        outline: none;
        background-color: white;
    }

    .password {
        position: relative;
    }

    .eye-icon {
        background: none;
        border: none;
        cursor: pointer;
        position: absolute;
        right: -15px;
        top: 7.5px;
    }

    .forgot-password {
        text-align: right;
        margin-bottom: 20px;
    }

    .forgot-password a {
        color: var(--primary_color);
        text-decoration: none;
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
</style>
