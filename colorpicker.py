import pyaudio
import wave
import audioop
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

audiomode = False

@app.route("/")
def root():
    global audiomode
    audiomode = not audiomode
    return "Hello World!" + str(audiomode)

@app.route("/color/<color>")
def color(color):
    print(color)
    return color

def listen():
    global audiomode
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    while audiomode:
        data = stream.read(CHUNK)
        rms = audioop.rms(data, 2)    # here's where you calculate the volume
        print(rms)

    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)