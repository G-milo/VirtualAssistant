import tkinter as tk
import urllib
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pywhatkit
import socket
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def check_internet_connection():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False

def check_internet_and_run():
    if check_internet_connection():
        engine.say("Hello, I am Mia. What can I do for you?")
        engine.runAndWait()
    else:
        engine.say("Sorry, an internet connection is required for me to function. Please connect to the internet and try again.")
        engine.runAndWait()
        exit()

check_internet_and_run()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"You said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, I couldn't access the speech recognition service.")
        return ""

def get_date():
    now = datetime.datetime.now()
    date = now.strftime("%B %d, %Y")
    return date

def get_time():
    now = datetime.datetime.now()
    time = now.strftime("%I:%M %p")
    return time

def search_wikipedia(query):
    speak("Searching Wikipedia...")
    query = query.replace("wikipedia", "")
    try:
        page = wikipedia.page(query)
        webbrowser.open(page.url)
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia:")
        speak(results)
    except wikipedia.exceptions.PageError:
        speak("Sorry, I couldn't find any matching results.")
    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple matching results. Please be more specific.")

def search_on_google(query):
    speak("Searching on Google...")
    url = f"https://www.google.com/search?q={query}"
    try:
        webbrowser.open(url)
    except webbrowser.Error:
        speak("Sorry, I couldn't perform the search.")

def open_folder(folder_path):
    try:
        os.startfile(folder_path)
    except FileNotFoundError:
        speak("Sorry, I couldn't find the folder.")

def process_command():
    command = entry.get().lower()
    speak("You said: " + command)

    if "search on google" in command:
        query = command.replace("search on google", "").strip()
        if query:
            search_query = urllib.parse.quote_plus(query)
            url = f"https://www.google.com/search?q={search_query}"
            search_on_google(url)
        else:
            speak("Please provide a search query.")
    elif "tell me about" in command:
        about = command.replace("tell me about", "").strip()
        if about:
            search_wikipedia(about)
        else:
            speak("Please provide a specific name.")
    elif 'play' in command:
        song = command.replace('play','')
        speak('Okay Please wait a moment')
        pywhatkit.playonyt(song)
    elif "date" in command:
        date = get_date()
        speak(f"The date is {date}.")
    elif "time" in command:
        time = get_time()
        speak(f"The time is {time}.")
    elif "open" in command:
        speak("Opening....")
        open_command = command.replace("open", "").strip().lower()
        if "documents" in open_command:
            open_folder("C:\\Users\\User\\Documents") #modify according to the device path
        elif "downloads" in open_command:
            open_folder("C:\\Users\\User\\Downloads")
        elif "photos" in open_command:
            open_folder("C:\\Users\\User\\Pictures")
        elif "music" in open_command:
            open_folder("C:\\Users\\User\\Music")
        elif "videos" in open_command:
            open_folder("C:\\Users\\User\\Videos")
        else:
            speak("Sorry, I don't know how to open that folder.")
    elif "single" in command or "relationship" in command:
        speak("I am an AI assistant. I don't have a relationship status.")
    elif "birthday" in command:
        speak("I don't have a specific birthday as I am an AI program.")
    elif "thank you" in command:
        speak("You're welcome! It's my pleasure to assist you.")
    elif "hello" in command or "hi" in command:
        speak("Hello! How can I assist you?")
    elif "goodbye" in command or "bye" in command:
        speak("Goodbye! Have a nice day!")
        exit()
    else:
        speak("Sorry, I cannot perform that action.")
    entry.delete(0, tk.END)

def process_speech():
    command = listen().lower()
    entry.delete(0, tk.END)
    entry.insert(0, command)


window = tk.Tk()
window.title("Mia")
window.geometry("800x500")
window.configure(bg="black")

label = tk.Label(window, text="MIA", font=("Algerian", 36, "bold"), fg="lime green", bg="black")
label.pack(pady=25)

entry = tk.Entry(window, font=("Arial", 14), width=55)
entry.pack(pady=40)

button = tk.Button(window, text="SUBMIT", font=("Serif", 14, "bold"), command=process_command,bg="pink", width=10)
button.pack(pady=10)

speech_label = tk.Label(window, text="MIA is Listening 🎤", font=("Lucida Fax", 14, "italic"), fg="lime green", bg="black")

def process_speech():
    command = listen().lower()
    entry.delete(0, tk.END)
    entry.insert(0, command)
    speech_label.pack(pady=20)

speech_button = tk.Button(window, text="SPEECH", font=("Serif", 14, "bold"), command=process_speech,bg="pink", width=10)
speech_button.pack(pady=10)

window.mainloop()
