<script lang="ts">
    import Button from "../shared/Button.svelte";
    
    let fullName = "";
    let email = "";
    let password = "";
    let passwordError = "";
    let showPassword = false;

    function togglePassword(){
        showPassword = !showPassword;
    }

    function validatePassword(password: string): boolean {
        const lengthRequirement = /.{8,}/;
        const specialCharRequirement = /[!@#$%^&*(),.?":{}|<>]/;
        const uppercaseRequirement = /[A-Z]/; // At least 1 uppercase letter
        const numberRequirement = /[0-9]/;

        if (!lengthRequirement.test(password)) {
            passwordError = "Password must be at least 8 characters long.";
            return false;
        }
        if (!specialCharRequirement.test(password)) {
            passwordError = "Password must contain at least 1 special character.";
            return false;
        }
        if (!uppercaseRequirement.test(password)) {
            passwordError = "Password must contain at least 1 uppercase letter.";
            return false;
        }
        if (!numberRequirement.test(password)) {
            passwordError = "Password must contain at least 1 number.";
            return false;
        }

        passwordError = "";
        return true;
    }

    async function signup() {
        if (!validatePassword(password)) {
            return;
        }

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
                window.location.href = "/login"; // Redirect user to login page
            } else {
                alert(`Error: ${data.error}`);
            }
        } catch (error) {
            console.error("Signup failed:", error);
            alert("Something went wrong. Please try again.");
        }
    }

    function handleEmailInput(event: any) {
        email = event.target.value.toLowerCase(); // Convert input to lowercase
    }
</script>

<main>
    <div class="signup-form">
        <div class="title">
            <h1>Sign Up</h1>
        </div>
        <div class="form-container">
            <div class="form-left">
                <h2>Full Name</h2>
                <input placeholder="John Smith" type="text" bind:value={fullName} />

                <h2>Email</h2>
                <input placeholder="johnsmith@gmail.com" type="email" bind:value={email} on:input={handleEmailInput}/>

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

                {#if passwordError}
                    <p class="error">{passwordError}</p>
                {/if}

                <Button on:click={signup} style="display:block; width: 60%; font-size: 24px; padding: 15px; margin: auto; margin-top: 20px">Sign Up</Button>

                <p class="login-link">
                    Already have an account? <a href="/login">Login</a>
                </p>
            </div>
            <div class="form-right">
                <h2>Rules for password</h2>
                <ul>
                    <li>8 characters or longer</li>
                    <li>Must contain 1 special character</li>
                    <li>Must contain at least 1 uppercase letter</li>
                    <li>Must contain at least 1 number</li>
                </ul>
            </div>
        </div>
    </div>
</main>
<style>
    :global(body) {
        background-color: var(--background_color);
        color: var(--text_color, #1e1e1e);
        font-family: 'Montserrat', sans-serif;
        margin: 0;
    }

    main {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 90vh;
        background-color: var(--background_color);
        margin-top: -25px;
    }

    .signup-form {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        height: fit-content;
        max-width: 1000px;
        background-color: var(--secondary_color); 
        padding: 40px;
        margin-top: -60px;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
    }

    .title {
        text-align: center;
        margin-top: -15px;
    }

    .form-container {
        display: flex; 
        flex-direction: row;
        justify-content: space-between;
        width: 100%;
        margin-top: -10px;
    }

    .form-left {
        width: 50%;
    }

    .form-right{
        padding-left: 80px;
        width: 45%
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

    .error {
        color: red;
        font-size: 14px;
        margin-top: -10px;
        margin-bottom: 10px;
    }

    .login-link {
        font-size: 16px;
        color: #333;
        margin-top: 50px;
    }

    .login-link a {
        color: #f03e3e;
        text-decoration: none;
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
