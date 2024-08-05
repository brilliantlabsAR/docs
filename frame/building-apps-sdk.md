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
- [x] Flutter for mobile (iOS and Android)
- [ ] React Native for mobile (and computer?)

For each section below, you may expand the platform you are targeting to see details specific to that platform, including function signatures and examples.

### Status
{: .no_toc }

| Python            | Swift             | Kotlin            | Flutter           | React Native      |
|:------------------|:------------------|:------------------|:------------------|:------------------|
| [![Available on PyPI](https://img.shields.io/pypi/v/frame_sdk)](https://pypi.org/project/frame-sdk/) | Coming soon | Coming soon | [![Available on Pub.dev](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FOkGoDoIt%2Fframe-sdk-flutter%2Fmaster%2Fpubspec.yaml&query=version&prefix=v&label=pub.dev)](https://pub.dev/packages/frame_sdk) | Coming soon |

The Python SDK is feature-complete, but will be updated continuously as the underlying platform capabilities change.

The Flutter SDK is an early preview and may be incomplete or unstable.  Please report any issues to us on discord and we will fix them ASAP.

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

### Flutter

The `frame_sdk` library is available [on pub.dev](https://pub.dev/packages/frame_sdk).

```sh
flutter pub add frame_sdk
```

## Basic Communication

Where available, most Frame communication happens via async functions.

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

### Flutter SDK Basics

Make sure to `import 'package:frame_sdk/frame_sdk.dart';`.  You may also need to import `package:frame_sdk/bluetooth.dart`, `package:frame_sdk/display.dart`, `package:frame_sdk/camera.dart`, or `package:frame_sdk/motion.dart` to access types, enums, and constants.

At some point early in your app's execution, you should call `BrilliantBluetooth.requestPermission();` to prompt the user to provide Bluetooth permission.

You can see an example Flutter usage in [the package's example page](https://pub.dev/packages/frame_sdk/example).  Here's a very simplified example:

```dart
// other imports
import 'package:frame_sdk/frame_sdk.dart';

void main() {
  // Request bluetooth permission
  BrilliantBluetooth.requestPermission();
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  late final Frame frame;

  @override
  void initState() {
    super.initState();
    initPlatformState();
    frame = Frame();

    runExample();
  }

  Future<void> runExample() async {
    // connect
    await frame.connect();
    // Check if connected
    print("Connected: ${frame.isConnected}");
    // Get battery level
    int batteryLevel = await frame.getBatteryLevel();
    print("Frame battery: $batteryLevel%");

    // ... continue here ...
  }

  // Future<void> initPlatformState() and other boilerplate flutter here
}
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

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }

```dart
Future<String?> runLua(String luaString,
      {bool awaitPrint = false,
      bool checked = false,
      Duration? timeout,
      bool withoutHelpers = false}) async
```

Examples:

```dart
// basic usage
await frame.runLua("frame.display.text('Hello world', 50, 100);frame.display.show()");

// return data via print()
String curTime = await frame.runLua("print(frame.time.utc())", awaitPrint: true);
print("Frame epoch time is $curTime.");

// both the lua code you send and any replies sent back via print() can be of any length
print(await frame.runLua("text = 'Look ma, no MTU limit! ';text=text..text;text=text..text;text=text..text;text=text..text;print(text)", awaitPrint: true));

// let long running commands run in parallel
await frame.runLua("spinning_my_wheels = 0;while true do;spinning_my_wheels=spinning_my_wheels+1;end", checked: false);
print("Frame is currently spinning its wheels, but Dart keeps going");

// raises a timeout exception after 10 seconds
await frame.runLua("spinning_my_wheels = 0;while true do;spinning_my_wheels=spinning_my_wheels+1;end", checked: true, timeout: Duration(seconds: 10));

// raises an exception with a Lua syntax error
await frame.runLua("Syntax?:Who\$needs!syntax?", checked: true);
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


<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }

```dart
Future<String> evaluate(String luaExpression) async
```

Examples:

```dart
print(await frame.evaluate("1+2"));
// prints 3

print(await frame.evaluate("frame.battery_level() > 50"));
// prints True or False

print(await frame.evaluate("'w00t'"));
// prints w00t

// will throw an exception if there is no value returned or if there is a syntax error
print(await frame.evaluate("not_defined"));
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

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<int> getBatteryLevel()
```

Example:

```dart
int batteryLevel = await frame.getBatteryLevel();
print("Frame battery: $batteryLevel%");
```

</details>

### Delay

```python
async frame.delay(seconds: float)
```

Delays execution on Frame for a given number of seconds.  Technically this sends a sleep command, but it doesn't actually change the power mode.  This function does not block, returning immediately.

* `seconds` *(float)*: Seconds to delay.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def delay(self, seconds: float)
```

Examples:

```python
# wait for 5 seconds
await frame.delay(5)
print("Frame is paused, but python is still running")
```

</details>

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<void> delay(double seconds)
```

Examples:

```dart
// wait for 5 seconds
await frame.delay(5);
print("Frame is paused, but Dart is still running");
```

</details>

### Sleep

```python
async frame.sleep(deep_sleep: bool = False) -> None
```

Puts the Frame into sleep mode.  There are two modes: normal and deep.

Normal sleep mode can still receive bluetooth data, and is essentially the same as clearing the display and putting the camera in low power mode.  The Frame will retain the time and date, and any functions and variables will stay in memory.

Deep sleep mode saves additional power, but has more limitations.  The Frame will not retain the time and date, and any functions and variables will not stay in memory.  Blue data will not be received.  The only way to wake the Frame from deep sleep is to tap it.

The difference in power usage is fairly low, so it's often best to use normal sleep mode unless you need the extra power savings.

* `deep_sleep` *(boolean)*: `True` for deep sleep, `False` for normal sleep.  Defaults to `False`.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }

```python
async def sleep(self, deep_sleep: bool = False) -> None
```

Examples:

```python
# put the Frame into normal sleep mode
await frame.sleep()

# put the Frame into deep sleep mode
await frame.sleep(True)
```

</details>

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }

```dart
Future<void> sleep({bool deepSleep = false})
```

Examples:

```dart
// put the Frame into normal sleep mode
await frame.sleep();

// put the Frame into deep sleep mode
await frame.sleep(deepSleep: true);
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

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<void> stayAwake(bool value)
```

Example:

```dart
await frame.stayAwake(true);
// don't forget to turn this back off or you may damage your Frame
```

</details>

### Send Break Signal

```python
async frame.bluetooth.send_break_signal()
```

Sends a break signal to the device which will break any currently executing Lua script.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def send_break_signal(self)
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

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<void> sendBreakSignal()
```

Example:
```dart
await frame.runLua("spinning_my_wheels = 0;while true do;spinning_my_wheels=spinning_my_wheels+1;end", checked: false);
print("Frame is currently spinning its wheels, but Dart keeps going");

await frame.bluetooth.sendBreakSignal();
print("Now Frame has been broken out of its loop and we can talk to it again");

print(await frame.evaluate("'I\\'m back!'"));
// prints I'm back!
```

</details>

### Send Reset Signal

```python
async frame.bluetooth.send_reset_signal()
```

Sends a reset signal to the device which will reset the Lua virtual machine.  This clears all variables and functions, and resets the stack.  It does not clear the filesystem.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def send_reset_signal(self)
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

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<void> sendResetSignal()
```

Example:

```dart
await frame.runLua("data = 1", checked: true);
print(await frame.evaluate("data"));
// prints 1


await frame.bluetooth.sendResetSignal();
print("Frame has been reset");

print(await frame.evaluate("data"));
// raises an exception
// TODO: (or returns nil? not actually sure)
```

</details>

### Run On Wake

```python
async frame.run_on_wake(lua_script: Optional[str] = None, callback: Optional[Callable[[], None ]] = None) -> None
```

Runs the specified lua_script and/or callback when the Frame wakes up from sleep (via a tap gesture).  This allows your to define the "home "screen", for example by displaying the battery or time when the frame is woken.  In the Noa app, this is where you see the "Tap me in..." message.

Any `lua_script` or `callback` will clear any previously set run on wake commands.  To remove all run on wake commands, pass `None`/`null` for both `lua_script` and `callback`.

* `lua_script` *(string)*: The lua script to run on the Frame when the Frame wakes up.  This runs even if the Frame is not connected via bluetooth at the time of the wakeup.
* `callback` *(callable)*: A callback function locally to run when the Frame wakes up.  This will only run if the Frame is connected via bluetooth at the time of the wakeup.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def run_on_wake(self, lua_script: Optional[str] = None, callback: Optional[Callable[[], None ]] = None) -> None
```

Example:

```python
# set a wake screen via script, so when you tap to wake the frame, it shows the battery level and then goes back to sleep after 10 seconds of inactivity
await f.run_on_wake(lua_script="""frame.display.text('Battery: ' .. frame.battery_level() ..  '%', 10, 10);
                    frame.display.show();
                    frame.sleep(10);
                    frame.display.text(' ',1,1);
                    frame.display.show();
                    frame.sleep()""")
```

</details>

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<void> runOnWake({String? luaScript, void Function()? callback})
```

Example:

```dart
// set a wake screen via script, so when you tap to wake the frame, it shows the battery level and then goes back to sleep after 10 seconds of inactivity
await frame.runOnWake(
  luaScript: """frame.display.text('Battery: ' .. frame.battery_level() ..  '%', 10, 10);
                    frame.display.show();
                    frame.sleep(10);
                    frame.display.text(' ',1,1);
                    frame.display.show();
                    frame.sleep()""",
);
```

</details>

### Set Print Debugging (Python)

```python
frame.bluetooth.set_print_debugging(value: bool)
```

In Python, sometimes it's useful for debugging to see all raw data that is transmitted to Frame, as well as the raw data received from Frame.  This function allows you to turn that on or off.

For Flutter, debug info is logged to the Logger, so set the log level or subscribe to the logger to see logging instead.

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

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<Uint8List> waitForData({Duration timeout = const Duration(seconds: 30)})
```

Examples:

```dart
await frame.runLua("""
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
""", checked: false);

Uint8List full_file_data = await frame.bluetooth.waitForData();
print(utf8.decode(full_file_data));
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

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<void> writeFile(String path, Uint8List data, {bool checked = false})
```

Example:

```dart
await frame.files.writeFile("example_file.txt", utf8.encode('Hello "real" world'), checked: true);

String lyrics = "Never gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you";
await frame.files.writeFile("/music/rick_roll.txt", utf8.encode(lyrics), checked: true);

ByteData data = await rootBundle.load('assets/icons.dat');
await frame.files.writeFile("/sprites/icons.dat", data.buffer.asUint8List());
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

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<Uint8List> readFile(String path)
```

Example:

```dart
String fileContent = utf8.decode(await frame.files.readFile("greeting.txt"));
print(fileContent);
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

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<bool> deleteFile(String path)
```

Example:

```dart
bool didDelete = await frame.files.deleteFile("main.lua");
print("Deleted? $didDelete");
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

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<bool> fileExists(String path)
```

Example:

```dart
bool exists = await frame.files.fileExists("main.lua");
print("Main.lua ${exists ? 'exists' : 'does not exist'}");
```

</details>

---

## Camera

Filesystem functions are available via `frame.camera`.

{: .note }
The `frame.camera.auto_sleep` function is currently ignored pending further testing, and may be removed in a future version.


### Take Photo

```python
async frame.camera.take_photo(autofocus_seconds: Optional[int] = 3, quality: Quality = Quality.MEDIUM, autofocus_type: AutofocusType = AutofocusType.AVERAGE) -> bytes:
```

Take a photo with the camera and return the photo data in jpeg format as bytes.

By default, the image is rotated to the correct orientation and some metadata is added.  If you want to skip these, then set `frame.camera.auto_process_photo` to `False`.  This will result in a photo that is rotated 90 degrees clockwise and has no metadata.

You'll need to import `Quality` and `AutofocusType` from `frame.camera` to use these.

* `autofocus_seconds` *(optional int)*: If `autofocus_seconds` is provided, the camera will attempt to set exposure and other setting automatically for the specified number of seconds before taking a photo.  Defaults to 3 seconds.  If you want to skip autofocus altogether, then set this to `None`/`null`.
* `quality` *(Quality)*: The quality of the photo to take.  Defaults to `Quality.MEDIUM`.  Values are `Quality.LOW` (10), `Quality.MEDIUM` (25), `Quality.HIGH` (50), and `Quality.FULL` (100).
* `autofocus_type` *(AutofocusType)*: The type of autofocus to use.  Defaults to `AutofocusType.AVERAGE`.  Values are `AutofocusType.AVERAGE` ("AVERAGE"), `AutofocusType.SPOT` ("SPOT"), and `AutofocusType.CENTER_WEIGHTED` ("CENTER_WEIGHTED").


<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def take_photo(self, autofocus_seconds: Optional[int] = 3, quality: Quality = Quality.MEDIUM, autofocus_type: AutofocusType = AutofocusType.AVERAGE) -> bytes
```

Examples:

```python
from frame_sdk.camera import Quality, AutofocusType

# take a photo
photo_bytes = await frame.camera.take_photo()

# take a photo with more control and save to disk
photo_bytes = await frame.camera.take_photo(autofocus_seconds=2, quality=Quality.HIGH, autofocus_type=AutofocusType.CENTER_WEIGHTED)
with open("photo.jpg", "wb") as file:
    file.write(photo_bytes)

# turn off auto-rotation and metadata
frame.camera.auto_process_photo = False
# take a very fast photo
photo_bytes = await frame.camera.take_photo(autofocus_seconds=None, quality=Quality.LOW)
print(len(photo_bytes))
```

</details>

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<Uint8List> takePhoto({int? autofocusSeconds = 3, PhotoQuality quality = PhotoQuality.medium, AutoFocusType autofocusType = AutoFocusType.average}) async
```

Examples:

```dart
import 'package:frame/camera.dart';

// Take a photo
Uint8List photoBytes = await frame.camera.takePhoto();

// Take a photo with more control
Uint8List photoBytes = await frame.camera.takePhoto(
  autofocusSeconds: 2,
  quality: PhotoQuality.high,
  autofocusType: AutoFocusType.centerWeighted
);

// Turn off auto-rotation and metadata
frame.camera.autoProcessPhoto = false;
// Take a very fast photo
Uint8List photoBytes = await frame.camera.takePhoto(
  autofocusSeconds: null,
  quality: PhotoQuality.low
);
print(photoBytes.length);
```

</details>

### Save Photo

```python
async frame.camera.save_photo(path: str, autofocus_seconds: Optional[int] = 3, quality: Quality = Quality.MEDIUM, autofocus_type: AutofocusType = AutofocusType.AVERAGE)
```

Take a photo with the camera and save it to disk as a jpeg image.  This is the same as calling `frame.camera.take_photo()` and then saving the bytes to disk.

By default, the image is rotated to the correct orientation and some metadata is added.  If you want to skip these, then set `frame.camera.auto_process_photo` to `False`.  This will result in a photo that is rotated 90 degrees clockwise and has no metadata.

You'll need to import `Quality` and `AutofocusType` from `frame.camera` to use these.

* `path` *(string)*: The local path to save the photo.  The photo is always saved in jpeg format regardless of the extension you specify.
* `autofocus_seconds` *(optional int)*: If `autofocus_seconds` is provided, the camera will attempt to set exposure and other setting automatically for the specified number of seconds before taking a photo.  Defaults to 3 seconds.  If you want to skip autofocus altogether, then set this to `None`/`null`.
* `quality` *(Quality)*: The quality of the photo to take.  Defaults to `Quality.MEDIUM`.  Values are `Quality.LOW` (10), `Quality.MEDIUM` (25), `Quality.HIGH` (50), and `Quality.FULL` (100).
* `autofocus_type` *(AutofocusType)*: The type of autofocus to use.  Defaults to `AutofocusType.AVERAGE`.  Values are `AutofocusType.AVERAGE` ("AVERAGE"), `AutofocusType.SPOT` ("SPOT"), and `AutofocusType.CENTER_WEIGHTED` ("CENTER_WEIGHTED").

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }

```python
async def save_photo(self, path: str, autofocus_seconds: Optional[int] = 3, quality: Quality = Quality.MEDIUM, autofocus_type: AutofocusType = AutofocusType.AVERAGE)
```

Examples:

```python
from frame_sdk.camera import Quality, AutofocusType

# take a photo and save to disk
await f.camera.save_photo("frame-test-photo.jpg")

# or with more control
await f.camera.save_photo("frame-test-photo-2.jpg", autofocus_seconds=3, quality=Quality.HIGH, autofocus_type=AutofocusType.CENTER_WEIGHTED)
```

</details>

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<void> savePhoto(String path, {int? autofocusSeconds = 3, PhotoQuality quality = PhotoQuality.medium, AutoFocusType autofocusType = AutoFocusType.average}) async
```

Examples:

```dart
import 'package:frame/camera.dart';

// take a photo and save to disk
await frame.camera.savePhoto("frame-test-photo.jpg");

// or with more control
await frame.camera.savePhoto(
  "frame-test-photo-2.jpg",
  autofocusSeconds: 3,
  quality: PhotoQuality.high,
  autofocusType: AutoFocusType.centerWeighted
);

```

</details>

---

## Display

Display functions are available via `frame.display`.

The display engine of allows drawing of text, sprites and vectors. These elements can be layered atop one another simply in the order they are called, and then be displayed in one go using the `show()` function.

The Frame display is capable of rendering up to 16 colors at one time. These colors are preset by default, however each color can be overridden.  See more information about the [palette here](/frame/building-apps-lua/#color-palette).

### Write Text

```python
async frame.display.write_text(text: str, x: int = 1, y: int = 1, max_width: Optional[int] = 640, max_height: Optional[int] = None, align: Alignment = Alignment.TOP_LEFT, color: PaletteColors = PaletteColors.WHITE)
```

Writes `text` to the display at the specified `x`,`y`position, optionally including word wrapping and alignment.  The text is not displayed until `frame.display.show()` is called.

* `x` *(int)*: The x position to write the text at.
* `y` *(int)*: The y position to write the text at.
* `max_width` *(optional int)*: The maximum width for the text bounding box.  If text is wider than this, it will be word-wrapped onto multiple lines automatically.  Set to the full width of the display by default (640px), but can be overridden with `None`/`null` to disable word-wrapping.
* `max_height` *(optional int)*: The maximum height for the text bounding box.  If text is taller than this, it will be cut off at that height.  Also useful for vertical alignment.  Set to the full height of the display by default (400px), but can be overridden with `None`/`null` to the vertical cutoff (which may result in errors if the text runs too far past the bottom of the display.
* `align` *(Alignment)*: The alignment of the text, both horizontally if a `max_width` is provided, and vertically if a `max_height` is provided.  Can be any value in `frame.display.Alignment`:
   * `frame.display.Alignment.TOP_LEFT` = Alignment.TOP_LEFT **(DEFAULT)**
   * `frame.display.Alignment.TOP_CENTER` = Alignment.TOP_CENTER
   * `frame.display.Alignment.TOP_RIGHT` = Alignment.TOP_RIGHT
   * `frame.display.Alignment.MIDDLE_LEFT` = Alignment.MIDDLE_LEFT
   * `frame.display.Alignment.MIDDLE_CENTER` = Alignment.MIDDLE_CENTER
   * `frame.display.Alignment.MIDDLE_RIGHT` = Alignment.MIDDLE_RIGHT
   * `frame.display.Alignment.BOTTOM_LEFT` = Alignment.BOTTOM_LEFT
   * `frame.display.Alignment.BOTTOM_CENTER` = Alignment.BOTTOM_CENTER
   * `frame.display.Alignment.BOTTOM_RIGHT` = Alignment.BOTTOM_RIGHT
* `color` *(PaletteColors)*: The color of the text.  Defaults to `PaletteColors.WHITE`.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def write_text(self, text: str, x: int = 1, y: int = 1, max_width: Optional[int] = 640, max_height: Optional[int] = None, align: Alignment = Alignment.TOP_LEFT, color: PaletteColors = PaletteColors.WHITE):
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
await frame.display.draw_rect_filled(x=400, y=220, w=200, h=150, border_width=8, border_color=PaletteColors.RED, fill_color=PaletteColors.CLOUDBLUE)
# draw the text
await frame.display.write_text("in the box", x=400, y=220, w=200, h=150, align=Alignment.MIDDLE_CENTER, color=PaletteColors.YELLOW)
await frame.display.show()
```
</details>


<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<void> writeText(String text,
    {int x = 1,
    int y = 1,
    int? maxWidth = 640,
    int? maxHeight,
    PaletteColors? color,
    Alignment2D align = Alignment2D.topLeft})
```

Examples:

```dart
await frame.display.writeText("Hello world", x: 50, y: 50);
await frame.display.show();

await frame.display.writeText("Top-left", align: Alignment2D.topLeft);
await frame.display.writeText("Top-Center", align: Alignment2D.topCenter);
await frame.display.writeText("Top-Right", align: Alignment2D.topRight);
await frame.display.writeText("Middle-Left", align: Alignment2D.middleLeft);
await frame.display.writeText("Middle-Center", align: Alignment2D.middleCenter);
await frame.display.writeText("Middle-Right", align: Alignment2D.middleRight);
await frame.display.writeText("Bottom-Left", align: Alignment2D.bottomLeft);
await frame.display.writeText("Bottom-Center", align: Alignment2D.bottomCenter);
await frame.display.writeText("Bottom-Right", align: Alignment2D.bottomRight);
await frame.display.show();

await frame.display.writeText(
    "I am longer text\nMultiple lines can be specified manually or word wrapping can occur automatically",
    align: Alignment2D.topCenter);
await frame.display.show();

// the following text will be horizontally and vertically centered within a box on the lower right of the screen
// draw the outline
await frame.display.drawRectFilled(
    x: 400, y: 220, w: 200, h: 150, borderWidth: 8, borderColor: PaletteColors.red, fillColor: PaletteColors.white);
// draw the text
await frame.display.writeText("in the box", x: 400, y: 220, maxWidth: 200, maxHeight: 150, align: Alignment2D.middleCenter, color: PaletteColors.yellow);
await frame.display.show();
```
</details>


### Show Text

```python
async frame.display.show_text(text: str, x: int = 1, y: int = 1, max_width: Optional[int] = 640, max_height: Optional[int] = None, align: Alignment = Alignment.TOP_LEFT, color: PaletteColors = PaletteColors.WHITE)
```

`show_text` is the same as `write_text` except that it immediately displays the text on the screen.  It's equivalent to calling `frame.display.write_text()` and then `frame.display.show()`.

Note that each time you call `show_text()`, it will clear any previous text and graphics.  If you want to add text to the screen without erasing what's already there, then you should use `write_text()` instead.

### Scroll Text

```python
async frame.display.scroll_text(text: str, lines_per_frame: int = 5, delay: float = 0.12, color: PaletteColors = PaletteColors.WHITE)
```

Animates scrolling text vertically.  Best when `text` is longer than the display height.  You can adjust the speed of the scroll by changing `lines_per_frame` and `delay`, but note that depending on how much text is on the screen, a `delay` below 0.12 seconds may result in graphical glitches due to hardware limitations.

This function blocks until the text has finished scrolling, and includes a small margin on time on either end to make sure the text is fully readable.

* `text` *(str)*: The text to scroll.  It is automatically wrapped to fit the display width.
* `lines_per_frame` *(int)*: The number of vertical pixels to scroll per frame.  Defaults to 5.  Higher values scroll faster, but will be more jumpy.
* `delay` *(float)*: The delay between frames in seconds.  Defaults to 0.12 seconds.  Lower values are faster, but may cause graphical glitches.
* `color` *(PaletteColors)*: The color of the text.  Defaults to `PaletteColors.WHITE`.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def scroll_text(self, text: str, lines_per_frame: int = 5, delay: float = 0.12, color: PaletteColors = PaletteColors.WHITE)
```

Example:

```python
print("scrolling about to start")
await frame.display.scroll_text("Never gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nNever gonna stop\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you")
print("scrolling finished")

print("scrolling slowly about to start")
await frame.display.scroll_text("Never gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nNever gonna stop\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you", lines_per_frame=2, color=PaletteColors.YELLOW)
print("scrolling slowly finished")
```

</details>

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<void> scrollText(String text, {int linesPerFrame = 5, double delay = 0.12, PaletteColors? textColor}) async
```

Example:

```dart
print("scrolling about to start");
await frame.display.scrollText("Never gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nNever gonna stop\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you");
print("scrolling finished");

print("scrolling slowly about to start");
await frame.display.scrollText("Never gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you\nNever gonna stop\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you", linesPerFrame: 2, textColor: PaletteColors.yellow);
print("scrolling slowly finished");
```

</details>

### Draw Rectangle

```python
frame.display.draw_rect(x: int, y: int, w: int, h: int, color: PaletteColors = PaletteColors.WHITE)
```

Draws a filled rectangle specified `color` at `x`,`y` with `w` width and `h` height.

The rectangle is drawn in the current buffer, which is not displayed until you call `frame.display.show()`.

Currently, the `x`, `y`, `w`, and `h` parameters are rounded down to the closest multiple of 8, for performance reasons.  This is likely to be changed in the future.

* `x` *(int)*: The x position of the upper-left corner of the rectangle.
* `y` *(int)*: The y position of the upper-left corner of the rectangle.
* `w` *(int)*: The width of the rectangle.
* `h` *(int)*: The height of the rectangle.
* `color` *(PaletteColors)*: The color of the rectangle.  Defaults to `PaletteColors.WHITE`.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def draw_rect(self, x: int, y: int, w: int, h: int, color: PaletteColors = PaletteColors.WHITE)
```

Example:

```python
# draws a white rectangle 200x200 pixels in the center of the screen
await frame.display.draw_rect(220, 100, 200, 200, PaletteColors.WHITE)

# draws a red rectangle 16x16 pixels in the center of the screen
await frame.display.draw_rect(320-8, 200-8, 16, 16, PaletteColors.RED)

# show both rectangles
await frame.display.show()
```

</details>

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<void> drawRect(int x, int y, int w, int h, PaletteColors color) async
```

Example:

```dart
// draws a white rectangle 200x200 pixels in the center of the screen
await frame.display.drawRect(220, 100, 200, 200, PaletteColors.white);

// draws a red rectangle 16x16 pixels in the center of the screen
await frame.display.drawRect(320-8, 200-8, 16, 16, PaletteColors.red);

// show both rectangles
await frame.display.show();
```

</details>

### Draw Rectangle Filled

```python
frame.display.draw_rect_filled(x: int, y: int, w: int, h: int, border_width: int, border_color: PaletteColors, fill_color: PaletteColors)
```

Draws a filled rectangle with a border and fill color at `x`,`y` with `w` width and `h` height, with an inset border `border_width` pixels wide.  The total size of the rectangle including the border is `w`x`h`.

Currently, the `x`, `y`, `w`, `h`, and `border_width` parameters are rounded down to the closest multiple of 8, for performance reasons.  This is likely to be changed in the future.

* `x` *(int)*: The x position of the upper-left corner of the rectangle.
* `y` *(int)*: The y position of the upper-left corner of the rectangle.
* `w` *(int)*: The width of the rectangle.
* `h` *(int)*: The height of the rectangle.
* `border_width` *(int)*: The width of the border in pixels.
* `border_color` *(PaletteColors)*: The color of the border.
* `fill_color` *(PaletteColors)*: The color of the fill.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def draw_rect_filled(self, x: int, y: int, w: int, h: int, border_width: int, border_color: PaletteColors, fill_color: PaletteColors)
```

Example:

```python
# draws a dialog box with a border and text
await frame.display.draw_rect_filled(x=100, y=100, w=200, h=200, border_width=8, border_color=PaletteColors.RED, fill_color=PaletteColors.CLOUDBLUE)
await frame.display.write_text("Hello world!", x=110, y=110, w=180, h=180, align=Alignment.MIDDLE_CENTER)
await frame.display.show()
```

</details>

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<void> drawRectFilled(int x, int y, int w, int h, int borderWidth, PaletteColors borderColor, PaletteColors fillColor) async
```

Example:

```dart
// draws a dialog box with a border and text
await frame.display.drawRectFilled(100, 100, 200, 200, 8, PaletteColors.RED, PaletteColors.CLOUDBLUE);
await frame.display.writeText("Hello world!", x: 110, y: 110, maxWidth: 180, maxHeight: 180, align: Alignment2D.middleCenter);
await frame.display.show();
```

</details>

### Additional Display Helpers

While the above functions are the most common ones you'll use, there are a few other display-related functions and properties that you may find useful on occasion.

#### Line Height
{: .no_toc }

```python
frame.display.line_height: int = 60
```

The `line_height` property (`lineHeight` in Flutter) is used to get and set the height of each line of text in pixels.  It is 60 by default, however you may override that value to change the vertical spacing of the text in all text displaying functions.  It must be greater than 0.

#### Character Width
{: .no_toc }

```python
frame.display.char_width: int = 4
```

The `char_width` property (`charWidth` in Flutter) is used to get and set the extra horizontal spacing after each character.  It is 4 by default, however you may override that value to change the horizontal spacing of the text in all text displaying functions.

#### Get Text Width and Height
{: .no_toc }

```python
frame.display.get_text_width(text: str) -> int
frame.display.get_text_height(text: str) -> int
```

```dart
int frame.display.getTextWidth(String text)
int frame.display.getTextHeight(String text)
```

Gets the rendered width and height of text in pixels.  Text on Frame is variable width, so this is important for positioning text.  Note that these functions do not perform any text wrapping but do respect any manually-included line breaks, and you can use the outputs in your own word-wrapping or positioning logic.  The width is affected by the `char_width` property, and the height is affected by the `line_height` property (as well as `char_width` if word wrapping).

#### Wrap Text
{: .no_toc }

```python
frame.display.wrap_text(text: str, max_width: int) -> str
```

```dart
String frame.display.wrapText(String text, int maxWidth)
```

Wraps text to fit within a specified width.  It does this by inserting line breaks at space characters, returning a string with extra '\n' characters where line wrapping is needed.

## Microphone

The microphone is accessible via the `frame.microphone` object.  The microphone on Frame allows for streaming audio to a host device in real-time.

### Record Audio
```python
async frame.microphone.record_audio(silence_cutoff_length_in_seconds: Optional[int] = 3, max_length_in_seconds: int = 30) -> np.ndarray
```

Records audio from the microphone and returns it as a numpy array of int16 or int8 depending on the `bit_depth`.

* `silence_cutoff_length_in_seconds` *(int)*: The length of silence in seconds to allow before stopping the recording.  Defaults to 3 seconds, however you can set to None to disable silence detection.  Uses the `silence_threshold` to adjust sensitivity.
* `max_length_in_seconds` *(int)*: The maximum length of the recording in seconds, regardless of silence.  Defaults to 30 seconds.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def record_audio(self, silence_cutoff_length_in_seconds: Optional[int] = 3, max_length_in_seconds: int = 30) -> np.ndarray
```

Examples:

```python
# record audio for up to 30 seconds, or until 3 seconds of silence is detected
audio = await frame.microphone.record_audio()

# record audio for 5 seconds without silence detection
audio = await frame.microphone.record_audio(silence_cutoff_length_in_seconds=None, max_length_in_seconds=5)
```

</details>

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<Uint8List> recordAudio({Duration? silenceCutoffLength = const Duration(seconds: 3), Duration maxLength = const Duration(seconds: 30)}) async
```

Examples:

```dart
// record audio for up to 30 seconds, or until 3 seconds of silence is detected
Uint8List audio = await frame.microphone.recordAudio();

// record audio for 5 seconds without silence detection
Uint8List audio = await frame.microphone.recordAudio(silenceCutoffLength: null, maxLength: Duration(seconds: 5));
```

</details>

### Save Audio File
```python
async frame.microphone.save_audio_file(filename: str, silence_cutoff_length_in_seconds: int = 3, max_length_in_seconds: int = 30) -> float
```

Records audio from the microphone and saves it to a file in PCM Wav format.  Returns the number of seconds of audio recorded.

* `filename` *(str)*: The name of the file to save the audio to.  Regardless of any filename extension, the file will be saved as a PCM wav file.
* `silence_cutoff_length_in_seconds` *(int)*: The length of silence in seconds to allow before stopping the recording.  Defaults to 3 seconds, however you can set to None to disable silence detection.  Uses the `silence_threshold` to adjust sensitivity.
* `max_length_in_seconds` *(int)*: The maximum length of the recording in seconds, regardless of silence.  Defaults to 30 seconds.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def save_audio_file(self, filename: str, silence_cutoff_length_in_seconds: int = 3, max_length_in_seconds: int = 30) -> float
```

Examples:

```python
# record audio for up to 30 seconds, or until 3 seconds of silence is detected
await frame.microphone.save_audio_file("audio.wav")

# record audio for 5 seconds without silence detection
await frame.microphone.save_audio_file("audio.wav", silence_cutoff_length_in_seconds=None, max_length_in_seconds=5)
```

</details>

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<double> saveAudioFile(String filename, {Duration? silenceCutoffLength = const Duration(seconds: 3), Duration maxLength = const Duration(seconds: 30)}) async
```

Examples:

```dart
// record audio for up to 30 seconds, or until 3 seconds of silence is detected
await frame.microphone.saveAudioFile("audio.wav");

// record audio for 5 seconds without silence detection
await frame.microphone.saveAudioFile("audio.wav", silenceCutoffLength: null, maxLength: Duration(seconds: 5));
```

</details>

### Play Audio
```python
frame.microphone.play_audio_background(audio_data: np.ndarray, sample_rate: Optional[int] = None, bit_depth: Optional[int] = None)
frame.microphone.play_audio(audio_data: np.ndarray, sample_rate: Optional[int] = None, bit_depth: Optional[int] = None)
async frame.microphone.play_audio_async(audio_data: np.ndarray, sample_rate: Optional[int] = None, bit_depth: Optional[int] = None)
```

```dart
void playAudio(Uint8List audioData, {int? sampleRate, int? bitDepth})
```

Helpers to play audio from `record_audio()` on your computer.  `play_audio` blocks until playback is complete, while `play_audio_async` plays the audio in a coroutine.  Note that only `play_audio_background` works on Windows at the moment.

* `audio_data` *(np.ndarray)*: The audio data to play, as returned from `record_audio()`.
* `sample_rate` *(int)*: The sample rate of the audio data, in case it's different from the current `sample_rate`.
* `bit_depth` *(int)*: The bit depth of the audio data, in case it's different from the current `bit_depth`.

### Sample Rate and Bit Depth

```python
frame.microphone.sample_rate: int = 8000
frame.microphone.bit_depth: int = 16
```

```dart
int frame.microphone.sampleRate = 8000;
int frame.microphone.bitDepth = 16;
```

The `sample_rate` property (`sampleRate` in Flutter) is used to get and set the sample rate of the microphone.  It is 8000 by default, however you may override that value to change the sample rate of the microphone.  Valid values are 8000 and 16000.

The `bit_depth` property (`bitDepth` in Flutter) is used to get and set the bit depth of the microphone.  It is 16 by default, however you may override that value to change the bit depth of the microphone.  Valid values are 8 and 16.

Transfers are limited by the Bluetooth bandwidth which is typically around 40kBps under good signal conditions. The audio bitrate for a given `sample_rate` and `bit_depth` is: `sample_rate * bit_depth / 8` bytes per second. An internal 32k buffer automatically compensates for additional tasks that might otherwise briefly block Bluetooth transfers. If this buffer limit is exceeded however, then discontinuities in audio might occur.

### Silence Threshold

```python
frame.microphone.silence_threshold: float = 0.02
```

```dart
double frame.microphone.silenceThreshold = 0.02;
```

The `silence_threshold` property (`silenceThreshold` in Flutter) is used to get and set the threshold for detecting silence in the audio stream.  Valid values are between 0 and 1.  0.02 is the default, however you may adjust this value to be more or less sensitive to sound.


## Motion

Motion data is available via the `frame.motion` object.  The motion data is collected by the accelerometer and compass on the Frame.  You may also register a callback for when the user taps the Frame.

### Get Direction

```python
async frame.motion.get_direction() -> Direction
```

Gets the current orientation of the Frame.  Returns a `Direction` object.

The `Direction` object contains the following properties:

| Property     | Type   | Range         | Description                                      | Examples |
|--------------|--------|---------------|--------------------------------------------------|---------------|
| `roll`       | float  | -180 to 180   | The roll angle of the Frame, in degrees.         | 20.0 (right side up, head tilted to the left), -20.0 (left side up, head tilted to the right)          |
| `pitch`      | float  | -180 to 180   | The pitch angle of the Frame, in degrees.        | 40.0 (nose pulled down, looking at the floor), -40.0 (nose pulled up, looking towards the ceiling)          |
| `heading`    | float  | 0 to 360      | The heading angle of the Frame, in degrees.      | *not yet implemented*      |
| `amplitude()`| float  | >= 0          | Returns the amplitude of the motion vector.      | 0 (looking straight ahead), 20 (a bit away from looking straight ahead)           |

The `roll`, `pitch`, and `heading` properties represent the orientation of the Frame in 3D space. The `amplitude()` method returns the magnitude of the motion vector, which can be useful for detecting the intensity of movements.

A standard "looking forward" position has a roll of 0 and a pitch of 0.

{: .warning }
The compass data is not yet implemented, so the heading value will always be 0.  You can still get the pitch and roll values, however.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }

```python
async def get_direction(self) -> Direction
```

Example:

```python
direction = await frame.motion.get_direction()
print(direction)

intensity_of_motion = 0
prev_direction = await f.motion.get_direction()
for _ in range(10):
    await asyncio.sleep(0.1)
    direction = await f.motion.get_direction()
    intensity_of_motion = max(intensity_of_motion, (direction-prev_direction).amplitude())
    prev_direction = direction
print(f"Intensity of motion: {intensity_of_motion}")
await f.display.show_text(f"Intensity of motion: {intensity_of_motion}", align=Alignment.MIDDLE_CENTER)
```

</details>


<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }

```dart
Future<Direction> getDirection() async
```

Example:

```dart
// get the direction
Direction direction = await frame.motion.getDirection();

// track the intensity of motion
double intensityOfMotion = 0;
Direction prevDirection = await frame.motion.getDirection();
for (int i = 0; i < 10; i++) {
  await Future.delayed(Duration(milliseconds: 100));
  direction = await frame.motion.getDirection();
  intensityOfMotion = max(intensityOfMotion, (direction - prevDirection).amplitude());
  prevDirection = direction;
}
print("Intensity of motion: $intensityOfMotion");
await frame.display.showText("Intensity of motion: $intensityOfMotion", align: Alignment.middleCenter);
```

</details>

### Run On Tap

```python
async frame.motion.run_on_tap(lua_script: Optional[str] = None, callback: Optional[Callable[[], None]] = None) -> None
```

Run a Lua script and/or callback when the user taps the Frame.  Replaces any previously set callbacks.  If None is provided for both `lua_script` and `callback`, then previously set callbacks will be removed.

* `lua_script` *(str)*: A Lua script to run on the Frame when the user taps the Frame.  This runs even if the Frame is not connected via bluetooth at the time of the tap.
* `callback` *(Callable[[], None]])*: A callback function to run locally when the user taps the Frame.  This will only run if the Frame is connected via bluetooth at the time of the tap.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def run_on_tap(self, lua_script: Optional[str] = None, callback: Optional[Callable[[], None]] = None) -> None:
```

Example:
```python
def on_tap(self):
    print("Frame was tapped!")

# assign both a local callback and a lua script.  Or you could just do one or the other.
await f.motion.run_on_tap(lua_script="frame.display.text('I was tapped!',1,1);frame.display.show();", callback=on_tap)
```

</details>

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<void> runOnTap({String? luaScript, void Function()? callback}) async
```

Example:
```dart
void onTap() {
  print("Frame was tapped!");
}

// assign both a local callback and a lua script. Or you could just do one or the other.
await f.motion.runOnTap(luaScript: "frame.display.text('I was tapped!',1,1);frame.display.show();", callback: onTap);
```

</details>

### Wait For Tap
```python
async frame.motion.wait_for_tap() -> None
```

Blocks until the user taps the Frame.

<details markdown="block">
<summary>Python</summary>

#### Python
{: .no_toc }
```python
async def wait_for_tap(self) -> None
```

Example:
```python
print("Waiting for tap...")
await f.display.show_text("Tap me to continue", align=Alignment.MIDDLE_CENTER)
await f.motion.wait_for_tap()
print("Tap received!")
await f.display.show_text("tap complete", align=Alignment.MIDDLE_CENTER)
```

</details>

<details markdown="block">
<summary>Flutter</summary>

#### Flutter
{: .no_toc }
```dart
Future<void> waitForTap() async
```

Example:
```dart
print("Waiting for tap...");
await f.display.showText("Tap me to continue", align: Alignment.middleCenter);
await f.motion.waitForTap();
print("Tap received!");
await f.display.showText("Tap complete", align: Alignment.middleCenter);
```

</details>


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

        print("Tap the Frame to continue...")
        await f.display.show_text("Tap the Frame to take a photo", align=Alignment.MIDDLE_CENTER)
        await f.motion.wait_for_tap()

        # take a photo and save to disk
        await f.display.show_text("Taking photo...", align=Alignment.MIDDLE_CENTER)
        await f.camera.save_photo("frame-test-photo.jpg")
        await f.display.show_text("Photo saved!", align=Alignment.MIDDLE_CENTER)
        # or with more control
        await f.camera.save_photo("frame-test-photo-2.jpg", autofocus_seconds=3, quality=f.camera.HIGH_QUALITY, autofocus_type=f.camera.AUTOFOCUS_TYPE_CENTER_WEIGHTED)
        # or get the raw bytes
        photo_bytes = await f.camera.take_photo(autofocus_seconds=1)

        print("About to record until you stop talking")
        await f.display.show_text("Say something...", align=Alignment.MIDDLE_CENTER)
		# record audio to a file
        length = await f.microphone.save_audio_file("test-audio.wav")
        print(f"Recorded {length:01.1f} seconds: \"./test-audio.wav\"")
        await f.display.show_text(f"Recorded {length:01.1f} seconds", align=Alignment.MIDDLE_CENTER)
        await asyncio.sleep(3)

        # or get the audio directly in memory
        await f.display.show_text("Say something else...", align=Alignment.MIDDLE_CENTER)
        audio_data = await f.microphone.record_audio(max_length_in_seconds=10)
        await f.display.show_text(f"Playing back {len(audio_data) / f.microphone.sample_rate:01.1f} seconds of audio", align=Alignment.MIDDLE_CENTER)
        # you can play back the audio on your computer
        f.microphone.play_audio(audio_data)
        # or process it using other audio handling libraries, upload to a speech-to-text service, etc.

        print("Move around to track intensity of your motion")
        await f.display.show_text("Move around to track intensity of your motion", align=Alignment.MIDDLE_CENTER)
        intensity_of_motion = 0
        prev_direction = await f.motion.get_direction()
        for _ in range(10):
            await asyncio.sleep(0.1)
            direction = await f.motion.get_direction()
            intensity_of_motion = max(intensity_of_motion, (direction-prev_direction).amplitude())
            prev_direction = direction
        print(f"Intensity of motion: {intensity_of_motion:01.2f}")
        await f.display.show_text(f"Intensity of motion: {intensity_of_motion:01.2f}", align=Alignment.MIDDLE_CENTER)
        print("Tap the Frame to continue...")
        await f.motion.wait_for_tap()
		
        # Show the full palette
        width = 640 // 4
        height = 400 // 4
        for color in range(0, 16):
            tile_x = (color % 4)
            tile_y = (color // 4)
            await f.display.draw_rect(tile_x*width+1, tile_y*height+1, width, height, color)
            await f.display.write_text(f"{color}", tile_x*width+width//2+1, tile_y*height+height//2+1)
        await f.display.show()

        print("Tap the Frame to continue...")
        await f.motion.wait_for_tap()

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

        # set a wake screen via script, so when you tap to wake the frame, it shows the battery and time
        await f.run_on_wake("""frame.display.text('Battery: ' .. frame.battery_level() ..  '%', 10, 10);
                            if frame.time.utc() > 10000 then
                                local time_now = frame.time.date();
                                frame.display.text(time_now['hour'] .. ':' .. time_now['minute'], 300, 160);
                                frame.display.text(time_now['month'] .. '/' .. time_now['day'] .. '/' .. time_now['year'], 300, 220) 
                            end;
                            frame.display.show();
                            frame.sleep(10);
                            frame.display.text(' ',1,1);
                            frame.display.show();
                            frame.sleep()""")

        # tell frame to sleep after 10 seconds then clear the screen and go to sleep, without blocking for that
        await f.run_lua("frame.sleep(10);frame.display.text(' ',1,1);frame.display.show();frame.sleep()")

    print("disconnected")

asyncio.run(main())

```


## Flutter

```dart
import 'dart:convert';
import 'dart:typed_data';
import 'package:frame_sdk/frame_sdk.dart';
import 'package:frame_sdk/display.dart';
import 'package:frame_sdk/motion.dart';
import 'package:frame_sdk/camera.dart';
import 'package:frame_sdk/microphone.dart';
import 'package:frame_sdk/bluetooth.dart';
import 'package:logging/logging.dart';
import 'package:flutter/material.dart';
import 'dart:async';
import 'dart:math';
import 'package:path_provider/path_provider.dart';

Future<void> runExample() async {
  // Request bluetooth permission
  await BrilliantBluetooth.requestPermission();


  final frame = Frame();

  // Connect to the frame
  while (!frame.isConnected) {
    print("Trying to connect...");
    final didConnect = await frame.connect();
    if (didConnect) {
      print("Connected to device");
    } else {
      print("Failed to connect to device, will try again...");
    }
  }

  // Get battery level
  int batteryLevel = await frame.getBatteryLevel();
  print("Frame battery: $batteryLevel%");

  // Write file
  await frame.files.writeFile("greeting.txt", utf8.encode("Hello world"));

  // Read file
  String fileContent = utf8.decode(await frame.files.readFile("greeting.txt"));
  print(fileContent);

  // Display text
  await frame.runLua("frame.display.text('Hello world', 50, 100);frame.display.show()");

  // Evaluate expression
  print(await frame.evaluate("1+2"));

  print("Tap the Frame to continue...");
  await frame.display.showText("Tap the Frame to take a photo", align: Alignment2D.middleCenter);
  await frame.motion.waitForTap();

  // Take and save photo
  await frame.display.showText("Taking photo...", align: Alignment2D.middleCenter);
  await frame.camera.savePhoto("frame-test-photo.jpg");
  await frame.display.showText("Photo saved!", align: Alignment2D.middleCenter);

  // Take photo with more control
  await frame.camera.savePhoto("frame-test-photo-2.jpg",
      autofocusSeconds: 3,
      quality: PhotoQuality.high,
      autofocusType: AutoFocusType.centerWeighted);

  // Get raw photo bytes
  Uint8List photoBytes = await frame.camera.takePhoto(autofocusSeconds: 1);
  print("Photo bytes: ${photoBytes.length}");

  print("About to record until you stop talking");
  await frame.display.showText("Say something...", align: Alignment2D.middleCenter);

  // Record audio to file
  double length = await frame.microphone.saveAudioFile("test-audio.wav");
  print("Recorded ${length.toStringAsFixed(1)} seconds: \"./test-audio.wav\"");
  await frame.display.showText("Recorded ${length.toStringAsFixed(1)} seconds", align: Alignment2D.middleCenter);
  await Future.delayed(const Duration(seconds: 3));

  // Record audio to memory
  await frame.display.showText("Say something else...", align: Alignment2D.middleCenter);
  Uint8List audioData = await frame.microphone.recordAudio(maxLength: const Duration(seconds: 10));
  await frame.display.showText(
      "Recorded ${(audioData.length / frame.microphone.sampleRate.toDouble()).toStringAsFixed(1)} seconds of audio",
      align: Alignment2D.middleCenter);

  print("Move around to track intensity of your motion");
  await frame.display.showText("Move around to track intensity of your motion", align: Alignment2D.middleCenter);
  double intensityOfMotion = 0;
  Direction prevDirection = await frame.motion.getDirection();
  for (int i = 0; i < 10; i++) {
    await Future.delayed(const Duration(milliseconds: 100));
    Direction direction = await frame.motion.getDirection();
    intensityOfMotion = max(intensityOfMotion, (direction - prevDirection).amplitude());
    prevDirection = direction;
  }
  print("Intensity of motion: ${intensityOfMotion.toStringAsFixed(2)}");
  await frame.display.showText("Intensity of motion: ${intensityOfMotion.toStringAsFixed(2)}", align: Alignment2D.middleCenter);
  print("Tap the Frame to continue...");
  await frame.motion.waitForTap();

  // Show the full palette
  int width = 640 ~/ 4;
  int height = 400 ~/ 4;
  for (int color = 0; color < 16; color++) {
    int tileX = (color % 4);
    int tileY = (color ~/ 4);
    await frame.display.drawRect(tileX * width + 1, tileY * height + 1, width, height, PaletteColors.fromIndex(color));
    await frame.display.writeText("$color",
        x: tileX * width + width ~/ 2 + 1,
        y: tileY * height + height ~/ 2 + 1);
  }
  await frame.display.show();

  print("Tap the Frame to continue...");
  await frame.motion.waitForTap();

  // Scroll some long text
  await frame.display.scrollText(
      "Never gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you");

  // Display battery indicator and time as a home screen
  batteryLevel = await frame.getBatteryLevel();
  PaletteColors batteryFillColor = batteryLevel < 20
      ? PaletteColors.red
      : batteryLevel < 50
          ? PaletteColors.yellow
          : PaletteColors.green;
  int batteryWidth = 150;
  int batteryHeight = 75;
  await frame.display.drawRect(
      640 - 32, 40 + batteryHeight ~/ 2 - 8, 32, 16, PaletteColors.white);
  await frame.display.drawRectFilled(
      640 - 16 - batteryWidth,
      40 - 8,
      batteryWidth + 16,
      batteryHeight + 16,
      8,
      PaletteColors.white,
      PaletteColors.voidBlack);
  await frame.display.drawRect(
      640 - 8 - batteryWidth,
      40,
      (batteryWidth * 0.01 * batteryLevel).toInt(),
      batteryHeight,
      batteryFillColor);
  await frame.display.writeText("$batteryLevel%",
      x: 640 - 8 - batteryWidth,
      y: 40,
      maxWidth: batteryWidth,
      maxHeight: batteryHeight,
      align: Alignment2D.middleCenter);
  await frame.display.writeText(DateTime.now().toString(), align: Alignment2D.middleCenter);
  await frame.display.show();

  // Set a wake screen via script
  await frame.runOnWake(luaScript: """
    frame.display.text('Battery: ' .. frame.battery_level() ..  '%', 10, 10);
    if frame.time.utc() > 10000 then
      local time_now = frame.time.date();
      frame.display.text(time_now['hour'] .. ':' .. time_now['minute'], 300, 160);
      frame.display.text(time_now['month'] .. '/' .. time_now['day'] .. '/' .. time_now['year'], 300, 220) 
    end;
    frame.display.show();
    frame.sleep(10);
    frame.display.text(' ',1,1);
    frame.display.show();
    frame.sleep()
  """);

  // Tell frame to sleep after 10 seconds then clear the screen and go to sleep
  await frame.runLua("frame.sleep(10);frame.display.text(' ',1,1);frame.display.show();frame.sleep()");
}

```