---
title: MicroPython
description: A guide on how to use MicroPython on your Monocle AR device.
image: /micropython/images/monocle-micropython.png
nav_order: 3
---

# MicroPython API
{: .no_toc }

---

MicroPython lets you prototype and build you applications fast without having to dive deep into any C development. With a few lines of Python you can draw to the display, access the camera, and even offload processing to the FPGA when needed. Of course you get all the other benefits of Python too. Best of all, it's completely wireless, and you can access the Python REPL simply over Bluetooth.

The [MicroPython firmware for Monocle](https://github.com/Itsbrilliantlabs/monocle-micropython) is a customized port which is largely based on the [upstream MicroPython](https://github.com/micropython/micropython) project. It has a large and growing user base, so we're frequently able to update features from the upstream project as they becoming available.

The majority of the MiroPython language is documented on the [MicroPython docs](https://docs.micropython.org/en/latest/index.html). The supported subset of libraries are shown in the [table below](#supported-modules).

The additional modules listed under this page are specifically designed to allow access to the Monocle hardware. Check their pages to view the API.

---

## Quick start
{: .no_toc }

Go to [this page](repl.siliconwitchery.com) using Google Chrome, and connect to your Monocle using the Web Bluetooth API.

![Accessing MicroPython on Monocle using the web REPL interface]()

Once you're connected, try running this code:

```python
import touch
import display

fn change_text():
    display.fill(0)
    display.text("touched!", 0, 0, 0xffffff)
    display.show()

touch.bind(touch.A, touch.TAP, change_text)

display.fill(0)
display.text("tap touch A", 0, 0, 0xffffff)
display.show
```

---

## Mobile app
{: .no_toc }

You can also try the mobile app on iOS or Android which we're gradually adding more features to. It's also a great place to start if you'd like to [make your own mobile app]() for Monocle.

<div style="text-align:center" markdown="1">
[<img src="https://upload.wikimedia.org/wikipedia/commons/3/3c/Download_on_the_App_Store_Badge.svg" alt="Apple App Store badge" width="175"/>](https://apps.apple.com/us/app/monocle-by-brilliant/id1632203938)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
[<img src="https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg" alt="Google Play Store badge" width="175"/>](https://play.google.com/store/apps/details?id=com.brilliantmonocle)
</div>

---

## Library reference
{: .no_toc }

{: .note }
> The Monocle MicroPython API below is a work in progress. The ❌ icon signifies a feature which is not implemented yet, but is planned.

1. TOC
{:toc}

---

### `builtins`

> Minimal MicroPython [builtin functions and exceptions](https://docs.micropython.org/en/latest/library/gc.html) are supported along with the subset listed below. 

| Members | Description |
|:--------|:------------|
| `bytearray` **class** | Byte arrays are supported
| `dict` **class**      | Dictionaries are fully supported
| `enumerate` **class** | Enumerate loops are supported
| `float` **class**     | Floating point numbers are supported
| `max()` **function**  | The max function is supported
| `min()` **function**  | The min function is supported
| `reversed` **class**  | Reversing lists are supported
| `set` **class**       | Sets are supported
| `slice` **class**     | Slices are supported
| `str` **class**       | Unicode and string handling is supported

---

### `gc`

> Standard MicroPython [garbage collection](https://docs.micropython.org/en/latest/library/gc.html) is supported.

---

### `device` – Monocle specific

> Device contains general information about the Monocle's hardware and firmware, as well as power options and firmware updating.

| Members | Description |
|:--------|:------------|
| `NAME` **constant** ❌                          | Constant which holds `'monocle'` as a **string**
| `mac_address()` **function**                   | Returns the 48-bit MAC address as a 17 character **string** in the format `xx:xx:xx:xx:xx:xx`, where each `xx` is a byte in lowercase hex format
| `VERSION` **constant**                         | Constant containing the firmware version as a **string**. E.g. `'v22.342.1252'`. The version string is based on the release date: YY.DDD.HHMM
| `GIT_TAG` **constant**                         | Constant containing the build git tag as a 7 character **string**
| `update_available()` **function** ❌            | Checks if a new firmware update is available. Returns either `True` or `False`, or `NO_CONNECTION` if the device could not reach the update server<br>See [firmware updates](#firmware-updates) to understand how the update process is done
| `update()` **function** ❌                      | Starts a firmware update if there's one available. This will restart the device. If an update could not be done, a message will be displayed:<br>- `'IS_LATEST'` if there is no new update<br>- `'NO_CONNECTION'` if the device could not reach the update server<br>See [firmware updates](#firmware-updates) to understand how the update process is done
| `battery_level()` **function** ❌               | Returns the battery level percentage as an **integer**
| `reset()` **function**                         | Resets the device
| `reset_cause()` **function**                   | Returns the reason for the previous reset or startup state. These can be either:<br>- `'POWERED_ON'` if the device was powered on normally<br>- `'SOFTWARE_RESET'` if `reset()` was used<br>- `'CRASHED'` if the device had crashed
| `shutdown(component)`&nbsp;**function**&nbsp;❌ | Shuts down a particular component passed into the optional `component` parameter:<br>- `'DISPLAY'` shuts down only the display<br>- `'CAMERA'` shuts down only the camera<br>- If no argument is given the device is placed into the lowest power mode. Everything is shutdown including the FPGA. Only networking will remain active
| `wakeup(component)` **function** ❌             | Wakes up a particular component passed into the optional `component` parameter:<br>- `'DISPLAY'` wakes up only the display<br>- `'CAMERA'` wakes up the camera<br>- If `wakeup('DISPLAY')` or `wakeup('CAMERA')` is called after `shutdown()`, the FPGA subsystem will automatically be powered up<br>- If no argument is given, all components are woken up
| `DISPLAY` **constant** ❌                       | Constant value for use with the `shutdown()` or `wakeup()` functions
| `CAMERA` **constant** ❌                        | Constant value for use with the `shutdown()` or `wakeup()` functions

---

### `led` – Monocle specific

> The LED module contains functions to control the red and green LED on the front of Monocle.

| Members | Description |
|:--------|:------------|
| `on(led)` **function** ❌            | Illuminates the led. `led` can be either `'RED'` or `'GREEN'`
| `off(led)`&nbsp;**function**&nbsp;❌ | Turns off the led. `led` can be either `'RED'` or `'GREEN'`
| `RED` **constant** ❌                | Enumeration of the red led which can be passed to `led.on()` or `led.off()`
| `GREEN` **constant** ❌              | Enumeration of the green led which can be passed to `led.on()` or `led.off()`

---

### `fpga` – Monocle specific

> The FPGA module allows for direct control of the FPGA, as well as the ability to update the bitstream.

| Members | Description |
|:--------|:------------|
| `read(addr, n)` **function** ❌                | Reads `n` number of bytes from the 16-bit address `addr`, and returns a **list** of bytes
| `write(addr,data[])`&nbsp;**function**&nbsp;❌ | Writes all bytes from a given list `bytes[]` to the 16-bit address `addr`
| `update(url)` **function** ❌                  | Downloads and reboots the FPGA with a bitstream provided over Bluetooth. Automatically wakes up the FPGA if it was shutdown. Returns a status once completed:<br>- `'DONE'` if completed successfully<br>- `'NO_CONNECTION'` if the URL could not be reached. In this case, the update isn't performed, and the FPGA continues to run the existing bitstream<br>- `'INCOMPLETE_DOWNLOAD'` if the download wasn't successful. In this case, the update isn't performed, and the FPGA continues to run the existing bitstream<br>- `'BAD_BITSTREAM'` if the bitstream was written, but the FPGA didn't boot. In this case, the FPGA will be no longer be running as a valid image is not available. Another update must be performed<br>See [FPGA bitstreams](#fpga-bitstreams) to understand how the update process is done
| `state()` **function** ❌                      | Returns the current state of the FPGA:<br>- `'RUNNING'` if the FPGA is running a valid bitstream.<br>- `'NOT_POWERED'` if the FPGA subsystem is not powered<br>- `'BAD_BITSTREAM'` if the FPGA can't run the bitstream stored in memory. An update must be performed.

---

### `camera` – Monocle specific

> The camera module allows for capturing images and transferring them back to a module device.

| Members | Description |
|:--------|:------------|
| `capture()`&nbsp;**function**&nbsp;❌ | Captures an image and returns it to the mobile device over Bluetooth. See [downloading media](#downloading-media) to understand how media transfers are performed. Returns `'NOT_POWERED'` if the camera, or FPGA subsystem is not powered
| `stop()` **function** ❌              | Stops any ongoing camera image transfer that is currently in progress

---

### `microphone` – Monocle specific

> The microphone module allows for capturing audio and streaming it to a module device.

| Members | Description |
|:--------|:------------|
| `capture(ms)`&nbsp;**function**&nbsp;❌ | Captures `ms` milliseconds worth of audio, and transfers it to the mobile device over Bluetooth. See [downloading media](#downloading-media) to understand how media transfers are performed. Returns `'NOT_POWERED'` if the FPGA subsystem is not powered
| `stop()` **function** ❌                | Stops any ongoing audio transfer that is currently in progress

---

### `display` – Monocle specific

> The display module allows for drawing to the micro OLED display of Monocle.

| Members | Description |
|:--------|:------------|
| `fill(color)` **function** ❌                        | 
| `pixel(x, y, color)` **function** ❌                 | 
| `hline(x,y,width,color)` **function** ❌             | 
| `vline(x,y,height,color)` **function** ❌            | 
| `vline(x1,y1,x2,y2,color)`&nbsp;**function**&nbsp;❌ | 
| `text("string",x,y,color)` **function** ❌           | 
| `show()` **function** ❌                             | . Returns `'NOT_POWERED'` if the display, or FPGA subsystem is not powered

---

### `touch` – Monocle specific

> The touch module allows for reacting to touch events when the user touches the buttons on top of Monocle.

| Members | Description |
|:--------|:------------|
| `bind(pad,action,callback)`&nbsp;**function**&nbsp;❌ | 
| `state(pad)` **function** ❌                          |
| `A` **constant** ❌                                   |
| `B` **constant** ❌                                   |
| `TAP` **constant** ❌                                 |
| `DOUBLE_TAP` **constant** ❌                          |
| `LONG_PRESS` **constant** ❌                          |
| `SLIDE` **constant** ❌                               |

---

### `time` – Monocle specific

> The timer module allows for getting/setting the time and date, adding delays into your programs, as well as triggering events on regular intervals.

| Members | Description |
|:--------|:------------|
| `gmtime(epoch)` **function**    | Returns a tuple containing the time and data according to GMT. If the epoch argument is provided, the epoch timestamp is used, other the internal time of the device
| `localtime(epoch)` **function** | Returns a tuple containing the time and data according to local time. If the epoch argument is provided, the epoch timestamp is used, other the internal time of the device
| `mktime(tuple)` **function**    | The inverse of gmtime(). Returns an epoch seconds value from the 9-tuple given
| `time()` **function**           | Returns the number of seconds since the epoch. If the true time hasn't been set, this will be the number of seconds since power on
| `set_time(secs)` **function**   | Set the real time clock to a given value in seconds from the epoch
| `sleep(secs)` **function**      | Sleep for a given number of seconds
| `sleep_ms(msecs)` **function**  | Sleep for a given number of milliseconds
| `ticks_ms()` **function**       | Returns the time in ms since power on

---

### `math`

> Standard MicroPython [math](https://docs.micropython.org/en/latest/library/math.html) functions are supported.

---

### `micropython`

> Standard MicroPython [internals](https://docs.micropython.org/en/latest/library/micropython.html) are supported.

---

### `ubinascii`

> Standard MicroPython [binary/ASCII conversions](https://docs.micropython.org/en/latest/library/binascii.html) are supported.

---

---

### `uerrno`

> Standard MicroPython [system error codes](https://docs.micropython.org/en/latest/library/errno.html) are supported.

---

### `uio`

> Standard MicroPython [IO streams](https://docs.micropython.org/en/latest/library/io.html) **except** for `FileIO` are supported.

---

### `ujson`

> Standard MicroPython [JSON handling](https://docs.micropython.org/en/latest/library/json.html) is supported.

---

### `urandom`

> Standard MicroPython [random number generation](https://docs.micropython.org/en/latest/library/random.html) is supported.

---

### `ure`

> Standard MicroPython [regular expressions](https://docs.micropython.org/en/latest/library/re.html) are supported.

---

## Under the hood
{: .no_toc }

### Communication
{: .no_toc }

### Downloading media
{: .no_toc }

### Firmware updates
{: .no_toc }

### FPGA bitstreams
{: .no_toc }
