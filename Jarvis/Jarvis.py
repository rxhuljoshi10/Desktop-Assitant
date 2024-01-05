from Modules import *

class Assistance:
    def __init__(self):
        self.datafile = self.getPath("data file")
        self.putData("fileName",__file__)
        self.engine = pyttsx3.init()
        self.speechRate = self.getData("speech_rate")
        self.engine.setProperty('rate', self.speechRate)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[self.getData("voice")].id)
        self.botName = self.getData("botName").capitalize()
        self.input_method = self.getData("input_method")
        # recog_lang = self.getData("recog_lang")
        self.Language = self.getData("language")
        # checkRoutine = self.getData("checkRoutine")
        self.sleep = False
        self.somethingelse = False
        self.validatecommand = False
        self.IncreDecre = "volume"
        self.prevcmnd = ""

        if not self.internet_connection():
            if self.input_method == "mic":
                self.switchInputMethod()
   
    def start(self):
        os.system("cls")
        greet = self.greetings()
        self.speak(greet+" sir, I am "+ self.botName)
        self.speak("Let me know if you need any help..!!")
        try:
            self.loop()
        except Exception as e:
            self.speak("Looks like there was some error..!!")
            print(e)
            time.sleep(1)
            self.loop()
    
    def speak(self, text, language = None):
        print(f"{self.botName} :  {text}")
        if language == None:
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            voicePath = "C:\\Users\\joshi\\Documents\\Programs\\Storage\\output.mp3"
            try:
                tts = gTTS(text=text, lang=language)
            except:
                self.self.speak("Specified language is not supported..!!")
                return 
            tts.save(voicePath)
            self.playSound(voicePath)

    def loop(self):
        while 1:
            if keyboard.is_pressed('`'):
                self.switchInputMethod()

            # if self.checkRoutine:
            #     routine()

            if self.somethingelse:
                self.validatecommand = False
                print()
                words=("Do you want any other help sir?",
                        "Anything else?",
                        "What else can i do for you?")
                self.speak(random.choice(words))

            cmnd = self.take_cmnd()
            if cmnd:
                self.getResponse(cmnd)

    def take_cmnd(self):
        if self.input_method == "keyboard":
            self.validatecommand = False
            output=input("\n:- ")
            print("")
            return output.lower()

        if not self.sleep:
            print("\nListening...")
            
        listener=sr.Recognizer()
        try:
            with sr.Microphone() as source:
                listener.energy_threshold=300
                listener.dynamic_energy_threshold = True  
                audio_text=listener.listen(source,0,10)
                # lan = self.getData("recog_lang")
                command = listener.recognize_google(audio_text,language="en")
                # if lan != "en":
                #     command = translate_text(command,"en")
                command = command.lower()

        except:
            if not self.sleep:
                self.speak("Going into sleep mode..!!\n")
                self.sleepmode()
            return

        if self.validatecommand:
            flag=0
            for i in [self.botName.lower(),"wake","name"]:
                if i in command:

                    flag=1
                    self.sleep = False
                    break
            
            if flag == 0:
                return False
            
        if not self.sleep:
            print("\nYou Said : "+command+"\n")

        return command
    
    def sleepmode(self):
        self.sleep = True
        self.validatecommand = True
        self.somethingelse = False

    def getResponse(self, cmnd):

        def activities():
            activity = ("songs","movies","games")
            activity = random.choice(activity)
            if activity == "songs":
                self.speak("Here, listen to some songs...")
                playSongs()

            elif activity == 'movies':
                os.startfile(self.getPath("netflix"))
                self.speak("Here, watch some movies...")

            elif activity == 'games':
                self.speak("Here, play some games")
                playGames()
            
            self.sleepmode()

        def camera(cmnd):   
            if cmnd == "on":
                self.speak("Opening camera..!!")
            os.startfile(self.getPath("camera"))
            if cmnd == "takepic":
                time.sleep(0.5)
                self.speak("Smile please...!!")
                time.sleep(1)
                p.press("enter")
                time.sleep(0.2)
                p.hotkey("alt","f4")
                self.speak("Captured your pic..!!")

        def clock(n):
            search('clock')
            p.press('enter')
            time.sleep(1.5)
            for i in range(n):
                p.press('down')
            p.press('enter')
            self.speak("Here you go...!!")

        def cmndline(query):
            os.startfile(self.getPath("cmd"))
            if query == 'none':
                return   
            time.sleep(0.5)
            p.typewrite(f'cd "{self.getPath("python")}"')
            p.press('Enter')
            p.typewrite("pip "+ query +" ")
            self.speak("Please enter the module name..!!")
            self.sleepmode()

        def gettime():
            now=datetime.now()
            live_time=now.strftime("%I:%M %p")
            return live_time

        def getNextword(string,word,tillthisword=None):
            flag = 0
            newstring = ''
            for stringwords in string.split():
                if flag == 1:
                    if tillthisword!=None:
                        if stringwords != tillthisword:
                            newstring += stringwords + " "
                            continue
                        break
                    newstring = stringwords
                    break
                if stringwords == word:
                    flag = 1
            
            if newstring == "":
                return None
            return newstring.strip()

        def getLangvoice(langcode):
            if langcode == "hi" or langcode == "mr":
                return 1
            if langcode == "ja" or langcode == "zh-CN":
                return 2
            else:
                return 0

        def getLangcode(lang):
            if LANGCODES.get(lang):
                return LANGCODES.get(lang)
            elif LANGUAGES.get(lang):
                return LANGUAGES.get(lang)
            
        def get_weather_data(location):
            try:
                url = f"https://www.timeanddate.com/weather/india/{location}"
                r = requests.get(url)
                data = BeautifulSoup(r.text, "html.parser")
                temp = data.find("div", class_="h2").text.strip()
                weather_status = data.find("p").text
                return temp,weather_status

            except:
                self.speak("Data is not available for the specified location")

        def networkError():
            if self.input_method == "mic":
                self.speak("Looks like there is no internet connection..!!")
                self.switchInputMethod()

        def openPath(app):
            path = self.getPath(app)
            if not path:
                return 0
            self.speak("Opening " + app)
            if "https" in path:
                webbrowser.open(path)
            else:
                os.startfile(path) 
            return 1

        def playSongs():
            os.startfile(self.getPath("play_songs"))
            self.sleepmode()

        def playGames(game=None):
            if not game:
                games = self.getPath("games")
                game = random.choice(list(games))
            
            self.speak("Starting" +" " + game)
            os.startfile(self.getPath(game))
            self.sleepmode()

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
                p.hotkey("win","a")
                return

            p.hotkey("win","a")
            self.speak("Done..!!")

        def reboot():
            self.speak("Rebooting myself..!!")
            current_file_path = os.path.abspath(self.getData("fileName"))
            os.startfile(current_file_path)
            exit(1)

        def removeWords(query):
            remWords = [self.botName.lower(),'start', 'open', 'the', 'say', 'in', 'please','hi', 'hey', 'hello', 'pronounce', 'how', 'to', 'are', 'search', 'for', 'find', 'can', 'you', 'what', 'who', 'is', 'my']
            words = query.split()
            filtered_words = []
            for word in words:
                if word.lower() not in remWords:
                    filtered_words.append(word)
            filtered_query = ' '.join(filtered_words)
            return filtered_query

        def routine():
            current_time = datetime.now().strftime("%H:%M")
            routines = self.getData("routines")
            for rTime in routines:
                if current_time == rTime:
                    self.speak(routines[rTime])

        def search(cmnd):
            p.hotkey("win",'s')
            time.sleep(0.8)
            p.typewrite(cmnd)
            time.sleep(0.7)
            
        def translateText(word,lang):
            lang = getLangcode(lang)
            if not lang:
                self.speak("Specified language is invalid..!!")
                return 0
            try:
                text = GoogleTranslator(source='auto', target=lang).translate(word)
                clipboard.copy(text)
                return text
            except:
                networkError()

        def volume(query):
            if query == "low":
                volbtn='volumedown'
            elif query == "high":
                volbtn='volumeup'
            p.press(volbtn,presses=10)

        def windows(cmnd):
            if "shutdown" in cmnd:
                self.speak("Shutting down windows, see you later sir..!!")
                os.system("shutdown /s /t 1")
                exit(1)
            
            elif "restart" in cmnd:
                self.speak("Restarting windows..!!")
                os.system ("shutdown /r /t 1")

            elif "sleep" in cmnd:
                self.speak("Sleeping windows..!!")
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

  


        self.somethingelse = True
        self.validatecommand = False

        if "more" in cmnd or "again" in cmnd:
            self.getResponse(self.prevcmnd)
            return

        self.prevcmnd = cmnd

        if (not "change" in cmnd and "your name" in cmnd) or "who are you" in cmnd.split() or "what are you" in cmnd.split() or "about you" in cmnd:
                self.speak("My name is "+self.botName+",")
                self.speak("Im an AI system, built to control your windows")
                self.speak("Say, 'Open Task Folder' to see all the commands I can handle for you")
                self.somethingelse = False
                
        elif 'quit' in cmnd or "turn off "+self.botName in cmnd:
            self.speak("Turning myself off")
            self.speak("See you later sir")
            quit()
        
        elif "change" in cmnd and "name" in cmnd:
            newname = getNextword(cmnd,"to")
            if not newname:
                self.speak("What name do you want me to keep sir?")
                newname = self.take_cmnd()
            self.speak(newname+", sounds cool to me..!!")
            self.speak(f"Changing my name from {self.botName} to {newname}")
            self.botName = newname
            self.putData("botName",self.botName)
        
        elif "change" in cmnd and "voice" in cmnd:
            voice = self.getData("voice")
            if voice == 0:
                self.change_voice(7)
                self.speak("Changed into female voice..!!")           
            
            elif voice == 7:
                self.change_voice(0)
                self.speak("Changed into male voice..!!")

            else:
                self.speak("You need to change your language first sir..!!")

        elif "change" in cmnd and "language" in cmnd:
            nolanguage = False
            if "to" not in cmnd:
                self.speak("In which language you want me to switch sir?")
                nolanguage = True

            while 1:
                if nolanguage:
                    cmnd = self.take_cmnd()

                cmnd = cmnd.split()
                for i in cmnd:
                    lang = i
            
                try:
                    self.Language = lang
                    langcode = getLangcode(lang)
                    break
                except:
                    self.speak("I misheard it sir... what was the language again?")
                    nolanguage = True

            self.speak(f"Switching my language to {lang}")
            self.putData("recog_lang",langcode)
            self.change_voice(getLangvoice(langcode))
        
        elif "translate" in cmnd:
            if not self.internet_connection:
                networkError()
            pattern = r"translate (.+) in (\w+)"
            match = re.search(pattern,cmnd,re.IGNORECASE)
            if match:
                word = match.group(1)
                lang = match.group(2)
            else:
                self.speak("In order to translate, you need to say 'Translate {word or sentence} in {specific language}'")
                return
            self.speak("Translating...")
            transText = translateText(word,lang)
            if transText:
                self.speak("It is said as : ")
                self.speak(transText,getLangcode(lang))

        elif "increase" in cmnd or "higher" in cmnd:
            if "volume" in cmnd:
                self.IncreDecre = "volume"
                volume("high")

            elif "rate" in cmnd:
                self.IncreDecre = "speech rate"
                self.speechRate(self.engine.getProperty('rate') + 20)

            elif "brightness" in cmnd:
                self.IncreDecre = "brightness"
                quickaccess("brightness","right")
            
            else:
                self.getResponse(self.prevcmnd + self.IncreDecre)
                return
                
            self.speak(self.IncreDecre + " increased..!!")    

        elif "decrease" in cmnd or "reduce" in cmnd or "lower" in cmnd:
            if "volume" in cmnd:
                self.IncreDecre = "volume"
                volume("low")

            elif "rate" in cmnd:
                self.IncreDecre = "speech rate"
                self.speechRate(self.engine.getProperty('rate') - 20)

            elif "brightness" in cmnd:
                self.IncreDecre = "brightness"
                quickaccess("brightness","left")

            else:
                self.getResponse(self.prevcmnd + self.IncreDecre)
                return

            self.speak(self.IncreDecre + " decreased..!!")

        elif "speech rate" in cmnd:
            self.speak(f"Current speech rate is : {self.engine.getProperty('rate')}")

        elif "desktop" in cmnd or "home" in cmnd:
            p.hotkey("win","d")
            self.speak("Here you go..!!")

        elif "learn" in cmnd or "new language" in cmnd:
            self.speak("Which learning platform you want me to open, 'code with harry' or 'w3school' ? ")
            cmnd = self.take_cmnd()
            if "harry" in cmnd:
                self.getResponse("open harry channel")
            elif "school" in cmnd:
                self.getResponse("open w3school")
            else:
                self.getResponse(cmnd)
        
        elif "language code" in cmnd:
            pass
        
        elif "language" in cmnd:
            self.speak("I can self.speak almost all languages..!!")
            self.speak("Just say 'Change language to (one you want)'")

        elif "spell" in cmnd or "spelling" in cmnd:
            if "of" in cmnd:
                word = getNextword(cmnd,"of",self.botName)
            elif "spell" in cmnd:
                word = getNextword(cmnd,"spell","")
            if word=="":
                self.speak("What is the word sir?")
                word = self.take_cmnd()

            word = word.strip()
            clipboard.copy(word)
            spelling = []
            for i in word:
                spelling.append(i)
            
            self.speak("It is spell as...")
            self.speak(spelling)
            self.speak(word)
            self.speak("Copied the spelling of this word")

        elif "pronounce" in cmnd or "say" in cmnd:
            cmnd=removeWords(cmnd)
            self.speak(cmnd)
        
        elif "switch input" in cmnd:
            self.switchInputMethod()
        
        elif "refresh" in cmnd:
            p.hotkey('win','m')
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
            p.hotkey("alt","tab")
            self.speak("Done..!!")

        elif "windows" in cmnd:
            windows(cmnd)
        
        elif "thanks" in cmnd or "thank you" in cmnd :
            self.speak("It's my pleasure sir..!!")
            self.sleepmode()

        elif "nothing" in cmnd.split() or "no" in cmnd.split() or 'not' in cmnd.split() or "nope" in cmnd.split() or "sleep" in cmnd or  "break" in cmnd:
            self.speak('Okay...')
            self.speak("Let me know if you need something..!!")
            self.sleepmode()

        elif "how are you" in cmnd or "how you doing" in cmnd or "what's up" in cmnd:
            self.speak("I'm doing great, how about you sir?")
            cmnd=self.take_cmnd()
            if cmnd:
                if "not" in cmnd.split() or "sad" in cmnd or "bored" in cmnd:
                    self.getResponse("bored")

                elif "fine" in cmnd or "good" in cmnd or "perfect" in cmnd:
                    self.speak("Nice to hear that..!!")
                
                else:
                    self.getResponse(cmnd)
        
        elif "bored" in cmnd:
            self.speak("Ohh... let me help you!")
            activities()
        
        elif "zoom" in cmnd or "i can't see" in cmnd:
            if "out" in cmnd:
                say = "zoomed out..!!"
                ope = "-"
            else:
                say = "zoomed in..!!"
                ope = "+"
            for i in range(5):
                p.hotkey('ctrl',ope)
            self.speak(say)

        elif ("sound" in cmnd or "voice" in cmnd) and "record" in cmnd:
            self.speak("Starting your sound recorder program..!!")
            os.startfile(self.getPath("soundRecorder"))
            self.sleepmode()

        elif "screen recording" in cmnd:
            self.speak("Starting screen recording..!!")
            p.hotkey('win','alt','r')
            self.sleepmode()
        
        elif "clear" in cmnd:
            os.system('cls')
            self.speak("Cleared previous commands...")
            
        elif "date" in cmnd.split():
            now=datetime.now()
            date=now.strftime("%d of %B, %A")
            self.speak("Today's date is "+date)
        
        elif "news" in cmnd:
            self.speak("Getting you today's top 10 news...")
            url = 'https://www.bbc.com/news'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            headlines = soup.find('body').find_all('h3')
            
            for x in range(1,10):
                self.speak(headlines[x].text.strip())

        elif "how to" in cmnd:
            self.speak("Searching..!!")
            cmnd = removeWords(cmnd)
            try:
                cmnd = search_wikihow(cmnd,1)
                assert len(cmnd) == 1
                self.speak(cmnd[0].summary)
            except:
                self.speak("Oops, network error..!!")
            
        elif "battery" in cmnd:
            battery = psutil.sensors_battery()
            percentage = battery.percent
            self.speak(f"You have {percentage} percent battery left..!!")

        elif "timer" in cmnd.split():
            # if "seconds" in cmnd or "second" in cmnd:
            #     if "second" in cmnd.split():
            #         unit = 'second'
            #     else:
            #         unit = 'seconds'

            # elif "minutes" in cmnd or "minute" in cmnd:
            #     if "minute" in cmnd.split():
            #         unit = 'minute'
            #     else:    
            #         unit = 'minutes'

            # elif "hours" in cmnd:
            #     unit = 'hours'
            
            # else:
            #     self.speak("In order to set a timer, you have to say, 'set a timer for specific minutes,seconds or hours'")
            #     self.somethingelse = False

            # duration = int(getpreviousword(cmnd,unit))
            # # Timer.settimer(duration,unit)
            # self.speak(f"Timer set for {duration} {unit}..!!")
            # timerset = True
            # sleepmode()
            clock(1)

        elif "alarm" in cmnd:
            clock(2)
                    
        elif "stopwatch" in cmnd:
            self.speak("Opening your stop watch program..!!")
            os.startfile(self.getPath("stop_watch"))

        elif "maximize" in cmnd:
            p.hotkey("win","up")
            self.speak("Maximized..!!")

        elif "minimise" in cmnd:
            p.hotkey("win","m")
            self.speak("Minimized..!!")

        elif "full screen" in cmnd or "exit full screen" in cmnd:
            p.press('f11')
            self.speak("Done..!!")
        
        elif "switch window" in cmnd or "previous window" in cmnd:
            p.hotkey("alt","tab")

        elif "virtual desktop" in cmnd:
            p.hotkey("win","ctrl","d")
            self.speak("Virtual Desktop Created..!!")
        
        elif "mute" in cmnd:
            p.press("volumemute")
        
        elif "volume" in cmnd:
            if "lower" in cmnd or "low" in cmnd or "decrease" in cmnd or "down" in cmnd:
                volbtn='volumedown'
                volsay = "decreased..!!"

            elif "higher" in cmnd or "high" in cmnd or "increase" in cmnd or 'up' in cmnd:
                volbtn='volumeup'
                volsay = "increased..!!"

            else:
                return
            p.press(volbtn,presses=10)
            self.speak("Volume "+volsay)

        elif "hear" in cmnd:
            p.press("volumeup",presses=10)
            self.speak("Volume increased..!!")

        elif "wi-fi" in cmnd or "wifi" in cmnd:
            quickaccess("wifi","none")

        elif "bluetooth" in cmnd:
            quickaccess("bluetooth","none")

        elif "sorry" in cmnd:
            self.speak("Not a problem sir")
            self.sleepmode()

        elif "*" in cmnd:
            self.speak("Sorry, I cannot respond to inappropriate language..!!")

        elif "note" in cmnd.split() :  
            openPath("notepad")
            self.speak("You can make notes here...")

        elif "jokes" in cmnd or "joke" in cmnd:
            jokes=pyjokes.get_joke()
            self.speak(jokes)
            cmnd = self.take_cmnd()
            if "hahaha" in cmnd or "ha ha" in cmnd or "haha" in cmnd:
                self.speak("I know the joke was so lame, no need to laugh..!!")
            else :
                self.getResponse(cmnd)

        elif "open" in cmnd and "path" in cmnd:
            openPath("BotsPathFolder")

        elif "path" in cmnd:
            pathName = getNextword(cmnd,"of","")
            print(pathName)
            
            path = self.getPath(pathName)
            if path:
                clipboard.copy(path)
                p.hotkey('ctrl','v')
                self.speak("Copied the path sir..!!")
            else:
                self.speak("Can't find the specified path")

        elif "post" in cmnd and "instagram" in cmnd:
            self.speak("Posting new video on your anime page on instagram..!!")
            os.startfile("C:\\Users\\joshi\\Documents\\Programs\\Python\\AI_instapost\\InstaPost.py") 

        elif "mouse position" in cmnd or "cursor" in cmnd:
            self.speak("Getting your cursor position")
            time.sleep(2)
            data=p.position()
            self.speak(data)
            clipboard.copy(str(data))
            
        elif "temperature" in cmnd or "weather" in cmnd:
            self.speak("Let me check..!!")
            location = getNextword(cmnd,"in")
            if not location:
                location = getNextword(cmnd,"of")
                if not location:
                    location = "pune"
            wheatherData = get_weather_data(location)
            if wheatherData:
                if "temperature" in cmnd:
                    self.speak(f"Current temperature in {location} is {wheatherData[0]}")
                else:
                    wheatherData = wheatherData[1].replace(".",",")
                    self.speak(f"Its {wheatherData} in {location}")

        elif "search" in cmnd or "find" in cmnd:
            cmnd = removeWords(cmnd)
            if cmnd==' ':
                self.speak("What do you want me to search sir?")
                cmnd=self.take_cmnd()
                if 'cancel' in cmnd or "don't search" in cmnd:
                    return
            self.speak("Searching...")
            search(cmnd)
            self.speak("Here are the results I got sir..!!")  
        
        elif "update" in cmnd or "reboot" in cmnd:
            reboot()
        
        elif "reminder" in cmnd:
            self.speak("Here are your reminders : ")
            reminders = self.getData("reminders")
            for r in reminders:
                self.speak(f"{r} : {reminders[r]}")

        elif "routine" in cmnd:
            self.speak("Here are your routines : ")
            routines = self.getData("routines")
            for r in routines:
                self.speak(f"{r} : {routines[r]}")

        elif "songs" in cmnd:
            self.speak("Playing songs for you...")
            playSongs()

        elif "game" in cmnd or "play" in cmnd:
            game = None
            games = self.getPath("games").keys()
            for g in games:
                if g in cmnd:
                    game = g
                    break
            
            playGames(game)

        elif "greet" in cmnd or "morn" in cmnd or "even" in cmnd or "after" in cmnd:
            greet = self.greetings()
            self.speak(greet+" sir")
            self.speak("Let me know if you need something")
            self.somethingelse = False

        elif "module" in cmnd:
            if "uninstall" in cmnd:
                cmndline('uninstall')        
            
            else:
                cmndline('install')

        elif "command line" in cmnd or "cmd" in cmnd:
            self.speak("Opening CMD")
            cmndline('none')
    
        
        elif "browser" in cmnd:
            self.speak("Opening Browser")
            p.hotkey("win","2")
            self.sleepmode()

        elif "code" in cmnd:
            #vspath="C:\\Users\\joshi\\AppData\\Local\\Programs\\Microsoft VS Code\\Code"
            #os.startfile(vspath)
            p.hotkey('win','3')
            self.speak("Here you go..!!")
            self.speak("Have a great coding sir..!!")
            self.sleepmode()

        elif "bin" in cmnd:
            self.speak("Opening recycle bin..!!")
            p.hotkey("ctrl","alt","0")
            self.sleepmode()

        elif "your settings" in cmnd:
            self.speak("Here's my settings")
            os.startfile(self.getPath("data file"))

        elif "settings" in cmnd:
            p.hotkey("win","i")
            self.speak("Here you go..")
        
        elif "task manager" in cmnd:
            p.hotkey("ctrl","shift","esc")

        elif "notifications" in cmnd.split() or "notification" in cmnd.split():
            p.hotkey("win","n")
            self.speak("Here are your notifications..!!")

        elif "files" in cmnd:
            p.hotkey("win","e")    
            self.speak("Here are your files")
            
        elif "calendar" in cmnd:
            self.speak("Opening Calendar")
            search('calendar')
            p.press("enter")

        elif "self" in cmnd:
            search("microsoft self")
            p.press("enter")
            self.speak("Here is your microsoft self")
            self.sleepmode()

        elif "snip" in cmnd:
            p.hotkey("win","shift",'s')
            self.speak("Here you go")
            
        elif "camera" in cmnd:
            camera("on")
            
        elif "selfie" in cmnd or "pic" in cmnd:
            camera("takepic")

        elif "capture" in cmnd or "video" in cmnd:
            pass
            # # import cv2
            # import numpy as np

            # cap = cv2.VideoCapture(0)

            # fourcc = cv2.VideoWriter_fourcc(*'XVID')
            # out = cv2.VideoWriter('screen_recording.avi', fourcc, 20.0, (640, 480))
            # while True:
            #     ret, frame = cap.read()
            #     out.write(frame)
            #     cv2.imshow("Screen Recording", frame)
                
            #     if cv2.waitKey(1) & 0xFF == ord('q'):
            #         break

            # out.release()
            # cv2.destroyAllWindows()

        elif "desktop" in cmnd or "home" in cmnd:
            p.hotkey("win","d")
            self.speak("Here you go..!!")

        
        elif "can you do" in cmnd or "task" in cmnd or "commands" in cmnd:
            taskfolder = self.getPath("tasksfolder")
            os.startfile(taskfolder)
            self.speak("Here are the tasks i can handle for you sir..!!")
            self.sleepmode()

        elif "netflix" in cmnd or "movie" in cmnd:
            if "offline" in cmnd or self.internet_connection()==0:
                openPath("movies folder")
                self.speak("Here are your movies...")
            else:
                openPath("netflix")
                self.speak("Have a great watching sir..!!")
            self.sleepmode()

        elif "open" in cmnd or 'start' in cmnd:
            application = removeWords(cmnd)
            success = openPath(application)
            if success:
                self.sleepmode()
            else:
                webbrowser.open(f"https://www.{application}.com/")

        elif "close" in cmnd:
            p.hotkey("alt","f4")
            self.speak("At once..")


        elif "stop" in cmnd or "pause" in cmnd:
            p.press("space")
            self.speak("Done..!!")

        elif "screenshot" in cmnd:
            p.hotkey("win",'printscreen')
            self.speak("Screenshot saved successfully..!!")
    
        elif "time" in cmnd.split() or "timing" in cmnd:
            self.speak("Current time is "+ gettime())

        elif "hey" in cmnd or "hello" in cmnd or 'hi' in cmnd.split() or "wake" in cmnd or self.botName in cmnd:
            words = ["What's the command sir?","How can I help you sir?","Yo Yo what's up"]
            self.speak(random.choice(words))
            self.somethingelse = False

        else:
            # cmnd = cmnd.replace(self.botName,"")
            # result = getresults(cmnd)
            # self.speak(result)
            self.speak("Sorry, I have no action stored for this command")
            self.speak("I am still in progress..!!")

    
    def getData(self, outerObj, innerObj=None):
        with open (self.datafile,"r") as f:
            data = json.load(f)
            f.close()
            if innerObj:
                return data[outerObj][innerObj]
            else:
                return data[outerObj]

    def putData(self, object, val):
        with open (self.datafile,"r") as f:
            data = json.load(f)
            f.close()
        data[object] = val
        with open (self.datafile,"w") as f:
            json.dump(data,f,indent=4)

    def speechRate(self, rate=None):
        self.engine.setProperty('rate',rate)
        self.putData("speech_rate",rate)

    def change_voice(self, val):
        voices = self.engine.getProperty('voices')
        self.putData("voice",val)
        self.engine.setProperty('voice', voices[val].id)

    def switchInputMethod(self):
        if self.input_method == "keyboard":
            self.speak("Switching input method to 'mic'")
            self.putData("input_method","mic")
            self.input_method="mic"
        else:
            self.speak("Switching input method to 'Keyboard'")
            self.putData("input_method","keyboard")
            self.input_method="keyboard"

    def getPath(self, pathName, splitWords = True):
        pathfile = "C:\\Users\\joshi\\Documents\\Programs\\Python\\Jarvis\\path.json"
        with open (pathfile,"r") as f:
            data = json.load(f)
            f.close()

            for key in data.keys():
                if pathName in key.split():
                    return data[key]
                try:
                    values = data[key]
                    for subkey in values.keys():
                        if pathName in subkey.split():
                            return values[subkey]
                except:
                    pass
            
            if not splitWords:
                return None
            
            for word in pathName.split():
                path = self.getPath(word,False)
                if path:
                    return path
            
            return None

    def greetings(self):
        now=datetime.now()
        hour=int(now.strftime("%H"))
        if hour>=0 and hour<12:
            return "Good Morning"
        elif hour>=12 and hour<18:
            return "Good Afternoon"
        else:
            return "Good Evening"

    def internet_connection(self):
        url = "https://www.google.com"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return 1
            else:
                return 0 
        except requests.exceptions.RequestException:
            return 0

    def playSound(self, path):
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.quit()

if __name__ == "__main__":
    Bot = Assistance().start()
