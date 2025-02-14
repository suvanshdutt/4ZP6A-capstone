<script>
    import { onMount } from "svelte";
    import Button from "../shared/Button.svelte";

    // Data variables
    let fileInput;
    let user = { fullName: "Loading..." };
    let reports = [];
    let selectedFile = null;
    let uploadMessage = "";
    let totalReports = 0;

    // Fetch user data and reports using api/user
    async function fetchUserData() {
        try {
            const res = await fetch("/api/user");
            const data = await res.json();
            if (res.ok) {
                user = { fullName: data.fullName };
            } else {
                console.error("Failed to fetch user:", data.error);
            }
        } catch (error) {
            console.error("Error fetching user data:", error);
        }
    }

    // Fetch reports using api/reports
    async function fetchReports() {
        try {
            const res = await fetch("/api/reports");
            const data = await res.json();
            if (res.ok) {
                reports = [...data.reports];
                totalReports = data.totalReports;
            } else {
                console.error("Failed to fetch reports:", data.error);
            }
        } catch (error) {
            console.error("Error fetching reports:", error);
        }
    }
    // Standard triggerFileSelect function to open file dialog, NOT AFFILIATED WITH API DIRECTLY
    function triggerFileSelect(event) {
        event.preventDefault();
        fileInput.click();
    }

    // Handle file change event uses api/upload to upload file
    function handleFileChange(event) {
        const file = event.target.files[0];
        if (file) {
            if (!["image/jpeg", "image/png", "image/webp"].includes(file.type)) {
                uploadMessage = "Invalid file type. Please upload an image.";
                return;
            }
            selectedFile = file;
            uploadMessage = `Selected file: ${file.name}`;
        }
    }
    // Upload file using api/upload endpoint and FormData
    async function uploadFile() {
        if (!selectedFile) {
            uploadMessage = "Please select an image to upload.";
            return;
        }

        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
            const response = await fetch("/api/upload", {
                method: "POST",
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                uploadMessage = "Upload successful!";
                selectedFile = null;
            } else {
                uploadMessage = `Upload failed: ${result.error}`;
            }
        } catch (error) {
            uploadMessage = "Error uploading file.";
            console.error("Upload error:", error);
        }
    }
    onMount(() => {
        fetchUserData();
        fetchReports();
    });
</script>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            font-family: 'Roboto', sans-serif;
        }
    </style>
</head>
<body class="bg-[#fbede9] text-gray-800">

    <div class="flex flex-col md:flex-row">
        <aside class="w-64 bg-[#fbede9] -200 p-4 shadow-lg">
            <h2 class="text-2xl font-bold text-red-600 mb-6">Medical Dashboard</h2>
            <ul>
                <li class="mb-4">
                    <a href="/dashboard" class="flex items-center text-gray-700 hover:text-red-500 transition duration-200">
                        <i class="fas fa-file-upload mr-2"></i> Upload X-Ray
                    </a>
                </li>
                <li class="mb-4">
                    <a href="/dashboard" class="flex items-center text-gray-700 hover:text-red-500 transition duration-200">
                        <i class="fas fa-history mr-2"></i> Report History
                    </a>
                </li>
                <li class="mb-4">
                    <a href="/dashboard" class="flex items-center text-gray-700 hover:text-red-500 transition duration-200">
                        <i class="fas fa-cog mr-2"></i> Settings
                    </a>
                </li>
            </ul>
        </aside>

        <div class="flex-1 flex flex-col">
            <header class="bg-[#fbede9]  p-4 flex justify-between items-center shadow">
                <div class="flex items-center">
                    <!-- Display user's full name, the information  is pulled from the session cook-->
                    <h1 class="text-2xl font-bold text-red-600">Welcome, {user.fullName}</h1> 
                </div>
                <div class="flex items-center space-x-4">
                    <i class="fas fa-bell text-gray-700"></i>
                </div>
            </header>

            <main class="flex-1 p-6">
                <section class="bg-white rounded-lg shadow-lg p-6 mb-6">
                    <h2 class="text-xl font-bold text-red-500 mb-4">Upload X-Ray</h2>
                    <div class="border-dashed border-2 border-red-500 rounded-lg p-10 text-center shadow hover:shadow-xl transition">
                        <p class="text-gray-600 mb-4">Drag and drop your X-Ray files here</p>
                        <!-- Button to trigger file select -->
                        <!-- Uses the api route api/upload to upload the file -->

                        <Button class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-500 transition" on:click={triggerFileSelect}>Browse Files</Button>
                        <input type="file" class="hidden" bind:this={fileInput} on:change={handleFileChange} accept="image/jpeg, image/png, image/webp" />
                        <p class="text-gray-500 mt-2">{uploadMessage}</p>
                        {#if selectedFile}
                            <Button class="mt-4 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-500 transition" on:click={uploadFile}>
                                Upload
                            </Button>
                        {/if}
                    </div>
                </section>

                <section class="bg-white rounded-lg shadow-lg p-6 mb-6">
                    <h2 class="text-xl font-bold text-red-500 mb-4">Report History</h2>
                    <div class="mb-4">
                        <input type="text" placeholder="Search Reports..." class="border rounded-lg p-2 w-full" />
                    </div>
                    <!-- Table that displays reports-->
                    <!-- Uses the api route api/reports to fetch the reports -->
                    <div class="overflow-x-auto">
                        <table class="min-w-full bg-white">
                                <thead>
                                    <tr class="w-full bg-[#fbede9] -200">
                                        <th class="py-2 px-4 text-left cursor-pointer">Date <i class="fas fa-sort"></i></th>
                                        <th class="py-2 px-4 text-left cursor-pointer">Image Name <i class="fas fa-sort"></i></th>
                                        <th class="py-2 px-4 text-left cursor-pointer">Patient Name <i class="fas fa-sort"></i></th>
                                        <th class="py-2 px-4 text-left cursor-pointer">Status</th>
                                        <th class="py-2 px-4 text-left">Action</th>
                                    </tr>
                                </thead>
                            <tbody>
                                
                    <!-- Uses the api route api/reports to fetch the reports -->
                    <!-- Loops through the reports array to display each report -->
                    <!-- Dynamic classes are used to display the status of the report -->
                                {#each reports as report}
                                    <tr class="border-b">
                                        <td class="py-2 px-4">{report.date}</td>
                                        <td class="py-2 px-4">{report.filename}</td>
                                        <td class="py-2 px-4">{report.patientName}</td>
                                        <td class="py-2 px-4">
                                            {#if report.status === "Completed"}
                                                <span class="bg-green-200 text-green-800 px-2 py-1 rounded">Completed</span>
                                            {:else}
                                                <span class="bg-yellow-200 text-yellow-800 px-2 py-1 rounded">Pending</span>
                                            {/if}
                                        </td>
                                        <td class="py-2 px-4">
                                            <button class="text-red-500 hover:underline">Download</button>
                                        </td>
                                    </tr>
                                {/each}
                            </tbody>
                        </table>
                    </div>
                    <div class="flex justify-between mt-4">
                        <span class="text-gray-600">Showing 1-4 of 20 reports</span>
                        <div>
                            <button class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-500 transition">Previous</button>
                            <button class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-500 transition">Next</button>
                        </div>
                    </div>
                </section>

                <section class="bg-white rounded-lg shadow-lg p-6">
                    <h2 class="text-xl font-bold text-red-500 mb-4">Report Summary</h2>
                    <p>Total Reports: {totalReports}</p>
                
                </section>

                <section class="bg-white rounded-lg shadow-lg p-6 mt-6">
                    <h2 class="text-xl font-bold text-red-500 mb-4">Recent Activity</h2>
                    <ul>
                        {#each reports.slice(0, 5) as report}
                            <li class="mb-2">{report.date}: Uploaded {report.filename}</li>
                        {/each}
                    </ul>
                </section>
            </main>
        </div>
    </div>

</body>
</html>
