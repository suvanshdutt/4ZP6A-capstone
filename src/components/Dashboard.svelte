<script lang="ts">
    import { onMount } from "svelte";
    import Button from "../shared/Button.svelte";
    import { isLoggedIn } from "../stores/authStore";
    isLoggedIn.set(true);

    // Data variables
    let fileInput: any;
    let user = { fullName: "Loading..." };
    let reports:any[] = [];
    let selectedFile:any = null;
    let uploadMessage = "";
    let totalReports = 0;
    let showLogoutDialog = false;
    let searchQuery = "";

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
            // Log additional error details
            if (error instanceof TypeError) {
                console.error("Network error or CORS issue:", error.message);
            } else {
                console.error("Unexpected error:", error);
            }
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
            // Log additional error details
            if (error instanceof TypeError) {
                console.error("Network error or CORS issue:", error.message);
            } else {
                console.error("Unexpected error:", error);
            }
        }
    }
    // Standard triggerFileSelect function to open file dialog, NOT AFFILIATED WITH API DIRECTLY
    function triggerFileSelect(event: any) {
        event.preventDefault();
        fileInput.click();
    }

    // Handle file change event uses api/upload to upload file
    function handleFileChange(event: any) {
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
                await fetchReports();
                location.reload();
            } else {
                uploadMessage = `Upload failed: ${result.error}`;
            }
        } catch (error) {
            uploadMessage = "Error uploading file.";
            console.error("Upload error:", error);
            if (error instanceof TypeError) {
                console.error("Network error or CORS issue:", error.message);
            } else {
                console.error("Unexpected error:", error);
            }
        }
    }

    function handleLogout() {
        window.location.href = "/";
    }

    function confirmLogout() {
        showLogoutDialog = true;
    }

    function cancelLogout() {
        showLogoutDialog = false;
    }

    function scrollToReportHistory() {
        const reportHistorySection = document.getElementById('report-history');
        if (reportHistorySection) {
            reportHistorySection.scrollIntoView({ behavior: 'smooth' });
        }
    }

    function ViewResult(report:any) {
        window.location.href = `/result?id=${report.uid}`;
    }

    $: filteredReports = reports.filter(report => 
        report.filename.toLowerCase().includes(searchQuery.toLowerCase())
    );

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

<!-- Logout Confirmation Dialog -->
{#if showLogoutDialog}
    <div class="dialog-box-bg">
        <div class="dialog-box">
            <button class="close-button" on:click={cancelLogout} type="button">
                <img class="close-icon" src="https://img.icons8.com/?size=100&id=7FSknHLAHdnP&format=png&color=da3029" alt="close"/>
            </button>
            <h2 class="heading2">Are you sure you want to logout?</h2>
            <div class="logout-buttons">
                <Button inverse={true} on:click={cancelLogout} style="font-weight:normal; padding: 7px 15px; border-radius: 10px">Cancel</Button>
                <Button on:click={handleLogout} style="font-weight:normal; padding: 7px 15px; border-radius: 10px;">Logout</Button>
            </div>
        </div>
    </div>
{/if}

<body class="bg-[#fbede9] text-gray-800">

    <div class="flex flex-col md:flex-row">
        <aside class="w-64 bg-[#fbede9] -200 p-4 shadow-lg">
            <h2 class="text-2xl font-bold text-red-600 mb-6">Medical Dashboard</h2>
            <ul>
                <li class="mb-4">
                    <button on:click={triggerFileSelect} class="flex items-center text-gray-700 hover:text-red-500 transition duration-200" type="button">
                        <i class="fas fa-file-upload mr-2"></i> Upload X-Ray
                    </button>
                </li>
                <li class="mb-4">
                    <button on:click={scrollToReportHistory} class="flex items-center text-gray-700 hover:text-red-500 transition duration-200" type="button">
                        <i class="fas fa-history mr-2"></i> Report History
                    </button>
                </li>
                <li class="mb-4">
                    <button on:click={confirmLogout} class="flex items-center text-gray-700 hover:text-red-500 transition duration-200" type="button">
                        <i class="fas fa-sign-out-alt mr-2"></i> Log Out
                    </button>
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
                    <button on:click={confirmLogout} class="logout-button" type="button">
                        Log Out
                    </button>
                </div>
            </header>

            <main class="flex-1 p-6">
                <section class="bg-white rounded-lg shadow-lg p-6 mb-6">
                    <h2 class="text-xl font-bold text-red-500 mb-4">Upload X-Ray</h2>
                    <div class="border-dashed border-2 border-red-500 rounded-lg pt-10 pb-6 text-center custom-shadow hover:shadow-xl transition">
                        <p class="text-gray-600 mb-4">Upload your X-Ray files here</p>
                        <!-- Button to trigger file select -->
                        <!-- Uses the api route api/upload to upload the file -->

                        <Button on:click={triggerFileSelect}>Browse Files</Button>
                        <input type="file" class="hidden" bind:this={fileInput} on:change={handleFileChange} accept="image/jpeg, image/png, image/webp" />
                        <p class="text-gray-500 mt-6 mb-2">{uploadMessage}</p>
                        {#if selectedFile}
                            <Button on:click={uploadFile}>
                                Upload
                            </Button>
                        {/if}
                    </div>
                </section>

                <section id="report-history" class="bg-white rounded-lg shadow-lg p-6 mb-6">
                    <h2 class="text-xl font-bold text-red-500 mb-4">Report History</h2>
                    <div class="mb-4">
                        <input 
                            type="text" 
                            placeholder="Search Reports..." 
                            class="border rounded-lg p-2 w-full" 
                            bind:value={searchQuery}
                        />
                    </div>
                    <!-- Table that displays reports-->
                    <!-- Uses the api route api/reports to fetch the reports -->
                    <div class="overflow-x-auto">
                        <table class="min-w-full bg-white">
                                <thead>
                                    <tr class="w-full bg-[#fbede9] -200">
                                        <th class="py-2 px-4 text-left">Date</th>
                                        <th class="py-2 px-4 text-left">Image Name</th>
                                        <th class="py-2 px-4 text-left">Patient Name</th>
                                        <th class="py-2 px-4 text-left">Status</th>
                                        <th class="py-2 px-4 text-left">Action</th>
                                    </tr>
                                </thead>
                            <tbody>
                                
                    <!-- Uses the api route api/reports to fetch the reports -->
                    <!-- Loops through the reports array to display each report -->
                    <!-- Dynamic classes are used to display the status of the report -->
                                {#each filteredReports as report}
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
                                            {#if report.status === "Completed"}
                                                <button class="text-red-500 hover:underline" on:click={() => ViewResult(report)}>View Results</button>
                                            {:else}
                                                <span class="bg-yellow-200 text-yellow-800 px-2 py-1 rounded">Pending</span>
                                            {/if}
                                            
                                        </td>
                                    </tr>
                                {/each}
                            </tbody>
                        </table>
                    </div>
                    <div class="flex justify-between mt-4">
                        <span class="text-gray-600">Showing {filteredReports.length} reports</span>
                        <div class="flex gap-6">
                            <Button style="font-weight:normal; padding: 7px 15px; border-radius: 10px"> Back</Button>
                            <Button style="font-weight:normal; padding: 7px 15px; border-radius: 10px"> Next</Button>
                        </div>
                    </div>
                </section>

                <!-- Removed summary for now, not usefull-->
                <!-- <section class="bg-white rounded-lg shadow-lg p-6">
                    <h2 class="text-xl font-bold text-red-500 mb-4">Report Summary</h2>
                    <p>Total Reports: {totalReports}</p>
                
                </section> -->

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


<style>
    .custom-shadow:hover {
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    }

    .dialog-box-bg {
        position: fixed;
        inset: 0;
        background-color: rgba(0,0,0,0.3); 
        backdrop-filter: blur(1px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 100;
    }

    .dialog-box {
        position: relative;
        background-color: var(--background_color);
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.25);
        max-width: 400px;
        width: 90%;
        padding-top: 40px;
    }

    .close-button {
        background: none;
        border: none;
        cursor: pointer;
        font-size: 16px;
        position: absolute;
        top: 15px;
        right: 15px;
    }

    .close-icon {
        width: 24px;
        height: 24px;
    }

    .heading2 {
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        color: var(--heading_text);
    }

    .logout-buttons {
        display: flex;
        justify-content: center;
        gap: 50px;
    }

    .logout-button {
        color: var(--grey_text);
        transition: color 0.3s ease-in-out;
        margin-right: 15px;
        font-size: 18px;
        font-weight: bold;
    }

    .logout-button:hover {
        color: red;
    }
</style>