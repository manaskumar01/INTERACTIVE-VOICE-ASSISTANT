from pipes import quote
import re
import sqlite3
import eel
import webbrowser
import os
import psutil
from engine.command import speak
import pywhatkit as kit
from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

@eel.expose
def openCommand(query):
    query = query.replace("open", "")
    query.lower()
    app_name = query.strip()
    if app_name != "":
        try:
            cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute('SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])
                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)

def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

def close_application(query):
    app_name = query.replace("close", "").strip()
    for process in psutil.process_iter(['name']):
        if app_name.lower() in process.info['name'].lower():
            process.terminate()
            speak(f"{app_name} has been closed.")
