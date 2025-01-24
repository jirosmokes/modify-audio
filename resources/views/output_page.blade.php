<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Akira</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>

    <style>
        /* Optional: Style the drop area */
        .drop-area {
            border: 5px solid #1A3C10;
            padding: 20px;
            border-radius: 10px;
            min-height: 200px;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: background-color 0.3s;
            color: #1A3C10;
        }
    </style>
</head>
<body class="bg-gray-100 font-sans flex flex-col min-h-screen">

    <!-- Header Section -->
    <header class="bg-[#1A3C10] text-white text-center py-12">
        <h1 class="text-4xl sm:text-5xl font-bold leading-tight">Welcome to Akira</h1>
        <p class="mt-4 text-lg sm:text-xl">Innovating Child-Friendly Audio Experiences</p>
    </header>

    <!-- Main Content -->
    <div class="flex-grow">
        <div class="max-w-4xl mx-auto mt-12">
            <h3 class="text-4xl font-semibold text-center text-[#1A3C10] mb-4">Processed Video</h3>
            
            <div class="flex justify-between space-x-8">
                <div id="drop-area" 
                     class="drop-area flex-1 h-64 border border-gray-400 rounded-lg bg-gray-100 text-center flex items-center justify-center bg-[#F1FBEF]">
                  <p class="text-[#1A3C10]-800 text-2xl font-medium">Old Video</p>
                </div>
                <div id="drop-area"  
                     class="drop-area flex-1 h-64 border border-gray-400 rounded-lg bg-gray-100 text-center flex items-center justify-center bg-[#F1FBEF]">
                  <p class="text-[#1A3C10]-800 text-2xl font-medium">New Video</p>
                </div>
            </div>
        </div>
        <div class="text-center">
            <form action="/wala_pa" method="POST">
                @csrf
                <button type="submit" name="submit" class="mb-5 mt-6 px-8 py-3 bg-[#1A3C10] text-white font-semibold text-lg rounded-md hover:bg-[#145A02] transition duration-300 focus:outline-none focus:ring-4 focus:ring-[#145A02] focus:ring-opacity-50">
                    Download
                </button>
            </form>
        </div>
    </div>

    <!-- Footer Section -->
    <footer class="bg-[#1A3C10] text-white py-8">
        <div class="text-center">
            <p class="text-sm">&copy; 2025 Akira. All Rights Reserved.</p>
            <p class="text-sm mt-2">Developed by <strong>Akira</strong> | Contact: <a href="mailto:akira@gmail.com" class="text-[#145A02] hover:text-white">akira@gmail.com</a></p>
        </div>
    </footer>

</body>
</html>
