from BOT_Commands import *
import keyboard

def loop():
    while 1:
        if keyboard.is_pressed('`'):
            switchinput()

        if BOT.checkRoutine:
            routine()

        if store.somethingelse:
            store.validatecommand = False
            print()
            words=("Do you want any other help sir?",
                    "Anything else?",
                    "What else can i do for you?")
            speak(random.choice(words))

        cmnd = take_cmnd()
        if cmnd:
            command(cmnd)

def main():
    engine.setProperty('rate',BOT.speechRate)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[getdata("voice")].id) 

    noNetwork = 0
    if not internet_connection():
        noNetwork = True

    greet=greetings()

    os.system("cls")
    speak(greet+" sir, I am "+ BOT.botname)
    speak("Let me know if you need any help..!!")
    
    if noNetwork:
        networkError()
    
    # loop()
    try:
        loop()
    except Exception as e:
        speak("Looks like there was some error..!!")
        print(e)
        time.sleep(1)
        loop()

if __name__ == "__main__":
    main()
