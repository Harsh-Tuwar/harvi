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
playsound('./robot_start.mp3')
speak('Initializing Harvi, your AI personal assistant...')
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
		elif 'open' in statement or "search" in statement:
			if 'open' in statement:
				websiteName = (statement.split("open", 1)[1].strip()).replace(" ", "")
			if 'search' in statement:
				websiteName = (statement.split("search", 1)[1].strip()).replace(" ", "")
			print(websiteName)
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
		elif 'time' in statement:
			strTime = datetime.datetime.now().strftime("%H:%M:%S")
			print(f"the time is {strTime}")
			speak(f"the time is {strTime}")

		elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
			speak("I was built by Harsh")
			print("I was built by Harsh")

		elif "who is harsh" in statement or "who is he" in statement:
			webbrowser.open_new_tab(f"https://whoistuwar.now.sh")
			speak("Here is Harsh's personal website. You can find more about him over here.")
			print("Here is Harsh's personal website. You can find more about him over here.")
        
		elif 'camera' in statement or 'capture' in statement or 'click' in statement:
			ec.capture(0, "robo cam", "img.jpg")

		elif "weather" in statement:
			api_key="8ef61edcf1c576d65d836254e11ea420"
			base_url="https://api.openweathermap.org/data/2.5/weather?"
			speak("whats the city name")
			city_name=takeCommand()
			complete_url=base_url+"appid="+api_key+"&q="+city_name
			response = requests.get(complete_url)
			x=response.json()
			
			if x["cod"]!="404":
				y=x["main"]
				current_temperature = y["temp"]
				current_humidiy = y["humidity"]
				z = x["weather"]
				weather_description = z[0]["description"]
				speak(" Temperature in kelvin unit is " +
						str(current_temperature) +
						"\n humidity in percentage is " +
						str(current_humidiy) +
						"\n description  " +
						str(weather_description))
				print(" Temperature in kelvin unit = " +
						str(current_temperature) +
						"\n humidity (in percentage) = " +
						str(current_humidiy) +
						"\n description = " +
						str(weather_description))
			else:
				speak(" City Not Found ")

		# elif 'ask' in statement:
        #     speak('I can answer to computational and geographical questions and what question do you want to ask now')
        #     question=takeCommand()
        #     app_id="R2K75H-7ELALHR35X"
        #     client = wolframalpha.Client('R2K75H-7ELALHR35X')
        #     res = client.query(question)
        #     answer = next(res.results).text
        #     speak(answer)
            #subprocess.call(["shutdown", "/l"])
        #     print(answer)

		elif "log off" in statement or "sign out" in statement:
			speak('Ok , your pc will log off in 10 sec make sure you exit from all applications')
			subprocess.call(["shutdown", "/l"])

time.sleep(2)
