# RFID Hardware Configuration

This document outlines the wiring diagram and pin configuration required to interface the ESP32 microcontroller with the RC522 RFID reader/writer module for animal tag verification.

## Wiring Diagram (ESP32 to RC522)

| RC522 Pin | ESP32 Pin | Connection Type | Description |
|-----------|-----------|-----------------|-------------|
| 3.3V      | 3.3V      | Power           | 3.3V Power Supply (DO NOT connect to 5V) |
| RST       | GPIO 22   | Digital Out     | Reset Pin |
| GND       | GND       | Ground          | Common Ground |
| IRQ       | N/C       | -               | Not Connected |
| MISO      | GPIO 19   | SPI MISO        | Master Input Slave Output |
| MOSI      | GPIO 23   | SPI MOSI        | Master Output Slave Input |
| SCK       | GPIO 18   | SPI SCK         | SPI Clock |
| SDA (SS)  | GPIO 21   | SPI SS (CS)     | Slave Select / Chip Select |

## Required Arduino IDE Libraries

To compile the firmware, make sure to install the following libraries via the Arduino Library Manager:

1. **MFRC522** by GithubCommunity (v1.4.10 or later)
2. **ArduinoJson** by Benoit Blanchon (v6.x or later)

## Tag Formatting Specifications

Livestock identification tags utilize ISO 11784/11785 standard RFID tags. Ensure that the reader reads the standard MIFARE 1KB S50 cards/fobs programmed with a unique 12-digit animal ID.
