/**
 * --- IMPORTS ---
 * 
 * The imports for bcrypt and json are important for the authentication functionality.
 * - bcrypt is a library that allows us to hash and compare passwords securely.
 * - json is a utility function that allows us to return JSON responses from the server.
 * 
 * --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 * 
 * --- USES---
 * Used by login.svelte to authenciate users
 * Connects to MongoDB to check if user exists and password is correct
 * 
 * --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 * 
 * 
 * ---OVERVIEW AND FUNCTIONALITY---
 * If user is found and password is correct, a session cookie is set
 * 
 * The password is hashed using bcrypt and compared to the hashed password in the database
 * 
 * Creates a server side cookie which is json object which contains the email/username and full name of the user, the email/username is unique.
 * It returns the followuing error/status messages:
 * 
 * POST function expects a JSON object with the following properties:
 * @param {string} action - "login"
 * @param {string} _username - Username
 * @param {string} user_pass - Password
 * @param {string} fullName - Full name
 * @returns {object} - JSON object with a message or error
 * 
 * --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 * 
 * ---ERRORS/FEEDBACK---
 * It returns the followuing error/status messages:
 * @status {200} - If login is successful
 * @status {400} - If username or password is missing
 * @status {500} - If there is an internal server error
 * 
 * --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 */


import type{ RequestEvent } from "@sveltejs/kit";
import { MongoClient } from "mongodb";
import bcrypt from "bcrypt"; 
import { json } from "@sveltejs/kit";



const MONGO_URI = "mongodb+srv://chestxraygrpacc:y40YFGS0bNGSPHSY@chestxray.qfyks.mongodb.net/?retryWrites=true&w=majority"; // MongoDB URI

export async function POST({ request, cookies }: RequestEvent) { // POST function
    const { action, _username, user_pass, fullName } = await request.json(); // Parse request body

    if (!_username || !user_pass) {
        return json({ error: "Username and password are required" }, { status: 400 });
    }

    const client = new MongoClient(MONGO_URI);

    

    try {
        await client.connect();
        const db = client.db("ChestXraydb");
        const users = db.collection("users");
         if (action === "login") {
            // **Login Logic**
            const user = await users.findOne({ _username });

            if (!user) {
                return json({ error: "User not found" }, { status: 404 });
            }

            const passwordMatch = await bcrypt.compare(user_pass, user.user_pass);
            if (!passwordMatch) {
                return json({ error: "Invalid password" }, { status: 401 });
            }

            // **Set session cookie with full name**
            const sessionData = JSON.stringify({ _username, fullName: user.fullName });
            
            // Web server cookie which lasts for 7 days

            cookies.set("session", sessionData, {
                path: "/",
                httpOnly: true,
                secure: false, // Use `true` in production (requires HTTPS)
                sameSite: "strict",
                maxAge: 60 * 60 * 24 * 7, // Expires in 7 days
            });

            return json({ message: "Login successful!" }, { status: 200 });
        } else {
            return json({ error: "Invalid action" }, { status: 400 });
        }
    } catch (error) {
        console.error(error);
        return json({ error: "Internal server error" }, { status: 500 });
    } finally {
        await client.close();
    }
}