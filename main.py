import pyttsx3 as p
import speech_recognition as sr
from Music import MusicPlayer
from Selenium_web import infow
from News import fetch_news
import random
import time
import randfacts
from Weather import get_weather, des, temp
from Jokes import *
from dotenv import load_dotenv
load_dotenv()
import os
import datetime
News_api_key = os.getenv('News_api_key')

# Initialize text-to-speech engine
engine = p.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

greetings = ["Hello!", "Hi there!", "Hey!", "Greetings!"]
thanks = ["Thank you!", "Thanks a lot!", "Thanks!", "I appreciate it!", "It's my Pleasure"]
goodbye = ["See you soon!", "Take care Bye!", "Until next time!"]
understand = ["Got it!", "I understand!", "Alright!", "Okay!"]
apologies = ["I'm sorry!", "My apologies!", "Sorry about that!"]
prompts = ["What can I do for you?", "How can I assist you?", "What else would you like to do?"]


# Function to speak out text
def speak(text):
    engine.say(text)
    engine.runAndWait()

today_date=datetime.datetime.now()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        return(" good morning")
    elif hour>=12 and hour<18:
        return("good afternoon")
    else:
        return("good evening")
def recognize_speech(repeat_prompt=False):
    try:
        with sr.Microphone() as source:
            r = sr.Recognizer()
            r.energy_threshold = 10000
            r.adjust_for_ambient_noise(source, duration=1.2)

            print("Listening...")
            audio = r.listen(source)

        print("Recognizing...")
        text = r.recognize_google(audio)
        print("You said:", text)
        return text

    except sr.UnknownValueError:
        if repeat_prompt:
            print("Sorry, I didn't catch that. Could you please repeat?")
            speak(random.choice(apologies) + " Could you please repeat?")
            return recognize_speech(repeat_prompt=False)  # Recursively call recognize_speech without repeat prompt
        else:
            return None
    except sr.RequestError:
        print("Sorry, there was an issue with the speech recognition service.")
        speak(random.choice(apologies) + " There was an issue with the speech recognition service. Please try again.")

    return None


# Main loop
if __name__ == "__main__":
    speak("Hello Pavithra. "+wishme())
    speak("This is your personal voice assistant Neva.")
    speak(
        "Today's date is " + today_date.strftime("%d") + " of " +
        today_date.strftime("%B") + ". It's currently " +
        today_date.strftime("%I:%M %p")
    )
    speak("How can I assist you?")

    waiting = False  # Flag to indicate if assistant is waiting

    while True:
        if not waiting:
            command = recognize_speech()

            if command:
                if "what can you do for me" in command:
                    speak("I can give information, I can play video, I can tell jokes, news and much more.")
                    speak(random.choice(prompts))

                elif "nice to meet you" in command:
                    speak("It's wonderful to meet you too!")
                    speak(random.choice(prompts))

                elif "who are you" in command:
                    speak("I am Neva, your voice assistant.")
                    speak(random.choice(prompts))

                elif "how are you" in command:
                    speak("I am good. Thanks for asking.")
                    speak(random.choice(prompts))

                elif "thanks" in command:
                    speak(random.choice(thanks))
                    speak(random.choice(prompts))

                elif any(keyword in command.lower() for keyword in ["stop", "exit"]):
                    speak(random.choice(goodbye))
                    break


                elif "information" in command.lower() or "informations" in command.lower():
                    speak("What topic would you like information on?")
                    query = recognize_speech()
                    if query:
                        speak(f"Searching {query} on Wikipedia...")
                        assistant = infow()
                        info_text = assistant.get_info(query)

                        info_text_lines = info_text.split('\n')[:2]
                        info_text_to_speak = ' '.join(info_text_lines)
                        speak(info_text_to_speak)
                        assistant.close_driver()
                        speak(random.choice(prompts))

                elif "music" in command.lower() and "play" in command.lower():
                    speak("Which song would you like to listen to?")
                    query = recognize_speech()
                    if query:
                        speak(f"Searching {query} on YouTube...")
                        player = MusicPlayer()
                        player.play(query)

                        print("Enjoy !!!")
                        while player.is_playing():

                            command = recognize_speech()

                            if command and any(keyword in command.lower() for keyword in ["stop", "exit"]):
                                speak("Stopping the music.")
                                player.stop()
                                break

                            elif command and "wait" in command.lower():
                                speak("Okay, I will wait.")
                                waiting = True
                                break

                        speak(random.choice(prompts))

                elif "news" in command.lower() or "headlines" in command.lower():
                    speak("Fetching latest news headlines...")
                    headlines = fetch_news(News_api_key, country='us', num_headlines=3)

                    if headlines:
                        for headline in headlines:
                            print(headline)
                            speak(headline)
                    else:
                        speak("Failed to fetch news headlines. Please try again later.")
                    speak(random.choice(prompts))

                elif "wait" in command.lower():
                    speak("Alright, I'll wait.")
                    waiting = True  # Set waiting flag to True
                    speak(random.choice(prompts))

                elif "fact" in command.lower() or "facts" in command.lower():
                    speak("Yeah sure. Why not?")
                    x = randfacts.get_fact()
                    print(x)
                    speak("Did you know that " + x)  # Added space after "that"

                elif "joke" in command.lower() or "jokes" in command.lower():
                    speak("Feels like you are in a good mood. Get ready for some chuckles.")
                    setup, punchline = joke()
                    if setup and punchline:
                        print(setup)
                        speak(setup)
                        print(punchline)
                        speak(punchline)
                        speak("You loved it right?. Anything else you want me to do?")
                    else:
                        speak("Sorry, I couldn't fetch a joke right now. Please try again later.")

                elif "weather" in command.lower() or "temperature" in command.lower():
                    speak("Sure! Which city's weather do you want to know about?")
                    city = recognize_speech(repeat_prompt=False)
                    if city:
                        temperature = temp(city)
                        description = des(city)
                        if temperature is not None and description is not None:
                            print(f"The current temperature in {city} is {temperature} degrees Celsius.")
                            speak(f"The current temperature in {city} is {temperature} degrees Celsius.")
                            print(f"The weather is {description}.")
                            speak(f"The weather is {description}.")
                            print("Anything else?")
                            speak("Anything else?")
                        else:
                            speak(f"Sorry, I couldn't fetch the weather information for {city}. Please try again later.")

                else:
                    speak("I'm sorry, I didn't catch that. Please repeat")


            else:
                print("Sorry, I didn't catch that. Could you please repeat?")
                speak("I'm sorry, I didn't catch that. Could you please repeat?")


        else:
            time.sleep(15)

            # Check if there's a command to resume
            command = recognize_speech()
            if command and "resume" in command.lower():
                speak("Resuming...")
                waiting = False
                speak(random.choice(prompts))

    # Cleanup: Stop the engine and exit the program
    engine.stop()
