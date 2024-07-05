import pyttsx3


# Function to convert text to audio
def audio_handler(text, output_file):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_file)
    engine.runAndWait()
