import os
print('Current directory:', os.getcwd())
print('Files in directory:', os.listdir('.'))
if os.path.exists('backend'):
    os.chdir('backend')
    print('Changed to backend directory:', os.getcwd())
    print('Files in backend:', os.listdir('.'))
    print('Voice.mp3 exists:', os.path.exists('voice.mp3'))
    if os.path.exists('voice.mp3'):
        print('Voice.mp3 size:', os.path.getsize('voice.mp3'))
