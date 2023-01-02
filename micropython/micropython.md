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

> Minimal MicroPython [built in functions](https://docs.micropython.org/en/latest/library/gc.html) are supported along with the additional features listed below. 

| Members | Description |
|:--------|:------------|
| `bytearray` **class** | Byte arrays are supported
| `dict` **class**      | Dictionaries are supported
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

> The device class contains general information about the Monocle's hardware and firmware, along with battery state and firmware updating.

| Members | Description |
|:--------|:------------|
| `NAME` **constant** ❌                         | Constant which holds `'monocle'` as a **string**
| `mac_address()` **function**                  | Returns the 48-bit MAC address as a 17 character **string** in the format `xx:xx:xx:xx:xx:xx`, where each `xx` is a byte in lowercase hex format
| `VERSION` **constant**                        | Constant containing the firmware version as a **string**. E.g. `'monocle-firmware-v22.342.1252'`.
| `GIT_TAG` **constant**                        | Constant containing the build git tag as a 7 character **string**
| `update(url,start)`&nbsp;**function**&nbsp;❌ | Checks the given URL for a firmware update file. If `start` was provided as `True` the update will be started automatically. Otherwise returns:<br>- `AVAILABLE` if an update is available, but `start` was not given or was set to `False`<br>- `'IS_LATEST'` if there is no new update<br>See [firmware updates](#firmware-updates) to understand how the update process is done
| `battery_level()` **function** ❌              | Returns the battery level percentage as an **integer**
| `reset()` **function**                        | Resets the device
| `reset_cause()` **function**                  | Returns the reason for the previous reset or startup state. These can be either:<br>- `'POWERED_ON'` if the device was powered on normally<br>- `'SOFTWARE_RESET'` if `reset()` or `update()` was used<br>- `'CRASHED'` if the device had crashed

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
| `power(power_on)` **function** ❌              | Powers up the FPGA if `True` is given otherwise powers down with `False`. If no argument is given, the current powered state of the FPGA is returned
| `update(url)` **function** ❌                  | Downloads and reboots the FPGA with a bitstream provided from the `url`. Automatically wakes up the FPGA if it is shutdown. If the update is interrupted part way through, the FPGA will no longer be running a valid application, and must be updated again. See [FPGA bitstreams](#fpga-bitstreams) to understand how the update process is done
| `state()` **function** ❌                      | Returns the current state of the FPGA:<br>- `'RUNNING'` if the FPGA is running a valid bitstream.<br>- `'NOT_POWERED'` if the FPGA is not powered<br>- `'BAD_BITSTREAM'` if the FPGA can't run the bitstream stored in memory. Another `update()` must be performed.
| `ON` **constant** ❌                           | Equal to `True`. For use with `fpga.power()`. Used to turn the FPGA on.
| `OFF` **constant** ❌                          | Equal to `False`. For use with `fpga.power()`. Used to turn the FPGA off.

---

### `camera` – Monocle specific

> The camera module allows for capturing images and transferring them back to a module device.

| Members | Description |
|:--------|:------------|
| `capture()` **function** ❌                 | Captures an image and returns it to the mobile device over Bluetooth. See [downloading media](#downloading-media) to understand how media transfers are performed
| `stop()` **function** ❌                    | Stops any ongoing camera image transfer that is currently in progress
| `power(power_on)`&nbsp;**function**&nbsp;❌ | Powers up the camera if `True` is given otherwise powers down with `False`. If no argument is given, the current powered state of the camera is returned
| `ON` **constant** ❌                        | Equal to `True`. For use with `camera.power()`. Used to turn the camera on.
| `OFF` **constant** ❌                       | Equal to `False`. For use with `camera.power()`. Used to turn the camera off.

---

### `microphone` – Monocle specific

> The microphone module allows for capturing audio and streaming it to a module device.

| Members | Description |
|:--------|:------------|
| `stream()`&nbsp;**function**&nbsp;❌ | Streams audio from the microphone to the mobile device over Bluetooth. See [downloading media](#downloading-media) to understand how media transfers are performed
| `stop()` **function** ❌             | Stops any ongoing audio transfer that is currently in progress

---

### `display` – Monocle specific

> The display module allows for drawing to the micro OLED display of Monocle.

| Members | Description |
|:--------|:------------|
| `fill(color)` **function** ❌                        | 
| `pixel(x, y, color)` **function** ❌                 | 
| `hline(x,y,width,color)` **function** ❌             | 
| `vline(x,y,height,color)` **function** ❌            | 
| `line(x1,y1,x2,y2,color)` **function** ❌            | 
| `text("string",x,y,color)`&nbsp;**function**&nbsp;❌ | 
| `show()` **function** ❌                             | 
| `power(power_on)` **function** ❌                    | Powers up the display if `True` is given otherwise powers down with `False`. If no argument is given, the current powered state of the display is returned
| `ON` **constant** ❌                                 | Equal to `True`. For use with `display.power()`. Used to turn the display on.
| `OFF` **constant** ❌                                | Equal to `False`. For use with `display.power()`. Used to turn the display off.

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
