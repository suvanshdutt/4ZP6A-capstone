/**
 * --- Uses ---
 * THIS API ENDPOINT IS UTILIZED BY DASHBOARD.SVELTE TO RETRIEVE REPORTS FROM THE DATABASE
 * 
 * --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 * 
 * --- Functionality ---
 * 
 * The GET function is the main function that handles the retrieval of reports from the database.
 * 
 * It takes the cookies as a parameter and parses the session from the cookies to check if the user is authenticated.
 * 
 * It connects to the database, retrieves the user's data, and extracts the images array from the user's data.
 * 
 * It formats the image data to include the date, filename, patient name, and status.
 * 
 * The variable img is a json object that contains the image data.
 * - date: The date of the image (converted from timestamp)
 * - filename: The filename of the image
 * - patientName: The patient's name (extracted from the session cookie)
 * - status: The status of the image (placeholder for future use)
 * 
 * It sorts the images by timestamp in descending order (newest first) and returns the reports and the total number of reports.
 * 
 * ASYNC FUNCTION GET()
 * @params {cookies}
 * @returns {json}
 * 
 * --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 * --- Errors/Feedback ---
 * 
 * Following are the error messages that can be returned:
 * - 401: Not authenticated
 * - 404: User not found
 * - 500: Internal server error
 * 
 * --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 */



import { MongoClient } from "mongodb";
import { json } from "@sveltejs/kit";

const MONGO_URI = "mongodb+srv://chestxraygrpacc:y40YFGS0bNGSPHSY@chestxray.qfyks.mongodb.net/?retryWrites=true&w=majority"; // MongoDB URI
const client = new MongoClient(MONGO_URI); 

export async function GET({ cookies }) {
    const sessionToken = cookies.get("session");

    if (!sessionToken) {
        return json({ error: "Not authenticated" }, { status: 401 }); // Unauthorized if no session token
    }

    try {
        await client.connect();
        const db = client.db("ChestXraydb");
        const users = db.collection("users");

        const sessionData = JSON.parse(sessionToken); // Parse cookie
        const user = await users.findOne({ _username: sessionData._username }); // Find user by username

        if (!user) {
            return json({ error: "User not found" }, { status: 404 });
        }

        // Get images sorted by timestamp (newest first)
        const reports = (user.images || [])
            .map((img) => ({
                date: img.timestamp ? new Date(img.timestamp).toLocaleDateString() : "Unknown", // Using timestamp
                filename: img.filename || "Unknown",
                patientName: sessionData.fullName, // Extracted from session cookie
                status: "Pending", // Placeholder TODO : Will need this for when the AI model is connected. 
            }))
            .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)); // Sort by newest first

        return json({ reports, totalReports: reports.length });
    } catch (error) {
        console.error("Database error:", error);
        return json({ error: "Internal server error" }, { status: 500 });
    }
}

