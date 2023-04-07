---
title: MicroPython
description: A guide on how to use MicroPython on your Monocle AR device.
image: /micropython/images/monocle-micropython.png
nav_order: 3
---

# MicroPython API
{: .no_toc }

---

MicroPython lets you prototype and build your applications quickly without having to dive into any low level programming. With a few lines of Python, you can draw to the display, access the camera, and offload processing to the FPGA. Of course you get all the other benefits of Python too. Best of all, it's completely wireless, and you can access the Python REPL fully over Bluetooth.

The [MicroPython firmware for Monocle](https://github.com/brilliantlabsAR/monocle-micropython) is a customized firmware which is largely based on the [upstream MicroPython](https://github.com/micropython/micropython) project. Thanks to the large MicroPython community, we're always updating to new features as they come out on the upstream project.

A subset of the standard MicroPython libraries are currently supported, with more periodically being added. Additionally, some extra modules are included which let you easily interact with the Monocle hardware. Be sure to check out the [MicroPython docs site](https://docs.micropython.org/en/latest/index.html),  as well as the docs here to familiarize yourself with all the features.

---

## Quick start
{: .no_toc }

{: .note }
> **Check that you're on the [latest firmware](#firmware-updates).**

Get started by trying out the [Web Bluetooth REPL](https://repl.brilliant.xyz) using Google Chrome on your PC, Mac, or Android, or use a Web Bluetooth compatible web browser on your iOS device such as [Bluefy](https://apps.apple.com/us/app/bluefy-web-ble-browser/id1492822055).

![Accessing MicroPython on Monocle using the web REPL interface](/micropython/images/micropython-web-repl.png)

Once you're connected, try running this code:

```python
import touch
import display

def change_text(button):
    display.text(f"Button {button} touched!", 0, 0, 0xffffff)
    display.show()

touch.callback(touch.BOTH, change_text)

display.text("Tap a touch button", 0, 0, 0xffffff)
display.show()
```

---

## Mobile app
{: .no_toc }

We're gradually building our companion app along with some extra features to help you get the most out of Monocle. It's also a great place to start if you'd like to make your own app, and the source code is freely available on our [GitHub](https://github.com/brilliantlabsAR/brilliant-mobile-app).

<div style="text-align:center" markdown="1">
[<img src="https://upload.wikimedia.org/wikipedia/commons/3/3c/Download_on_the_App_Store_Badge.svg" alt="Apple App Store badge" width="175"/>](https://apps.apple.com/us/app/monocle-by-brilliant/id1632203938)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
[<img src="https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg" alt="Google Play Store badge" width="175"/>](https://play.google.com/store/apps/details?id=com.brilliantmonocle)
</div>

---

## Library reference
{: .no_toc }

{: .note }
> MicroPython for Monocle is always being updated so be sure to check back frequently. The ❌ icon signifies a feature which is not implemented yet, but is planned.

1. TOC
{:toc}

---

### `builtins`

> Standard MicroPython [built in functions](https://docs.micropython.org/en/latest/library/builtins.html) are supported.

```
import builtins

# List all built-in functions supported by MicroPython
help(builtins)
```

---

### `device` – Monocle specific

> The device class contains general information about the Monocle's hardware and firmware.

| Members | Description |
|:--------|:------------|
| `NAME` **constant**                           | Constant which holds `'monocle'` as a **string**.
| `mac_address()` **function**                  | Returns the 48-bit MAC address as a 17 character **string** in the format `'xx:xx:xx:xx:xx:xx'`, where each `xx` is a byte in lowercase hex format.
| `VERSION` **constant**                        | Constant containing the firmware version as a **string**. E.g. `'monocle-firmware-v22.342.1252'`.
| `GIT_TAG` **constant**                        | Constant containing the build git tag as a 7 character **string**.
| `GIT_REPO` **constant**                       | Constant containing the project git repo as a **string**.
| `battery_level()` **function**                | Returns the battery level percentage as an **integer**.
| `reset()` **function**                        | Resets the device.
| `reset_cause()` **function**                  | Returns the reason for the previous reset or startup state. These can be either:<br>- `'POWERED_ON'` if the device was powered on normally<br>- `'SOFTWARE_RESET'` if `device.reset()` was called<br>- `'CRASHED'` if the device had crashed.
| `prevent_sleep(enable)`&nbsp;**function**     | Enables or disables sleeping of the device when put back into the charging case. Sleeping is enabled by default. If no argument is given. The currently set value is returned. **WARNING: Running monocle for prolonged periods may result in display burn in, as well as reduced lifetime of components.**
| `force_sleep()` **function**                  | Puts the device to sleep. All hardware components are shut down, and Bluetooth is disconnected. Upon touching either of the touch pads, the device will wake up, and reset.

```python
import device

# Check the firmware version manually
print(device.VERSION)

# Prevent the device from sleeping while put in the charging case
# not for too long to avoid burn-ins marks on the dislay...
device.prevent_sleep(True)

# Reboot the deice from MicroPython
device.reset()

```

---

### `display` – Monocle specific

> The display module allows for drawing to the micro OLED display. An image can be prepared using the functions below, and then `show()` can be used to print the image to the display.

| Members | Description |
|:--------|:------------|
| `fill(color)` **function**                   | Fills the entire display with a color. `color` should be a 24-bit RGB value such as `0xAABBCC`.
| `pixel(x, y, color)` **function** ❌           | Draws a single pixel of color `color` at the position `x`, `y`.
| `hline(x,y,width,color)` **function**        | Draws a horizontal line from the position `x`, `y`, with a given `width` and `color`.
| `vline(x,y,height,color)` **function**       | Draws a vertical line from the position `x`, `y`, with a given `height` and `color`.
| `line(x1,y1,x2,y2,color)` **function**       | Draws a straight line from the position `x1`, `y1`, to the position `x2`, `y2`, with a given `color`.
| `text("string",x,y,color)`&nbsp;**function** | Draws text at the position `x`, `y`, with a given `color`.
| `show()` **function**                        | Prints the populated frame buffer to the display. After this call, another series of drawing functions may be called and `show()` can be used to print the next frame. This also clears the display.
| `brightness(level)` **function**             | Sets the display's brightness. `level` can be 0, 1, 2, 3, or 4.
| `WIDTH` **constant**                         | The display width in pixels. Equal to 640.
| `HEIGHT` **constant**                        | The display height in pixels. Equal to 400.

---

### `camera` – Monocle specific

> The camera module allows for capturing images and transferring them to another device over Bluetooth.

| Members | Description |
|:--------|:------------|
| `capture()` **function** ❌                    | Captures an image and returns it to a device over Bluetooth. See [downloading media](#downloading-media) to understand how media transfers are done.
| `overlay(enable)` **function**               | Enables or disables an overlay of what the camera is currently seeing onto the display.
| `output(x,y,format)`&nbsp;**function**&nbsp;❌ | Set the output resolution and format. `x` and `y` represent the output resolution in pixels. `format` can be either `RGB`, `'YUV'` or `'JPEG'`. The default output settings are `camera.output(640, 400, 'YUV')`.
| `zoom(multiplier)` **function** ❌             | Sets the zoom level of the camera. Multiplier can be any floating point number between 1 and 8.
| `RGB` ❌ **constant**                          | String constant which represents a RGB565 output format.
| `YUV` ❌ **constant**                          | String constant which represents a YUV422 output format.
| `JPEG` ❌ **constant**                         | String constant which represents a jpeg output format.

```python
import camera

# Verify the overlay status
camera.overlay()

# Turn on and off the mirroring from camera to display
camera.overlay(True)
camera.overlay(False)
```

---

### `microphone` – Monocle specific

> The microphone module allows for capturing audio and streaming it to another device over Bluetooth.

| Members | Description |
|:--------|:------------|
| `stream()`&nbsp;**function**&nbsp;❌ | Streams audio from the microphone to a device over Bluetooth. See [downloading media](#downloading-media) to understand how media transfers are performed.

---

### `touch` – Monocle specific

> The touch module allows for reacting to touch events from the capacitive touch pads on Monocle.

| Members | Description |
|:--------|:------------|
| `callback(pad,callback)`&nbsp;**function** | Attaches a callback handler to one or both of the touch pads. If `pad` is given as `touch.BOTH`, a single callback will be used to capture both touch events. Otherwise `touch.A` or `touch.B` can be used to assign separate callback functions if desired. `callback` should be a predefined function taking one argument. This argument will equal the pad which triggered the callback. To unassign a callback, issue `touch.callback()` with `None` in the `callback` argument. To view the currently assigned callback, issue `touch.callback()` without the `callback` argument.
| `state(pad)` **function**                  | Returns the current touch state of the touch pads. If `pad` is not specified, either `'A'`, `'B'`, `'BOTH'` or `None` will be returned depending on which pads are currently touched. If `pad` is specified, then `True` or `False` will be returned for the touch state of that pad.
| `A` **constant**                           | String constant which represents Pad A.
| `B` **constant**                           | String constant which represents Pad B.
| `BOTH` **constant**                        | String constant which represents both pads.

```python
import touch

# Define a function used as a callback
def fn(arg):
    if arg == touch.A:
        print("button A")
    if arg == touch.B:
        print("button B")

# Bind the callback to the button actions
touch.callback(touch.BOTH, fn)
```

---

### `led` – Monocle specific

> The LED module contains functions to control the red and green LED on the front of Monocle.

| Members | Description |
|:--------|:------------|
| `on(color)` **function**             | Illuminates an led. `color` can be either `led.RED` or `led.GREEN`.
| `off(color)`&nbsp;**function**&nbsp; | Turns off an led. `color` can be either `led.RED` or `led.GREEN`.
| `RED` **constant**                   | String constant which represents the red led.
| `GREEN` **constant**                 | String constant which represents the green led.

```python
import led

# Turn the green LED on
led.on(led.GREEN)
```

---

### `fpga` – Monocle specific

> The FPGA module allows for direct control of the FPGA, as well as the ability to update the bitstream.

| Members | Description |
|:--------|:------------|
| `read(addr, n)` **function**            | Reads `n` number of bytes from the 16-bit address `addr`, and returns a **bytes object**.
| `write(addr,bytes[])`&nbsp;**function** | Writes all bytes from a given **bytes object** `bytes[]` to the 16-bit address `addr`.

```
import fpga

# Read the FGPA release version
fpga.read(0x0002, 3)

# Write command `0x34` to FPGA peripheral `0x12` 
fpga.write(0x1234, b'')

# Write a command then some payload data to FPGA
fpga.write(0x1234, b'\x01\x02\x03\x04\x05')
```

---

### `storage` - Monocle specific

> Storage can be used for reading or writing to files within the non-volatile storage. `"file"` can be any user defined string, however certain strings are reserved for special uses such as `"fpga-bitstream"` which is used to store the FPGA application.

| Members | Description |
|:--------|:------------|
|`read("file",length,offset)`&nbsp;**function**&nbsp;❌ | Reads and returns a **bytes object** of length `length` from a file `file` within the non-volatile storage. `offset` is an optional position in bytes from the start of the file to read from.
|`append("file", bytes[])` **function** ❌              | Appends data from a **bytes object** `bytes[]` to the end of a file within. If the file doesn't exist, then it's created.
|`delete("file")` **function** ❌                       | Deletes a file from the storage.
|`list()` **function** ❌                               | Lists all files within the storage.
|`FPGA_BITSTREAM` **constant** ❌                       | A special filename which is used for storing the FPGA bitstream. It is used by the `update.fpga()` function to update the FPGA application.

```python
import os

# Create a new file in write mode
with open("path_to_file.py", "w") as f:

    # Write some python code to that file
    f.write("print('hello world!')\n")

# List the existing files at the root directory "/"
os.list("/")

# Execute an existing python file
import path_to_file
```

---

### `bluetooth` - Monocle specific

> The `bluetooth` module can be used to transfer byte data between Monocle and the host Bluetooth device. Bytes can contain any arbitrary data, and avoids having to pollute the REPL interface with printing data out as strings. The [raw data service](#communication) is used for all communications under the `bluetooth` module.

| Members | Description |
|:--------|:------------|
|`send(bytes[])` **function**                   | Sends data from a **bytes object** `bytes[]` over Bluetooth using the [raw data service](#communication). The length of `bytes[]` must be equal to or less than the value returned by the `bluetooth.max_length()` function.
|`receive_callback(callback)`&nbsp;**function** | Assigns a callback to receive data over the [raw data service](#communication). `callback` must be a predefined function taking one argument. The value of the argument will be a **bytes object** `bytes[]` containing the received data. To unbind the callback, issue this function with `callback` set as `None`. If `callback` isn't given when issuing this function, the currently set callback will be returned if it is set.
|`connected()` **function**                     | Returns `True` if the [raw data service](#communication) is connected, otherwise returns `False`.
|`max_length()` **function**                    | Returns the maximum data size the Bluetooth host allows for single transfers.

```python
import bluetooth

# Get the MTU size to make sure of how much data we can send.
len = bluetooth.max_length()

# Send a string over Bluetooth
# The host at the other side will need some code that reads that string.
# This will be sent as a single BLE packet of the same size.
str = "hello world"
bluetooth.send(str[:len])

# Define a function that will handle data reception
# The host at the other end will need some code that sends that string.
def fn(bytes):
    print(bytes)

# Activate the reception of all data to that function
bluetooth.receive_callback(fn)
```

---

### `time` – Monocle specific

> The time module allows for getting/setting the time and date as well as adding delays into your programs.

| Members | Description |
|:--------|:------------|
| `time(secs)` **function**                      | Sets or gets the current system time in seconds. If `secs` is not provided, the current time is returned, otherwise the time is set according to the value of `secs`. `secs` should be referenced from midnight on the 1st of January 1970.
| `now(epoch)` **function**                      | Returns a dictionary containing a human readable date and time. If no argument is provided, the current system time is used. If `epoch` is provided, that value will be used to generate the dictionary. The epoch should be referenced from midnight on the 1st of January 1970.
| `zone(offset)` **function**                    | Sets or gets the time zone offset from GMT as a **string**. If `offset` is provided, the timezone is set to the new value. `offset` must be provided as a string, eg *"8:00"*, or *"-06:30"*.
| `mktime(dict)` **function**                    | The inverse of `now()`. Converts a dictionary provided into an epoch timestamp. The returned epoch value will be referenced from midnight on the 1st of January 1970.
| `sleep(secs)` **function**                     | Sleep for a given number of seconds.
| `sleep_ms(msecs)` **function**                 | Sleep for a given number of milliseconds.
| `ticks_ms()` **function**                      | Returns a timestamp in milliseconds since power on.
| `ticks_add(ticks, delta)` **function**         | Offsets a timestamp value by a given number. Can be positive or negative.
| `ticks_diff(ticks1,ticks2)`&nbsp;**function** | Returns the difference between two timestamps. i.e. `ticks1 - ticks2`, but takes into consideration if the numbers wrap around.

```python
import utime

# Sleep for 1.5 second
time.sleep_ms(1500)

# Build a time/date string value into a timestamp, using the UTC (00:00) timezone
t = time.mktime({"timezone": "00:00", "weekday": "friday", "minute": 2, "day": 20, "yearday": 20, "month": 1, "second": 51, "hour": 22, "year": 2023})

# Set that time to be the current time
time.time(t)

# Show the current time in HH:MM format
t = time.now()
hour = t["hour"]
minute = t["minute"]
print(f"{hour:02d}:{minute:02d}")
```

---

### `update` - Monocle specific

> The update module allows for firmware upgrades of the MicroPython firmware, as well as the FPGA bitstream over bluetooth.

| Members | Description |
|:--------|:------------|
| `micropython()`&nbsp;**function** | Puts the device into over-the-air device firmware update mode. The device will stay in DFU mode for 5 minutes or until an update is finished being performed. The device will then restart with an updated MicroPython firmware.
| `fpga(url)` **function** ❌ | Downloads and reboots the FPGA with a bitstream provided from the `url`. If the update is interrupted part way through, the FPGA will no longer be running a valid application, and must be updated again. See [FPGA bitstream updates](#fpga-bitstream-updates) to understand how the update process is done.

```python
import update

# Reboot the Monocle into update mode
update.micropython()
```

---

### `gc`

> Standard MicroPython [garbage collection](https://docs.micropython.org/en/latest/library/gc.html) is supported.

```python
import gc

# Show the memory usage (in percent)
mem_used = gc.mem_alloc() / (gc.mem_alloc() + gc.mem_free())
print('{:d}%'.format(round(mem_used * 100)))

# Manually run the garbage collector
gc.collect()
```

### `math`

> Standard MicroPython [math](https://docs.micropython.org/en/latest/library/math.html) functions are supported.

### `micropython`

> Standard MicroPython [internals](https://docs.micropython.org/en/latest/library/micropython.html) are supported.

### `uarray`

> Standard MicroPython [arrays](https://docs.micropython.org/en/latest/library/array.html) are supported.

### `uasyncio`

> Standard MicroPython [asynchronous scheduling](https://docs.micropython.org/en/latest/library/uasyncio.html) is supported.

### `ubinascii`

> Standard MicroPython [binary/ASCII conversions](https://docs.micropython.org/en/latest/library/binascii.html) are supported.

### `ucollections`

> Standard MicroPython [collection and container types](https://docs.micropython.org/en/latest/library/collections.html) are supported.

### `uerrno`

> Standard MicroPython [system error codes](https://docs.micropython.org/en/latest/library/errno.html) are supported.

### `uhashlib`

> Standard MicroPython [hashing algorithms](https://docs.micropython.org/en/latest/library/hashlib.html) are supported.

### `uio`

> Standard MicroPython [IO streams](https://docs.micropython.org/en/latest/library/io.html) **except** for `FileIO` are supported.

### `ujson`

> Standard MicroPython [JSON handling](https://docs.micropython.org/en/latest/library/json.html) is supported.

### `urandom`

> Standard MicroPython [random number generation](https://docs.micropython.org/en/latest/library/random.html) is supported.

### `ure`

> Standard MicroPython [regular expressions](https://docs.micropython.org/en/latest/library/re.html) are supported.

### `uselect`

> Standard MicroPython [stream event waiting](https://docs.micropython.org/en/latest/library/select.html) is supported.

### `ustruct`

> Standard MicroPython [struct primitives](https://docs.micropython.org/en/latest/library/struct.html) are supported.

### `usys`

> Standard MicroPython [system specific functions](https://docs.micropython.org/en/latest/library/sys.html) are supported.

---

## Under the hood
{: .no_toc }

This section describes how data is transferred to and from Monocle over Bluetooth.

### Communication
{: .no_toc }

All MicroPython communication, i.e. the REPL interface, is accessed via a single Bluetooth *Service* containing two *Characteristics*.

- **Serial service UUID**: 6e400001-b5a3-f393-e0a9-e50e24dcca9e
- **Serial RX characteristic UUID**: 6e400002-b5a3-f393-e0a9-e50e24dcca9e
- **Serial TX characteristic UUID**: 6e400003-b5a3-f393-e0a9-e50e24dcca9e

The RX characteristic is *write* only, and transports serial string data from the central BLE device to Monocle. The TX characteristic is *notification* only and delivers messages back from Monocle, to the central BLE device.

Each characteristic transports string data of any length up to the negotiated *MTU size - 3 bytes*. Longer strings must be chopped up and will be automatically rejoined on the receiving side by Monocle. Likewise if Monocle wishes to send longer responses than can fit into a single MTU payload, the data will arrive sequentially, and can be concatenated by the central Bluetooth app. The diagram below describes how communication operates between Monocle and a central device.

![Sequence diagram of the Monocle serial data service](/micropython/images/bluetooth-serial-service-sequence-diagram.svg)

A secondary Bluetooth *Service*, again containing two *Characteristics*, is used to transport raw data such as image, audio and firmware update data. The mechanism for the raw data service is similar to the serial data service, aside from the fact that `null` or `0` characters may also be included within the payload.

- **Raw data service UUID**: e5700001-7bac-429a-b4ce-57ff900f479d
- **Raw data RX Characteristic UUID**: e5700002-7bac-429a-b4ce-57ff900f479d
- **Raw data TX Characteristic UUID**: e5700003-7bac-429a-b4ce-57ff900f479d

Raw data transfer may often be bigger than a single MTU payload. Similarly to the serial data, it may need to be broken up into pieces. To help reconstruct the packets sent or received by Monocle, a flag is present at the start of each payload to determine if it's either a starting payload, middle payload, end payload, or a small single buffer payload. The exact mechanisms for different types of data transfer are outlined below.

### Downloading media
{: .no_toc }

Media files such as audio and images may be downloaded from the Monocle using the raw data service mentioned in the [Communication section](#communication). Files may also be sent asynchronously by Monocle when they are ready.

Due to the small payload size of Bluetooth packets, the file may be spit into many *chunks* and need to be recombined by the receiving central device. A flag at the start of each payload indicates if it is the **START**, **MIDDLE** or **END** of the file. A very small file may also be transferred using the **SMALL** flag.

The first payload includes metadata about the file such as the filename (with a relevant file extension) and the file size. The sequence diagram below describes how a file is broken into several parts and the data can be recombined to construct the full file: 

![Sequence diagram of the Monocle raw data service](/micropython/images/bluetooth-raw-data-service-sequence-diagram.svg)

### Firmware updates
{: .no_toc }

Updates of the MicroPython firmware are handled using Nordic's over-the-air device firmware update process. 

To perform an update:

1. Check which version of the firmware you current have by entering `import device; device.VERSION`.

1. Download the latest `monocle-vXX.XXX.XXXX.zip` package from our [GitHub releases](https://github.com/brilliantlabsAR/monocle-micropython/releases) page.

1. Issue an update command over MicroPython using `import update; update.micropython()`. Monocle will now reboot into DFU mode.

1. Using the nRF Connect App, for [desktop](https://www.nordicsemi.com/Products/Development-tools/nrf-connect-for-desktop), [Android](https://play.google.com/store/apps/details?id=no.nordicsemi.android.mcp&hl=en&gl=US), or [iOS](https://apps.apple.com/se/app/nrf-connect-for-mobile/id1054362403), you can reconnect to Monocle, select the downloaded `.zip` file, and update to the latest version.

### FPGA bitstream updates
{: .no_toc }

Details coming soon.
