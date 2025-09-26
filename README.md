Portable Doorbell with Raspberry Pi Pico W

This is a small project for creating a portable doorbell using a Raspberry Pi Pico W and MicroPython. When the button is pressed, you receive a Telegram notification directly on your phone.


Firmware

I used MicroPython firmware for the Raspberry Pi Pico W. You can download it here:
https://micropython.org/download/RPI_PICO2_W/

Hardware Setup

Soldering:
Soldered the header pins to the Pico W board.

Circuit Wiring:

Connected a 10 kΩ resistor between 3V3 and GP0.

Connected the push button wires:

One wire to GND

The other to GP0 (the same pin as the resistor)

When the button is pressed, GP0 goes low, signaling the button press.

Note: Soldering the resistor is optional. Raspberry Pi Pico W with MicroPython can simulate the button state in software if needed.


Telegram Integration

Created a bot using BotFather on Telegram.

Used the bot’s API token to send messages.

Each button press triggers a Telegram message to the configured chat ID.


Requirements

Raspberry Pi Pico W

MicroPython firmware (latest version)

USB cable for flashing firmware

Push button and 10 kΩ resistor (optional)

Telegram Bot token from BotFather


