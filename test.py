from uflask import uFlask, render_template, make_response
import machine
import time

app = uFlask()

@app.route('/')
def home():
    return make_response('home page')

@app.route('/on')
def on():
    LED_PIN = 2
    led = machine.Pin(LED_PIN, machine.Pin.OUT)
    led.value(0)
    return make_response('led on')

@app.route('/off')
def off():
    LED_PIN = 2
    led = machine.Pin(LED_PIN, machine.Pin.OUT)
    led.on()
    return make_response('led off')


app.run()
