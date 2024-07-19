---
title: Frame SDK Reference
description: A reference of Frame SDK functionality for building apps to talk to Frame AR glasses.
image: /images/frame/frame-splash.png
nav_order: 1
parent: Building Apps
---

# Frame App SDK
{: .no_toc }

---

The most common structure is to build an iOS or Android mobile app which uses our SDKs to communicate with the Frame over Bluetooth.  Your app is in control and uses Frame as an accessory, with the Lua and BTLE details mostly abstracted away for you.

## Supported Platforms

- [x] Python from a Mac, Linux, or Windows computer
- [ ] Swift from a Mac or iOS device
- [ ] Kotlin from Android
- [ ] Flutter for mobile (and computer?)
- [ ] React Native for mobile (and computer?)

### Status
| Python            | Swift             | Kotlin            | Flutter           | React native      |
|:------------------|:------------------|:------------------|:------------------|:------------------|
| Basic library available, full SDK in preview | Coming soon | Coming soon |  Coming soon | Coming soon |


## Installation

<details markdown="block">
<summary>Python</summary>

### Python

{: .warning }
The current version `0.1.11` on pip is pretty barebones.  This page refers to the newer preview that is currently [available on Github](https://github.com/OkGoDoIt/frame-utilities-for-python/tree/add-long-communication).

The `frameutils` library is available on pip.

```sh
pip3 install frameutils
```

</details>


## Basic Communication

Where available, all Frame communication happens via async functions.

<details markdown="block">
<summary>Python</summary>

### Python SDK Basics

Make sure to `import asyncio` and only use Frame in async functions.  The Frame class handles the connection for you, all you have to do is wrap any code in `async with Frame() as frame:` and then use that `frame` object to call any of the functions.  Once that `frame` object goes out of scope (after the `with` statement or on an exception), the connection is automatically closed.

```python
import asyncio
from frameutils import Frame


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

#### Using `frameutils` for Direct Bluetooth Communication

{: .note }
This is the only usage supported by the current version `0.1.11` on pip.  The rest of this SDK documentation is for the newer preview that is currently [available on Github](https://github.com/OkGoDoIt/frame-utilities-for-python/tree/add-long-communication).

The Bluetooth module of frameutils can be used to communicate with Frame from any Python desktop app. It makes use of [Bleak](https://github.com/hbldh/bleak) under the hood.

While this page mainly documents the high-level SDK functionality, you can also use the `frameutils` library as a lower-level interface to directly communicate with Frame over Bluetooth.

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
await(frame.run_lua("spinning_my_wheels = 0;while true do;spinning_my_wheels=spinning_my_wheels+1;end", checked=False))
print("Frame is currently spinning its wheels, but python keeps going")

# raises a timeout exception after 10 seconds
await(frame.run_lua("spinning_my_wheels = 0;while true do;spinning_my_wheels=spinning_my_wheels+1;end", checked=True, timeout=10))

# raises an exception with the Lua syntax error
await(frame.run_lua("Syntax?:Who$needs!syntax?", checked=True))
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

## System Functions

### Get Battery Level

```python
async frame.get_battery_level() -> int
```

Gets the Frame battery level as an integer from 0 to 100.  Equivalent to `await self.evaluate("frame.battery_level()")`.

<details markdown="block">
<summary>Python</summary>

#### Python
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
```python
async def send_break_signal(self, show_me:bool=False)
```

Example:
```python
await(frame.run_lua("spinning_my_wheels = 0;while true do;spinning_my_wheels=spinning_my_wheels+1;end", checked=False))
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

Blocks until data has been received from Frame via `frame.bluetooth.send()`.  This is used for example when waiting for Frame to transmit data from a photo or audio.

TODO: link to documentation for sending data
This waits for bluetooth send data, not `print()` statements.  If you want to send data beyond what fits in the MTU, then you can send data in multiple chunks by prepending each chunk with `\001` (0x01) and sending a final chunk with `\002` (0x02).  You can optionally include the total chunk count in the final message for reliability checking (for example, if you send 3 chunks, then the final message should be `\0023`).

* `timeout` *(float)*: The maximum number of seconds to wait for data.  Defaults to 30 seconds.

<details markdown="block">
<summary>Python</summary>

#### Python
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

## Filesystem

Filesystem functions are available via `Frame.files`.

### Write File

```python
async frame.file.write_file(path: str, data: bytes, checked: bool = False)
```

Write a file to the device's storage.  If the file already exists, it will be overwritten.  There are no length limits to the file, as it will be transferred reliably over multiple bluetooth transmissions.

* `path` *(string)*: The full filename to write on the Frame.  Even if no leading '/' is included, the path is relative to the root of the filesystem.
* `data` *(bytes)*: The data to write to the file.  If specifying as a string literal, don't forget to escape quotes as needed, and also to encode the string to bytes.
* `checked` *(boolean)*: If `True`, then each step of writing with wait for acknowledgement from the Frame before continuing.  This is more reliable but slower.  If `False`, then the file will be written fully asynchronously and without error checking.

<details markdown="block">
<summary>Python</summary>

#### Python
```python
async def write_file(self, path: str, data: bytes, checked: bool = False)
```

Examples:

```python
await frame.file.write_file("example_file.txt", b"Hello \"real\" world", checked=True)

lyrics = "Never gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you"
await frame.file.write_file("/music/rick_roll.txt", lyrics.encode(), checked=True)

with open("icons.dat", "rb") as f:
    await frame.file.write_file("/sprites/icons.dat", f.read())
```

</details>

### Read File

```python
async frame.file.read_file(path: str) -> bytes
```

Reads a file from the device in full.  There are no length limits to the file, as it will be transferred reliably over multiple bluetooth transmissions.  Returns raw byte data.  If you want it as a string, then use `.decode()`.

Raises an exception if the file does not exist.

* `path` *(string)*: The full filename to read on the Frame.  Even if no leading '/' is included, the path is relative to the root of the filesystem.

<details markdown="block">
<summary>Python</summary>

#### Python
```python
async def read_file(self, path: str) -> bytes
```

Examples:

```python
# print a text file
print(await frame.file.read_file("example_file.txt").decode())

# save a raw file locally
with open("~/blob.bin", "wb") as f:
    f.write(await frame.file.read_file("blob_on_frame.bin"))
```

</details>

### Delete File

```python
async frame.file.delete_file(path: str) -> bool
```

Delete a file on the device.  Returns `True` if the file was deleted, `False` if it didn't exist or failed to delete.

* `path` *(string)*: The full path to the file to delete.  Even if no leading '/' is included, the path is relative to the root of the filesystem.

#### Python
```python
async def delete_file(self, path: str) -> bool
```

Examples:

```python
did_delete = await frame.file.delete_file("main.lua")
print(f"Deleted? {did_delete}")
```

</details>

### File Exists?
```python
async frame.file.file_exists(path: str) -> bool
```

Check if a file exists on the device.  Returns `True` if the file exists, `False` if it does not.  Does not work on directories, only files.

* `path` *(string)*: The full path to the file to check.  Even if no leading '/' is included, the path is relative to the root of the filesystem.

<details markdown="block">
<summary>Python</summary>

#### Python
```python
async def file_exists(self, path: str) -> bool
```

Example:

```python
exists = await frame.file.file_exists("main.lua")
print(f"Main.lua {'exists' if exists else 'does not exist'}")
```

</details>

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

## Display

{ .note }
The display functions are currently in a private branch for further testing and will be added soon.

## Microphone

{ .warning }
The microphone functions have not yet been written.

## Motion

{ .warning }
The IMU functions have not yet been written.

