import { MongoClient } from "mongodb";
import bcrypt from "bcrypt";

/**
 * ---Imports---
 * 
 * * MongoClient: A class that allows you to connect to a MongoDB database and run operations on it.
 * * bcrypt: A library to help you hash passwords.
 * 
 * ------------------------------------------------------------------------------------------------------------------------------
 * 
 * ---Usage---
 * 
 * Signup.svelte utilizes this to create a new user in the database.
 * 
 * ------------------------------------------------------------------------------------------------------------------------------
 * 
 * ---Functionality---
 * 
 * This endpoint allows a user to sign up for an account.
 * - POST request a JSON body containing _username, user_pass, and fullName
 * - Checks if the user already exists in the database
 * - Hashes the password using bcrypt
 * - Inserts the new user into the database
 * @param {Request} request
 * @returns {Response} response
 * 
 * ------------------------------------------------------------------------------------------------------------------------------
 * 
 * ---Error Handling/Feedback---
 * 
 * Following are the error/response codes:
 * - 500: Internal server error
 * - 201: User signed up successfully!
 * - 500: Internal server error
 * ------------------------------------------------------------------------------------------------------------------------------
 */
// MongoDB connection URL

const MONGO_URI = "mongodb+srv://chestxraygrpacc:y40YFGS0bNGSPHSY@chestxray.qfyks.mongodb.net/?retryWrites=true&w=majority";

import type { RequestEvent } from "@sveltejs/kit";

export async function POST({ request }: RequestEvent) {
    const { _username, user_pass, fullName } = await request.json(); // Added fullName

    if (!_username || !user_pass || !fullName) {
        return new Response(
            JSON.stringify({ error: "Username, password, and full name are required" }),
            { status: 400, headers: { "Content-Type": "application/json" } }
        );
    } 

    const client = new MongoClient(MONGO_URI);

    try {
        await client.connect();
        const db = client.db("ChestXraydb");
        const users = db.collection("users");

        // Check if user exists
        const existingUser = await users.findOne({ _username });
        if (existingUser) {
            return new Response(
                JSON.stringify({ error: "Username already exists" }),
                { status: 400, headers: { "Content-Type": "application/json" } }
            );
        }

        // Hash password
        const hashedPassword = await bcrypt.hash(user_pass, 10);

        // Insert new user into MongoDB
        await users.insertOne({
            _username,
            user_pass: hashedPassword,
            fullName, // Storing fullName in the database
            images: []
        });

        return new Response(
            JSON.stringify({ message: "User signed up successfully!" }),
            { status: 201, headers: { "Content-Type": "application/json" } }
        );
    } catch (error) {
        console.error(error);
        return new Response(
            JSON.stringify({ error: "Internal server error" }),
            { status: 500, headers: { "Content-Type": "application/json" } }
        );
    } finally {
        await client.close();
    }
}