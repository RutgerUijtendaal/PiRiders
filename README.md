# Pi Riders

School project building a car that follows a line and listens to directions using a RPi, 3 IR sensors and two 28BYJ-48 Step Motors

### Prerequisites

To run you need to install RPi GPIO on the Pi.

```
sudo apt-get install python-rpi.gpio python3-rpi.gpio
```

### Running

Run the main function with Python3.

```
python3 main.py
```

### Notes

The code is heavily commented with explanations as it's a school project. Program flow should be easiliy to follow from main() onwards.

### Changing data

All pin numbers and step speed are stored in constants.py. Use this file to change variables

### Website

The bot uses a website to get the next destination from. URLs are hardcoded into the constants. The bot expects a json to read the destination from.

```
{
    'delivery' : true,
    'destination' : $name
}
```

After a destination is reached it posts to the website to signal a new destination can be set.