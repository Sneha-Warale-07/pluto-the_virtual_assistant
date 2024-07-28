import webbrowser
import speech_recognition as sr
import pyttsx3
import musiclib
import appslib
import reply
import urllib.parse

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def get_reply(user_input):
    print(user_input)
    user_input = user_input.lower()
    for key in reply.reply:
        if key in user_input:
            return reply.reply[key]
    return "Sorry, I didn't understand that."

def search(user_input):
    search_term = user_input
    speak(f"searching {user_input}")
    encoded_search_term = urllib.parse.quote(search_term)
    search_url = f"https://www.google.com/search?q={encoded_search_term}"
    webbrowser.open(search_url)
 
def processcommand(c):
    print(c)
    if c.lower().startswith("open"):
        app = c.lower().split(" ", 1)[1]
        speak(f"Opening {app}")
        link = appslib.app.get(app)
        if link:
            webbrowser.open(link)
        else:
            speak("App not found.")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[1]
        speak(f"Playing {song}")
        link = musiclib.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found.")
    elif any(key in c.lower() for key in reply.reply):
        response = get_reply(c)
        speak(response)
    elif c.lower().startswith("search"):
        srch = c.lower().split(" ",1)[1]
        search(srch)
    elif c.lower() == "exit":
        speak("Exiting Pluto. Goodbye!")
        return False
    else:
        speak("Command not recognized.")
        print("Error: Command not recognized")
    return True

if __name__ == "__main__":
    speak("Initializing Pluto....")
    running = True
    while running:
        # Obtain audio from the microphone
        r = sr.Recognizer()
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening!")
                audio = r.listen(source, timeout=2, phrase_time_limit=5)
            word = r.recognize_google(audio)
            print(word)
            if "pluto" in word.lower():
                speak("Yes, any command?")
                # Listen for command 
                with sr.Microphone() as source:
                    print("Pluto active....")
                    audio = r.listen(source)
                    commands =r.recognize_google(audio)
                    processcommand(commands)
            elif any(key in word.lower() for key in reply.reply):
                response = get_reply(word)
                speak(response)
            elif word.lower() == "exit":
                speak("Exiting Pluto. Goodbye!")
                break
        except Exception as e:
            print(f"Error: {e}")
