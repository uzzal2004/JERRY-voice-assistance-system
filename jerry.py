import speech_recognition as sr 
import pyttsx3 
import logging 
import os 
import datetime 
import wikipedia 
import webbrowser 
import random 
import subprocess 
import google.generativeai as genai

# Logging configuration 
LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"

os.makedirs(LOG_DIR, exist_ok=True)

log_path = os.path.join(LOG_DIR,LOG_FILE_NAME)

logging.basicConfig(
    filename=log_path,
    format = "[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level= logging.INFO
)



# Activating voice from our system 
engine = pyttsx3.init("sapi5") 
engine.setProperty('rate', 170)
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)


# This is speak function
def speak(text):
    """This function converts text to voice

    Args:
        text
    returns:
        voice
    """
    engine.say(text)
    engine.runAndWait()



# This function recognize the speech and convert it to text 

def takeCommand():
    """This function takes command & recognize

    Returns:
        text as query
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...") 
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        logging.info(e)
        print("Say that again please")
        return "None"
    
    return query


def greeting():
    hour = (datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning sir!")
    elif hour>=12 and hour<=18:
        speak("Good Afternoon sir!")
    else:
        speak("Good Evening sir!")
    

    speak("I am Jerry. Please tell me how may I help you today?")


def play_music():
    music_dir = "D:\\anaconda_notebook\\inceptionbd\\JERRY-voice-assistance-system\\music"  
    try:
        songs = os.listdir(music_dir)
        if songs:
            random_song = random.choice(songs)
            speak(f"Playing a random song sir: {random_song}")
            os.startfile(os.path.join(music_dir, random_song))
            logging.info(f"Playing music: {random_song}")
        else:
            speak("No music files found in your music directory.")
    except Exception:
        speak("Sorry sir, I could not find your music folder.")


def gemini_model_response(user_input):
    GEMINI_API_KEY = "Tested working correctly"
    genai.configure(api_key=GEMINI_API_KEY) 
    model = genai.GenerativeModel("gemini-2.5-flash") 
    prompt = f"Your name is Jerry, You act like Jerry. Answar the provided question in short, Question: {user_input}"
    response = model.generate_content(prompt)
    result = response.text

    return result

greeting()

while True:
    query = takeCommand().lower()
    print(query)

    # Tell Time:

    if "What time is it?" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir the time is {strTime}")
        logging.info("User asked for current time.")

    
    # Wikipedia Search
         
    elif "wikipedia" in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
        logging.info("User requested information from Wikipedia.")
    
    # Web Browser Automation:
    # YouTube search
    elif "youtube" in query:
        speak("Opening YouTube for you.")
        query = query.replace("youtube", "")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        logging.info("User requested to search on YouTube.")
    
    elif "open google" in query:
        speak("ok sir. please type here what do you want to read")
        webbrowser.open("google.com")
        logging.info("User requested to open Google.")
    
    elif "open LinkedIn" in query:
        speak("ok sir. opening LinkedIn")
        webbrowser.open("linkedin.com")
        logging.info("User requested to open LinkedIn.")

    # Note: Make "Jerry" Your Own! (Bonus Challenge)
    #     
    # close vscode

    elif "close vs code" in query or "vs code close" in query:
        speak("closing the vs code")
        subprocess.run(["taskkill", "/F", "/IM","Code.exe"], check=True)
        logging.info("User requested to close visual studio.")

    # shutdown computer

    elif "shutdown computer" in query or "computer shutdown" in query:
        speak("shuting down the computer")
        subprocess.run(["shutdown", "/s", "/t","30"], check=True)
        logging.info("User requested shutdown computer.")
    
    elif "exit" in query:
        speak("Thank you for your time sir. Have a great day ahead!")
        logging.info("User exited the program.")
        exit()

    else:
        response = gemini_model_response(query)
        speak(response)
        logging.info("User asked for others question")

