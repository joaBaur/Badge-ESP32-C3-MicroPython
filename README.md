# Badge-ESP32-C3-MicroPython

Badge mit ESP32-C3 Super Mini Breakout, OLED 128x64 I2C, 4x Taster und Piezo-Buzzer, programmiert in MicroPython.

## Hardware

Basis-Board: [ESP32-C3 Super Mini](https://prilchen.de/belegungsplan-esp32-c3-supermini/)

| Komponente         | Signal    | ESP32-C3 Pin      |
|---------------------|-----------|--------------------|
| OLED 128x64 (I2C)   | SDA       | GPIO6 (D4)         |
| OLED 128x64 (I2C)   | SCL       | GPIO7 (D5)         |
| OLED 128x64 (I2C)   | VCC       | 3V3                |
| OLED 128x64 (I2C)   | GND       | GND                |
| Taster 1            | Schalter  | GPIO1 (gegen GND)  |
| Taster 2            | Schalter  | GPIO2 (gegen GND)  |
| Taster 3            | Schalter  | GPIO3 (gegen GND)  |
| Taster 4            | Schalter  | GPIO4 (gegen GND)  |
| Piezo-Buzzer (passiv) | Signal  | GPIO0              |
| Piezo-Buzzer (passiv) | GND     | GND                |

Die Taster werden intern per Software-Pullup (`Pin.PULL_UP`) auf High gezogen, ein Taster-Kontakt liegt jeweils gegen GND. Ein gedrückter Taster liest also `0` (Low). Es sind keine externen Pullup-Widerstände nötig. Der Buzzer ist **passiv** und wird per PWM angesteuert (nicht direkt an 3V3/GND anschließen).

## Funktionsweise

Beim Start zeigt das OLED-Display den Text "Hello World" an (zweizeilig, vergrößerte Schrift).

Wird einer der vier Taster gedrückt:

- gibt der passive Buzzer einen Ton in einer der Noten C4, D4, E4 oder F4 aus (262 Hz / 294 Hz / 330 Hz / 349 Hz),
- zeigt das OLED-Display groß die zugehörige Zahl (1, 2, 3 oder 4) an.

Sobald der Taster losgelassen wird, verstummt der Ton und das Display zeigt wieder "Hello World" an. Eine einfache Flankenerkennung mit kurzer Wartezeit dient als Entprellung der Taster.

### Dateien

| Datei         | Beschreibung                                                        |
|---------------|----------------------------------------------------------------------|
| `main.py`     | Hauptprogramm (wird von MicroPython beim Boot automatisch gestartet) |
| `ssd1306.py`  | Treiber für das SSD1306-OLED-Display (I2C/SPI)                       |

## Badge flashen (Code übertragen)

Die Übertragung erfolgt mit [`mpremote`](https://docs.micropython.org/en/latest/reference/mpremote.html). MicroPython muss bereits auf dem ESP32-C3 geflasht sein.

### mpremote installieren

```
python -m pip install --user mpremote
```

### Verbundene Boards anzeigen

```
mpremote connect list
```

### Dateien auf das Board kopieren

Passe `COM5` an den tatsächlichen COM-Port des Boards an (siehe `mpremote connect list` bzw. Geräte-Manager):

```
mpremote connect COM5 cp ssd1306.py :
mpremote connect COM5 cp main.py :
mpremote connect COM5 reset
```

Nach dem Reset startet das Board automatisch `main.py`.

### Live-Ausgabe / REPL

Um die Ausgabe des Boards direkt zu sehen oder eine interaktive REPL zu öffnen:

```
mpremote connect COM5
```

Mit `Strg+]` bzw. `Strg+C` wird die Verbindung/das laufende Programm beendet.
