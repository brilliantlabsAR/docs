---
title: MicroPython
description: A guide on how to use MicroPython to drive your Monocle hardware.
image: /images/monocle-micropython.png
nav_order: 3
---

# MicroPython API
{: .no_toc }

MicroPython lets you prototype and build you applications fast without having to dive deep into any C development. With a few lines of Python you can draw to the display, access the camera, and even offload processing to the FPGA when needed. Of course you get all the other benefits of Python too. Best of all, it's completely wireless, and you can access the Python REPL simply over Bluetooth.

The [MicroPython firmware for Monocle](https://github.com/Itsbrilliantlabs/monocle-micropython) is a customized port which is largely based on the [upstream MicroPython](https://github.com/micropython/micropython) project. It has a large and growing user base, so we're frequently able to update features from the upstream project as they becoming available.

## Contents
{: .no_toc }

1. TOC
{:toc}

## Quick start

Go to [this page](repl.siliconwitchery.com) using Google Chrome, and connect to your Monocle using the Web Bluetooth API.

![Accessing MicroPython on Monocle using the web REPL interface]()

Once you're connected, try running this code:

```python
from machine import *
import framebuf

fbuf = framebuf.FrameBuffer(bytearray(640 * 400 * 2), 640, 400, framebuf.RGB565)
fbuf.fill(0)
fbuf.text('MicroPython!', 0, 0, 0xffff)

machine.Display.show(fbuf)
```

You can also try the mobile app on iOS or Android which we're gradually adding more features to. It's also a great place to start if you'd like to make your own mobile app for Monocle.

## API status

| Status                                     | Module & class                                                     | Description |
|:------------------------------------------:|:-------------------------------------------------------------------|:------------|
| <span style="color:green">Supported</span> | builtins **module**                                                | There are many default built-in functions enabled. Only differences in the base feature set are listed here
| <span style="color:orange">Planned</span>  | builtins.bytearray **class**                                       | Byte arrays are supported
| <span style="color:red">Not planned</span> | builtins.complex **class**                                         | Complex numbers are not supported
| <span style="color:orange">Planned</span>  | builtins.dict **class**                                            | All MicroPython dictionary functions including dict.fromkeys() are supported
| <span style="color:orange">Planned</span>  | builtins.enumerate **class**                                       | Enumerate loops are supported
| <span style="color:orange">Planned</span>  | builtins.float **class**                                           | Floating point numbers are supported
| <span style="color:orange">Planned</span>  | builtins.max **function**                                          | Max is supported
| <span style="color:orange">Planned</span>  | builtins.min **function**                                          | Min is supported
| <span style="color:orange">Planned</span>  | builtins.reversed **class**                                        | Reversing lists are supported
| <span style="color:orange">Planned</span>  | builtins.set **class**                                             | Sets are supported
| <span style="color:orange">Planned</span>  | builtins.slice **class**                                           | Slices are supported
| <span style="color:orange">Planned</span>  | builtins.str **class**                                             | Unicode support, and extra string functions are supported
| <span style="color:orange">Planned</span>  | framebuf **module**                                                | Frame drawing functions are supported
| <span style="color:orange">Planned</span>  | gc **module**                                                      | Garbage collection functions are supported
| <span style="color:orange">Planned</span>  | machine.Battery.level() **function**                               | Returns the current battery level as a percentage
| <span style="color:orange">Planned</span>  | machine.Camera.capture(*url*) **function**                         | Sends the last captured image over Bluetooth
| <span style="color:orange">Planned</span>  | machine.Camera.stop() **function**                                 | Stops any ongoing image stream or capture currently in progress
| <span style="color:orange">Planned</span>  | machine.Display.show(framebuffer) **function**                     | Pushes a framebuffer object to the FPGA for drawing onto the display
| <span style="color:orange">Planned</span>  | machine.FPGA.download(url) **function**                            | Downloads and reboots the FPGA with the bitstream from the url provided. If a url is not provided, the bitstream is requested over bluetooth. Automatically powers up the FPGA if it was powered down
| <span style="color:orange">Planned</span>  | machine.FPGA.spi_read(cmd, addr, bytes) **function**               | Reads n bytes from the FPGA with a given command and address. Returns a byte array
| <span style="color:orange">Planned</span>  | machine.FPGA.spi_write(cmd, addr, bytes, buffer) **function**      | Writes n bytes from buffer to the FPGA with a given command and address. 
| <span style="color:orange">Planned</span>  | machine.FPGA.status() **function**                                 | Returns the current status of the FPGA
| <span style="color:orange">Planned</span>  | machine.Microphone.stream(*url*) **function**                      | Starts streaming audio data over Bluetooth
| <span style="color:orange">Planned</span>  | machine.Microphone.stop() **function**                             | Stops any ongoing audio stream
| <span style="color:orange">Planned</span>  | machine.Power.hibernate(enable) **function**                       | Enables or disables all the high power devices. Networking remains active. Upon re-enabling the FPGA will remain in reset until booted using FPGA.boot()
| <span style="color:orange">Planned</span>  | machine.Power.reset() **function**                                 | Resets the device
| <span style="color:orange">Planned</span>  | machine.Power.reset_cause() **function**                           | Returns the reason for the previous reset or startup state
| <span style="color:orange">Planned</span>  | machine.Power.shutdown(timeout) **function**                       | Places the device into deep-sleep and powers down all high power devices. If a timeout is given, the device will wake up again after that many seconds, otherwise the device will only wake up upon inserting, and removing from the case. Upon wakeup, the device will reset, and the cause can be seen using the Power.reset_cause() function
| <span style="color:orange">Planned</span>  | machine.Timer.Timer(id, period, callback, oneshot) **constructor** | Creates a new Timer object on timer id with the period in milliseconds and a given callback handler. The oneshot value can optionally be set to true if only a single trigger is required. By default the timer is repeating
| <span style="color:orange">Planned</span>  | machine.Timer.value() **function**                                 | Returns the current count value of the timer in milliseconds
| <span style="color:orange">Planned</span>  | machine.Timer.deinit() **function**                                | De-initializes the timer and stops any callbacks
| <span style="color:orange">Planned</span>  | machine.Touch **class**                                            | 
| <span style="color:orange">Planned</span>  | machine.mac_address() **function**                                 | Returns the 48bit MAC address of the device as a 17 character string. Each byte is delimited with a colon
| <span style="color:orange">Planned</span>  | machine.update(start) **function**                                 | Checks for firmware updates and returns True if it is available. If start is set to True, the update process is begun, and the device will enter the bootloader state
| <span style="color:green">Supported</span> | machine.board_name **string**                                      | Returns the device name as a string
| <span style="color:green">Supported</span> | machine.git_tag **string**                                         | Returns the firmware build git tag as a string
| <span style="color:green">Supported</span> | machine.mcu_name **string**                                        | Returns the device's main MCU name as a string
| <span style="color:green">Supported</span> | machine.version **string**                                         | Returns the firmware version number as a string
| <span style="color:orange">Planned</span>  | math **module**                                                    | Math functions are supported
| <span style="color:green">Supported</span> | micropython **module**                                             | There are many default micropython functions enabled. Only differences in the base feature set are listed here
| <span style="color:orange">Planned</span>  | ubinascii **module**                                               | Binary to ASCII encodings are supported
| <span style="color:orange">Planned</span>  | uerrno **module**                                                  | System error codes are supported
| <span style="color:red">Not planned</span> | uio.open(file, mode) **function**                                  | File opening is not supported (yet)
| <span style="color:orange">Planned</span>  | uio.                                                               | String and Byte IO streams are supported
| <span style="color:orange">Planned</span>  | ujson **module**                                                   | JSON handling functions are supported
| <span style="color:orange">Planned</span>  | urandom **module**                                                 | Additional random number functions are supported
| <span style="color:orange">Planned</span>  | ure **module**                                                     | Regular expression handling functions are supported
| <span style="color:orange">Planned</span>  | utime.gmtime(epoch) **function**                                   | Returns a tuple containing the time and data according to GMT. If the epoch argument is provided, the epoch timestamp is used, other the internal time of the device
| <span style="color:orange">Planned</span>  | utime.localtime(epoch) **function**                                | Returns a tuple containing the time and data according to local time. If the epoch argument is provided, the epoch timestamp is used, other the internal time of the device
| <span style="color:orange">Planned</span>  | utime.mktime(tuple) **function**                                   | The inverse of gmtime(). Returns an epoch seconds value from the 9-tuple given
| <span style="color:orange">Planned</span>  | utime.time() **function**                                          | Returns the number of seconds since the epoch. If the true time hasn't been set, this will be the number of seconds since power on
| <span style="color:orange">Planned</span>  | utime.set_time(secs) **function**                                  | Set the real time clock to a given value in seconds from the epoch
| <span style="color:orange">Planned</span>  | utime.sleep(secs) **function**                                     | Sleep for a given number of seconds
| <span style="color:orange">Planned</span>  | utime.sleep_ms(msecs) **function**                                 | Sleep for a given number of milliseconds
| <span style="color:orange">Planned</span>  | utime.sleep_us(usecs) **function**                                 | Sleep for a given number of microseconds
| <span style="color:orange">Planned</span>  | utime.ticks_ms() **function**                                      | Returns the time in ms since power on
| <span style="color:orange">Planned</span>  | utime.ticks_us() **function**                                      | Returns the time in us since power on
