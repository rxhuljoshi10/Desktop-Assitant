import os
import sys
import pyttsx3
import datetime
from datetime import datetime
import speech_recognition as sr
import pyautogui as p
import time
import wikipedia
import webbrowser
import pygame
import random
import requests
from bs4 import BeautifulSoup
# from PyDictionary import PyDictionary
import pyjokes
from pywikihow import search_wikihow
# import openpyxl
import json
import clipboard
import psutil
from iso639 import Lang
import keyboard


class routineclass:
    timecheck = False
    ctime = 0
    srs = "sleep"

class Timer:
    duration_time = 0

    def unittoseconds(unit):
        if unit == "seconds":
            return 1
        elif unit == "minutes" or unit == "minute":
            return 60
        elif unit == "hours" or unit == "hour":
            return 3600

    def settimer(duration,unit):
        Timer.duration_time = time.time() + duration * Timer.unittoseconds(unit)

numbers = [1,2,3,4,5,6,7,8,9,10]

def speak(whattosay):
    global bot
    lan = getdata("recog_lang")
    if lan != "en":
        langtext = translate_text(whattosay,lan)
        print(f"{bot} : {langtext} ({whattosay})") 
        engine.say(langtext)
    else:
        print(f"{bot} :  {whattosay}")
        engine.say(whattosay)
    engine.runAndWait()

def getdata(object):
    with open ("jarvisdata.json","r") as f:
        data = json.load(f)
        f.close()
        return data[object]

def putdata(object, val):
    with open ("jarvisdata.json","r") as f:
        data = json.load(f)
        f.close()
    data[object] = val
    with open ("jarvisdata.json","w") as f:
        json.dump(data,f,indent=4)

def switchinput():  
    global input_method
    if input_method:
        speak("Switching input method to 'Speak'")
        putdata("input_method",False)
        input_method=False
    else:
        speak("Switching input method to 'Keyboard'")
        putdata("input_method",True)
        input_method=True

def quickcmndaccess(cmnd):
    global quickcmnd
    global asksomethingelse
    global cmndpass
    asksomethingelse = False
    cmndpass = True
    quickcmnd = True
    start(cmnd)

def turnoffbot():
    speak("Turning myself off")
    speak("See you later sir")
    quit()

def playbeep(beep):
    pygame.mixer.init()
    if beep=='startsleep':
        beep='C:\\Users\\joshi\\Documents\\Programs\\Python\\Jarvis\\start.wav'
    elif beep=='done':
        beep='done.mp3'
    elif beep=='alarm':
        beep='alarm.mp3'
    elif beep=="bankai":
        beep="C:\\Users\\joshi\\Downloads\\Music\\bankai.mp3"
    pygame.mixer.music.load(beep)
    pygame.mixer.music.play()

def greetings():
    now=datetime.now()
    hour=int(now.strftime("%H"))
    if hour>=0 and hour<12:
        return "Good Morning"
    elif hour>=12 and hour<18:
        return "Good Afternoon"
    else:
        return "Good Evening"
 
def windows(cmnd):
    p.hotkey('win','d')
    p.hotkey("alt",'f4')
    if cmnd=='restart':
        winkey='restarting'
        p.press('right')
    elif cmnd=="sleep":
        winkey="sleeping"
        p.press("left")
    else:
        winkey="shutting down"
    p.press("tab")
    speak("Are you sure you want to "+cmnd+" the windows?")
    print("YES or NO")
    cnfm=take_cmnd()
    if "yes" in cnfm or "ok" in cnfm:
        speak(winkey+" windows")
        p.press("enter")
        quit()
    else:
        p.press("right")
        p.press("enter")

def gettime():
    now=datetime.now()
    live_time=now.strftime("%I:%M %p")
    return live_time

def openpath(path,app,WeborOs):
    speak("Opening "+app+"..!!")
    if WeborOs == "web":
        webbrowser.open(path)
    else:
        os.startfile(path)
    sleepmode()

def windows(cmnd):
    if cmnd == "shutdown":
        speak("Shutting down windows, see you later sir..!!")
        os.system("shutdown /s /t 1")
        turnoffbot()
        
    elif cmnd == "restart":
        speak("Restarting windows..!!")
        os.system ("shutdown /r /t 1")

    elif cmnd == "sleep":
        speak("Sleeping windows..!!")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def search(cmnd):
    p.hotkey("win",'s')
    time.sleep(0.2)
    p.typewrite(cmnd)
    time.sleep(0.7)

def getNextword(string,word,tillthisword=None):
    flag = 0
    newstring = ''
    for stringwords in string.split():
        if flag == 1:
            if tillthisword!=None:
                if stringwords != tillthisword:
                    newstring += stringwords + " "
                    continue
                return newstring   
            return stringwords
        if stringwords == word:
            flag = 1

    return newstring

def getpreviousword(string,word):
    for i in string.split():
        j = getNextword(string,i)
        if j == word:
            return i

def cmndline(wtd):
    cmdpath="C:\\Users\\joshi\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\System Tools\\Command Prompt"
    
    os.startfile(cmdpath)
    if wtd=='none':
        return
    
    time.sleep(0.5)
    p.typewrite('cd "C:\Python310\Scripts"')
    p.press('Enter')
    p.typewrite("pip "+wtd+" ")
    speak("Please enter the module name..!!")
    sleepmode()

def sendwhatsappmsg(name,msg):
    search("whatsapp")
    p.press("enter")
    time.sleep(8)
    # p.click(x=151,y=159)
    # time.sleep(1)
    p.typewrite(name)
    time.sleep(0.5)
    p.press("down")
    time.sleep(0.5)
    p.press("enter")
    time.sleep(0.5)
    p.typewrite(msg)
    time.sleep(0.1)
    p.press("enter")
    p.hotkey("win","d")
    speak("Message sent successfully...")    

def reboot():
    speak("Rebooting myself..!!")
    os.startfile("C:\\Users\\joshi\\Desktop\\JARVIS")
    exit(1)

def clock(n):
    search('clock')
    p.press('enter')
    time.sleep(1)
    i=0
    n=int(n)
    while(i<n):
        p.press('down')
        i+=1
    p.press('enter')
    speak("Here you go...!!")

def change_voice(val):
    voices = engine.getProperty('voices')
    putdata("voice",val)
    engine.setProperty('voice', voices[val].id)

def getLangvoice(langcode):
    if langcode == "hi" or langcode == "mr":
        return 1
    if langcode == "ja" or langcode == "zh-CN":
        return 2
    else:
        return 0

def getLangcode(lan):
    if lan == "chinese":
        return "zh-CN"
    lan = lan.capitalize()
    return Lang(lan).pt1

def translate_text(word,lan):
    from deep_translator import GoogleTranslator
    to_translate = word
    text = GoogleTranslator(source='auto', target=lan).translate(to_translate)
    clipboard.copy(text)
    return text
       
def startgame():
    gamepath="C:\\Users\\joshi\\Documents\\Programs\\Python\\snake game\\snakegame.py"
    os.startfile(gamepath)
    sleepmode()

def quickaccess(wtd,btn):
    p.hotkey("win","a")
    time.sleep(1)
    if wtd == "wifi":
        p.press("enter")     
    elif wtd=="bluetooth":
        p.press("right")
        p.press("enter")
    elif wtd == "brightness":
        p.press("tab",presses=2,interval=0.2)
        p.press(btn,presses=20)
        if btn == "left":
            speak("Brightness reduced..!!")
        else:
            speak("Brightness increased..!!")
        p.hotkey("win","a")
        return

    p.hotkey("win","a")
    speak("Done..!!")

def camera(cmnd):
    
    if cmnd == "on":
        speak("Opening camera..!!")
    os.startfile("C:\\Users\\joshi\\Camera")
    if cmnd == "takepic":
        time.sleep(0.5)
        speak("Smile please...!!")
        time.sleep(1)
        p.press("enter")
        time.sleep(0.2)
        p.hotkey("alt","f4")
        speak("Captured your pic..!!")

def checkroutine():
    global sleep
    if not routineclass.timecheck:
        live_time = gettime()
        try:
            cmnd = getdata(live_time)
        except:
            return
        speak(cmnd)
        timer = take_cmnd()
        flag = 0
        for i in numbers:
            if str(i) in timer:
                flag = 1
                speak(f"Okay, I am giving you {i} more minutes..!!")
                sleep = True
                routineclass.timecheck = True
                routineclass.ctime = time.time() + 60 * i
                if "bed" in cmnd:
                    routineclass.srs = "shutdown"
                else:
                    routineclass.srs = "sleep"
        
        if flag == 0:
            if timer != "":
                routineclass.timecheck = True
                routineclass.ctime = time.time() + 60 * 5
                quickcmndaccess(timer)
            

    else:           
        if time.time() > routineclass.ctime:
            routineclass.timecheck = False
            speak("Your extra time is over sir..!!")
            windows(routineclass.srs)


def vippass():
    global sleep
    global asksomethingelse
    global cmndpass
    sleep = False
    asksomethingelse = False
    cmndpass = True
    start("")

def sleepmode():
    global sleep
    global asksomethingelse
    global cmndpass
    sleep = True
    cmndpass = False
    asksomethingelse = False
    start("")

def take_cmnd():
    global input_method
    global sleep

    if input_method:
        output=input("\n:- ")
        print("")
        return output

    if not sleep:
        print("\nListening...\n")
        
    listener=sr.Recognizer()
    try:
        with sr.Microphone() as source:
            listener.energy_threshold=300
            # listener.dynamic_energy_threshold = True  
            # listener.adjust_for_ambient_noise(source, duration=1)
            listener.dynamic_energy_threshold = True  
            audio_text=listener.listen(source,0,5)
            lan = getdata("recog_lang")
            command = listener.recognize_google(audio_text,language=lan)
            if lan != "en":
                command = translate_text(command,"en")
            command = command.lower()
            return command

    except:
        if sleep == False:
            speak("Going into sleep mode..!!\n")
        sleepmode()

def start(cmnd):
    global quickcmnd
    global sleep
    global asksomethingelse
    global input_method
    global bot
    global cmndpass
    global routine
    global timerset
    
    while 1:
        if routine:
            checkroutine()

        if timerset:
            print(Timer.duration_time)
            print(time.time())
            if Timer.duration_time < time.time():
                playbeep()
                timerset = False
        
        if keyboard.is_pressed('`'):
            switchinput()

        if asksomethingelse:
            cmndpass=True
            # sleep = False
            print("")
            words=("Do you want any other help sir?",
                    "Anything else?",
                    "What else can i do for you?")
            speak(random.choice(words))

        if quickcmnd:
            quickcmnd = False
        else:
            cmnd = take_cmnd()

        if (not "change" in cmnd and "your name" in cmnd) or "who are you" in cmnd or "what are you" in cmnd or "about you" in cmnd:
            speak("My name is "+bot+",")
            speak("Im an AI system, built to control your windows")
            speak("Say 'TASK' to see all the tasks I can handle for you")
            vippass()

        if cmndpass == False:
            if not input_method:
                flag=0
                for i in [bot,"wake"]:
                    if i in cmnd:
                        flag=1
                        break
                
                if flag==0:
                    continue
    
        if not input_method:
            sleep = False
            print("You Said : "+cmnd+"\n")

#COMMANDS:
        if 'quit' in cmnd or "turn off "+bot in cmnd:
            turnoffbot()

        elif "translate" in cmnd:
            word = getNextword(cmnd,"translate","in")
            if word == "":
                speak("Which word you want to translate?")
                word = take_cmnd()

            lan = getNextword(cmnd,"in")
            if lan == "":
                speak("In which language sir?")
                lan = take_cmnd()
                if "in" in lan.split():
                    lan = lan.replace("in ","")
                
            speak(f"Translating ' {word}' in {lan}..!!")
            try :
                translatedWord = translate_text(word,getLangcode(lan))
            except:
                speak("Specified language is not valid..!!")
                continue
            speak("It is said as, ")
            langcode = getLangcode(lan)
            previous = getdata("voice")
            change_voice(getLangvoice(langcode))
            speak(translatedWord)
            change_voice(previous)
            speak("I have copied this word to your clipboard..!!")

        elif "wikipedia" in cmnd:
            word = getNextword(cmnd,"of","")
            if word == "":
                speak("Wikipedia of what sir?")
                word = take_cmnd()
            speak(f"Searching wikipedia of ' {word}'..!!")
            try:
                wikiresult=wikipedia.summary(word,sentences=2)
                print(" ")
                speak("According to Wikipedia,")
                speak(wikiresult)
            except:
                speak("No results found")
       
        elif "meaning" in cmnd or "mean" in cmnd:
            from PyMultiDictionary import MultiDictionary
            dc = MultiDictionary()
            word = getNextword(cmnd,"of","")
            if word == "":
                word = getNextword(cmnd,"by","")
                if word == "":
                    speak("What is the word you want meaning of sir?")
                    word = take_cmnd()

            try:
                # word_list=["meaning","mean","of","a","me","tell","what","is","by","hey",bot]
                # rp_wd=""
                # word=''.join([rp_wd if idx in word_list else idx for idx in cmnd.split()])
                speak(f"Searching meaning of {word}..!!")
                mean=dc.meaning("en",word)

                mean = mean[1].split(".")
                mean = mean[0].split("is")
                mean = mean[1]

                speak(f"A {word} is{mean}.")

            except:
                speak("No results found..!!")

        elif "change" in cmnd and "name" in cmnd:
            speak("What name do you want me to keep sir?")
            botname = take_cmnd()
            speak(botname+", hmm... sounds good to me..!!")
            speak(f"Changing my name from {bot} to {botname}")
            bot = botname
            putdata("name",bot)
        
        elif "change" in cmnd and "voice" in cmnd:
            voice = getdata("voice")
            if voice == 0:
                change_voice(4)
                speak("Changed into female voice..!!")           
            
            elif voice == 4:
                change_voice(0)
                speak("Changed into male voice..!!")

            else:
                speak("You need to change your language first sir..!!")

        elif "change" in cmnd and "language" in cmnd:
            nolanguage = False
            if "to" not in cmnd:
                speak("In which language you want me to switch sir?")
                nolanguage = True

            while 1:
                if nolanguage:
                    cmnd = take_cmnd()

                cmnd = cmnd.split()
                for i in cmnd:
                    lang = i
                
                try:
                    langcode = getLangcode(lang)
                    break
                except:
                    speak("I misheard it sir... what was the language again?")
                    nolanguage = True

            speak(f"Switching my language to {lang}")
            putdata("recog_lang",langcode)
            change_voice(getLangvoice(langcode))

        elif "learn" in cmnd or "new language" in cmnd:
            speak("Which learning platform you want me to open, 'code with harry' or 'w3school' ? ")
            vippass()

        elif "language" in cmnd:
            speak("I can speak almost all languages..!!")
            speak("Just say 'Change language to (one you want)'")

        elif "spell" in cmnd or "spelling" in cmnd:
            if "of" in cmnd:
                word = getNextword(cmnd,"of",bot)
            elif "spell" in cmnd:
                word = getNextword(cmnd,"spell","")
            else:
                speak("What is word sir?")
                word = take_cmnd()
            speak("It is spell as...")
            for i in range(0,len(word)):
                speak(word[i]+",")

        elif "pronounce" in cmnd or "say" in cmnd:
            cmnd=cmnd.replace("pronounce","")
            cmnd=cmnd.replace("say","")
            speak(cmnd)
        
        elif "switch input" in cmnd:
            switchinput()
        
        elif "shutdown" in cmnd and "windows" in cmnd:
            windows("shutdown")
            
        elif "restart" in cmnd and "windows" in cmnd:
            windows("restart")
            
        elif "sleep" in cmnd and "windows" in cmnd:
            windows("sleep")
       
        elif "nothing" in cmnd.split() or "no" in cmnd.split() or 'not' in cmnd.split() or "nope" in cmnd.split() or "sleep" in cmnd or  "break" in cmnd:
            speak('Okay...')
            speak("Let me know if you need something..!!")
            sleepmode()

        elif "thanks" in cmnd or "thank you" in cmnd :
            speak("It's my pleasure sir..!!")
            sleepmode()

        elif "how are you" in cmnd or "how you doing" in cmnd or "what's up" in cmnd:
            speak("I'm doing great, how about you sir?")
            cmnd=take_cmnd()
            if "not" in cmnd.split() or "sad" in cmnd or "bored" in cmnd:
                speak("Oh..!!, let me play some songs for you")
                #playmusic()
            elif "fine" in cmnd or "good" in cmnd or "perfect" in cmnd:
                speak("Oh great..!!")
                cmndpass = True
                asksomethingelse = True
            else:
                quickcmndaccess(cmnd)
        
        elif "bored" in cmnd:
            speak("Oh.., why are you so bored when im with you sir..!!")
            bored=("spotify","netflix","game")
            bored=random.choice(bored)
            if bored=="spotify":
                p.hotkey('win','4')
                speak("Here, listen to some songs...")
            elif bored=='netflix':
                p.hotkey('win','3')
                speak("Here, watch some movies...")
            elif bored=='game':
                startgame()
                speak("Here , play some games...")
            
            sleepmode()
        
        elif "zoom" in cmnd or "i can't see" in cmnd:
            if "out" in cmnd:
                say = "zoomed out..!!"
                ope = "-"
            else:
                say = "zoomed in..!!"
                ope = "+"
            for i in range(5):
                p.hotkey('ctrl',ope)
            speak(say)

        elif "screen recording" in cmnd:
            speak("Starting screen recording..!!")
            p.hotkey('win','alt','r')
            sleepmode()

        elif "type" in cmnd:
            speak("What do you want me to type?")
            ty=take_cmnd()
            if ty=='cancel':
                sleepmode()
            p.typewrite(ty)
        
        elif "clear" in cmnd:
            os.system('cls')
            speak("Cleared previous commands...")
            
        elif "date" in cmnd.split():
            now=datetime.now()
            date=now.strftime("%d of %B, %A")
            speak("Today's date is "+date)
        
        elif "news" in cmnd:
            speak("Getting you today's top 10 news...")
            url = 'https://www.bbc.com/news'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            headlines = soup.find('body').find_all('h3')
            
            for x in range(1,10):
                speak(headlines[x].text.strip())

        elif "how to" in cmnd:
            speak("Searching..!!")
            cmnd.replace("how to","")
            cmnd.replace(bot,"")
            cmnd.replace("hey","")
            try:
                cmnd = search_wikihow(cmnd,1)
                assert len(cmnd) == 1
                speak(cmnd[0].summary)
            except:
                speak("Oops, network error..!!")
            
        elif "battery" in cmnd:
            battery = psutil.sensors_battery()
            percentage = battery.percent
            speak(f"You have {percentage} percent battery left..!!")

        elif "timer" in cmnd.split():
            if "seconds" in cmnd or "second" in cmnd:
                if "second" in cmnd.split():
                    unit = 'second'
                else:
                    unit = 'seconds'

            elif "minutes" in cmnd or "minute" in cmnd:
                if "minute" in cmnd.split():
                    unit = 'minute'
                else:    
                    unit = 'minutes'
    
            elif "hours" in cmnd:
                unit = 'hours'
            
            else:
                speak("In order to set a timer, you have to say, 'set a timer for specific minutes,seconds or hours'")
                vippass()

            duration = int(getpreviousword(cmnd,unit))
            Timer.settimer(duration,unit)
            speak(f"Timer set for {duration} {unit}..!!")
            timerset = True
            sleepmode()
   
        elif "alarm" in cmnd:
            clock('2')
                    
        elif "stopwatch" in cmnd:
            speak("Opening your stop watch program..!!")
            os.startfile("C:\\Users\\joshi\\Documents\\Programs\\Python\\stopwatch.py")

        elif "maximize" in cmnd:
            p.hotkey("win","up")
            speak("Maximized..!!")

        elif "minimise" in cmnd:
            p.hotkey("win","m")
            speak("Minimized..!!")

        elif "full screen" in cmnd or "exit full screen" in cmnd:
            p.press('f11')
            speak("Done..!!")
        
        elif "switch window" in cmnd or "previous window" in cmnd:
            p.hotkey("alt","tab")

        elif "tired" in cmnd:
            playbeep("bankai")
            sleepmode()

        elif "virtual desktop" in cmnd:
            p.hotkey("win","ctrl","d")
            speak("Virtual Desktop Created..!!")
        
        elif "mute" in cmnd:
            p.press("volumemute")
            speak('done')
        
        elif "volume" in cmnd:
            if "lower" in cmnd or "low" in cmnd or "decrease" in cmnd or "down" in cmnd:
                volbtn='volumedown'
                volsay = "decreased..!!"
    
            elif "higher" in cmnd or "high" in cmnd or "increase" in cmnd or 'up' in cmnd:
                volbtn='volumeup'
                volsay = "increased..!!"

            else:
                continue
            p.press(volbtn,presses=10)
            speak("Volume "+volsay)

        elif "wi-fi" in cmnd or "wifi" in cmnd:
            quickaccess("wifi","none")

        elif "bluetooth" in cmnd:
            quickaccess("bluetooth","none")

        elif "brightness" in cmnd:
            if "lower" in cmnd  or "decrease" in cmnd or "reduce" in cmnd or "very high" in cmnd:
                quickaccess("brightness","left")
            elif "higher" in cmnd or "increase" in cmnd  or 'very low' in cmnd:
                quickaccess("brightness","right")

        elif "sorry" in cmnd:
            speak("Not a problem sir")
            sleepmode()

        elif "*" in cmnd:
            speak("Sorry, I cannot respond to inappropriate language..!!")

        elif "jokes" in cmnd or "joke" in cmnd:
            jokes=pyjokes.get_joke()
            speak(jokes)
            cmnd = take_cmnd()
            if "hahaha" in cmnd or "ha ha" in cmnd or "haha" in cmnd:
                speak("I know the joke was so lame, no need to laugh..!!")
            else :
                if cmnd!="":
                    quickcmndaccess(cmnd)

        elif "refresh" in cmnd:
            p.hotkey('win','d')
            i=0
            while(i<3):
                time.sleep(0.2)
                p.hotkey("shift","f10")
                time.sleep(0.1)
                j=0
                while(j<4):
                    p.press('down')
                    j+=1
                p.press("enter")
                time.sleep(0.1)
                i+=1  
            p.hotkey("win","d")
            speak("Done..!!")
        
        elif "post" in cmnd and "instagram" in cmnd:
            speak("Posting new video on your anime page on instagram..!!")
            os.startfile("C:\\Users\\joshi\\Documents\\Programs\\Python\\AI_instapost\\InstaPost.py") 

        elif "mouse position" in cmnd or "cursor" in cmnd:
            speak("Getting your cursor position")
            time.sleep(2)
            data=p.position()
            speak(data)
            clipboard.copy(str(data))
         
        elif "send a whatsapp message" in cmnd or "whatsapp message" in cmnd or "send message" in cmnd:
            # cmndpass=True
            # speak("To whom do you want to send message sir?")
            # whatsname=take_cmnd()
            # if 'cancel' in whatsname:
            #     return
            # speak("What's the message?")
            # whatsmsg=take_cmnd()
            # if 'cancel' in whatsmsg:
            #     return
            # speak("Are you sure, you wanna send message '"+whatsmsg+"' to '"+whatsname+"'")
            # whatsconfirm=take_cmnd()
            # if "no" in whatsconfirm or "don't send" in whatsconfirm or 'cancel' in whatsconfirm:
            #     return
            # elif 'yes' in whatsconfirm or "ok" in whatsconfirm or "send" in whatsconfirm or 'sure' in whatsconfirm:
            #     speak("Okay, message will be send within 20 seconds..!!")
            #     sendwhatsappmsg(whatsname,whatsmsg)
            # else:
                return          
            
        elif "temperature" in cmnd:
            speak("Checking current temperature..!!")
            s="temperature in pune"
            try:
                url="https://www.google.com/search?q="+s
                r=requests.get(url)
                data=BeautifulSoup(r.text,"html.parser")
                temp=data.find("div",class_="BNeawe").text
                speak(f"Current {s} is {temp}")
            except:
                speak("Oops, network error..!!")

        elif "search" in cmnd or "find" in cmnd:
            cmnd=cmnd.replace("search","")
            cmnd=cmnd.replace("for","")
            cmnd=cmnd.replace("find","")
            cmnd=cmnd.replace("please","")
            cmnd=cmnd.replace(bot,"")

            if cmnd==' ':
                speak("What do you want me to search sir?")
                cmnd=take_cmnd()
                if 'cancel' in cmnd or "don't search" in cmnd:
                    return
            speak("Searching...")
            search(cmnd)
            speak("Here are the results I got sir..!!")  
        
        elif "update" in cmnd or "reboot" in cmnd:
            reboot()
            
        elif "game" in cmnd:
            startgame()

        elif "greet" in cmnd or "morn" in cmnd or "even" in cmnd or "after" in cmnd:
            greet=greetings()
            speak(greet+" sir")
            speak("Let me know if you need something")
            vippass()

        elif "uninstall" in cmnd and "module" in cmnd:
            cmndline('uninstall')
            
        elif "install" in cmnd and "module" in cmnd:
            cmndline('install')

        elif "command line" in cmnd or "cmd" in cmnd:
            speak("Opening CMD")
            cmndline('none')

    
    #webapplications:
        elif "gmail" in cmnd:
            openpath("https://www.gmail.com/" , "gmail" , "web")

        elif "drive" in cmnd:
            openpath("https://drive.google.com/drive/my-drive" , "your google drive account", "web")

        elif "docs" in cmnd:
            openpath("https://docs.google.com/document/u/0/" , "your google docs", "web")

        elif "open database" in cmnd:
            openpath("https://onecompiler.com/postgresql" , "dbms compiler" , "web")

        elif "google" in cmnd:
            openpath("https://www.google.com/" , "Google" , "web")

        elif "youtube" in cmnd:
            openpath("https://www.youtube.com/" , "Youtube" , "web")

        elif "monkey" in cmnd or "practice typing" in cmnd:
            openpath("https://www.monkeytype.com/" , "Monkey Typing Test" , "web")

        elif "harry" in cmnd:
            openpath("https://www.youtube.com/@CodeWithHarry/playlists" , "Code With Harry on youtube" , "web")

        elif "school" in cmnd:
            openpath("https://www.w3schools.com/" , "W3school" , "web")

        elif "chat gpt" in cmnd:
            openpath("https://chat.openai.com/chat" , "Chat GPT" , "web")

        elif "anime" in cmnd:
            if "new" in cmnd:
                openpath("https://zoro.to/home" , "ZORO.to" ,"web")
            openpath("https://zoro.to/user/watch-list","your watchlist on ZORO.to","web")

        elif "git hub" in cmnd:
            openpath("https://github.com/" , "Github" , "web")


    #windows applications with paths:
        elif "note" in cmnd:
            openpath("notepad.exe","notepad","win")

        elif "calculator" in cmnd:
            openpath("calc.exe","calculator","win")

        elif "open" in cmnd and ("screenshots" in cmnd or "screenshot" in cmnd):
            openpath("C:\\Users\\joshi\\Pictures\\Screenshots" , "screenshots folder" , "win")

        elif "program" in cmnd or "project" in cmnd:
            openpath("C:\\Users\\joshi\\Documents\\Programs" , "your programs folder" , "win")

        elif "wallpapers" in cmnd:
            openpath("C:\\Users\\joshi\\Pictures\\Wallpapers" , "your wallpapers" , "win")
    
        elif "gallery" in cmnd:
            openpath("C:\\Users\\joshi\\Pictures" , "Gallery" , "win")

        elif "downloads" in cmnd:
            openpath("C:\\Users\\joshi\\Downloads" , "your downloads" , "win")

        elif "whatsapp" in cmnd:
            openpath("C:\\Users\\joshi\\Whatsapp.lnk" , "Whatsapp" , "win")
           
        elif "instagram" in cmnd:
            openpath("C:\\Users\\joshi\\Instagram.lnk" , "Instagram" , "win")

        elif "telegram" in cmnd:
            openpath("C:\\Users\\joshi\\Telegram Desktop.lnk" , "Telegram" , "win")

        elif "data" in cmnd or "your info" in cmnd:
            openpath("C:\\Users\\joshi\\Documents\\Programs\\Python\\Jarvis\\jarvisdata.json","my data file","win")


    #window applications with key shortcuts:
        elif "browser" in cmnd:
            speak("Opening Browser")
            p.hotkey("win","2")
            sleepmode()

        elif "netflix" in cmnd or "movie" in cmnd:
            p.hotkey('win','3')
            speak("Here you go ..!!")
            speak("Have a great watching sir..!!")
            sleepmode()

        elif "music" in cmnd or "song" in cmnd or "spotify" in cmnd:
            speak("Opening Spotify")
            p.hotkey('win','4')

        elif "code" in cmnd:
            #vspath="C:\\Users\\joshi\\AppData\\Local\\Programs\\Microsoft VS Code\\Code"
            #os.startfile(vspath)
            p.hotkey('win','5')
            speak("Here you go..!!")
            speak("Have a great coding sir..!!")
            sleepmode()

        elif "bin" in cmnd:
            speak("Opening recycle bin..!!")
            p.hotkey("ctrl","alt","0")
            sleepmode()

        elif "settings" in cmnd:
            p.hotkey("win","i")
            speak("Here you go..")
        
        elif "task manager" in cmnd:
            p.hotkey("ctrl","shift","esc")

        elif "notifications" in cmnd.split() or "notification" in cmnd.split():
            p.hotkey("win","n")
            speak("Here are your notifications..!!")

        elif "files" in cmnd:
            p.hotkey("win","e")    
            speak("Here are your files")
            
        elif "calendar" in cmnd:
            speak("Opening Calendar")
            search('calendar')
            p.press("enter")

        elif "store" in cmnd:
            search("microsoft store")
            p.press("enter")
            speak("Here is your microsoft store")
            sleepmode()

        elif "snip" in cmnd:
            p.hotkey("win","shift",'s')
            speak("Here you go")
            
        elif "camera" in cmnd:
            camera("on")
            
        elif "selfie" in cmnd or "pic" in cmnd:
            camera("takepic")

        elif "capture" in cmnd or "video" in cmnd:
            import cv2
            import numpy as np

            cap = cv2.VideoCapture(0)

            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('screen_recording.avi', fourcc, 20.0, (640, 480))
            while True:
                ret, frame = cap.read()
                out.write(frame)
                cv2.imshow("Screen Recording", frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            out.release()
            cv2.destroyAllWindows()

        
        elif "can you do" in cmnd or "task" in cmnd:
            taskfolder="C:\\Users\\joshi\\Documents\\Programs\\Python\\Jarvis\\cmndsicando.txt"
            os.startfile(taskfolder)
            speak("Here are the tasks i can handle for you sir..!!")
            sleepmode()


        elif "open" in cmnd:
            app=getNextword(cmnd,"open","")
            openpath(f"https://www.{app}.com/" , app , "web")

        elif "close" in cmnd:
            p.hotkey("alt","f4")
            speak("At once..")


        elif "stop" in cmnd or "pause" in cmnd:
            p.press("space")
            speak("Done..!!")

        elif "screenshot" in cmnd:
            p.hotkey("win",'printscreen')
            speak("Screenshot saved successfully..!!")

        elif "time" in cmnd.split() or "timing" in cmnd:
            speak("Current time is "+gettime())

        elif "what" in cmnd.split() or "who" in cmnd or "where" in cmnd.split() or "which" in cmnd or "how" in cmnd.split() or "when" in cmnd or "about" in cmnd:
            speak("Searching...")
            cmnd=cmnd.replace("hey","")
            cmnd=cmnd.replace(bot,"")
            cmnd=cmnd.replace("tell me","")
            url="https://www.google.com/search?q="+cmnd
            r=requests.get(url)
            data=BeautifulSoup(r.text,"html.parser",)
            temp=data.find("div",class_="BNeawe").text
            speak(temp)

        elif "hey" in cmnd or "hello" in cmnd or 'hi' in cmnd.split() or "wake" in cmnd or bot in cmnd:
            playbeep("startsleep")
            speak("What's the command sir?")
            vippass()

        else:
            speak("Sorry, I have no action stored for this command")
            speak("I am still in progress..!!")
            vippass()
            
        asksomethingelse = True


engine=pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 200) 

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[getdata("voice")].id) 


cmndpass = True
asksomethingelse = False
quickcmnd = False
sleep = False
timerset = False
routine = True


bot=getdata("name")
input_method=getdata("input_method")
greet=greetings()    

os.system("cls")
speak(greet+" sir, I am "+bot)
speak("Let me know if you need any help..!!")

while 1:
    try:
        start("")

    except Exception as e:
        speak("Looks like there was some error..!!")
        print(e)
        time.sleep(5)