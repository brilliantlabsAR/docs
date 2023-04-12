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

Get started by trying out the [Web Bluetooth REPL](https://repl.brilliant.xyz) using Google Chrome on your PC, Mac, or Android, or use a Web Bluetooth compatible web browser on your iOS device such as [Bluefy](https://apps.apple.com/us/app/bluefy-web-ble-browser/id1492822055).

![Accessing MicroPython on Monocle using the web REPL interface](/micropython/images/micropython-web-repl.png)

Once you're connected, try running this code:

You can either type it line by line, or use **Paste Mode**. Press **Ctrl-E** to enter paste mode, paste the whole thing, and then press **Ctrl-D** to execute the program.

```python
import touch
import display

def change_text(button):
    show([display.Text(f"Button {button} touched!", display.WHITE)])

touch.callback(touch.BOTH, change_text)

display.show([Text("Tap a touch button", display.WHITE)])
```

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

#### Example
{: .no_toc }

```python
import builtins
help(builtins) # Lists all of the built-in MicroPython functions
```

---

### `device` – Monocle specific

> The device class contains general information about the Monocle's hardware and firmware.

| Members | Description |
|:--------|:------------|
| `NAME` **constant**                           | Constant which holds `'monocle'` as a **string**.
| `mac_address()` **function**                  | Returns the 48-bit MAC address as a 17 character **string** in the format `'xx:xx:xx:xx:xx:xx'`, where each `xx` is a byte in lowercase hex format.
| `VERSION` **constant**                        | Constant containing the firmware version as a 12 character **string**. E.g. `'v22.342.1252'`.
| `GIT_TAG` **constant**                        | Constant containing the build git tag as a 9 character **string**.
| `GIT_REPO` **constant**                       | Constant containing the project git repo as a **string**.
| `battery_level()` **function**                | Returns the battery level percentage as an **integer**.
| `reset()` **function**                        | Resets the device.
| `reset_cause()` **function**                  | Returns the reason for the previous reset or startup state. These can be either:<br>- `'POWERED_ON'` if the device was powered on normally<br>- `'SOFTWARE_RESET'` if `device.reset()` was called<br>- `'CRASHED'` if the device had crashed.
| `prevent_sleep(enable)`&nbsp;**function**     | Enables or disables sleeping of the device when put back into the charging case. Sleeping is enabled by default. If no argument is given. The currently set value is returned. **WARNING: Running monocle for prolonged periods may result in display burn in, as well as reduced lifetime of components.**
| `force_sleep()` **function**                  | Puts the device to sleep. All hardware components are shut down, and Bluetooth is disconnected. Upon touching either of the touch pads, the device will wake up, and reset.
| `Storage(start, length)` **class**            | The `Storage` class is used internally for initializing and accessing the file system. This class shouldn't be accessed, unless you want to reformat the internal storage. To learn more about how MicroPython handles user files, have a look at the documentation [here](https://docs.micropython.org/en/latest/esp8266/tutorial/filesystem.html) and [here](https://docs.micropython.org/en/latest/reference/filesystem.html).

#### Example
{: .no_toc }

```python
import device
device.VERSION # Prints the device firmware version
device.battery_level() # Returns the current battery level as a percentage
```

---

### `display` – Monocle specific

> The display module allows for drawing to the micro OLED display. An image can be prepared using the functions below, and then `show()` can be used to print the image to the display.

| Members | Description |
|:--------|:------------|
| `brightness(level)` **function**             | Sets the display's brightness. `level` can be 0, 1, 2, 3, or 4.
| `Text(string, fg=)` **class**                | Text with the given `string` shown with the given color [1]
| `Rect(width, height, fg=)` **class**         | Rectangle with given width, height and color [1]
| `Line(x1, y1, x2, y2, fg=)` **class**        | Line with given coordinates and color [1]
| `Polygon(list, width=, fg=, bg=)` **class**  | Polygon with given fill and stroke color [1], the shape is defined by a `list` of tuples of `(x, y)` coordinates.
| `Polyline(list, width=, fg=)` **class**      | Segmented line with given color [1], the segments are defined by a `list` of tuples of `(x, y)` coordinates.
| `show(list)` **function**                    | Show a list of shapes onto the display.
| `WIDTH` **constant**                         | The display width in pixels. Equal to 640.
| `HEIGHT` **constant**                        | The display height in pixels. Equal to 400.
| `BLACK` **constant**                         | Configurable color, `#000000` by default [1].
| `RED` **constant**                           | Configurable color, `#ad2323` by default [1].
| `GREEN` **constant**                         | Configurable color, `#1d6914` by default [1].
| `BLUE` **constant**                          | Configurable color, `#2a4bd7` by default [1].
| `CYAN` **constant**                          | Configurable color, `#29d0d0` by default [1].
| `MAGENTA` **constant**                       | Configurable color, `#8126c0` by default [1].
| `YELLOW` **constant**                        | Configurable color, `#ffee33` by default [1].
| `WHITE` **constant**                         | Configurable color, `#ffffff` by default [1].
| `GRAY1` **constant**                         | Configurable color, `#1c1c1c` by default [1].
| `GRAY2` **constant**                         | Configurable color, `#383838` by default [1].
| `GRAY3` **constant**                         | Configurable color, `#555555` by default [1].
| `GRAY4` **constant**                         | Configurable color, `#717171` by default [1].
| `GRAY5` **constant**                         | Configurable color, `#8d8d8d` by default [1].
| `GRAY6` **constant**                         | Configurable color, `#aaaaaa` by default [1].
| `GRAY7` **constant**                         | Configurable color, `#c6c6c6` by default [1].
| `GRAY8` **constant**                         | Configurable color, `#e2e2e2` by default [1].

> [1]: The colors are small values that do not cover the full palette of the display.
> The 16 default values can be one of the constants listed above.
> There will be an API to customize these colors coming in the future.
> The default foreground is white and background is gray3.

```python
from display import *

# Create a list that will contain all the thing we want to display
list = [
  # It has a long red horizontal rectangle that we place near the middle
  Rect(10, 30, fg=RED).move(300, 200),

  # It has a vertical line with 5 segments doing some zig-zags.
  Polyline([(10,20), (40,40), (10,60), (40,80), (10,100), (40,120)], fg=RED),

  # It has a triangle filled in yellow, moved to the top right corner.
  Polygon([(0,0), (10,0), (5,8)], bg=YELLOW).move(WIDTH - 50, HEIGHT - 50),

  # It has a diagonal line through the whole display, bottom left to top right
  Line(0, 0, WIDTH, HEIGHT),

  # It has a text message in the middle
  Text("something").move(WIDTH/2, HEIGHT/2),
]

# Render these elements to the display
show(list)

# We are free to use an extra list and concatenate it while rendering:
list2 = [
  Text("something less", fg=WHITE),
  Text("something more", fg=WHITE),
]
show(list + list2)

# Then we display the first list with alternative text
show(list + [Text("something different", fg=YELLOW)])

# Finally, we modify each of the text list's content and display that
list2[0].str = "something else"
show(list + list2)
```

---

### `camera` – Monocle specific

> The camera module allows for capturing images and transferring them to another device over Bluetooth.

| Members | Description |
|:--------|:------------|
| `capture()` **function** ❌                    | Captures an image and returns it to a device over Bluetooth. See [downloading media](#downloading-media) to understand how media transfers are done.
| `overlay(enable)` **function**                 | Enables or disables an overlay of what the camera is currently seeing onto the display.
| `output(x,y,format)`&nbsp;**function**&nbsp;❌ | Set the output resolution and format. `x` and `y` represent the output resolution in pixels. `format` can be either `RGB`, `'YUV'` or `'JPEG'`. The default output settings are `camera.output(640, 400, 'YUV')`.
| `zoom(multiplier)` **function** ❌             | Sets the zoom level of the camera. Multiplier can be any floating point number between 1 and 8.
| `RGB` ❌ **constant**                          | String constant which represents a RGB565 output format.
| `YUV` ❌ **constant**                          | String constant which represents a YUV422 output format.
| `JPEG` ❌ **constant**                         | String constant which represents a jpeg output format.

#### Example
{: .no_toc }

```python
import camera
camera.overlay(True) # Turns on mirroring from the camera to the display
camera.overlay(False) # Turns off mirroring from the camera to the display
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

#### Example
{: .no_toc }

```python
import touch

# Define the touch callback function which is triggered upon a touch event
def fn(arg):
    if arg == touch.A:
        print("button A pressed!")
    if arg == touch.B:
        print("button B pressed!")

touch.callback(touch.BOTH, fn) # Attaches the callback to the both buttons
touch.callback(touch.A, fn) # Attaches the callback to an individual button
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

#### Example
{: .no_toc }

```python
import led
led.on(led.GREEN) # Turns on the green LED
led.on('GREEN') # Also turns on the green LED
led.off(led.GREEN) # Turns off the green LED
led.on(led.RED) # Turns on the red LED
led.off(led.RED) # Turns off the red LED
```

---

### `fpga` – Monocle specific

> The FPGA module allows for communicating with the FPGA over the internal SPI bus.

| Members | Description |
|:--------|:------------|
| `read(addr, n)` **function**            | Reads `n` number of bytes from the 16-bit address `addr`, and returns a **bytes object**.
| `write(addr,bytes[])`&nbsp;**function** | Writes all bytes from a given **bytes object** `bytes[]` to the 16-bit address `addr`.

#### Example
{: .no_toc }

```python
import fpga
fpga.read(0x1234, 5) # Reads 5 bytes from some FPGA register (0x1234 in this case)
fpga.write(0x1234, b'\x01\x02\x03') # Writes three bytes (1, 2, 3) to the FPGA register 0x1234
fpga.write(0x1234, b'hello fpga') # Writes the byte string 'hello fpga' to the FPGA register
fpga.write(0x1234, b'') # Doesn't write anything specific, but acts as a command or trigger
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

#### Example
{: .no_toc }

```python
import bluetooth
bluetooth.connected() # Returns True if the Bluetooth is connected. Always true when using the REPL, but useful for saved scripts
len = bluetooth.max_length() # Returns the maximum payload size we can send in one go

str = "hello world"
bluetooth.send(str[:len]) # Sends the string 'hello world' to the host. Limited by the maximum payload size

# Define a callback function which is triggered upon reception of Bluetooth data from the host
def fn(bytes):
    print(bytes)

bluetooth.receive_callback(fn) # Attaches the above function to the receive callback
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
| `ticks_diff(ticks1,ticks2)`&nbsp;**function**  | Returns the difference between two timestamps. i.e. `ticks1 - ticks2`, but takes into consideration if the numbers wrap around.

#### Example
{: .no_toc }

```python
import utime
time.sleep(1.5) # Sleeps for 1.5 seconds
time.sleep_ms(100) # Sleeps for 500ms
time.time(1681236168) # Sets the device system time using UTC timestamp
time.time() # Returns the current time (as a UTC timestamp), based on the system time
time.now() # Returns the current time as a human readable dictionary
```

---

### `update` - Monocle specific

> The update module allows for firmware upgrades of the MicroPython firmware, as well as the FPGA application over bluetooth. **This library use used automatically by the Brilliant REPL for firmware updates. You generally shouldn't need to call these manually, unless you're implementing your own update process.**

| Members | Description |
|:--------|:------------|
| `micropython()`&nbsp;**function** | Puts the device into over-the-air device firmware update mode. The device will stay in DFU mode for 5 minutes or until an update is finished being performed. The device will then restart with an updated MicroPython firmware.
| `Fpga` **class**                  | `Fpga` contains three low level functions which are used to update the FPGA. `Fpga.erase()` erases the existing application, `Fpga.write(bytes[])` sequentially writes in the new application, and `Fpga.read(address, length)` can be used to read back and verify the application. For details on how the FPGA application is updated, check out the [FPGA application updates](#fpga-application-updates) section.

#### Example
{: .no_toc }

```python
import update
update.micropython() # Reboots the device into update mode for updating the MicroPython firmware
```

---

### `gc`

> Standard MicroPython [garbage collection](https://docs.micropython.org/en/latest/library/gc.html) is supported.

#### Example
{: .no_toc }

```python
import gc

# Shows the current memory usage as a percentage
mem_used = gc.mem_alloc() / (gc.mem_alloc() + gc.mem_free())
print('{:d}%'.format(round(mem_used * 100)))

# Manually runs the garbage collector
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

> Standard MicroPython [IO streams](https://docs.micropython.org/en/latest/library/io.html) are supported.

### `ujson`

> Standard MicroPython [JSON handling](https://docs.micropython.org/en/latest/library/json.html) is supported.

### `uos`

> Standard MicroPython [operating system](https://docs.micropython.org/en/latest/library/os.html) services for file handling are supported.

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

For testing everything Bluetooth related, try our the nRF Connect App, for [desktop](https://www.nordicsemi.com/Products/Development-tools/nrf-connect-for-desktop), [Android](https://play.google.com/store/apps/details?id=no.nordicsemi.android.mcp&hl=en&gl=US), or [iOS](https://apps.apple.com/se/app/nrf-connect-for-mobile/id1054362403).

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

Within the Web REPL, firmware updates should show up automatically, and you'll be prompted to update. If it doesn't work. You can follow these steps:

1. Make sure you're using a Bluetooth enabled web browser such as Google Chrome on desktop, Android Chrome, or Bluefy on iOS.
1. Navigate to the repl at [repl.brilliant.xyz](https://repl.brilliant.xyz)
1. Take monocle out of the case. It should turn on.
1. Press any key in the repl to connect.
1. Select **monocle** from the Bluetooth menu that appears.
1. An update notification should appear at the bottom. Click it.
    
    If it doesn’t show up, you can force an update using the commands:

    ```python
    import update;update.micropython()
    ```
1. Monocle will disconnect, and you’ll see a message to reconnect again.
1. Press any key to reconnect and select **DFUTarg** from the Bluetooth menu.
1. The update should start, and you'll see the progress.
1. If anything goes wrong, simply try again.

---

Under the hood, the update `.zip` file is obtained from the [releases page](https://github.com/brilliantlabsAR/monocle-micropython/releases) of the *monocle-micropython* repository. After that Monocle is rebooted into device firmware update (DFU) mode where the Nordic DFU service handles the transfer of the file data. To read how the DFU mechanism works, you can check the Nordic documentation [here](https://infocenter.nordicsemi.com/topic/sdk_nrf5_v17.1.0/lib_dfu_transport_ble.html).

For testing everything Bluetooth related, try our the nRF Connect App, for [desktop](https://www.nordicsemi.com/Products/Development-tools/nrf-connect-for-desktop), [Android](https://play.google.com/store/apps/details?id=no.nordicsemi.android.mcp&hl=en&gl=US), or [iOS](https://apps.apple.com/se/app/nrf-connect-for-mobile/id1054362403).

### FPGA application updates
{: .no_toc }

FPGA application updates are automatically updated when using the Brilliant WebREPL.

For simplicity, the WebREPL encodes the application binary file to base-64 format, and simply sends the data over the raw REPL. The entire process is shown below.

```python
import device
import update
import ubinascii

# Erases the entire application
update.Fpga.erase()

# Send exactly 444430 bytes. Each write appends to the already written data
# There's no limitation on how many bytes you can send, but it should be
# tuned to match the host MTU length for a faster upload speed
update.Fpga.write(ubinascii.a2b_base64(b'TWFueSBoYW5kcyBtYWt...lIGxpZ2h0IHdvcmsu'))
...
update.Fpga.write(ubinascii.a2b_base64(b'yBtYWtTWFueSBoYW5kc...cmslIGxpZIHd2h0vu'))

# Write the special "done" flag at the end of the file
update.Fpga.write(b'done')

device.reset()
```
