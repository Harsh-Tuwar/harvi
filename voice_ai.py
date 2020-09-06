import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import json
import requests
from playsound import playsound

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

engine.runAndWait()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
	hour = datetime.datetime.now().hour
	if hour >= 0 and hour < 12:
		speak("Hello Master, Good Morning")
		print("Hello Master, Good Morning")
	elif hour >= 12 and hour < 18:
		speak("Hello Master, Good Afternoon")
		print("Hello Master, Good Afternoon")
	else:
		speak("Hello Master, Good Evening")
		print("Hello Master, Good Evening")

def takeCommand():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Listening...")
		audio = r.listen(source)

		try:
			statement = r.recognize_google(audio, language='en-in')
			print(f"user said: {statement}\n")

		except Exception as e:
			speak("Pardon Me, please try that again!")
			return "None"
		
		return statement

print('Initializing Harvi, your AI personal assistant...')
speak('Initializing Harvi, your AI personal assistant...')
playsound('./robot_start.mp3')
wishMe()

if __name__ == '__main__':
	while True:
		speak("Tell me how can I help you now?")
		statement = takeCommand().lower()
		if statement == 0:
			continue

		if "goodbye" in statement or "okay bye" in statement or "stop" in statement or "bye" in statement:
			speak("Okay, Have a good one!")
			playsound('./robot_end.mp3')
			print("Shutting Down...")
			break

		# fetching data from wiki
		if 'wikipedia' in statement:
			speak('Searchin Wikipedia...')
			statement = statement.replace("wikipedia", "")
			results = wikipedia.summary(statement, sentences=3)
			speak("According to Wikipedia, ")
			print(results)
			speak(results)

		# accessing the web
		if 'open' in statement:
			websiteName = (statement.split("open", 1)[1].strip()).replace(" ", "")
			url = f"https://www.{websiteName}.com"
			response = requests.get(url)
			if (response.status_code == 200):
				webbrowser.open_new_tab(f"https://www.{websiteName}.com")
				speak(f"{websiteName} is open now!")
			else:
				searchQuery = "https://www.google.com.tr/search?q={}".format(websiteName)
				webbrowser.open_new_tab(searchQuery)
			time.sleep(3)

		# time prediction
		if 'time' in statement:
			strTime = datetime.datetime.now().strftime("%H:%M:%S")
			print(f"the time is {strTime}")
			speak(f"the time is {strTime}")

		if "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
			speak("I was built by Harsh")
			print("I was built by Harsh")

		if "who is harsh" in statement or "who is he" in statement:
			webbrowser.open_new_tab(f"https://whoistuwar.now.sh")
			speak("Here is Harsh's personal website. You can find more about him over here.")
			print("Here is Harsh's personal website. You can find more about him over here.")
			
		# search stuff
		elif 'search' in statement:
			statement = statement.replace("search", "")
			webbrowser.open_new_tab(statement)
			time.sleep(2)

        # elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            