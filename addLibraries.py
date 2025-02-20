import subprocess
import sys

# List of required libraries
libraries = ["PyQt5", "moviepy","pydub", "librosa", "numpy", "matplotlib", "tensorflow"]

# Install each library
for lib in libraries:
    subprocess.run([sys.executable, "-m", "pip", "install", lib], check=True)
