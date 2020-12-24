import subprocess
import wolframalpha
import pyttsx3
import tkinter
import json
import random
import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import feedparser
import smtplib
import ctypes
import time
import requests
import shutil
from twilio.rest import Client
from clint.textui import progress
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen
from email.mime.text import MIMEText
import pytz
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import cv2
import pandas

number = round(random.random())
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[number].id)
f = open('cred.json', )
cred = json.load(f)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        print("Good Morning Sir!")
        speak("Good Morning Sir !")
    elif 12 <= hour < 18:
        print("Good Afternoon Sir!")
        speak("Good Afternoon Sir !")
    else:
        print("Good Evening sir!")
        speak("Good Evening Sir !")
    assname = "Hyperion"
    print("I am your assistant,", assname)
    speak("I am your Assistant")
    speak(assname)


def usrname():
    print("What should I call you Sir?")
    speak("What should i call you sir")
    uname = takeCommand()
    print("Welcome Mr.", uname)
    speak("Welcome Mister")
    speak(uname)
    print("How can I help you,sir")
    speak("How can i Help you, Sir")


def takeCommand():
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
        print(e)
        print("Unable to recognize your voice!!")
        speak("Unable to recognize your voice")
        return "None"
    return query


def takeCommand1():
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
        print(e)
        return "None"
    return query


def sendEmail(to, content, subject):
    from_email = cred["from_email"]
    from_password = cred["from_password"]
    content = content + "<br><br>Sent from Hyperion"
    msg = MIMEText(content, 'html')
    msg['Subject'] = subject
    msg['To'] = to
    msg['From'] = from_email
    gmail = smtplib.SMTP(cred["from_smtp"], cred["from_port"])
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)


def camera():
    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        check, frame = video.read()
        cv2.imshow("Camera", frame)
        key = cv2.waitKey(1)
        querynew = ""
        if key == ord('q') or 'exit' in querynew:
            break
    video.release()
    cv2.destroyAllWindows()


def take_picture():
    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    i = 3
    say = "Capturing in " + str(i)
    speak(say)
    while True:
        i = i - 1
        check, frame = video.read()
        cv2.imshow("Camera", frame)
        speak(i)
        if i == 1:
            cv2.imwrite("captured_pic.jpg", frame)
            break
    video.release()
    cv2.destroyAllWindows()
    print("Do you want to see the captured Photo?")
    speak("Do you want to see the captured Photo")
    choice = takeCommand()
    if 'yes' in choice or 'sure' in choice or 'yeah' in choice or choice is None:
        print("Opening Captured Photo")
        speak("Opening Captured photo")
        show_picture()


def show_picture():
    img = cv2.imread("captured_pic.jpg", 1)
    cv2.imshow("Captured Picture", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def face_detector():
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    font = cv2.FONT_HERSHEY_SIMPLEX
    while True:
        check, frame = video.read()
        frame_img = frame
        gray_img = cv2.cvtColor(frame_img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5)
        for x, y, w, h in faces:
            frame_img = cv2.rectangle(frame_img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(frame_img, 'face', (x, y - 10), font, 1, (0, 255, 0), 2, cv2.LINE_4)
        cv2.imshow("Face Detector", frame_img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()


def motion_detector():
    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    first_frame = None
    status_list = [None, None]
    times = []
    df = pandas.DataFrame(columns=["Start", "End"])
    while True:
        status = 0
        check, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        if first_frame is None:
            first_frame = gray
            continue
        delta_frame = cv2.absdiff(first_frame, gray)
        thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)
        (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contours in cnts:
            if cv2.contourArea(contours) < 10000:
                continue
            status = 1
            (x, y, w, h) = cv2.boundingRect(contours)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        status_list.append(status)
        if status_list[-1] == 1 and status_list[-2] == 0:
            times.append(datetime.datetime.now())
        if status_list[-1] == 0 and status_list[-2] == 1:
            times.append(datetime.datetime.now())
        cv2.imshow("Motion Detector", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            if status == 1:
                times.append(datetime.datetime.now())
            break
    for i in range(0, len(times), 2):
        df = df.append({"Start": times[i], "End": times[i + 1]}, ignore_index=True)
    df.to_csv("times.csv")
    video.release()
    cv2.destroyAllWindows()


def sanitize_query(text, query1, join):
    arrquery = query1.lower().split()
    if 'in' in arrquery and text == arrquery[arrquery.index("in") + 1]:
        arrquery.remove("in")
    if text in arrquery:
        arrquery.remove(text)
    if "search" in arrquery:
        arrquery.remove("search")
    elif "open" in arrquery:
        arrquery.remove("open")
    query1 = join.join(arrquery)
    return query1


def getLocation():
    ip = str(requests.get('https://api.ipify.org').text)
    complete_url = "http://api.ipstack.com/" + ip + "?access_key=" + cred['location_api']
    response = requests.get(complete_url)
    x = response.json()
    latitude = x['latitude']
    longitude = x['longitude']
    return (latitude, longitude)


if __name__ == '__main__':
    clear = lambda: os.system('cls')
    clear()
    wishMe()
    usrname()
    while True:
        query = takeCommand().lower()
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = sanitize_query("wikipedia", query, " ")
            results = wikipedia.summary(query, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'camera' in query:
            print("Opening Camera")
            print("Press q key to exit camera!!")
            speak("Opening Camera")
            speak("press q key to exit camera")
            camera()

        elif 'take a picture' in query or 'click picture' in query or 'take photo' in query or 'pic photo' in query or \
                'pk picture' in query or 'pk picture' in query or "ek photo" in query:
            print("Opening Camera")
            speak("Opening Camera")
            take_picture()

        elif 'show photo' in query or 'show picture' in query or 'som picture' in query or 'shoe picture' in query or \
                'shoe photo' in query:
            print("Opening Captured Photo")
            speak("Opening Captured photo")
            show_picture()

        elif 'motion detector' in query:
            print("Opening Motion Detector")
            print("Press q key to exit Motion Detector!!")
            speak("Opening Motion Detector")
            speak("press q key to exit Motion Detector!!")
            motion_detector()

        elif 'face detector' in query:
            print("Opening Face Detector")
            print("Press q key to exit Face Detector!!")
            speak("Opening Face Detector")
            speak("press q key to exit Face Detector!!")
            face_detector()

        elif 'youtube' in query:
            options = Options()
            options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(options=options, executable_path=cred["chromedriver_path"])
            speak("Here you go to Youtube\n")
            query = sanitize_query("youtube", query, "+")
            driver.get("http://www.youtube.com/results?search_query=" + query)

        elif 'google' in query:
            options = Options()
            options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(options=options, executable_path=cred["chromedriver_path"])
            speak("Here you go to Google\n")
            query = sanitize_query("google", query, "+")
            driver.get("https://www.google.com/search?q=" + query)

        elif 'search' in query:
            options = Options()
            options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(options=options, executable_path=cred["chromedriver_path"])
            query = sanitize_query("", query, "+")
            driver.get("https://www.google.com/search?q=" + query)

        elif 'stackoverflow' in query:
            options = Options()
            options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(options=options, executable_path=cred["chromedriver_path"])
            speak("Here you go to Stack Overflow.Happy coding")
            driver.get("https://stackoverflow.com")

        elif 'my site' in query:
            options = Options()
            options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(options=options, executable_path=cred["chromedriver_path"])
            speak("Here you go to your site")
            driver.get("https://www.soumyajitdattanow.xyz")

        elif 'my location' in query:
            speak("Getting Your coordinates")
            latitude, longitude = getLocation()
            speak("Coordinates aquired")
            options = Options()
            options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(options=options, executable_path=cred["chromedriver_path"])
            speak("Opening your location on map")
            try:
                url = "localhost:3000/" + str(latitude) + "/" + str(longitude)
                driver.get(url)
                time.sleep(10)
            except Exception as e:
                speak("sorry couldnt open map")

        # elif 'play music' in query or "play song" in query:
        # speak("Here you go with music")
        # music_dir = "G:\\Song"
        # music_dir = "C:\\Users\\GAURAV\\Music"
        # songs = os.listdir(music_dir)
        # print(songs)
        # os.startfile(os.path.join(music_dir, songs[1]))

        elif "open chrome" in query:
            speak("Google Chrome")
            os.startfile(cred["chrome_path"])

        # elif "firefox" in input or "mozilla" in input:
        # speak("Opening Mozilla Firefox")
        # os.startfile('C:\Program Files\Mozilla Firefox\\firefox.exe')

        # elif "word" in query:
        # speak("Opening Microsoft Word")
        # os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\\Word 2013.lnk')

        # elif "excel" in query:
        # speak("Opening Microsoft Excel")
        # os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\\Excel 2013.lnk')

        elif 'the time' in query:
            current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            hour = current_time.hour
            minute = current_time.minute
            if hour > 12:
                hour_str = str(hour - 12)
                ab = "pm"
            else:
                hour_str = str(hour)
                ab = "am"
            print("The time is " + hour_str + ":" + str(minute) + " " + ab)
            speak("The time is " + hour_str + " " + str(minute) + " " + ab)

        elif "roll a dice" in query:
            print("Rolling a dice....")
            speak("Rolling a dice")
            dice = round(random.random() * 6)
            diceresult = "Your result is " + str(dice)
            print(diceresult)
            speak(diceresult)

        elif "random number" in query:
            print("Creating a random number....")
            speak("Creating a random number....")
            randomn = round(random.random() * 10000)
            randomr = "Your random number is " + str(randomn)
            print(randomr)
            speak(randomr)

        # elif 'open opera' in query:
        # codePath = r"C:\\Users\\GAURAV\\AppData\\Local\\Programs\\Opera\\launcher.exe"
        # os.startfile(codePath)

        elif 'email to me' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                speak("What is the Subject?")
                subject = takeCommand()
                to = "soumyajitdatta123@gmail.com"
                sendEmail(to, content, subject)
                speak("Email has been sent !")
                print("Email has been sent !")
            except Exception as e:
                print(e)
                speak("I am not able to send this email")

        elif 'send a mail' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                speak("whom should i send?")
                to = input("Enter Email Address:")
                speak("What is the Subject?")
                subject = takeCommand()
                sendEmail(to, content, subject)
                print("Email has been sent !")
                speak("Email has been sent !")
            except Exception as e:
                print(e)
                speak("I am not able to send this email")

        elif 'how are you' in query:
            speak("I am fine, Thank you")
            speak("How are you, Sir")

        elif 'fine' in query or "good" in query:
            speak("It's good to know that your fine")

        elif "change my name to" in query:
            query = query.replace("change my name to", "")
            assname = query

        elif "change name" in query:
            speak("What would you like to call me, Sir ")
            assname = takeCommand()
            speak("Thanks for naming me " + assname)

        elif "what's your name" in query or "What is your name" in query:
            print("My friends call me", assname)
            speak("My friends call me")
            speak(assname)

        elif 'exit' in query:
            print("Thanks for giving me your time!")
            speak("Thanks for giving me your time")
            exit()

        elif "who made you" in query or "who created you" in query:
            speak("I have been created by Soumyajit.")

        elif 'joke' in query:
            joke = pyjokes.get_joke()
            print(joke)
            speak(joke)

        elif "calculate" in query:
            app_id = cred["wolfram_app_id"]
            client = wolframalpha.Client(app_id)
            indx = query.lower().split().index('calculate')
            query = query.split()[indx + 1:]
            if "".join(query) == "":
                speak("You did not give any value to calculate")
            print("calculate")
            res = client.query(' '.join(query))
            answer = next(res.results).text
            print("The answer is " + answer)
            speak("The answer is " + answer)

        elif "who am i" in query:
            speak("If you talk then definitely you are human.")

        elif "why you came to world" in query:
            speak("Thanks to Soumyajit. further It's a secret")

        elif 'is love' in query:
            speak("It is 7th sense that destroy all other senses")

        elif "who are you" in query:
            speak("I am your virtual assistant created by Soumyajit")

        elif 'reason for you' in query:
            speak("I was created as a Minor project by Mister Soumyajit")

        # elif 'change background' in query:
        # ctypes.windll.user32.SystemParametersInfoW(20,"Location of wallpaper",0)
        # speak("Background changed succesfully")

        # elif 'open bluestack' in query:
        # appli = r"C:\\ProgramData\\BlueStacks\\Client\\Bluestacks.exe"
        # os.startfile(appli)

        elif "weather" in query:
            api_key = cred["weather_apikey"]
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            print("Say City name :")
            speak("Say City name ")
            city_name = takeCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"] - 273.15
                current_pressure = y["pressure"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                data = " Temperature (in celcius) = " + str(
                    current_temperature) + "\n atmospheric pressure (in hPa unit) =" + str(
                    current_pressure) + "\n humidity (in percentage) = " + str(
                    current_humidiy) + "\n description = " + str(weather_description)
                print(data)
                speak(data)
            else:
                print("City Not Found!")
                speak(" City Not Found ")

        elif 'world news' in query:
            num = 2
            try:
                jsonObj = urlopen(
                    "http://newsapi.org/v2/top-headlines?country=us&apiKey=" + cred["newsapi_key"])
                data = json.load(jsonObj)
                i = 1
                speak('here are some top news from usa')
                print('''=============== USA ============''' + '\n')
                for item in data['articles']:
                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    speak(str(i) + '. ' + item['title'] + '\n')
                    if i == num:
                        break
                    i += 1
            except Exception as e:
                print(str(e))
                speak("Oops! unexpected error")
            try:
                jsonObj = urlopen(
                    "http://newsapi.org/v2/top-headlines?country=gb&apiKey=" + cred["newsapi_key"])
                data = json.load(jsonObj)
                i = 1
                speak('here are some top news from great britain')
                print('''=============== Great Britain ============''' + '\n')
                for item in data['articles']:
                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    speak(str(i) + '. ' + item['title'] + '\n')
                    if i == num:
                        break
                    i += 1
            except Exception as e:
                print(str(e))
                speak("Oops! unexpected error")
            try:
                jsonObj = urlopen(
                    "http://newsapi.org/v2/top-headlines?country=au&apiKey=" + cred["newsapi_key"])
                data = json.load(jsonObj)
                i = 1
                speak('here are some top news from australia')
                print('''=============== AUSTRALIA ============''' + '\n')
                for item in data['articles']:
                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    speak(str(i) + '. ' + item['title'] + '\n')
                    if i == num:
                        break
                    i += 1
            except Exception as e:
                print(str(e))
                speak("Oops! unexpected error")

        elif 'news' in query or 'indian news' in query or 'india news' in query:
            speak("How many articles do you want to hear")
            query = takeCommand()
            if type(query) is not int:
                speak("Please say a number")
                speak("Showing 5 articles")
                num = 5
            elif query is not None:
                num = int(query)
            else:
                speak("Showing 5 articles")
                num = 5
            try:
                jsonObj = urlopen(
                    "http://newsapi.org/v2/top-headlines?country=in&apiKey=" + cred["newsapi_key"])
                data = json.load(jsonObj)
                i = 1
                speak('here are some top news from India')
                print('''=============== INDIA ============''' + '\n')
                for item in data['articles']:
                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    speak(str(i) + '. ' + item['title'] + '\n')
                    if i == num:
                        break
                    i += 1
            except Exception as e:
                print(str(e))

        elif 'lock window' in query:
            speak("locking the device")
            ctypes.windll.user32.LockWorkStation()

        elif 'shutdown system' in query:
            speak("Hold On a Sec ! Your system is on its way to shut down")
            subprocess.call('shutdown / p /f')

        elif 'empty recycle bin' in query:
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
            speak("Recycle Bin Recycled")

        elif "don't listen" in query or "stop listening" in query:
            speak("for how much time you want to stop jarvis from listening commands")
            a = int(takeCommand())
            time.sleep(a)
            print(a)

        elif "where is" in query:
            query = query.replace("where is", "")
            location = query
            speak("User asked to Locate")
            speak(location)
            webbrowser.open("https://www.google.nl / maps / place/" + location + "")

        elif "restart" in query:
            subprocess.call(["shutdown", "/r"])

        elif "hibernate" in query or "sleep" in query:
            speak("Hibernating")
            subprocess.call("shutdown /h")

        elif "log off" in query or "sign out" in query:
            speak("Make sure all the application are closed before sign-out")
            time.sleep(5)
            subprocess.call(["shutdown", "/l"])

        elif "write a note" in query or "write note" in query or "create note" in query:
            speak("What should i write, sir")
            note = takeCommand()
            file = open('notes.txt', 'w')
            file.write(note)
            print("Note written Successfully!!")
            speak("note written sucessfully")

        elif "show note" in query or "show notes" in query or "shoe notes" in query or "so notes" in query:
            speak("Showing Notes")
            file = open("notes.txt", "r")
            note = file.read()
            print(note)
            speak(note)

        elif "delete note" in query or "delete notes" in query:
            file = open("notes.txt", "w")
            file.write("")
            print("Notes Deleted")
            speak("notes deleted")

        elif "email me note" in query or "email note" in query or "email mi note" in query:
            file = open("notes.txt", "r")
            content = file.read()
            try:
                subject = "Note"
                to = "soumyajitdatta123@gmail.com"
                sendEmail(to, content, subject)
                print("Email has been sent !")
                speak("Email has been sent !")
            except Exception as e:
                print(e)
                speak("I am not able to send this email")

        elif "send message" in query or "send me a message" in query or "send a message" in query:
            account_sid = cred["twilio_sid"]
            auth_token = cred["twilio_auth_token"]
            client = Client(account_sid, auth_token)
            print("Enter Your Message:")
            speak("Speak Your Message")
            message1 = takeCommand()
            try:
                message = client.messages \
                    .create(
                    body=message1,
                    from_='+12053902313',
                    to='+916290376589'
                )
                print("Message Sent Successfully")
                speak("Message Sent Successfully")
            except Exception as e:
                print("Error:", e)
                speak("Sorry! Couldnt Send message")

        elif "good morning" in query or "good evening" in query or "good night" in query:
            speak("A warm" + query)
            speak("How are you Mister")

        elif "will you be my gf" in query or "will you be my bf" in query:
            speak("I'm not sure about, may be you should give me some time")

        elif "how are you" in query:
            speak("I'm fine, glad you me that")

        elif "i love you" in query:
            speak("It's hard to understand")

        elif "what is" in query or "who is" in query:
            client = cred["wolfram_app_id"]
            res = client.query(query)
            try:
                print(next(res.results).text)
                speak(next(res.results).text)
            except StopIteration:
                print("No results")
        else:
            print("Nothing found.Try Again")
            speak("Nothing found. Try Again")
