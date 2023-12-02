# Screen Sync

## About
Screen Sync is a Python application designed to synchronize the colors of your computer screen with various smart light bulbs, including Tuya WiFi bulbs. It captures the dominant colors from your screen and sets your smart bulbs to match these colors in real-time, enhancing your entertainment and work environment with ambient lighting.


![Photo of ScreenSync in action](/screensync/assets/IMG_0877.JPG)

## Features
- Real-time screen color synchronization.
- Support for multiple bulb types (Currently for Tuya WiFi bulbs and bulbs via Zigbee2MQTT).
- Customizable settings for color processing and bulb control.
- Per-bulb type refresh rate settings
- Multiple zone sampling
- User-friendly GUI for easy interaction.

## To-Dos

- Add the ability to add bulbs via GUI
- Optimise MSS code to use multiprocessing // speed up sampling. We need to get to 50+ samples/sec as this seems to be what Tuya bulbs can handle
- Optimise latency Sample->Update
- Add ability to customise sampling
- Improve UI
- Add additional common bulb types 
