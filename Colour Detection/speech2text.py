import speech_recognition as sr
from moviepy.editor import VideoFileClip

def extract_audio(video_file, output_audio_file):
    # Load the video file
    video_clip = VideoFileClip(video_file)

    # Extract audio
    audio_clip = video_clip.audio

    # Write the extracted audio to a file
    audio_clip.write_audiofile(output_audio_file)

    # Close the video clip
    video_clip.close()

def transcribe_audio(audio_file):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load audio file
    with sr.AudioFile(audio_file) as source:
        print("Processing audio file...")

        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)

        # Read the audio file
        audio = recognizer.record(source)

        try:
            # Recognize speech using Google Speech Recognition
            text = recognizer.recognize_google(audio)

            print("Transcription:", text)
        
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return text

def SpeechToText(videofile):
    # Provide the path to the video file
    video_file = videofile # Change this to your video file path
    # Specify the output audio file path
    output_audio_file = "output_audio_file.wav"  # Change this to your desired output audio file path
    # Extract audio from the video
    extract_audio(video_file, output_audio_file)
    # Transcribe audio to text
    print("Audio transcription complete!")
    result=transcribe_audio(output_audio_file)
    yield (result)

if __name__=="__main__":
    SpeechToText()
