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


import type { RequestEvent } from "@sveltejs/kit"; // type import
import { MongoClient } from "mongodb";
import { json } from "@sveltejs/kit";
import { v4 as uuidv4 } from 'uuid';
const MONGO_URI = "mongodb+srv://chestxraygrpacc:y40YFGS0bNGSPHSY@chestxray.qfyks.mongodb.net/?retryWrites=true&w=majority"; // MongoDB URI
const client = new MongoClient(MONGO_URI); 

interface ImageData {
    uid?: string;
    filename?: string;
    timestamp?: string; // Ensure timestamp is a string
    status?: string;
}

interface Report {
    uid: string;
    date: string;
    filename: string;
    patientName: string;
    status: string;
    timestamp: string; // Needed for sorting
}

function getOrdinalSuffix(day: number): string {
    if (day > 3 && day < 21) return 'th'; // Covers 11th to 19th
    switch (day % 10) {
        case 1: return 'st';
        case 2: return 'nd';
        case 3: return 'rd';
        default: return 'th';
    }
}
const tokens = new Map(); // Temporary in-memory storage

function generateToken(heatmap:string): string {
    const token = uuidv4();
    tokens.set(token, heatmap);

    // Auto-expire tokens after 5 minutes
    setTimeout(() => tokens.delete(token), 5 * 60 * 1000);

    return token;
}

export async function GET({ cookies, url }: RequestEvent) {
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

        // Check if a specific report is requested via the query parameter "id"
        const reportId = url.searchParams.get("id");
        if (reportId) {
            const foundImage = (user.images || []).find((img: ImageData) => img.uid === reportId);
            if (!foundImage || !foundImage.data) {
                return json({ error: "Report not found" }, { status: 404 });
            }
            // Convert binary image data to a Base64-encoded string.
            const base64Image = Buffer.from(foundImage.data.buffer).toString("base64");
            // Assuming the image is stored as JPEG; adjust MIME type if needed.
            const imageUrl = `data:image/jpeg;base64,${base64Image}`;

            // Include predictions in the response
            const predictions = foundImage.predictions || []; // Extract predictions, default to empty array if none

            
            const heatmap = foundImage.heatmap; // Extract heatmap, default to empty string if none
            const heatmapBase64 = Buffer.from(heatmap.buffer).toString("base64");
            const heatmapUrl = `data:image/jpeg;base64,${heatmapBase64}`;

            return json({ imageUrl, predictions, heatmapUrl });
        }

        const easternTimeFormatter = new Intl.DateTimeFormat('en-US', {
            timeZone: 'America/New_York',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        });

        // Get images sorted by timestamp (newest first)
        const reports: Report[] = (user.images || []).map((img: ImageData): Report => {
            const date = img.timestamp ? new Date(img.timestamp) : null;
            const parts = date ? easternTimeFormatter.formatToParts(date) : [];
            const day = parts.find(part => part.type === 'day')?.value;
            const month = parts.find(part => part.type === 'month')?.value;
            const year = parts.find(part => part.type === 'year')?.value;
            const hour = parts.find(part => part.type === 'hour')?.value;
            const minute = parts.find(part => part.type === 'minute')?.value;
            const dayPeriod = parts.find(part => part.type === 'dayPeriod')?.value;

            const formattedDate = date ? `${day}${getOrdinalSuffix(Number(day))} ${month} ${year}, ${hour}:${minute} ${dayPeriod}` : "Unknown";

            return {
                uid: img.uid || "Unknown",
                date: formattedDate,
                filename: img.filename || "Unknown",
                patientName: sessionData.fullName,
                status: img.status || "Pending",
                timestamp: img.timestamp || "", // Ensure string type for sorting
            };
        });

        // Sort by timestamp (newest first)
        reports.sort((a: Report, b: Report) => {
            const timeA = a.timestamp ? new Date(a.timestamp).getTime() : 0;
            const timeB = b.timestamp ? new Date(b.timestamp).getTime() : 0;
            return timeB - timeA; 
        });

        return json({ reports, totalReports: reports.length });
    } catch (error) {
        console.error("Database error:", error);
        return json({ error: "Internal server error" }, { status: 500 });
    }
}

