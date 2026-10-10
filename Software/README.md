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
| LED-Strip WS2812 (4x) | Data    | GPIO5 (D3)         |
| LED-Strip WS2812 (4x) | +5V     | 5V                 |
| LED-Strip WS2812 (4x) | GND     | GND                |

Die Taster werden intern per Software-Pullup (`Pin.PULL_UP`) auf High gezogen, ein Taster-Kontakt liegt jeweils gegen GND. Ein gedrückter Taster liest also `0` (Low). Es sind keine externen Pullup-Widerstände nötig. Der Buzzer ist **passiv** und wird per PWM angesteuert (nicht direkt an 3V3/GND anschließen). Der WS2812-Strip wird über die 5V-Schiene versorgt, die Datenleitung läuft über GPIO5 und wird per `neopixel`-Modul (Software-Protokoll über RMT) angesteuert.

## Funktionsweise

Beim Start zeigt das OLED-Display den Text "Hello World" an (zweizeilig, vergrößerte Schrift).

Wird einer der vier Taster gedrückt:

- gibt der passive Buzzer einen Ton in einer der Noten C4, D4, E4 oder F4 aus (262 Hz / 294 Hz / 330 Hz / 349 Hz),
- zeigt das OLED-Display groß die zugehörige Zahl (1, 2, 3 oder 4) an,
- leuchten auf dem WS2812-Strip entsprechend viele LEDs (1, 2, 3 bzw. 4) in einer festen Farbe bei 30% Helligkeit:

  | Taster | Anzahl LEDs | Farbe |
  |--------|-------------|-------|
  | 1      | 1           | Blau  |
  | 2      | 2           | Grün  |
  | 3      | 3           | Rot   |
  | 4      | 4           | Weiß  |

Sobald der Taster losgelassen wird, verstummt der Ton, das Display zeigt wieder "Hello World" an und die LEDs erlöschen. Eine einfache Flankenerkennung mit kurzer Wartezeit dient als Entprellung der Taster.

### Dateien

| Datei         | Beschreibung                                                        |
|---------------|----------------------------------------------------------------------|
| `main.py`     | Hauptprogramm (wird von MicroPython beim Boot automatisch gestartet) |
| `ssd1306.py`  | Treiber für das SSD1306-OLED-Display (I2C/SPI)                       |

## Badge flashen (Code übertragen)

Die Übertragung aus VS Code auf das Board erfolgt mit [`mpremote`](https://docs.micropython.org/en/latest/reference/mpremote.html). MicroPython muss bereits auf dem ESP32-C3 geflasht sein.

### python installieren

```
winget install -e --id Python.Python.3.13 --source winget --accept-package-agreements --accept-source-agreements
```

-e (exact) stellt sicher, dass winget das richtige Python-Paket herunterlädt und nicht irgendein anderes, das mit „python“ übereinstimmt.
Dadurch werden Python (und pip) automatisch zum PATH hinzugefügt, danach am besten am rechner ab- und wieder anmelden, damit der aktualiserte PATH übernommen wird

Überprüfung mit:

```
python --version
```

### mpremote installieren

```
python -m pip install --user mpremote
```

### Verbundene Boards anzeigen

```
mpremote connect list
```

### Dateien auf das Board kopieren

Passe `COMx` an den tatsächlichen COM-Port des Boards an (siehe `mpremote connect list` bzw. Geräte-Manager):

```
mpremote connect COMx cp ssd1306.py :
mpremote connect COMx cp main.py :
mpremote connect COMx reset
```

Nach dem Reset startet das Board automatisch `main.py`.

### Live-Ausgabe / REPL

Um die Ausgabe des Boards direkt zu sehen oder eine interaktive REPL zu öffnen:

```
mpremote connect COMx
```

Mit `Strg+]` bzw. `Strg+C` wird die Verbindung/das laufende Programm beendet.
