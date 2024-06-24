import RPi.GPIO as GPIO
import time
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   5 :  {'name' : 'PIN 5 BCM', 'state' : GPIO.LOW},
   6 :  {'name' : 'PIN 6 BCM', 'state' : GPIO.LOW},
   12 : {'name' : 'PIN 12 BCM', 'state' : GPIO.LOW},
   13 : {'name' : 'PIN 13 BCM', 'state' : GPIO.LOW},
   16 : {'name' : 'PIN 16 BCM', 'state' : GPIO.LOW},
   17 : {'name' : 'PIN 17 BCM', 'state' : GPIO.LOW},
   19 : {'name' : 'PIN 19 BCM', 'state' : GPIO.LOW},
   20 : {'name' : 'PIN 20 BCM', 'state' : GPIO.LOW},
   21 : {'name' : 'PIN 21 BCM', 'state' : GPIO.LOW},
   22 : {'name' : 'PIN 22 BCM', 'state' : GPIO.LOW},
   23 : {'name' : 'PIN 23 BCM', 'state' : GPIO.LOW},
   24 : {'name' : 'PIN 24 BCM', 'state' : GPIO.LOW},
   25 : {'name' : 'PIN 25 BCM', 'state' : GPIO.LOW},
   26 : {'name' : 'PIN 26 BCM', 'state' : GPIO.LOW},
   27 : {'name' : 'PIN 27 BCM', 'state' : GPIO.LOW}
   }

# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

@main.route('/')
@login_required
#def index():
#return render_template('index.html')
def index():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : pins
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('index.html', **templateData)


#@main.route('/profile')
#@login_required
#def profile():
#    return render_template('profile.html', name=current_user.name)
@main.route("/<changePin>/<action>")
@login_required
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."
   if action == "trigger":
      GPIO.output(changePin, GPIO.HIGH)
      message = "Turned " + deviceName + " on."
      time.sleep(2)
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins
   }

   return render_template('index.html', **templateData)