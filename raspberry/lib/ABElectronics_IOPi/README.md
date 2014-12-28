AB Electronics UK IO Pi Python Library
=====

Python Library to use with IO Pi Raspberry Pi expansion board from http://www.abelectronics.co.uk

Install
====
To download to your Raspberry Pi type in terminal: 

```
git clone https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```

The IO Pi library is located in the ABElectronics_IOPi directory

The library requires python-smbus to be installed.
```
sudo apt-get update
sudo apt-get install python-smbus
```
Add the location where you downloaded the python libraries into PYTHONPATH e.g. download location is Desktop
```
export PYTHONPATH=${PYTHONPATH}:~/Desktop/ABElectronics_Python_Libraries/ABElectronics_IOPi/
```

The example python files in /ABElectronics_Python_Libraries/ABElectronics_IOPi/demos/ will now run from the terminal.

If you want to run the demo scripts without modifying the python path you will need to move the demo scripts into the same folder as the ABElectronics_IOPi.py file.

Functions:
----------

```
setPinDirection(pin, direction):
```
Sets the IO direction for an individual pin  
**Parameters:** pin - 1 to 16, direction - 1 = input, 0 = output  
**Returns:** null

```
setPortDirection(port, direction): 
```
Sets the IO direction for the specified IO port  
**Parameters:** port - 0 = pins 1 to 8, port 1 = pins 8 to 16, direction - 1 = input, 0 = output  
**Returns:** null
```
setPortPullups(self, port, value)
```
Set the internal 100K pull-up resistors for the selected IO port  
**Parameters:** port - 1 to 16, value: 1 = Enabled, 0 = Disabled  
**Returns:** null

```
writePin(pin, value)
```
Write to an individual pin 1 - 16  
**Parameters:** pin - 1 to 16, value - 1 = Enabled, 0 = Disabled
**Returns:** null
```
writePort(self, port, value)
```
Write to all pins on the selected port  
**Parameters:** port - 0 = pins 1 to 8, port 1 = pins 8 to 16, value -  number between 0 and 255 or 0x00 and 0xFF  
**Returns:** null
```
readPin(pin)
```
Read the value of an individual pin 1 - 16   
**Parameters:** pin: 1 to 16  
**Returns:** 0 = logic level low, 1 = logic level high
```
readPort(port)
```
Read all pins on the selected port  
**Parameters:** port - 0 = pins 1 to 8, port 1 = pins 8 to 16  
**Returns:** number between 0 and 255 or 0x00 and 0xFF
```
invertPort(port, polarity)
```
Invert the polarity of the pins on a selected port  
**Parameters:** port - 0 = pins 1 to 8, port 1 = pins 8 to 16, polarity - 0 = same logic state of the input pin, 1 = inverted logic state of the input pin  
**Returns:** null

```
invertPin(pin, polarity)
```
Invert the polarity of the selected pin  
**Parameters:** pin - 1 to 16, polarity - 0 = same logic state of the input pin, 1 = inverted logic state of the input pin
**Returns:** null
```
mirrorInterrupts(value)
```
Mirror Interrupts  
**Parameters:** value - 1 = The INT pins are internally connected, 0 = The INT pins are not connected. INTA is associated with PortA and INTB is associated with PortB  
**Returns:** null
```
setInterruptType(port, value)
```
Sets the type of interrupt for each pin on the selected port  
**Parameters:** port 0 = pins 1 to 8, port 1 = pins 8 to 16, value: 1 = interrupt is fired when the pin matches the default value, 0 = the interrupt is fired on state change  
**Returns:** null
```
setInterruptDefaults(port, value)
```
These bits set the compare value for pins configured for interrupt-on-change on the selected port.  
If the associated pin level is the opposite from the register bit, an interrupt occurs.    
**Parameters:** port 0 = pins 1 to 8, port 1 = pins 8 to 16, value: compare value  
**Returns:** null
```
setInterruptOnPort(port, value)
```
Enable interrupts for the pins on the selected port  
**Parameters:** port 0 = pins 1 to 8, port 1 = pins 8 to 16, value: number between 0 and 255 or 0x00 and 0xFF  
**Returns:** null

```
setInterruptOnPin(pin, value)
```
Enable interrupts for the selected pin  
**Parameters:** pin - 1 to 16, value - 0 = interrupt disabled, 1 = interrupt enabled  
**Returns:** null

```
readInterruptStatus(port)
```
Enable interrupts for the selected pin  
**Parameters:** port 0 = pins 1 to 8, port 1 = pins 8 to 16  
**Returns:** status

```
readInterruptCature(port)
```
Read the value from the selected port at the time of the last interrupt trigger  
**Parameters:** port 0 = pins 1 to 8, port 1 = pins 8 to 16  
**Returns:** status
```
resetInterrupts()
```
Set the interrupts A and B to 0  
**Parameters:** null  
**Returns:** null
Usage
====
To use the IO Pi library in your code you must first import the library:
```
from ABElectronics_IOPi import IOPI
```
Next you must initialise the IO object:
```
bus1 = IOPI(0x20)
```

We will read the inputs 1 to 8 from bus 2 so set port 0 to be inputs and enable the internal pull-up resistors 

```
bus1.setPortDirection(0, 0xFF)
bus1.setPortPullups(0, 0xFF)
```

You can now read the pin 1 with:
```
print 'Pin 1: ' + str(bus1.readPin(1))
```
