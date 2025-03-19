/**
 * ---IMPORTS---
 * 
 * The imports for Binary and sharp are important for the MongoDB and image processing functionality.
 * 
 * Sharp is a high-performance image processing library that allows us to resize and compress images before storing them in the database.
 * 
 * The Binary class is used to store binary data in MongoDB. We will use it to store the compressed image data.
 * --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 * ---Usage---
 * THIS API ENDPOITN IS UTLIZED BY DASHHOARD.SVELTE TO UPLOAD IMAGES TO THE DATABASE
 * --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 * 
 * ---Overview and Functionality---
 * The ALLOWED_MIME_TYPES array contains the MIME types that are allowed for image uploads. We will only accept JPEG, PNG, and WebP images.
 * 
 * The connectDB function is an async function that connects to the MongoDB database and returns the database object
 * 
 * The POST function is the main function that handles the image upload. 
 * - It takes the request and cookies as parameters.
 * - It parses the session from the cookies and checks if the user is authenticated.
 * - It gets the uploaded file from the request data. It checks if the file is a valid image and if it is one of the allowed MIME types.
 * - It converts the file to a buffer and compresses the image using sharp.
 * - It connects to the database, stores the compressed image data, and updates the user's images array with the new image.
 * - It returns a success message if the upload is successful or an error message if there is an issue.
 * 
 * @params {request, cookies}
 * @returns {json}
 * 
 * --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 * ---Errors/Feedback---
 * 
 * Following are the error messages that can be returned:
 * 
 * - 401: Not authenticated
 * - 400: Invalid session data  or Session missing username
 * - 400: No valid image uploaded
 * - 415: Invalid file type. Only JPEG, PNG, and WebP are allowed.
 * - 404: User not found or image not saved
 * - 500: Internal server error
 * 
 * It returns the following success message 
 * - 201: Upload successful
 * --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 */


import { MongoClient, Binary } from "mongodb";
import { json } from "@sveltejs/kit";
import sharp from "sharp";
import type { RequestEvent } from "@sveltejs/kit";
import { v4 as uuidv4 } from 'uuid';
import zlib from 'zlib';

const MONGO_URI = "mongodb+srv://chestxraygrpacc:y40YFGS0bNGSPHSY@chestxray.qfyks.mongodb.net/?retryWrites=true&w=majority"; 
const DATABASE_NAME = "ChestXraydb";
const HF_SPACE_URL = "https://chestanalysis-dense121.hf.space"; // Space URL

const ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp"];

async function connectDB() {
    const client = new MongoClient(MONGO_URI);
    await client.connect();
    return client.db(DATABASE_NAME);
}

interface ImageData {
    uid: string,
    filename: string;
    data: Binary;
    predictions: number[];
    heatmap?: Binary;
    timestamp: Date;
    status: string;
}

interface UserDocument {
    _username: string;
    images?: ImageData[];
}

async function pollForResult(eventId: string): Promise<any> {
    const pollUrl = `${HF_SPACE_URL}/gradio_api/call/predict/${eventId}`;

    for (let attempt = 0; attempt < 30; attempt++) { // Poll for up to 30 seconds
        const response = await fetch(pollUrl, {
            method: "GET",
            headers: { "Accept": "application/json" }
        });

        if (response.ok) {
            const text = await response.text();
            if (text.includes("event: complete")) {
                const jsonString = text.split("data: ")[1];
                return JSON.parse(jsonString);
            }
        }

        await new Promise((res) => setTimeout(res, 1000)); // Wait 1s before retrying
    }

    throw new Error("Polling timed out");
}

export async function POST({ request, cookies }: RequestEvent) {
    const sessionCookie = cookies.get("session");
    if (!sessionCookie) {
        return json({ error: "Not authenticated" }, { status: 401 });
    }

    let session;
    try {
        session = JSON.parse(sessionCookie);
    } catch {
        return json({ error: "Invalid session data" }, { status: 400 });
    }

    const username = session._username;
    if (!username) {
        return json({ error: "Session missing username" }, { status: 400 });
    }

    const data = await request.formData();
    const file = data.get("file");

    if (!file || !(file instanceof Blob)) {
        return json({ error: "No valid image uploaded" }, { status: 400 });
    }

    if (!ALLOWED_MIME_TYPES.includes(file.type)) {
        return json({ error: "Invalid file type. Only JPEG, PNG, and WebP are allowed." }, { status: 415 });
    }

    try {
        const arrayBuffer = await file.arrayBuffer();
        const inputBuffer = Buffer.from(arrayBuffer);

        const compressedBuffer = await sharp(inputBuffer)
            .resize(512)
            .jpeg({ quality: 70 })
            .toBuffer();

        const db = await connectDB();
        const users = db.collection<UserDocument>("users");

        const uniqueId = uuidv4();

        const newImage: ImageData = {
            uid: uniqueId,
            filename: file.name,
            data: new Binary(compressedBuffer),
            predictions: [],
            timestamp: new Date(),
            status: "Pending"
        };

        const updateResult = await users.updateOne(
            { _username: username },
            { $push: { images: newImage } as any }
        );
        const base64Image = Buffer.from(newImage.data.buffer).toString("base64");
        

        if (updateResult.modifiedCount === 0) {
            return json({ error: "User not found or image not saved" }, { status: 404 });
        }

        console.log(" Image saved to MongoDB. Sending to Hugging Face...");

        // Step 1: Send Base64 image to Hugging Face API
        const hfInitResponse = await fetch(`${HF_SPACE_URL}/gradio_api/call/predict`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ data: [base64Image] }) 
        });

        if (!hfInitResponse.ok) {
            console.error("Hugging Face API Error:", await hfInitResponse.text());
            return json({ error: "Hugging Face request failed" }, { status: 500 });
        }

        const initResult = await hfInitResponse.json();
        const eventId = initResult.event_id;

        if (!eventId) {
            console.error(" ERROR: Hugging Face API did not return an event_id");
            return json({ error: "Failed to retrieve event_id from Hugging Face" }, { status: 500 });
        }

        console.log("EVENT_ID retrieved:", eventId);


        const predictionResponse = await fetch(`${HF_SPACE_URL}/gradio_api/call/predict/${eventId}`, {
            method: "GET",
            headers: { "Accept": "application/json" }
        });
        

        
        if (!predictionResponse.ok) {
            console.error("ERROR: Failed to fetch prediction from Hugging Face");
            return json({ error: "Failed to fetch prediction" }, { status: 500 });
        }
        
        
        // Read response as text since it's not standard JSON
        const textResponse = await predictionResponse.text();
        console.log("Raw API Response:", textResponse);
        
        //  Extract JSON part manually
        const match = textResponse.match(/data:\s*(\[.*\])/s);
        if (!match) {
            console.error("ERROR: Failed to extract JSON from response");
            return json({ error: "Invalid API response format" }, { status: 500 });
        }
        
        const jsonData = JSON.parse(match[1]); // Extract JSON array
        console.log("Prediction received:", Object.values(jsonData[0].predictions)) ;

        // Extract heatmap
        //push the heatmap to the database
       

        const heatmapBase64 = jsonData[0].heatmap;
        const heatmapBuffer = Buffer.from(heatmapBase64, "base64");

        const compressedHeatmapBuffer = await sharp(heatmapBuffer)
            .resize(512)
            .jpeg({ quality: 70 })
            .toBuffer();

        
        // Update predictions in MongoDB
        await users.updateOne(
            { _username: username, "images.uid": uniqueId, "images.filename": file.name},
            { 
                $set: { 
                    "images.$.predictions": Object.values(jsonData[0].predictions),
                    "images.$.status": "Completed",
                    "images.$.heatmap": new Binary(compressedHeatmapBuffer)
                } as any }// Extract predictions object
        );
        
        return json({ message: "Upload and prediction successful", prediction: jsonData[0].predictions}, { status: 201 })

    } catch (error) {
        console.error("Error:", error);
        return json({ error: "Internal server error" }, { status: 500 });
    }
}


