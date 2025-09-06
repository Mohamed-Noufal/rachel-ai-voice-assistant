import subprocess
import os
import urllib.request
import zipfile

print("Installing FFmpeg for Windows...")

# FFmpeg download URL for Windows
ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
ffmpeg_zip = "ffmpeg.zip"
ffmpeg_dir = "ffmpeg"

try:
    # Download FFmpeg
    print("Downloading FFmpeg...")
    urllib.request.urlretrieve(ffmpeg_url, ffmpeg_zip)
    print("✅ FFmpeg downloaded successfully")

    # Extract FFmpeg
    print("Extracting FFmpeg...")
    with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
        zip_ref.extractall(ffmpeg_dir)
    print("✅ FFmpeg extracted successfully")

    # Find ffmpeg.exe
    for root, dirs, files in os.walk(ffmpeg_dir):
        if 'ffmpeg.exe' in files:
            ffmpeg_path = os.path.join(root, 'ffmpeg.exe')
            break

    if 'ffmpeg_path' in locals():
        print(f"✅ FFmpeg found at: {ffmpeg_path}")

        # Copy to backend directory
        import shutil
        backend_ffmpeg = os.path.join('backend', 'ffmpeg.exe')
        shutil.copy2(ffmpeg_path, backend_ffmpeg)
        print(f"✅ FFmpeg copied to: {backend_ffmpeg}")

        # Add to PATH for current session
        os.environ['PATH'] = os.path.dirname(backend_ffmpeg) + os.pathsep + os.environ['PATH']
        print("✅ FFmpeg added to PATH")

    else:
        print("❌ Could not find ffmpeg.exe in extracted files")

    # Clean up
    if os.path.exists(ffmpeg_zip):
        os.remove(ffmpeg_zip)
    if os.path.exists(ffmpeg_dir):
        import shutil
        shutil.rmtree(ffmpeg_dir)

except Exception as e:
    print(f"❌ Error installing FFmpeg: {e}")
    print("Please install FFmpeg manually from: https://ffmpeg.org/download.html")
