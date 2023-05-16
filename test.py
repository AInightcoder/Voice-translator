import pyttsx3

engine = pyttsx3.init()
voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
engine.setProperty('voice', voice_id)
engine.setProperty('rate', 150) # adjust the speech rate to 150 words per minute
engine.setProperty('volume', 0.7) # adjust the volume to 70%

engine.say("Привет, как дела?") # Speak the text in Russian
engine.runAndWait() # wait for speech to finish
