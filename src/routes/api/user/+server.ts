
/**
 * ---Usage---
 * Used by dashboard.svelte to get user information, such as full name and email address which is used to display the user's name on the dashboard
 * --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 * 
 * ---Overview and Functionality---
 * GET function expects a session cookie to be set with the user's email/username
 * 
 * In our case, the cookie is named "session" and is a JSON object with the following properties:
 * @param {string} _username - Username
 * @param {string} fullName - Full name
 * 
 * The function connects to MongoDB to get the user's full name and email address
 * it returns a JSON object with the user's full name and email address.
 * 
 * --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 * ---Errors/Feedback---
 * The following are the error messages that can be returned:
 * - 401: Not authenticated
 * - 400: Invalid session data
 * - 404: User not found
 * - 500: Internal server error
 * --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 */

import { MongoClient } from "mongodb";
import { json } from "@sveltejs/kit";


const MONGO_URI = "mongodb+srv://chestxraygrpacc:y40YFGS0bNGSPHSY@chestxray.qfyks.mongodb.net/?retryWrites=true&w=majority";

export async function GET({ cookies }) {
    const session = cookies.get("session");

    if (!session) {
        return json({ error: "Not authenticated" }, { status: 401 });
    }

    let sessionData;
    try {
        sessionData = JSON.parse(session); // Parse session as JSON
    } catch (err) {
        return json({ error: "Invalid session data" }, { status: 400 });
    }

    const client = new MongoClient(MONGO_URI);
    try {
        await client.connect();
        const db = client.db("ChestXraydb");
        const users = db.collection("users");

        const user = await users.findOne({ _username: sessionData._username });

        if (!user) {
            return json({ error: "User not found" }, { status: 404 });
        }
        return json({
            fullName: user.fullName,
            email: user._username
        });

    } catch (error) {
        console.error("Database error:", error);
        return json({ error: "Internal server error" }, { status: 500 });
    } finally {
        await client.close();
    }
}