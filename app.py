import subprocess
import sys, os
import pathlib
import speech_recognition as sr 

def convert(file, filename):
    
    # Convert video.mp4 to video.mp3
    command = ['ffmpeg', '-i', file, r"convert\{}.mp3".format(filename)]
    # print(*command)
    subprocess.run(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    # # Convert video.mp3 to video.wav
    command = ['ffmpeg', '-i', r'convert\{}.mp3'.format(filename), r"convert\{}.wav".format(filename)]
    subprocess.run(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    # # Convert video.wav to split video-xxx.wav
    # ffmpeg -i video.wav -f segment -segment_time 200 -c copy out%03d.wav
    command = ['ffmpeg', '-i', r'convert\{}.wav'.format(filename), '-f', 'segment', '-segment_time', '200', '-c', 'copy',  r"convert\{}-%03d.wav".format(filename)]
    subprocess.run(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

def translate(filename):
    files = list_file(filename)
    count = 1
    count_max = len(files)
    for file in files:
        print('{}/{}. Proses {}...'.format(count, count_max, file))
        translate_to_text(file, filename)
        count += 1

def list_file(filename):
    py = pathlib.Path().glob(r"convert\{}-*.wav".format(filename))
    result = []
    for file in py:
        # print(file)
        result.append(r'{}'.format(file))
    return result 

def translate_to_text(file, filename):
    r = sr.Recognizer()
    audio = sr.AudioFile(file)

    with audio as source:
        audio_file = r.record(source)
    result = r.recognize_google(audio_file, language="id-ID")

    # exporting the result 
    with open(r'data\{}.txt'.format(filename),mode ='a+') as filetext: 
        filetext.write(result) 

def cleanup(filename):
    # Delete all file in convert
    os.unlink(r'convert\{}.wav'.format(filename))
    files = list_file(filename)
    for file in files:
        os.unlink(file)
    

def main(file):
    
    filename = os.path.basename(file)
    # filename, file_extension = os.path.splitext(filename)
    filename = os.path.splitext(filename)[0]
    # print(filename)
    # print(file_extension)

    # Check if folder exists
    folders = ['convert', 'data']
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

    print('Proses konversi mp4 ke wav.')
    convert(file, filename)
    print('Proses ekstrak wav ke text')
    translate(filename)
    print('Proses clean up folder convert')
    cleanup(filename)
    print('Selesai...')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('Usage: %s file-video.mp4' % os.path.relpath(__file__))
