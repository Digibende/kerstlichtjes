#import pyaudio
import wave
import audioop
from flask import Flask, current_app
from flask_cors import CORS, cross_origin
import time

from neopixel import *

# LED strip configuration:
LED_COUNT      = 300      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


app = Flask(__name__)
CORS(app)

audiomode = False

@app.route("/")
def root():
    #global audiomode
    #audiomode = not audiomode
    #return "Hello World!" + str(audiomode)
    return current_app.send_static_file('index.html')

@app.route("/color/<hexcolor>")
def color(hexcolor):
    print(hexcolor)
    rgbcolor = hex_to_rgb(hexcolor)
    print(rgbcolor)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(*rgb_to_grb(rgbcolor)))
    strip.show()
    return hexcolor

def rgb_to_grb(value):
    return (value[1], value[0], value[2])

def hex_to_rgb(value):
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

'''
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
'''

if __name__ == "__main__":
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()
    app.run(host='0.0.0.0', port=80, debug=True)