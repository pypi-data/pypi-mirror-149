import sounddevice as sd
import soundfile as sf
import librosa

def play(file,fs):
    data,_=sf.read(file)
    sd.play(data,fs)

def stop():
    sd.stop()

def record(file,senconds,fs,ch,msg):
    myrecording = sd.rec(int(senconds * fs), samplerate=fs, channels=ch)
    if msg==True:
        print('Start recording!')
    sd.wait()
    sf.write(file, myrecording, fs, 'PCM_24')
    if msg==True:
        print(myrecording)
        print('End recording!')
    
def query_devices():
    return sd.query_devices()


def SaRa(f):
     y, sr = librosa.load(f, sr=None)
     t=int(len(y))/sr
     return (sr,t)
     
def resample_rate(path,new_sample_rate):
    signal, sr = librosa.load(path, sr=None)
    new_signal = librosa.resample(signal, sr, new_sample_rate)
    sf.write(path, new_signal , new_sample_rate ,'PCM_24')
