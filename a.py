import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia

listener = sr.Recognizer()
engine = pyttsx3.init()


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    global command
    try:
        with sr.Microphone() as source:
            print("Listening....")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if "sema" in command:
                command = command.replace("sema", "")
                print(command)
    except:
        print("error")
    return command



def run_sema():
    command = take_command()
    print(command)
    if "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        print(time)
        talk("Current time is" + time)
    elif "who is" in command:
        person = command.replace("what is", "")
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif "are you single" in command:
        talk("Yes i am single, do you want to take me out")
    else:
        talk("I did not understand your question, please say it again")


while True:
    run_sema()