---
title: Lua API
description: A guide on how to use Lua on your Frame AR glasses.
image: /images/frame/frame-splash.png
nav_order: 3
parent: Frame
---

# Lua API
{: .no_toc }

---

Lua is a tiny and extensible scripting language that's designed to be power efficient and quick to learn. Frame features a complete Lua virtual machine based on the latest public release of Lua. Dedicated hardware APIs allow direct access to all of Frame's peripherals at a high level so that developers can start building apps quickly and easily.

There's no special cables or setup needed. Lua on Frame is accessed solely over Bluetooth, such that any user created host app can easily execute scripts by simply pushing Lua strings to the device.

To learn more how the underlying Bluetooth communication with Frame works, check out the Bluetooth section of the [Building Apps](/frame/building-apps#bluetooth) page.

---

## Library reference
{: .no_toc }

This page describes all of the Frame specific Lua APIs available to the developer along with some helpful examples. Certain libraries allow for more low level access that can be used for debugging and hacking the various subsystems of Frame.

{: .note }
The API specification is still undergoing heavy development. Some of them may change over the coming month or so.

1. TOC
{:toc}

---

### Display

The display engine of allows drawing of text, sprites and vectors. These elements can be layered atop one another simply in the order they are called, and then be displayed in one go using the `show()` function.

The Frame display is capable of rendering up to 16 colors at one time. These colors are preset by default, however each color can be overridden by any 8bit YCbCr color using the `palette` command.

| API&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
|:---------|:------------|
| `frame.display.palette{}`                                             | *Details coming soon*
| `frame.display.text(string, x, y, {color='WHITE', align='TOP_LEFT'})` | Prints the given `string` to the display at `x` and `y`. A `color` can optionally be provided to print the text in one of the 16 palette colors, and `align` can optionally be provided to jutify the text as either `'TOP_LEFT'`, `'TOP_CENTER'`, `'TOP_RIGHT'`, `'MIDDLE_LEFT'`, `'MIDDLE_CENTER'`, `'MIDDLE_RIGHT'`, `'BOTTOM_LEFT'`, `'BOTTOM_CENTER'`, or `'BOTTOM_RIGHT'`
| `frame.display.bitmap()`                                              | *Details coming soon*
| `frame.display.vector()`                                              | *Details coming soon*
| `frame.display.show()`                                                | Shows the drawn objects on the display


#### Example
{: .no_toc }

```lua
-- Display 'Hello world' at x = 50 and y = 100
frame.display.clear()
frame.display.text('Hello world', 50, 100)
frame.display.show()
```

---

### Camera

The camera capability of Frame allows for capturing and downloading of single JPEG images over Bluetooth. The sensor's full resolution is 1280x720 pixels in portrait orientation, however only square images up to 720x720 pixels can be captured at a time. The user can select which portion of the sensor's window is captured using the `pan` control. Additionally, the resolution of the capture can be cropped to either 360x360, 240x240 or 180x180 by using the `zoom` function. Smaller resolutions will increase the image quality, however the `quality` factor can be reduced to decrease the image file size, and increase download speeds of the image over Bluetooth.

| API&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
|:---------|:------------|
| `frame.camera.capture{zoom=1, pan=0, quality=1.0}` | Captures a single image from the camera. `zoom` can be either `1`, `2`, `3`, or `4` returning 720x720, 360x360, 240x240 or 180x180 images respectively. `pan` can be used to tilt the camera view either up or down. A value of `10` represents the highest viewing angle, `0` is center, and `-10` is the lowest. The `quality` factor can help reduce image size by reducing the JPEG quality. A value of `1.0` represents full quality, and can be reduced to `0.01` for the lowest quality and smallest file size
| `frame.camera.read(num_bytes)`                     | Reads out a number of bytes from the camera capture memory as a byte string. Once all bytes have been read, `nil` will be returned

#### Example
{: .no_toc }

```lua
local mtu = frame.bluetooth.max_length()

frame.camera.capture() -- Capture an image using default settings

while true do
    local data = frame.camera.read(mtu)
    if data == nil then
        break
    end
    bluetooth.send(data)
end
```

| Low&nbsp;level&nbsp;functions&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
|:---------|:------------|
| `frame.camera.sleep()`                      | Puts the camera to sleep and reduces power consumption. Note the `frame.sleep()` function will automatically put the camera to sleep
| `frame.camera.wake()`                       | Wakes up the camera if it has previously been asleep. Note that following wakeups from `frame.sleep()` automatically wakes up the camera
| `frame.camera.set_register(address, value)` | Allows for hacking the camera's internal registers

---

### Microphone

The microphone of Frame allows for up to 80kB of recording at a time into a circular buffer. If the recorded data is read out and faster than it is recorded, then the recording can go on continiously. If transfering audio over bluetooth, this limit is around 40kBps under good signal conditions. The audio bitrate for a given `sample_rate` and `bit_depth` is: `sample_rate * bit_depth / 8` bytes per second.

| API&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
|:---------|:------------|
| `frame.microphone.record{seconds=inf, sample_rate=8000, bit_depth=8}` | Starts recording for a number of `seconds` if it is given, otherwise records continiously. `sample_rate` may be either `20000`, `16000`, `12500`, `10000`, `8000`, `5000` or `4000`. `bit_depth` maybe either `16`, `8`, or `4`
| `frame.microphone.stop()`                                             | Stops any ongoing recording
| `frame.microphone.read(num_bytes)`                                    | Reads out a number of bytes from the recording buffer. Once all bytes have been read, `nil` will be returned

#### Example
{: .no_toc }

```lua
local mtu = frame.bluetooth.max_length()

frame.microphone.record{seconds = 3} -- Record 3 second of audio

frame.sleep(3) -- Wait for the recording to complete and send all the data

while true do
    local data = frame.microphone.read(mtu)
    if data == nil then
        break
    end
    bluetooth.send(data)
end
```

---

### Motion sensor (IMU)

The IMU API allows reading both accelerometer and compass data, as well as assigning a callback function for tap gestures.

The tap gesture will always wake up Frame from `frame.sleep()`.

| API | Description |
|:---------|:------------|
| `frame.imu.direction()`           | Returns a table containing the `roll`, `pitch` and `heading` angles of the wearer's head position 
| `frame.imu.tap_callback(handler)` | Assigns a callback to the tap gesture. `handler` must be a function, or can be `nil` to deactive the callback

| Low&nbsp;level&nbsp;functions | Description |
|:---------|:------------|
| `frame.imu.raw()` | Returns a table of the raw `accelerometer` and `compass` measurements. Each containing a table with `x`, `y`, and `z` values

#### Example
{: .no_toc }

```lua
print(frame.imu.direction()['pitch']) -- Prints the angle of the wears head (up or down)

function tapped() -- Prints 'tapped' whenever the user taps the side of their Frame
    print('tapped')
end

frame.imu.tap_callback(tapped)
```

---

### Bluetooth

The Bluetooth API allows for sending and receiving raw byte data over Bluetooth. For a full description of how this can be used, check out the [Bluetooth section](/frame/building-apps#bluetooth) of the Building Apps page.

| API | Description |
|:---------|:------------|
| `frame.bluetooth.address()`                 | Returns the device MAC address as a 17 character string. E.g. `4E:87:B5:0C:64:0F`
| `frame.bluetooth.receive_callback(handler)` | Assigns a callback to handle received Bluetooth data. `handler` must be a function, or can be `nil` to deactive the callback
| `frame.bluetooth.max_length()`              | Returns the maximum length of data that can be sent or received in a single transfer
| `frame.bluetooth.send(data)`                | Sends data to the host device. `data` must be a string, but can contain byte values including 0x00 values anywhere in the string. The total length of the string must be less than or equal to `frame.bluetooth.max_length()`

#### Example
{: .no_toc }

```lua
function get_data(data) -- Called everytime byte data arrives to Frame
    print(data)
end

frame.bluetooth.receive_callback(get_data)

frame.bluetooth.send('\x10\x12\x00\xFF') -- Sends the bytes: 0x10, 0x12, 0x00, 0xFF to the host
```

---

### File system

The file system API allows for writing and reading files to Frame's non-volatile storage. These can include executable Lua scripts, or other user files.

| API&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
|:---------|:------------|
| `frame.file.open(filename, mode)`   | Opens a file and returns a file object. `filename` can be any name, and `mode` can be either `'read'`, `'write'`, or `'append'`.
| `frame.file.remove(name)`           | Removes a file or directory of given `name`
| `frame.file.rename(name, new_name)` | Renames a file or directory of given `name` to `new_name`
| `frame.file.listdir(directory)`     | Lists all files in the directory path given. E.g. `'/'` for the filesystem root directory. The list is returned as a table with `name`, `size`, and `type`
| `frame.file.mkdir(pathname)`        | Creates a new directory with the given `pathname`
| `f:read(*num_bytes)`                | Reads a number of bytes from a file. If no argument is give, the whole line is returned
| `f:write(data)`                     | Writes data to the file. `data` must be a string and can contain any byte data
| `f:close()`                         | Closes the file. It is important to close files once done writing, otherwise they may become courrupted

#### Example
{: .no_toc }

```lua
frame.file.mkdir('/my_files') -- Make a new directory

f = frame.file.open('/my_files/log.txt', 'write') -- Create a new file (or overwrite if it exists)
f:write('Log:\n')
f:close()

f = frame.file.open('/my_files/log.txt', 'append') -- Append two lines to the file
f:write('Logged a new line\n')
f:close()

f = frame.file.open('/my_files/log.txt', 'append')
f:write('Logged another line\n')
f:close()

-- Print all the files in the directory
local files = frame.file.listdir('/my_files')

for index, data in ipairs(files) do
    print(index)

    for key, value in pairs(data) do
        print('\t', key, value)
    end
end
```

---

### Time functions

The time functions allow for accurate timekeeping on Frame. The `utc()` function can be used to set the time on Frame using a UTC timestamp. Frame will then keep the time until it's put back onto charge, or placed into deep sleep using `frame.sleep()`. The `date()` function can be used to return a human readable time and date.

| API | Description |
|:---------|:------------|
| `frame.time.utc(*timestamp)`  | Sets or gets the current time. `timestamp` can be provided as a UTC timestamp to set the internal real-time clock. If no argument is given, Frame's current time is returned as a UTC timestamp. If no timestamp was initially set, this number will simply represent the powered on time of Frame in seconds.
| `frame.time.zone(*offset)`    | Sets or gets the timezone offset. If `offset` is given, the timezone will be set, otherwise the currently set timezone is returned. The format of the timezone should be a string, e.g. '-7:00', or '5:30'.
| `frame.time.date(*timestamp)` | Returns a table containing `second`, `minute`, `hour`, `day`, `month`, `year`, `weekday`, `day of year`, and `is daylight saving`. If the optional `timestamp` argument is given, that timestamp will be used to calculate the corresponding date.

#### Example
{: .no_toc }

```lua
frame.time.utc(1708551112) -- Set the current time to Wed Feb 21 2024 21:31:52 UTC
frame.time.zone('-7:00') -- Set the timezone to pacific time

local time_now = frame.time.date()

-- print the local time and date
print(time_now['hour'])
print(time_now['minute'])
print(time_now['month'])
print(time_now['day'])
```

---

### System functions

The system API provides miscellaneous functions such as `sleep` and `update`. It also contains some low level functions which are handy for developing apps and custom FPGA images. 

| API | Description |
|:---------|:------------|
| `frame.FIRMWARE_VERSION` | Returns the current firmware version as a 12 character string. E.g. `'v24.046.1546'`
| `frame.GIT_TAG`          | Returns the current firmware git tag as a 7 character string. E.g. `'4a6ea0b'`
| `frame.battery_level()`  | Returns the battery level as a percentage between `1` and `100`
| `frame.sleep(*seconds)`  | Sleeps for a given number of seconds. `seconds` can be a decimal number such as `1.25`. If no argument is given, Frame will go to sleep until a tap gesture wakes it up
| `frame.update()`         | Reboots Frame into the firmware bootloader. Check the [firmware updates](/frame/building-apps#firmware-updates) section of the Building Apps page to see how this is used

| Low&nbsp;level&nbsp;functions&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
|:---------|:------------|
| `frame.stay_awake(enable)`            | Prevents Frame from going to sleep while it's docked onto the charging cradle. This can help during development where continious power is needed, however may degrade the display or cause burn-in if used for extended periods of time
| `frame.fpga_read(address, num_bytes)` | Reads a number of bytes from the FPGA at the given address
| `frame.fpga_write(address, data)`     | Writes data to the FPGA at a given address. `data` can be a string containing any byte values