import parselmouth
import glob
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.io.wavfile as wav
from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank


sns.set() # Use seaborn's default style to make attractive graphs

def draw_spectrogram(spectrogram, dynamic_range=70):
    X, Y = spectrogram.x_grid(), spectrogram.y_grid()
    sg_db = 10 * np.log10(spectrogram.values)
    plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - dynamic_range, cmap='afmhot')
    plt.ylim([spectrogram.ymin, spectrogram.ymax])
    plt.xlabel("time [s]")
    plt.ylabel("frequency [Hz]")

def draw_intensity(intensity):
    plt.plot(intensity.xs(), intensity.values.T, linewidth=3, color='w')
    plt.plot(intensity.xs(), intensity.values.T, linewidth=1)
    plt.grid(False)
    plt.ylim(0)
    plt.ylabel("intensity [dB]")


def draw_pitch(pitch):
    pitch_values = pitch.selected_array['frequency']
    pitch_values[pitch_values==0] = np.nan

    return pitch_values


def analyse_sound(snd):
    sound = snd
    harmonicity = sound.to_harmonicity()
    return harmonicity.values[harmonicity.values != -200].mean()

def plot_intensity(snd):
    # Plot nice figures using Python's "standard" matplotlib library
    # plt.figure()
    # plt.plot(snd.xs(), snd.values.T)
    # plt.xlim([snd.xmin, snd.xmax])
    # plt.xlabel("time [s]")
    # plt.ylabel("amplitude")
    # plt.show()

    intensity = snd.to_intensity()
    # spectrogram = snd.to_spectrogram()
    # plt.figure()
    # draw_spectrogram(spectrogram)
    # plt.twinx()
    # draw_intensity(intensity)
    # plt.xlim([snd.xmin, snd.xmax])
    # plt.show() # or plt.savefig("spectrogram.pdf")
    return intensity.values

def get_pitch(snd):
    pitch = snd.to_pitch()
    # If desired, pre-emphasize the sound fragment before calculating the spectrogram
    # pre_emphasized_snd = snd.copy()
    # pre_emphasized_snd.pre_emphasize()
    # spectrogram = pre_emphasized_snd.to_spectrogram(window_length=0.03, maximum_frequency=8000)
    # plt.figure()
    # draw_spectrogram(spectrogram)
    # plt.twinx()
    pitch_values = draw_pitch(pitch)
    # plt.xlim([snd.xmin, snd.xmax])
    # plt.show() # or plt.savefig("spectrogram_0.03.pdf")
    return pitch_values


##sound filename here

# snd = parselmouth.Sound("aryan.wav")
# snd = parselmouth.Sound("aryan-2.wav")


# snd = parselmouth.Sound(sys.argv[1])
# snd.pre_emphasize()

def makemodel(name):
    i = 0
    a = np.array([])
    s1 = 0
    s2 = 0
    s3 = 0
    mfccs = []
    fbanks = []
    mfccds = []
    for wave_file in glob.glob(name + "*.wav"):
        print("Processing {}...".format(wave_file))
        snd = parselmouth.Sound(wave_file)
        snd.pre_emphasize()

        pv = get_pitch(snd)
        hv = analyse_sound(snd)
        iv = plot_intensity(snd)



        k1 = np.nanmean(pv)
        k2 = np.nanmean(iv)
        k3 = hv
        print (k1)
        i = i +1
        s1 = s1 + k1
        s2 = s2 + k2
        s3 = s3 + k3

        (rate,sig) = wav.read(wave_file)
        mfcc_feat = mfcc(sig,rate)
        d_mfcc_feat = delta(mfcc_feat, 2)
        fbank_feat = logfbank(sig,rate)
        print(fbank_feat[1:3,:])
        mfccs.append(mfcc_feat)
        fbanks.append(fbank_feat)
        mfccds.append(d_mfcc_feat)

    print ("average pitch is " + str(s1/i))
    # print ("average pitch is " + str(np.nanmean(a)))
    print ("average intensity is " + str(s2/i))
    print ("average harmonicity is " + str(s3/i))

    # name = sys.argv[1]

    model = name + ":" + str(s1/i) +":" + str(s2/i) + ":" + str(s3/i)
    modeldata = ":##"+' '.join([str(elem) for elem in mfccs])+ "##" +' '.join([str(elem) for elem in fbanks]) + "##" +' '.join([str(elem) for elem in mfccds]) 

    filename = name+"-model.txt"
    file1 = open(filename,"w") 
    file1.write(model) 
    file1.write(modeldata)
    file1.close()
