import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
import time
from openai import OpenAI

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "06a556114af14ab1aef58749e16a1bf3"

def speak(text):
    # create a fresh engine per call to avoid audio driver/profile issues
    e = pyttsx3.init()
    try:
        e.setProperty('volume', 1.0)
    except Exception:
        pass
    e.say(text)
    e.runAndWait()
def aiprocess(command):
    client = OpenAI(api_key="api key")  # Replace with your actual API key
    completion = client.chat.completions.create(
    model="gpt-4o-mini",  
    messages=[
        {"role": "system", "content": "You are Jarvis, a helpful AI assistant."},
        {"role": "user", "content": command}
    ]
)

    return completion.choices[0].message.content
 
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()

            # Extract the articles
            articles = data.get('articles', [])

            # Speak the headlines (give the audio subsystem a short pause after microphone use)
            time.sleep(0.8)
            print("DEBUG: speaking headline intro")
            speak("Here are the latest headlines from India.")
            for article in articles[:5]:
                print(f"DEBUG: speaking headline: {article.get('title')}")
                speak(article['title'])
                time.sleep(0.4)

    else:
       output=aiprocess(c)
       speak(output) # Let OpenAI handle the request
        ##speak(output) 






if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
        word = ""
        print("recognizing...")
        try:
            # first listen to detect the wake word
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.4)
                print("Listening...")
                audio = r.listen(source, timeout=6, phrase_time_limit=6)

            try:
                word = r.recognize_google(audio)
                print("heard:", word)
            except Exception as e:
                print("recognition error (wake):", e)
                continue

            # check wake word
            if "jarvis" in word.lower():
                speak("Yes")
                time.sleep(0.6)
                # Listen for command
                
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.4)
                    print("Jarvis Active...")
                    audio = r.listen(source, timeout=8, phrase_time_limit=8)
                try:
                    command = r.recognize_google(audio)
                    print("command:", command)
                    processCommand(command)
                except Exception as e:
                    print("recognition error (command):", e)
                    continue

        except Exception as e:
            print("Error; {0}".format(e))