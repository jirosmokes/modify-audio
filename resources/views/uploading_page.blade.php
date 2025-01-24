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
            border: 2px dashed #1A3C10;
            background-color: #F1FBEF;
            padding: 20px;
            border-radius: 10px;
            min-height: 200px;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: background-color 0.3s;
        }
        .drop-area.hover {
            background-color: #e3f7e3;
        }
    </style>
</head>
<body class="bg-gray-100 font-sans">

    <!-- Header Section -->
    <header class="bg-[#1A3C10] text-white text-center py-12">
        <h1 class="text-4xl sm:text-5xl font-bold leading-tight">Welcome to Akira</h1>
        <p class="mt-4 text-lg sm:text-xl">Innovating Child-Friendly Audio Experiences</p>
    </header>

    <!-- Main Content Section -->
    <div class="max-w-4xl mx-auto bg-[#F1FBEF] p-8 rounded-2xl shadow-xl mt-10">
    <!-- Tutorial Section -->
        <h3 class="text-2xl font-semibold text-center text-[#1A3C10] mb-6">How to Use the Drag-and-Drop Feature</h3>
        <div class="space-y-4">
            <p class="text-lg text-gray-700">
                Follow these simple steps to upload your file using our drag-and-drop feature:
            </p>
            <ul class="pl-6 text-lg text-gray-700">
                <li><strong>Step 1:</strong> Click anywhere inside the dashed box below to open your file explorer.</li>
                <li><strong>Step 2:</strong> Drag a file from your computer and drop it into the dashed box.</li>
                <li><strong>Step 3:</strong> After dropping the file, a notification will appear showing the file name.</li>
                <li><strong>Step 4:</strong> Click "Learn More" to learn how we process the file for child-friendly listening.</li>
            </ul>
            <p class="text-lg text-gray-700">
                You can also directly click on the box to select a file from your computer.
            </p>
        </div>
    </div>

    <!-- Drag and Drop Section -->
    <div class="max-w-4xl mx-auto mt-12">
        <h3 class="text-2xl font-semibold text-center text-[#1A3C10] mb-4">Drag and Drop Your File</h3>
        
        <!-- Drop Area -->
        <div id="drop-area" class="drop-area">
            <p class="text-gray-600">Drag and drop a file here, or click to select one.</p>
        </div>
        
        <input id="file-input" type="file" class="hidden" />
    </div>

    <!-- Footer Section -->
    <footer class="bg-[#1A3C10] text-white py-6 mt-12">
        <div class="text-center">
            <p class="text-sm">&copy; 2025 Akira. All Rights Reserved.</p>
            <p class="text-sm mt-2">Developed by <strong>Akira</strong> | Contact: <a href="mailto:youremail@example.com" class="text-[#145A02] hover:text-white">akira@gmail.com</a></p>
        </div>
    </footer>

    <script>
        // Get the drop area and input element
        const dropArea = document.getElementById('drop-area');
        const fileInput = document.getElementById('file-input');

        // Add drag events for drop area
        dropArea.addEventListener('dragover', (event) => {
            event.preventDefault();  // Prevent default behavior (Prevent file opening)
            dropArea.classList.add('hover');
        });

        dropArea.addEventListener('dragleave', () => {
            dropArea.classList.remove('hover');
        });

        dropArea.addEventListener('drop', (event) => {
            event.preventDefault();
            dropArea.classList.remove('hover');
            const files = event.dataTransfer.files;
            if (files.length) {
                fileInput.files = files; // Assign the dropped file to the input
                alert(`You dropped: ${files[0].name}`);
            }
        });

        // Allow clicking on the drop area to open file picker
        dropArea.addEventListener('click', () => {
            fileInput.click();
        });

        // Handle file input change
        fileInput.addEventListener('change', () => {
            const file = fileInput.files[0];
            if (file) {
                alert(`You selected: ${file.name}`);
            }
        });
    </script>

</body>
</html>
