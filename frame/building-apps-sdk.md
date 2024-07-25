---
title: Frame SDK Reference
description: A reference of Frame SDK functionality for building apps to talk to Frame AR glasses.
image: /images/frame/frame-splash.png
nav_order: 1
parent: Building Apps
grand_parent: Frame
nav_enabled: true

---

# Frame App SDK
{: .no_toc }

---

The most common structure is to build an iOS or Android mobile app which uses our SDKs to communicate with the Frame over Bluetooth.  Your app is in control and uses Frame as an accessory, with the Lua and BTLE details mostly abstracted away for you.

## Supported Platforms
{: .no_toc }

- [x] Python from a Mac, Linux, or Windows computer
- [ ] Swift from a Mac or iOS device
- [ ] Kotlin from Android
- [ ] Flutter for mobile (and computer?)
- [ ] React Native for mobile (and computer?)

### Status
{: .no_toc }

| Python            | Swift             | Kotlin            | Flutter           | React native      |
|:------------------|:------------------|:------------------|:------------------|:------------------|
| Available, mostly complete | Coming soon | Coming soon |  Coming soon | Coming soon |

---

* TOC
{:toc .text-epsilon}

---

## Installation

Installation of the SDK depends on the platform you are targeting.  For this section and all sections below, expand the platform you are targeting to see details specific to that platform.

### Python

The `frame-sdk` library is available [on PyPI](https://pypi.org/project/frame-sdk/).

```sh
pip3 install frame-sdk
```

<details markdown="block">
<summary>Using `frameutils` for Direct Bluetooth Communication</summary>
#### Using `frameutils` for Direct Bluetooth Communication
{: .no_toc }

{: .note }
The [`frame-utilities-for-python`](https://github.com/brilliantlabsAR/frame-utilities-for-python) package is for low-level communication with both Frame and Monocle devices and is a thin wrapper around the bluetooth connection (making use of [Bleak](https://github.com/hbldh/bleak) under the hood), plus some internal tools that are used in the firmware preparation process.  The [`frame-sdk`](https://github.com/OkGoDoIt/frame-sdk-python) package is a higher-level SDK that provides a more convenient way for developers to build apps for Frame.

While this page mainly documents the high-level SDK functionality in `frame-sdk`, you can also use the `frameutils` library as a lower-level interface to directly communicate with Frame over Bluetooth.

```python
import asyncio
from frameutils import Bluetooth

async def main():
    bluetooth = Bluetooth()
    await bluetooth.connect()

    print(await bluetooth.send_lua("print('hello world')", await_print=True))
    print(await bluetooth.send_lua('print(1 + 2)', await_print=True))

    await bluetooth.disconnect()

asyncio.run(main())
```
</details>

## Basic Communication

Where available, all Frame communication happens via async functions.

### Python SDK Basics

Make sure to `import asyncio` and only use Frame in async functions.  The Frame class handles the connection for you, all you have to do is wrap any code in `async with Frame() as frame:` and then use that `frame` object to call any of the functions.  Once that `frame` object goes out of scope (after the `with` statement or on an exception), the connection is automatically closed.

```python
import asyncio
from frame_sdk import Frame


async def main():
    # the with statement handles the connection and disconnection to Frame
    async with Frame() as frame:
        print("connected")
        # f is a connected Frame device, so you can call await f.<whatever>
        # for example, let's get the current battery level
        print(f"Frame battery: {await frame.get_battery_level()}%")

    # outside of the with statement, the connection is automatically closed
    print("disconnected")

# make sure you run it asynchronously
asyncio.run(main())
```

### Sending Lua to the Frame

```python
async frame.run_lua(lua_string: str, await_print: bool = False, checked: bool = False, timeout: Optional[float] = 10) -> Optional[str]
```

You can send Lua code to run on your Frame.  You do not need to worry about the MTU length, the SDK will handle breaking up the code for you if needed.  By default this returns immediately, but you can opt to wait until a response is printed back from the frame (up to a timeout limit).  This function also patches any Lua calls to `print()` so that you can return strings that are longer than the MTU limit.

* `lua_string` *(string)*: The code to execute, as a string.  For string literals, don't forget to escape quotes as needed.  There is no length limit, and multiple lines are supported.  If you want to return a value to your app via `await_print`, then make sure this code includes a `print()` statement.
* `await_print` *(boolean)*: Whether or not to wait until the Lua code executing on the Frame returns a value via a `print()` statement.  If `true`, then the code will block at this point up to `timeout` seconds.
* `checked` *(boolean)*: If the lua code is not expected to return a value, but you still want to block until completion to ensure it ran successfully, then set `checked`.  If `True`, then then the code will block at this point up to `timeout` seconds waiting for the Lua code to complete executing on the Frame.  If any errors are thrown on the Frame, an exception will be raised by the SDK.  If `False` (and also `await_print` is `False`), then this function returns immediately and your code continues running while the Lua code runs in parallel on the Frame.  However if there are any errors on the Frame (or if your Lua code contains syntax errors), you will not know about them.
* `timeout` *(None/null or float)*: If `None`/`null`, then the default timeout will be used.  If specified and either `await_print` or `checked` is `True`, then waits for a maximum of `timeout` seconds before raising a timeout error.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }

```python
async def run_lua(self, lua_string: str, await_print: bool = False, checked: bool = False, timeout: Optional[float] = 10) -> Optional[str]
```

Examples:

```python
# basic usage
await frame.run_lua("frame.display.text('Hello world', 50, 100);frame.display.show()")

# return data via print()
time_since_reboot = await frame.run_lua("print(frame.time.utc() .. \" seconds\")", await_print = True)
print(f"Frame has been on for {time_since_reboot}.")

# both the lua code you send and any replies sent back via print() can be of any length
print(await frame.run_lua("text = 'Look ma, no MTU limit! ';text=text..text;text=text..text;text=text..text;text=text..text;print(text)", await_print = True))

# let long running commands run in parallel
await frame.run_lua("spinning_my_wheels = 0;while true do;spinning_my_wheels=spinning_my_wheels+1;end", checked=False)
print("Frame is currently spinning its wheels, but python keeps going")

# raises a timeout exception after 10 seconds
await frame.run_lua("spinning_my_wheels = 0;while true do;spinning_my_wheels=spinning_my_wheels+1;end", checked=True, timeout=10)

# raises an exception with the Lua syntax error
await frame.run_lua("Syntax?:Who$needs!syntax?", checked=True)
```

</details>

### Evaluating a Lua expression on the Frame

```python
async frame.evaluate(lua_expression: str, timeout: Optional[float] = 10) -> str
```

Evaluates a single Lua expression on the Frame and returns the answer.  Equivalent to calling `run_lua(f"print(tostring({lua_expression}))",await_print=true)`.

As with `run_lua()`, you do not need to worry about the MTU limit in either direction.

* `lua_expression` *(string)*: The lua expression to evaluate.  This should not contain multiple statements, any control structures, calls to `print()`, etc.  Just an expression to evaluate and return.
* `timeout` *(None/null or float)*: If `None`/`null`, then the default timeout will be used.  Waits for a maximum of `timeout` seconds before raising a timeout error.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }

```python
async def evaluate(self, lua_expression: str, timeout: Optional[float] = 10) -> str
```

Examples:

```python
print(await frame.evaluate("1+2"))
# prints 3

print(await frame.evaluate("frame.battery_level() > 50"))
# prints True or False

print(await frame.evaluate("'w00t'"))
# prints w00t

# will throw an exception if there is no value returned or if there is a syntax error
print(await frame.evaluate("not_defined"))
```

</details>

---

## System Functions

### Get Battery Level

```python
async frame.get_battery_level() -> int
```

Gets the Frame battery level as an integer from 0 to 100.  Equivalent to `await self.evaluate("frame.battery_level()")`.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def get_battery_level(self) -> int
```

Example:

```python
print(f"Frame battery: {await frame.get_battery_level()}%")
```

</details>


### Sleep

```python
async frame.sleep(seconds: Optional[float])
```

Sleeps for a given number of seconds. If no argument is given, Frame will go to sleep until a tap gesture wakes it up.  This does not block, so your calling code will continue even while Frame sleeps.

* `seconds` *(optional float)*: Seconds do sleep at a float, such as 1.25 or 0.01.  If not specified (or `None`/`null`), Frame will go to sleep until a tap gesture wakes it up.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def sleep(self, seconds: Optional[float])
```

Examples:

```python
# wait for 5 seconds
await frame.sleep(5)
print("Frame is sleeping, but python is still running")

# wait until tapped
await frame.sleep()
print("Frame is sleeping, but python is still running")
```

</details>

### Stay Awake

```python
async frame.stay_awake(value: bool)
```

Prevents Frame from going to sleep while it's docked onto the charging cradle.  This can help during development where continuous power is needed, however may degrade the display or cause burn-in if used for extended periods of time.

There is no way to read the current value, only to set a new value.

* `value` *(boolean)*: `True` for Frame to stay awake while charging, `False` to reset to normal operation so Frame turns off while charging.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def stay_awake(self, value: bool)
```

Example:

```python
await frame.stay_awake(True)
# don't forget to turn this back off or you may damage your Frame
```

</details>

### Send Break Signal

```python
async frame.bluetooth.send_break_signal(show_me: boolean = False)
```

Sends a break signal to the device which will break any currently executing Lua script.

* `show_me` *(boolean)*: For debugging.  If `True`, the exact bytes sent to the device will be printed.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def send_break_signal(self, show_me:bool=False)
```

Example:
```python
await frame.run_lua("spinning_my_wheels = 0;while true do;spinning_my_wheels=spinning_my_wheels+1;end", checked=False)
print("Frame is currently spinning its wheels, but python keeps going")

await frame.bluetooth.send_break_signal()
print("Now Frame has been broken out of its loop and we can talk to it again")

print(await frame.evaluate("'I\\m back!'"))
# prints I'm back!
```

</details>

### Send Reset Signal

```python
async frame.bluetooth.send_reset_signal(show_me: boolean = False)
```

Sends a reset signal to the device which will reset the Lua virtual machine.  This clears all variables and functions, and resets the stack.  It does not clear the filesystem.

* `show_me` *(boolean)*: For debugging.  If `True`, the exact bytes sent to the device will be printed.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def send_reset_signal(self, show_me:bool=False)
```

Example:

```python
await frame.run_lua("data = 1", checked=True)
print(await frame.evaluate("data"))
# prints 1


await frame.bluetooth.send_reset_signal()
print("Frame has been reset")

print(await frame.evaluate("data"))
# raises an exception
# TODO: (or returns nil? not actually sure)
```

</details>

### Set Print Debugging

```python
frame.bluetooth.set_print_debugging(value: bool)
```

Sometimes it's useful for debugging to see all raw data that is transmitted to Frame, as well as the raw data received from Frame.  This function allows you to turn that on or off.

* `value` *(boolean)*: `True` to enable, `False` to disable.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
def set_print_debugging(self, value: bool)
```

Example:

```python
frame.bluetooth.set_print_debugging(True)
print(await frame.evaluate("'Hello world!'"))
# prints:
# b'print(\'Hello world!\')'
# Hello world!
```

</details>

### Wait For Data

```python
async frame.bluetooth.wait_for_data(timeout: float = 30.0) -> bytes
```

Blocks until data has been received from Frame [via `frame.bluetooth.send()`](/frame/building-apps-bluetooth-specs/#sending-data).  This is used for example when waiting for Frame to transmit data from a photo or audio.

This waits for bluetooth send data, not `print()` statements.  If you want to send data beyond what fits in the MTU, then you can send data in multiple chunks by prepending each chunk with `\001` (0x01) and sending a final chunk with `\002` (0x02).  You can optionally include the total chunk count in the final message for reliability checking (for example, if you send 3 chunks, then the final message should be `\0023`).

* `timeout` *(float)*: The maximum number of seconds to wait for data.  Defaults to 30 seconds.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def wait_for_data(self, timeout: float = 30.0) -> bytes
```

Examples:

```python
await frame.run_lua("""
local mtu = frame.bluetooth.max_length()
local f = frame.file.open("example_file.txt", "read")
local chunkIndex = 0
while true do
    local this_chunk = f:read(mtu-1)
    if this_chunk == nil then
        break
    end
    frame.bluetooth.send('\\001' .. this_chunk)
    chunkIndex = chunkIndex + 1
end
frame.bluetooth.send('\\002' .. chunkIndex)
""", checked=False)

full_file_data = await frame.bluetooth.wait_for_data()
print(full_file_data.decode())
```

</details>

---

## Filesystem

Filesystem functions are available via `Frame.files`.

### Write File

```python
async frame.files.write_file(path: str, data: bytes, checked: bool = False)
```

Write a file to the device's storage.  If the file already exists, it will be overwritten.  There are no length limits to the file, as it will be transferred reliably over multiple bluetooth transmissions.

* `path` *(string)*: The full filename to write on the Frame.  Even if no leading '/' is included, the path is relative to the root of the filesystem.
* `data` *(bytes)*: The data to write to the file.  If specifying as a string literal, don't forget to escape quotes as needed, and also to encode the string to bytes.
* `checked` *(boolean)*: If `True`, then each step of writing with wait for acknowledgement from the Frame before continuing.  This is more reliable but slower.  If `False`, then the file will be written fully asynchronously and without error checking.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def write_file(self, path: str, data: bytes, checked: bool = False)
```

Examples:

```python
await frame.files.write_file("example_file.txt", b"Hello \"real\" world", checked=True)

lyrics = "Never gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you"
await frame.files.write_file("/music/rick_roll.txt", lyrics.encode(), checked=True)

with open("icons.dat", "rb") as f:
    await frame.files.write_file("/sprites/icons.dat", f.read())
```

</details>

### Read File

```python
async frame.files.read_file(path: str) -> bytes
```

Reads a file from the device in full.  There are no length limits to the file, as it will be transferred reliably over multiple bluetooth transmissions.  Returns raw byte data.  If you want it as a string, then use `.decode()`.

Raises an exception if the file does not exist.

* `path` *(string)*: The full filename to read on the Frame.  Even if no leading '/' is included, the path is relative to the root of the filesystem.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def read_file(self, path: str) -> bytes
```

Examples:

```python
# print a text file
print(await frame.files.read_file("example_file.txt").decode())

# save a raw file locally
with open("~/blob.bin", "wb") as f:
    f.write(await frame.files.read_file("blob_on_frame.bin"))
```

</details>

### Delete File

```python
async frame.files.delete_file(path: str) -> bool
```

Delete a file on the device.  Returns `True` if the file was deleted, `False` if it didn't exist or failed to delete.

* `path` *(string)*: The full path to the file to delete.  Even if no leading '/' is included, the path is relative to the root of the filesystem.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def delete_file(self, path: str) -> bool
```

Examples:

```python
did_delete = await frame.files.delete_file("main.lua")
print(f"Deleted? {did_delete}")
```

</details>

### File Exists?
```python
async frame.files.file_exists(path: str) -> bool
```

Check if a file exists on the device.  Returns `True` if the file exists, `False` if it does not.  Does not work on directories, only files.

* `path` *(string)*: The full path to the file to check.  Even if no leading '/' is included, the path is relative to the root of the filesystem.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def file_exists(self, path: str) -> bool
```

Example:

```python
exists = await frame.files.file_exists("main.lua")
print(f"Main.lua {'exists' if exists else 'does not exist'}")
```

</details>

---

## Camera

Filesystem functions are available via `frame.camera`.

{: .note }
The `frame.camera.auto_sleep` function is currently ignored pending further testing, and may be removed in a future version.


### Take Photo

```python
async frame.camera.take_photo(autofocus_seconds: Optional[int] = 3, quality: int = MEDIUM_QUALITY, autofocus_type: str = AUTOFOCUS_TYPE_AVERAGE) -> bytes:
```

Take a photo with the camera and return the photo data in jpeg format as bytes.

By default, the image is rotated to the correct orientation and some metadata is added.  If you want to skip these, then set `frame.camera.auto_process_photo` to `False`.  This will result in a photo that is rotated 90 degrees clockwise and has no metadata.

* `autofocus_seconds` *(optional int)*: If `autofocus_seconds` is provided, the camera will attempt to set exposure and other setting automatically for the specified number of seconds before taking a photo.  Defaults to 3 seconds.  If you want to skip autofocus altogether, then set this to `None`/`null`.
* `quality` *(int)*: The quality of the photo to take.  Defaults to `frame.camera.MEDIUM_QUALITY`.  Values are `frame.camera.LOW_QUALITY` (10), `frame.camera.MEDIUM_QUALITY` (25), `frame.camera.HIGH_QUALITY` (50), and `frame.camera.FULL_QUALITY` (100).
* `autofocus_type` *(str)*: The type of autofocus to use.  Defaults to `frame.camera.AUTOFOCUS_TYPE_AVERAGE`.  Values are `frame.camera.AUTOFOCUS_TYPE_AVERAGE` ("AVERAGE"), `frame.camera.AUTOFOCUS_TYPE_SPOT` ("SPOT"), and `frame.camera.AUTOFOCUS_TYPE_CENTER_WEIGHTED` ("CENTER_WEIGHTED").


<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def take_photo(self, autofocus_seconds: Optional[int] = 3, quality: int = MEDIUM_QUALITY, autofocus_type: str = AUTOFOCUS_TYPE_AVERAGE) -> bytes
```

Examples:

```python
# take a photo
photo_bytes = await frame.camera.take_photo()

# take a photo with more control and save to disk
photo_bytes = await frame.camera.take_photo(autofocus_seconds=2, quality=frame.camera.HIGH_QUALITY, autofocus_type=frame.camera.AUTOFOCUS_TYPE_CENTER_WEIGHTED)
with open("photo.jpg", "wb") as file:
    file.write(photo_bytes)

# turn off auto-rotation and metadata
frame.camera.auto_process_photo = False
# take a very fast photo
photo_bytes = await frame.camera.take_photo(autofocus_seconds=None, quality=frame.camera.LOW_QUALITY)
print(len(photo_bytes))
```

</details>

### Save Photo

```python
async frame.camera.save_photo(path: str, autofocus_seconds: Optional[int] = 3, quality: int = MEDIUM_QUALITY, autofocus_type: str = AUTOFOCUS_TYPE_AVERAGE)
```

Take a photo with the camera and save it to disk as a jpeg image.  This is the same as calling `frame.camera.take_photo()` and then saving the bytes to disk.

By default, the image is rotated to the correct orientation and some metadata is added.  If you want to skip these, then set `frame.camera.auto_process_photo` to `False`.  This will result in a photo that is rotated 90 degrees clockwise and has no metadata.

* `path` *(string)*: The local path to save the photo.  The photo is always saved in jpeg format regardless of the extension you specify.
* `autofocus_seconds` *(optional int)*: If `autofocus_seconds` is provided, the camera will attempt to set exposure and other setting automatically for the specified number of seconds before taking a photo.  Defaults to 3 seconds.  If you want to skip autofocus altogether, then set this to `None`/`null`.
* `quality` *(int)*: The quality of the photo to take.  Defaults to `frame.camera.MEDIUM_QUALITY`.  Values are `frame.camera.LOW_QUALITY` (10), `frame.camera.MEDIUM_QUALITY` (25), `frame.camera.HIGH_QUALITY` (50), and `frame.camera.FULL_QUALITY` (100).
* `autofocus_type` *(str)*: The type of autofocus to use.  Defaults to `frame.camera.AUTOFOCUS_TYPE_AVERAGE`.  Values are `frame.camera.AUTOFOCUS_TYPE_AVERAGE` ("AVERAGE"), `frame.camera.AUTOFOCUS_TYPE_SPOT` ("SPOT"), and `frame.camera.AUTOFOCUS_TYPE_CENTER_WEIGHTED` ("CENTER_WEIGHTED").

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }

```python
async def save_photo(self, path: str, autofocus_seconds: Optional[int] = 3, quality: int = MEDIUM_QUALITY, autofocus_type: str = AUTOFOCUS_TYPE_AVERAGE)
```

Examples:

```python
# take a photo and save to disk
await f.camera.save_photo("frame-test-photo.jpg")

# or with more control
await f.camera.save_photo("frame-test-photo-2.jpg", autofocus_seconds=3, quality=f.camera.HIGH_QUALITY, autofocus_type=f.camera.AUTOFOCUS_TYPE_CENTER_WEIGHTED)
```

</details>

---

## Display

Display functions are available via `frame.display`.

The display engine of allows drawing of text, sprites and vectors. These elements can be layered atop one another simply in the order they are called, and then be displayed in one go using the `show()` function.

The Frame display is capable of rendering up to 16 colors at one time. These colors are preset by default, however each color can be overridden.  See more information about the [palette here](/frame/building-apps-lua/#color-palette).

### Write Text

```python
async frame.display.write_text(text: str, x: int = 1, y: int = 1, max_width: Optional[int] = 640, max_height: Optional[int] = None, align: Alignment = Alignment.TOP_LEFT)
```

Writes `text` to the display at the specified `x`,`y`position, optionally including word wrapping and alignment.  The text is not displayed until `frame.display.show()` is called.

* `x` *(int)*: The x position to write the text at.
* `y` *(int)*: The y position to write the text at.
* `max_width` *(optional int)*: The maximum width for the text bounding box.  If text is wider than this, it will be word-wrapped onto multiple lines automatically.  Set to the full width of the display by default (640px), but can be overridden with `None`/`null` to disable word-wrapping.
* `max_height` *(optional int)*: The maximum height for the text bounding box.  If text is taller than this, it will be cut off at that height.  Also useful for vertical alignment.  Set to the full height of the display by default (400px), but can be overridden with `None`/`null` to the vertical cutoff (which may result in errors if the text runs too far past the bottom of the display.
* `align` *(Alignment)*: The alignment of the text, both horizontally if a `max_width` is provided, and vertically if a `max_height` is provided.  Can be any value in `frame.display.Alignment`:
   * `frame.display.Alignment.TOP_LEFT` = "top_left" **(DEFAULT)**
   * `frame.display.Alignment.TOP_CENTER` = "top_center"
   * `frame.display.Alignment.TOP_RIGHT` = "top_right"
   * `frame.display.Alignment.MIDDLE_LEFT` = "middle_left"
   * `frame.display.Alignment.MIDDLE_CENTER` = "middle_center"
   * `frame.display.Alignment.MIDDLE_RIGHT` = "middle_right"
   * `frame.display.Alignment.BOTTOM_LEFT` = "bottom_left"
   * `frame.display.Alignment.BOTTOM_CENTER` = "bottom_center"
   * `frame.display.Alignment.BOTTOM_RIGHT` = "bottom_right"


<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def write_text(self, text: str, x: int = 1, y: int = 1, max_width: Optional[int] = 640, max_height: Optional[int] = None, align: Alignment = Alignment.TOP_LEFT):
```

Examples:

```python
await frame.display.write_text("Hello world", 50, 50)
await frame.display.show()

await frame.display.write_text("Top-left", align=Alignment.TOP_LEFT)
await frame.display.write_text("Top-Center", align=Alignment.TOP_CENTER)
await frame.display.write_text("Top-Right", align=Alignment.TOP_RIGHT)
await frame.display.write_text("Middle-Left", align=Alignment.MIDDLE_LEFT)
await frame.display.write_text("Middle-Center", align=Alignment.MIDDLE_CENTER)
await frame.display.write_text("Middle-Right", align=Alignment.MIDDLE_RIGHT)
await frame.display.write_text("Bottom-Left", align=Alignment.BOTTOM_LEFT)
await frame.display.write_text("Bottom-Center", align=Alignment.BOTTOM_CENTER)
await frame.display.write_text("Bottom-Right", align=Alignment.BOTTOM_RIGHT)
await frame.display.show()

await frame.display.write_text("I am longer text\nMultiple lines can be specified manually or word wrapping can occur automatically", align=Alignment.TOP_CENTER)
await frame.display.show()

# the following text will be horizontally and vertically centered within a box on the lower right of the screen
# draw the outline
await frame.display.draw_rect_filled(x=400, y=220, w=200, h=150, border_width=8, border_color=3, fill_color=15)
# draw the text
await frame.display.write_text("in the box", x=400, y=220, w=200, h=150, align=Alignment.MIDDLE_CENTER)
await frame.display.show()
```
</details>

### Show Text

```python
async frame.display.show_text(text: str, x: int = 1, y: int = 1, max_width: Optional[int] = 640, max_height: Optional[int] = None, align: Alignment = Alignment.TOP_LEFT)
```

`show_text` is the same as `write_text` except that it immediately displays the text on the screen.  It's equivalent to calling `frame.display.write_text()` and then `frame.display.show()`.

Note that each time you call `show_text()`, it will clear any previous text and graphics.  If you want to add text to the screen without erasing what's already there, then you should use `write_text()` instead.

### Scroll Text

```python
async frame.display.scroll_text(self, text: str, lines_per_frame: int = 5, delay: float = 0.12)
```

Animates scrolling text vertically.  Best when `text` is longer than the display height.  You can adjust the speed of the scroll by changing `lines_per_frame` and `delay`, but note that depending on how much text is on the screen, a `delay` below 0.12 seconds may result in graphical glitches due to hardware limitations.

This function blocks until the text has finished scrolling, and includes a small margin on time on either end to make sure the text is fully readable.

* `text` *(str)*: The text to scroll.  It is automatically wrapped to fit the display width.
* `lines_per_frame` *(int)*: The number of vertical pixels to scroll per frame.  Defaults to 5.  Higher values scroll faster, but will be more jumpy.
* `delay` *(float)*: The delay between frames in seconds.  Defaults to 0.12 seconds.  Lower values are faster, but may cause graphical glitches.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def scroll_text(self, text: str, lines_per_frame: int = 5, delay: float = 0.12)
```

Example:

```python
print("scrolling about to start")
await frame.display.scroll_text("Never gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nNever gonna stop\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you")
print("scrolling finished")

print("scrolling slowly about to start")
await frame.display.scroll_text("Never gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nNever gonna stop\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you", lines_per_frame=2)
print("scrolling slowly finished")
```

</details>

### Draw Rectangle

```python
frame.display.draw_rect(self, x: int, y: int, w: int, h: int, color: int = 1)
```

Draws a filled rectangle specified `color` at `x`,`y` with `w` width and `h` height.

The rectangle is drawn in the current buffer, which is not displayed until you call `frame.display.show()`.

Currently, the `x`, `y`, `w`, and `h` parameters are rounded down to the closest multiple of 8, for performance reasons.  This is likely to be changed in the future.

* `x` *(int)*: The x position of the upper-left corner of the rectangle.
* `y` *(int)*: The y position of the upper-left corner of the rectangle.
* `w` *(int)*: The width of the rectangle.
* `h` *(int)*: The height of the rectangle.
* `color` *(int)*: The color of the rectangle.  Defaults to 1 (white).

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def draw_rect(self, x: int, y: int, w: int, h: int, color: int = 1)
```

Example:

```python
# draws a white rectangle 200x200 pixels in the center of the screen
await frame.display.draw_rect(220, 100, 200, 200)

# draws a red rectangle 16x16 pixels in the center of the screen
await frame.display.draw_rect(320-8, 200-8, 16, 16, 3)

# show both rectangles
await frame.display.show()
```

</details>

### Draw Rectangle Filled

```python
frame.display.draw_rect_filled(self, x: int, y: int, w: int, h: int, border_width: int, border_color: int, fill_color: int)
```

Draws a filled rectangle with a border and fill color at `x`,`y` with `w` width and `h` height, with an inset border `border_width` pixels wide.  The total size of the rectangle including the border is `w`x`h`.

Currently, the `x`, `y`, `w`, `h`, and `border_width` parameters are rounded down to the closest multiple of 8, for performance reasons.  This is likely to be changed in the future.

* `x` *(int)*: The x position of the upper-left corner of the rectangle.
* `y` *(int)*: The y position of the upper-left corner of the rectangle.
* `w` *(int)*: The width of the rectangle.
* `h` *(int)*: The height of the rectangle.
* `border_width` *(int)*: The width of the border in pixels.
* `border_color` *(int)*: The color of the border.
* `fill_color` *(int)*: The color of the fill.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def draw_rect_filled(self, x: int, y: int, w: int, h: int, border_width: int, border_color: int, fill_color: int)
```

Example:

```python
# draws a dialog box with a border and text
await frame.display.draw_rect_filled(x=100, y=100, w=200, h=200, border_width=8, border_color=1, fill_color=15)
await frame.display.write_text("Hello world!", x=110, y=110, w=180, h=180, align=Alignment.MIDDLE_CENTER)
await frame.display.show()
```

</details>

### Additional Display Helpers

While the above functions are the most common ones you'll use, there are a few other display-related functions and properties that you may find useful on occasion.

#### Line Height
{: .no_toc }

```python
frame.display.line_height: int = 60
```

The `line_height` property is used to get and set the height of each line of text in pixels.  It is 60 by default, however you may override that value to change the vertical spacing of the text in all text displaying functions.

#### Get Text Width and Height
{: .no_toc }

```python
frame.display.get_text_width(text: str) -> int
frame.display.get_text_height(text: str) -> int
```

Gets the rendered width and height of text in pixels.  Text on Frame is variable width, so this is important for positioning text.  Note that these functions do not perform any text wrapping but do respect any manually-included line breaks, and you can use the outputs in your own word-wrapping or positioning logic.  The text height is affected by the `line_height` property.

#### Wrap Text
{: .no_toc }

```python
frame.display.wrap_text(self, text: str, max_width: int) -> str
```

Wraps text to fit within a specified width.  It does this by inserting line breaks at space characters, returning a string with extra '\n' characters where line wrapping is needed.

## Microphone

{: .warning }
The microphone functions have not yet been implemented.

## Motion

{: .warning }
The IMU functions have not yet been implemented.

# Putting It All Together

Here's a more comprehensive example of how to use the Frame SDK to build an app.

## Python

```python
import asyncio
from frame_sdk import Frame
from frame_sdk.display import Alignment
import datetime

async def main():
    # the with statement handles the connection and disconnection to Frame
    async with Frame() as f:
        # you can access the lower-level bluetooth connection via f.bluetooth, although you shouldn't need to do this often
        print(f"Connected: {f.bluetooth.is_connected()}")

        # let's get the current battery level
        print(f"Frame battery: {await f.get_battery_level()}%")

        # let's write (or overwrite) the file greeting.txt with "Hello world".
        # You can provide a bytes object or convert a string with .encode()
        await f.files.write_file("greeting.txt", b"Hello world")

        # And now we read that file back.
        # Note that we should convert the bytearray to a string via the .decode() method.
        print((await f.files.read_file("greeting.txt")).decode())
        
        # run_lua will automatically handle scripts that are too long for the MTU, so you don't need to worry about it.
        # It will also automatically handle responses that are too long for the MTU automatically.
        await f.run_lua("frame.display.text('Hello world', 50, 100);frame.display.show()")

        # evaluate is equivalent to f.run_lua("print(\"1+2\"), await_print=True)
        # It will also automatically handle responses that are too long for the MTU automatically.
        print(await f.evaluate("1+2"))

        # take a photo and save to disk
        await f.display.show_text("Taking photo...", align=Alignment.MIDDLE_CENTER)
        await f.camera.save_photo("frame-test-photo.jpg")
        await f.display.show_text("Photo saved!", align=Alignment.MIDDLE_CENTER)
        # or with more control
        await f.camera.save_photo("frame-test-photo-2.jpg", autofocus_seconds=3, quality=f.camera.HIGH_QUALITY, autofocus_type=f.camera.AUTOFOCUS_TYPE_CENTER_WEIGHTED)
        # or get the raw bytes
        photo_bytes = await f.camera.take_photo(autofocus_seconds=1)

        # Show the full palette
        width = 640 // 4
        height = 400 // 4
        for color in range(0, 16):
            tile_x = (color % 4)
            tile_y = (color // 4)
            await f.display.draw_rect(tile_x*width+1, tile_y*height+1, width, height, color)
            await f.display.write_text(f"{color}", tile_x*width+width//2+1, tile_y*height+height//2+1)
        await f.display.show()
        await asyncio.sleep(5)

        # scroll some long text
        await f.display.scroll_text("Never gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you")

        # display battery indicator and time as a home screen
        batteryPercent = await f.get_battery_level()
        # select a battery fill color from the default palette based on level
        color = 2 if batteryPercent < 20 else 6 if batteryPercent < 50 else 9
        # specify the size of the battery indicator in the top-right
        batteryWidth = 150
        batteryHeight = 75
        # draw the endcap of the battery
        await f.display.draw_rect(640-32,40 + batteryHeight//2-8, 32, 16, 1)
        # draw the battery outline
        await f.display.draw_rect_filled(640-16-batteryWidth, 40-8, batteryWidth+16, batteryHeight+16, 8, 1, 15)
        # fill the battery based on level
        await f.display.draw_rect(640-8-batteryWidth, 40, int(batteryWidth * 0.01 * batteryPercent), batteryHeight, color)
        # write the battery level
        await f.display.write_text(f"{batteryPercent}%", 640-8-batteryWidth, 40, batteryWidth, batteryHeight, Alignment.MIDDLE_CENTER)
        # write the time and date in the center of the screen
        await f.display.write_text(datetime.datetime.now().strftime("%-I:%M %p\n%a, %B %d, %Y"), align=Alignment.MIDDLE_CENTER)
        # now show what we've been drawing to the buffer
        await f.display.show()

    print("disconnected")

asyncio.run(main())

```
