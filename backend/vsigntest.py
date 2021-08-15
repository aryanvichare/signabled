import os
import sys
import speech_recognition as sr
import pyttsx3
import parselmouth
import glob
import numpy as np
from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank
import scipy.io.wavfile as wav

import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

def getKeyFromPassword(password_provided):
    # password_provided = "password" # This is input in the form of a string
    password = password_provided.encode() # Convert to type bytes
    salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once
    return key







eng = pyttsx3.init()
eng.say("please speak a command sentence")
eng.runAndWait()


os.system('sox -t waveaudio -d t1.wav trim 0 5')
os.system('sox t1.wav -r 16k t3.wav')
os.system('sox t3.wav  t4.wav remix 1-2')


AUDIO_FILE = "t4.wav"



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



##now identify user


def draw_pitch(pitch):
    pitch_values = pitch.selected_array['frequency']
    pitch_values[pitch_values==0] = np.nan
    return pitch_values


def analyse_sound(snd):
    sound = snd
    harmonicity = sound.to_harmonicity()
    return harmonicity.values[harmonicity.values != -200].mean()

def plot_intensity(snd):
 
    intensity = snd.to_intensity()
    return intensity.values

def get_pitch(snd):
    pitch = snd.to_pitch()
    pitch_values = draw_pitch(pitch)
    return pitch_values


##sound filename here

# snd = parselmouth.Sound(sys.argv[1])
# snd.pre_emphasize()

modelname1 = sys.argv[1]
modelname2 = sys.argv[2]
modelname3 = sys.argv[3]
# testfile = sys.argv[4]
testfile = AUDIO_FILE



f = open(modelname1, "r")
model1 =f.read()

f2 = open(modelname2, "r") 
model2 = f2.read() 
f2.close()

f3 = open(modelname3, "r") 
model3 = f3.read() 
f3.close()

f4 = open("passwords.txt", "r") 
model4 = f4.read() 
f4.close()

m = model4.split(':')
passwords = []
for p in m:
    passwords.append(p)



m1 = model1.split(':')
m2 = model2.split(':')
m3 = model3.split(':')
name1 = m1[0]
pitch1 = float(m1[1])
name2 = m2[0]
pitch2 = float(m2[1])
name3 = m3[0]
pitch3 = float(m3[1])

pitches = []
pitches.append(pitch1)
pitches.append(pitch2)
pitches.append(pitch3)
names = []
names.append(name1)
names.append(name2)
names.append(name3)

i = 0
a = np.array([])
s1 = 0
s2 = 0
s3 = 0


snd = parselmouth.Sound(testfile)
snd.pre_emphasize()

pv = get_pitch(snd)
hv = analyse_sound(snd)
iv = plot_intensity(snd)

k1 = np.nanmean(pv)
k2 = np.nanmean(iv)
k3 = hv
print (k1)


(rate,sig) = wav.read(testfile)
mfcc_feat = mfcc(sig,rate)
d_mfcc_feat = delta(mfcc_feat, 2)
fbank_feat = logfbank(sig,rate)
print(fbank_feat[1:3,:])

print ("pitch is " + str(k1))
print ("intensity is " + str(k2))
print ("harmonicity is " + str(k3))

select = min(range(len(pitches)), key=lambda i: abs(pitches[i]-k1))

print (names[select])
print (pitches[select])


flag = False
if passwords[select] in sentence:
    print (" the user " +names[select] + " has been identified ")
    eng.say(" the user " +names[select] + " has been identified ")
    eng.runAndWait()
    flag = True

if flag == True:
    if "record" in sentence:
        text = sentence.split("record",1)[1]
        key = getKeyFromPassword(passwords[select])
        f = Fernet(key)
        message = text.encode()
        encrypted = f.encrypt(message)
        with open("ciphertext.txt", 'wb') as f:
            f.write(encrypted)
        eng.say(" message recorded and encrypted ")
        eng.runAndWait()
        

    if "retrieve" in sentence:
        key = getKeyFromPassword(passwords[select])
        f = Fernet(key)
        with open("ciphertext.txt", 'rb') as f:
            data = f.read()

        message = fernet.decrypt(data)
        # message = text.decode()
        eng.say("the retrieved  message is  " + message)
        eng.runAndWait()







# if abs(pitch1-k1) < abs(pitch2-k1):
#     print (name1)
# else:
#     print(name2)



# model = str(s1/i) +":" + str(s2/i) + ":" + str(s3/i)





# filename = name+"-model.txt"
# file1 = open(filename,"w") 
# file1.write(model) 
# file1.close()






print()
