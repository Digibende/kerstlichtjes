import pyaudio
import wave
import audioop
from flask import Flask, current_app
from flask_cors import CORS, cross_origin
import time

from neopixel import *
from random import randint

# LED strip configuration:
LED_COUNT      = 600      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
p = pyaudio.PyAudio()

print("loading pixels")
'''
while True:
    color = Color(randint(0,255),randint(0,255),randint(0,255))
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i,color)
    strip.show()
    time.sleep(.2)
'''

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK)
floor = 9999999
ceiling = 0
while True:
    data = stream.read(CHUNK, exception_on_overflow = False)
    rms = audioop.rms(data, 2)    # here's where you calculate the volume
    floor = min(floor, rms)
    #floor = 50
    ceiling = max(ceiling, rms)
    #ceiling = ceiling *.7
    #ceiling = 2000
    print(str(floor) + " "  + str(rms) + " " + str(ceiling))
    #0 - 599
    normal = rms - floor
    base = ceiling - floor
    if base <= 0:
        base = 1
    fraction = float(normal)/float(base)
    print(fraction)
    step = int(fraction * 599)
    print(str(step))
    #step = 600
    for i in range(0, step):
    #for i in range(0, strip.numPixels()):
    #   #print(i)
        strip.setPixelColor(i, Color(0,128,0))
    for i in range(step+1, strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,128))
    strip.show()
    #time.sleep(10)
stream.stop_stream()
stream.close()
p.terminate()
