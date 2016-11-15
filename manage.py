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
    audio_process = subprocess.Popen(["python","scripts/audio.py"])
    return "started audio"


@app.route("/audiokill")
def audiokill():
    global audio_process
    audio_process.kill()
    return "killed audio"


if __name__ == "__main__":
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    strip.begin()
    app.run(host='0.0.0.0', port=80, debug=True)