# ESP32 Car WiFi CUCSUR

Remote controlled car via WiFi with an ESP32 using MicroPython.

## Installation

1. Install [MicroPython](https://micropython.org/download/ESP32_GENERIC/) on your ESP32 using [esptool] (https://docs.espressif.com/projects/esptool/en/latest/esp32/) (You need to have [Python](https://www.python.org/) installed) or [Thonny IDE](https://thonny.org/). 

   With esptool:
  
   Erase the entire flash using:
   ```bash
   esptool.py --chip esp32 --port COM5 erase_flash
   ```
   Program the firmware starting at address 0x1000:
   ```bash
   esptool.py --chip esp32 --port COM5--baud 460800 write_flash -z 0x1000 ESP32_GENERIC-20230426-v1.20.0.bin
   ```
2. Using the [ampy](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy) module  or Thonny IDE, upload the main.py to the ESP32 microcontroller.

   With ampy:
   ```bash
    ampy --port COM5 put main.py
   ```


## Usage
1. Install the apk "Carro ESP32".
2. Connect to the ESP32 Car Wifi network.
3. Have fun!


## License

[MIT](https://choosealicense.com/licenses/mit/)
