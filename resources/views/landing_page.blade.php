<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Akira</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    
</head>
<body class="bg-gray-100 font-sans">

    <!-- Header Section -->
    <header class="bg-[#1A3C10] text-white text-center py-12">
        <h1 class="text-4xl sm:text-5xl font-bold leading-tight">Welcome to Akira</h1>
        <p class="mt-4 text-lg sm:text-xl">Innovating Child-Friendly Audio Experiences</p>
    </header>

    <!-- Main Content Section -->
    <div class="max-w-4xl mx-auto bg-[#F1FBEF] p-8 rounded-2xl shadow-xl mt-10">
        <h2 class="text-3xl font-semibold text-center mb-6 text-[#1A3C10]">Project Overview</h2>
        <p class="text-lg text-justify leading-relaxed text-gray-800 mb-6">
            Welcome to the project on "<strong>Extracting Overstimulating Audio Signals from Cartoon Videos Using STFT, MFCC, and VGG16 CNN and Retuning Audio Playback for Child-Friendly Listening</strong>."
            This research aims to enhance children's audio experiences by analyzing overstimulating audio signals from cartoons. Using Short-Time Fourier Transform (STFT), Mel Frequency Cepstral Coefficients (MFCC), and VGG16 Convolutional Neural Networks (CNN), we process and retune audio to create child-friendly listening environments.
        </p>
        <p class="text-lg text-justify leading-relaxed text-gray-800 mb-6">
            Join us in exploring innovative methods for improving the auditory experience for young audiences, making their viewing and listening experiences enjoyable and conducive to cognitive development.
        </p>
        
        <!-- Learn More Button -->
        <div class="text-center">
            <form action="/uploading_page" method="POST">
                @csrf
                <button type="submit" name="submit" class="mt-6 px-8 py-3 bg-[#1A3C10] text-white font-semibold text-lg rounded-md hover:bg-[#145A02] transition duration-300 focus:outline-none focus:ring-4 focus:ring-[#145A02] focus:ring-opacity-50">
                    Explore More
                </button>
            </form>
        </div>
    </div>

    <!-- Image Sections -->
    <div class="max-w-4xl mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 mt-12">
        <!-- Image 1 -->
        <div class="bg-white rounded-lg shadow-lg overflow-hidden">
            <img src="{{URL('image/111.jpeg')}}" alt="Image 1" class="w-full h-48 object-cover">
            <div class="p-4">
                <h3 class="text-lg font-semibold text-[#1A3C10]">Audio Signal Extraction</h3>
                <p class="text-sm text-gray-700 mt-2">Processing and extracting overstimulating audio signals for child-friendly listening.</p>
            </div>
        </div>

        <!-- Image 2 -->
        <div class="bg-white rounded-lg shadow-lg overflow-hidden">
            <img src="{{URL('image/222.png')}}" alt="Image 2" class="w-full h-48 object-cover">
            <div class="p-4">
                <h3 class="text-lg font-semibold text-[#1A3C10]">Cartoon Video Analysis</h3>
                <p class="text-sm text-gray-700 mt-2">Analyzing audio signals from cartoon videos using advanced algorithms.</p>
            </div>
        </div>

        <!-- Image 3 -->
        <div class="bg-white rounded-lg shadow-lg overflow-hidden">
            <img src="{{URL('image/333.jpg')}}" alt="Image 3" class="w-full h-48 object-cover">
            <div class="p-4">
                <h3 class="text-lg font-semibold text-[#1A3C10]">VGG16 CNN Implementation</h3>
                <p class="text-sm text-gray-700 mt-2">Utilizing VGG16 CNN to process audio signals for optimal retuning.</p>
            </div>
        </div>
    </div>

    <!-- Footer Section -->
    <footer class="bg-[#1A3C10] text-white py-6 mt-12">
        <div class="text-center">
            <p class="text-sm">&copy; 2025 Akira. All Rights Reserved.</p>
            <p class="text-sm mt-2">Developed by <strong>Akira</strong> | Contact: <a href="mailto:youremail@example.com" class="text-[#145A02] hover:text-white">akira@gmail.com</a></p>
        </div>
    </footer>

</body>
</html>
