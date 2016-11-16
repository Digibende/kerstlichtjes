from flask import Flask, render_template
from flask_cors import CORS, cross_origin
from flask_bootstrap import Bootstrap
import socket
import subprocess

from neopixel import *


# LED strip configuration:
LED_COUNT      = 600      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


global audio_process
global audio_running
audio_running = False

app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
CORS(app)


@app.route("/manage")
def manage():
    ip_addresses = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1]
    return render_template('manage.html', ip_addresses=ip_addresses)


@app.route("/")
def colorpicker():
    return render_template('colorpicker.html')


@app.route("/audio")
def audio():
    global audio_process
    global audio_running
    if 'audio_process' in globals():
        audio_process.kill()
    audio_process = subprocess.Popen(["python","/home/pi/hue-clone/scripts/audio.py"])
    audio_running = True
    return "started audio"


@app.route("/killaudio")
def killaudio():
    global audio_process
    global audio_running
    audio_process.kill()
    audio_running = False
    return "killed audio"

@app.route("/color/<hexcolor>")
def color(hexcolor):
    global audio_running
    print(hexcolor)
    rgbcolor = hex_to_rgb(hexcolor)
    print(rgbcolor)
    if not audio_running:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(*rgb_to_grb(rgbcolor)))
        strip.show()
    return hexcolor


def rgb_to_grb(value):
    return (value[1], value[0], value[2])


def hex_to_rgb(value):
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


if __name__ == "__main__":
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()
    app.run(host='0.0.0.0', port=80, debug=True)