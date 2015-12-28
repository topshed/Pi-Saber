from adxl345 import ADXL345 # Accelerometer library
from time import sleep
from gpiozero import PWMLED, Button
import Image, ImageDraw, threading, random
from Adafruit_LED_Backpack import BicolorMatrix8x8
from signal import pause

display = BicolorMatrix8x8.BicolorMatrix8x8()
display.begin()
display.clear()
display.write_display() #set up LED Matrix

leds = PWMLED(17) # String of LEDS
button = Button(26)
adxl345 = ADXL345() # Accelerometer
running = False

def shwoom(): #PWMs LEDs based on movement
    global running
    while running:
        axes = adxl345.getAxes(True)
        val = abs(axes['x'])/2.2 # read from x-axis
        if val > 1:
            val =1
        leds.value = val
        sleep(0.2)

def jitter(): # Sparkle effect on LED Matrix
    global running
    cols = cols = [BicolorMatrix8x8.YELLOW,
                   BicolorMatrix8x8.GREEN,
                   BicolorMatrix8x8.RED]
    while running:
        c = random.choice(cols) # Chose a random colour
        x = random.randint(0,7) # Choose random pixel
        y = random.randint(0,7)
        display.set_pixel(x,y,c)
        display.write_display()

def pressed(): # Run when button pressed
    print('pressed')
    global running
    if running: # If Pisaber already active...
        running = False
        display.clear()
        display.write_display()
        leds.off()
    else: # If not, turn LEDs and matrix on
        running = True
        image = Image.new('RGB', (8, 8))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, 7, 7), outline=(255, 0, 0), fill=(255, 255, 0))
        draw.line((1, 1, 6, 6), fill=(0, 255, 0))
        draw.line((1, 6, 6, 1), fill=(0, 255, 0))
        display.set_image(image) # Starting image
        display.write_display()
        sleep(0.7)
        # Run functions as two seperate threads
        t1 = threading.Thread(target=shwoom)
        t1.start()
        t2 = threading.Thread(target=jitter)
        t2.start()

button.when_pressed = pressed # function to be run
pause() #Stops program from ending straight away
