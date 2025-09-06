import zipfile
import os
import shutil

print("Checking for FFmpeg installation...")

ffmpeg_zip = "ffmpeg.zip"
ffmpeg_dir = "ffmpeg_extracted"

if os.path.exists(ffmpeg_zip):
    print(f"✅ Found {ffmpeg_zip}")

    # Extract FFmpeg
    print("Extracting FFmpeg...")
    try:
        with zipfile.ZipFile(ffmpeg_zip, 'r') as zip_ref:
            zip_ref.extractall(ffmpeg_dir)
        print("✅ FFmpeg extracted successfully")

        # Find ffmpeg.exe
        ffmpeg_exe = None
        for root, dirs, files in os.walk(ffmpeg_dir):
            if 'ffmpeg.exe' in files:
                ffmpeg_exe = os.path.join(root, 'ffmpeg.exe')
                break

        if ffmpeg_exe:
            print(f"✅ Found ffmpeg.exe at: {ffmpeg_exe}")

            # Copy to backend directory
            backend_ffmpeg = os.path.join('backend', 'ffmpeg.exe')
            shutil.copy2(ffmpeg_exe, backend_ffmpeg)
            print(f"✅ FFmpeg copied to: {backend_ffmpeg}")

            # Test FFmpeg
            import subprocess
            try:
                result = subprocess.run([backend_ffmpeg, '-version'],
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print("✅ FFmpeg is working correctly!")
                    print("FFmpeg version info:")
                    print(result.stdout.split('\n')[0])
                else:
                    print("❌ FFmpeg test failed")
            except Exception as e:
                print(f"❌ Error testing FFmpeg: {e}")

        else:
            print("❌ Could not find ffmpeg.exe in extracted files")

    except Exception as e:
        print(f"❌ Error extracting FFmpeg: {e}")

else:
    print(f"❌ {ffmpeg_zip} not found")
    print("Please run install_ffmpeg.py first")
