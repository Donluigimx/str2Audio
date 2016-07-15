import pyaudio
import numpy as np
import wave
from subprocess import Popen
import sys

class Recorder(object):
    '''A recorder class for recording audio to a WAV file.
    Records in mono by default.
    '''

    def __init__(self, channels=1, rate=44100, frames_per_buffer=1024):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

    def open(self, fname, mode='wb'):
        return RecordingFile(fname, mode, self.channels, self.rate,
                            self.frames_per_buffer)

class RecordingFile(object):
    def __init__(self, fname, mode, channels,
                rate, frames_per_buffer):
        self.fname = fname
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self._pa = pyaudio.PyAudio()
        self.wavefile = self._prepare_file(self.fname, self.mode)
        self._stream = None

    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        pass
        #self.close()

    def record(self, duration):
        # Use a stream with no callback function in blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer)
        for _ in range(int(self.rate / self.frames_per_buffer * duration)):
            audio = self._stream.read(self.frames_per_buffer)
            self.wavefile.writeframes(audio)
        return None

    def start_recording(self):
        # Use a stream with a callback in non-blocking mode
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer,
                                        stream_callback=self.get_callback())
        self._stream.start_stream()
        return self

    def stop_recording(self):
        self._stream.stop_stream()
        return self

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            return in_data, pyaudio.paContinue
        return callback


    def close(self):
        self._stream.close()
        self._pa.terminate()
        self.wavefile.close()

    def _prepare_file(self, fname, mode='wb'):
        wavefile = wave.open(fname, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(self.rate)
        return wavefile

class Note:
    'Musical note frequency'
    def __init__(self, Name, Freq, mult = 1):
        Freq = Freq * mult
        Sum = 2 * mult
        self.NoteName = Name
        self.LowFreq = Freq - Sum
        self.HighFreq = Freq + Sum
        self.RealFreq = Freq

Tones = [
            Note('Do4', 261.625565),
            Note('Do#4', 277.182631),
            Note('Re4', 293.664768),
            Note('Re#4', 311.126984),
            Note('Mi4', 329.627557),
            Note('Fa4', 349.228231),
            Note('Fa#4', 369.994423),
            Note('Sol4', 391.995436),
            Note('Sol#4', 415.304698),
            Note('La4', 440.000000),
            Note('La#4', 466.163762),
            Note('Si4', 493.883301),
            Note('Do5', 261.625565,2),
            Note('Do#5', 277.182631,2),
            Note('Re5', 293.664768,2),
            Note('Re#5', 311.126984,2),
            Note('Mi5', 329.627557,2),
            Note('Fa5', 349.228231,2),
            Note('Fa#5', 369.994423,2),
            Note('Sol5', 391.995436,2),
            Note('Sol#5', 415.304698,2),
            Note('La5', 440.000000,2),
            Note('La#5', 466.163762,2),
            Note('Si5', 493.883301,2),
            Note('Do6', 261.625565,4),
            Note('Do#6', 277.182631,4),
            Note('Re6', 293.664768,4),
            Note('Re56', 311.126984,4),
            Note('Mi6', 329.627557,4),
            Note('Fa6', 349.228231,4),
            Note('Fa#6', 369.994423,4),
            Note('Sol6', 391.995436,4),
            Note('Sol#6', 415.304698,4),
            Note('La6', 440.000000,4),
            Note('La#6', 466.163762,4),
            Note('Si6', 493.883301,4),
            Note('Do7', 261.625565,8),
            Note('Do#7', 277.182631,8),
            Note('Re7', 293.664768,8),
            Note('Re#7', 311.126984,8),
            Note('Mi7', 329.627557,8),
            Note('Fa7', 349.228231,8),
            Note('Fa#7', 369.994423,8),
            Note('Sol7', 391.995436,8),
            Note('Sol#7', 415.304698,8),
            Note('La7', 440.000000,8),
            Note('La#7', 466.163762,8),
            Note('Si7', 493.883301,8),
            Note('Do8', 261.625565,16),
            Note('Do#8', 277.182631,16),
            Note('Re8', 293.664768,16),
            Note('Re#8', 311.126984,16),
            Note('Mi8', 329.627557,16),
            Note('Fa8', 349.228231,16),
            Note('Fa#8', 369.994423,16),
            Note('Sol8', 391.995436,16),
            Note('Sol#8', 415.304698,16),
            Note('La8', 440.000000,16),
            Note('La#8', 466.163762,16),
            Note('Si8', 493.883301,16),
            Note('Do9', 261.625565,32),
            Note('Do#9', 277.182631,32),
            Note('Re9', 293.664768,32),
            Note('Re#9', 311.126984,32),
            Note('Mi9', 329.627557,32),
            Note('Fa9', 349.228231,32),
            Note('Fa#9', 369.994423,32),
            Note('Sol9', 391.995436,32),
            Note('Sol#4', 415.304698,32),
            Note('La9', 440.000000,32),
            Note('La#9', 466.163762,32),
            Note('Si9', 493.883301,32)
        ]

def binaryNoteSearch( Freq, List ):
    max = len(List) - 1
    min = 0
    while min <= max:
        mid = int((max+min)/2)
        note = List[mid]
        if Freq < note.RealFreq:
            if Freq > note.LowFreq:
                return mid
            else:
                max = mid - 1
            pass
        elif Freq > note.RealFreq:
            if Freq < note.HighFreq:
                return mid
            else:
                min = mid + 1
        else:
            return mid
    return -1

def getHz( swidth, window, RATE, data ):
    indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),\
                                             data))*window
    fftData=abs(np.fft.rfft(indata))**2
    which = fftData[1:].argmax() + 1
    if which != len(fftData)-1:
        if fftData[0] > 0:
            y0,y1,y2 = np.log(fftData[which-1:which+2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            thefreq = (which+x1)*RATE/chunk
        else:
            return -1
    else:
        thefreq = which*RATE/chunk
    return thefreq

def getScale( pos, List):
    NewList = [
                List[pos],#Tone
                List[pos+2],#Whole
                List[pos+4],#Whole
                List[pos+5],#Half
                List[pos+7],#Whole
                List[pos+9],#Whole
                List[pos+11],#Whole
                List[pos+12],#Half
                List[pos+14],#Whole
                List[pos+16],#Whole
                List[pos+17],#Half
                List[pos+19],#Whole
                List[pos+21],#Whole
                List[pos+23],#Whole
                List[pos+24],#Half
                List[pos+26],#Whole
                List[pos+28]#Whole
              ]
    return NewList

def getString( List ):
    secondRound = False
    string = ''
    if len(List) % 2 != 0:
        return 'ERROR'

    for value in List:
        if secondRound == False:
            av = value << 4
            secondRound = True
        else:
            av += value
            string += str(unichr(av).encode('latin-1', 'replace'))
            secondRound = False
    return string

chunk = 2048
def main():
    if len(sys.argv) > 1:
        wf = wave.open(sys.argv[1],'rb')
        firstTone = False
    else:
        inp = raw_input('Press enter to start record')
        while inp:
            inp = raw_input('Press enter to start record')
        rec = Recorder(channels = 1)
        with rec.open('Test.wav','wb') as recfile:
            recfile.start_recording()
            print 'Start recording...'
            inp = raw_input('Press enter to stop')
            while inp:
                inp = raw_input('Press enter to stop')
        recfile.stop_recording()
        wf = wave.open('Test.wav', 'rb')
        firstTone = True
        ScaleList = getScale(0, Tones)
        curPos = 0
    swidth = wf.getsampwidth()
    RATE = wf.getframerate()
    window = np.blackman(chunk)
    p = pyaudio.PyAudio()
    stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = RATE,
                output = True)

    data = wf.readframes(chunk)
    values = []
    while len(data) == chunk*swidth:
        stream.write(data)
        if ( firstTone == False):
            thefreq = getHz( swidth, window, RATE, data )
            posTone = binaryNoteSearch(thefreq, Tones)
            if posTone != -1:
                ScaleList = getScale( posTone, Tones )
                firstTone = True
                curPos = 0
                print "The freq is %f Hz. Note: %s" % ( round(thefreq), Tones[posTone].NoteName )
        else:
            thefreq = getHz( swidth, window, RATE, data )
            if( thefreq > ScaleList[curPos].HighFreq or ScaleList[curPos].LowFreq > thefreq ):
                posTone = binaryNoteSearch(thefreq, ScaleList)
                if posTone != -1:
                    if posTone != 16:
                        values.append(posTone)
                    if len(values) == 2:
                        Text = getString(values)
                        sys.stdout.write(Text)
                        values = []
                        sys.stdout.flush()
                    curPos = posTone;
        data = wf.readframes(chunk)

    Text = getString(values)
    print Text
    p.terminate()

if __name__ == '__main__':
    main()
