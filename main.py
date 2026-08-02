from machine import Pin, I2C, PWM
import time
import framebuf
from ssd1306 import SSD1306_I2C

# --- Konfiguration ---------------------------------------------------------

OLED_WIDTH = 128
OLED_HEIGHT = 64
OLED_SDA_PIN = 6  # D4
OLED_SCL_PIN = 7  # D5

BUZZER_PIN = 0

# Taster -> (Pin, Ton, Anzeige-Text)
# Noten C4-F4 in Hz
BUTTONS = (
    {"pin": 1, "freq": 262, "label": "1"},  # C
    {"pin": 2, "freq": 294, "label": "2"},  # D
    {"pin": 3, "freq": 330, "label": "3"},  # E
    {"pin": 4, "freq": 349, "label": "4"},  # F
)

# --- Hardware initialisieren -------------------------------------------

i2c = I2C(0, sda=Pin(OLED_SDA_PIN), scl=Pin(OLED_SCL_PIN), freq=400_000)
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

buzzer = PWM(Pin(BUZZER_PIN))
buzzer.duty(0)

for button in BUTTONS:
    button["obj"] = Pin(button["pin"], Pin.IN, Pin.PULL_UP)
    button["was_pressed"] = False


def draw_text_scaled(text, x, y, scale=1, col=1):
    # Der eingebaute 8x8-Font von framebuf kennt keine Skalierung.
    # Deshalb wird der Text zunaechst in einen kleinen 1x-Puffer gerendert
    # und anschliessend Pixel fuer Pixel als (scale x scale)-Bloecke
    # auf das Display uebertragen.
    width = len(text) * 8
    height = 8
    buf = bytearray(width * (height // 8))
    tmp = framebuf.FrameBuffer(buf, width, height, framebuf.MONO_VLSB)
    tmp.text(text, 0, 0, 1)

    for yy in range(height):
        for xx in range(width):
            if tmp.pixel(xx, yy):
                if scale == 1:
                    oled.pixel(x + xx, y + yy, col)
                else:
                    oled.framebuf.fill_rect(x + xx * scale, y + yy * scale, scale, scale, col)


def show_hello_world():
    oled.fill(0)
    scale = 2
    draw_text_scaled("Hello", (OLED_WIDTH - len("Hello") * 8 * scale) // 2, 12, scale)
    draw_text_scaled("World", (OLED_WIDTH - len("World") * 8 * scale) // 2, 34, scale)
    oled.show()


def show_number(label):
    oled.fill(0)
    scale = 6
    draw_text_scaled(label, (OLED_WIDTH - 8 * scale) // 2, (OLED_HEIGHT - 8 * scale) // 2, scale)
    oled.show()


def play_tone(freq):
    buzzer.freq(freq)
    buzzer.duty(512)  # 50% Tastverhaeltnis


def stop_tone():
    buzzer.duty(0)


# --- Hauptprogramm -------------------------------------------------------

show_hello_world()
was_any_pressed = False

while True:
    any_pressed = False

    for button in BUTTONS:
        pressed = not button["obj"].value()  # Pull-up: gedrueckt = Low

        if pressed and not button["was_pressed"]:
            # Flanke erkannt: Taster wurde gerade gedrueckt
            play_tone(button["freq"])
            show_number(button["label"])
            time.sleep_ms(20)  # einfaches Entprellen

        if pressed:
            any_pressed = True

        button["was_pressed"] = pressed

    if not any_pressed:
        stop_tone()
        if was_any_pressed:
            show_hello_world()

    was_any_pressed = any_pressed
    time.sleep_ms(10)
