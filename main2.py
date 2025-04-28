import speech_recognition as sr
import os
import webbrowser
import datetime
import random
import numpy as np
import google.generativeai as genai
import pyttsx3
import requests
import pywhatkit
from config import gemini_apikey

# Configure Gemini API
genai.configure(api_key=gemini_apikey)

# Text-to-speech engine
engine = pyttsx3.init()


def say(text):
    engine.say(text)
    engine.runAndWait()

# Initialize Gemini Chat Model
chatStr = ""
model = genai.GenerativeModel("gemini-1.5-pro")
chat_session = model.start_chat(history=[])

def chat(query):
    global chatStr, chat_session
    print(chatStr)
    chatStr += f"You: {query}\nJarvis: "
    try:
        response = chat_session.send_message(query)
        text = response.text
        say(text)
        chatStr += f"{text}\n"
        return text
    except Exception as e:
        say("Sorry, something went wrong.")
        print("Gemini Error:", e)
        return "Error"

def ai(prompt):
    text = f"Gemini response for Prompt: {prompt} \n *************************\n\n"
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(prompt)
        text += response.text
        if not os.path.exists("Gemini"):
            os.mkdir("Gemini")
        filename = f"Gemini/{'_'.join(prompt[:20].split())}.txt"
        with open(filename, "w") as f:
            f.write(text)
    except Exception as e:
        say("Sorry, could not generate response.")
        print("Gemini Error:", e)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return ""

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Jarvis A.I activated. Say 'Jarvis quit' to exit.")

    while True:
        query = takeCommand().lower()

        if "jarvis" in query:
            query = query.replace("jarvis", "").strip()
            print(f"Command after wake word: {query}")

            if not query:
                continue

            if any(kw in query for kw in ["quit", "exit", "stop", "goodbye"]):
                say("Goodbye, see you later!")
                break

            sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"]]
            for site in sites:
                if f"open {site[0]}" in query:
                    say(f"Opening {site[0]} sir...")
                    webbrowser.open(site[1])

            if "search youtube for" in query:
                search_term = query.replace("search youtube for", "").strip()
                say(f"Searching YouTube for {search_term}")
                pywhatkit.playonyt(search_term)

            elif "open music" in query:
                musicPath = "C:/Users/YourName/Music/song.mp3"
                os.system(f"start {musicPath}")

            elif "the time" in query:
                now = datetime.datetime.now()
                say(f"Sir, the time is {now.hour} bajke {now.minute} minutes")

            elif "open Raft" in query:
                os.system(f"open D:\RAFT\Raft (M4CKD0GE Repack)\Raft.exe")

            elif "open pass" in query:
                os.system(f"open /Applications/Passky.app")

            elif "using artificial intelligence" in query:
                ai(prompt=query)

            elif "reset chat" in query:
                chatStr = ""
                say("Chat history has been reset.")

            elif "tell me a joke" in query:
                chat("Tell me a joke")

            

            elif "calculate" in query:
                try:
                    expression = query.replace("calculate", "")
                    result = eval(expression)
                    say(f"The result is {result}")
                except Exception:
                    say("Sorry, I couldn't calculate that.")

            elif "send whatsapp" in query:
                try:
                    say("Who should I send it to?")
                    contact = takeCommand()
                    say("What should I say?")
                    message = takeCommand()
                    phone_number = "+911234567890"
                    pywhatkit.sendwhatmsg_instantly(phone_number, message)
                    say("Message sent successfully!")
                except Exception as e:
                    say("Failed to send WhatsApp message.")

            else:
                chat(query)
