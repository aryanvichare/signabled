import speech_recognition as sr




def getText(afile):
    
    r = sr.Recognizer()
    with sr.AudioFile(afile) as source:
        audio = r.record(source)

    sentence = ""

    try:
        sentence = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + sentence)
        # eng = pyttsx3.init()
        # eng.say("google A S R recognized the sentence as " + sentence )
        # eng.runAndWait()
        
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    return sentence


getText("aryan5.wav")