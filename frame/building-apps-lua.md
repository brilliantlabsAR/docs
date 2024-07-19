---
title: Lua API Reference
description: A reference of Lua functionality avilable on your Frame AR glasses.
image: /images/frame/frame-splash.png
nav_order: 2
parent: Building Apps
---

# Lua API
{: .no_toc }

---

Lua is a tiny and extensible scripting language that's designed to be power efficient and quick to learn. Frame features a complete Lua virtual machine based on the latest public release of Lua. Dedicated hardware APIs allow direct access to all of Frame's peripherals at a high level so that developers can start building apps quickly and easily.

{: .warning }
Note that the Lua virtual machine on the Frame has a very minimal standard library, so many guides on the internet about Lua may contain code that won't work on Frame.  It's best to think of Lua on Frame as a language syntax, not as a standard library.

There's no special cables or setup needed. Lua on Frame is accessed solely over Bluetooth, such that any user created host app can easily execute scripts by simply pushing Lua strings to the device.  To learn more how the underlying Bluetooth communication with Frame works, check out the Bluetooth section of the [Building Apps](/frame/building-apps#bluetooth) page.

---

## Library reference
{: .no_toc }

This page describes all of the Frame specific Lua APIs available to the developer along with some helpful examples. Certain libraries allow for more low level access that can be used for debugging and hacking the various subsystems of Frame.

{: .note }
The API specification is still undergoing heavy development. Some of them may change over time.

1. TOC
{:toc}

---

### Display

The display engine of allows drawing of text, sprites and vectors. These elements can be layered atop one another simply in the order they are called, and then be displayed in one go using the `show()` function.

The Frame display is capable of rendering up to 16 colors at one time. These colors are preset by default, however each color can be overridden by any 8bit YCbCr color using the `palette` command.

{: .warning }
The palette and vector commands are not yet implimented.

| API&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
|:---------|:------------|
| `frame.display.palette{}`                                             | *Coming soon*
| `frame.display.text(string, x, y, {color='WHITE'})`                   | Prints the given `string` to the display at `x` and `y`. A `color` can optionally be provided to print the text in one of the 16 palette colors.
| `frame.display.bitmap(x, y, width, num_colors, color_offset, data)`   | Allows manually drawing to the screen.
| `frame.display.vector()`                                              | *Coming soon*
| `frame.display.show()`                                                | Shows the drawn objects on the display

#### Buffering

The Frame display has 2 buffers.  All writing to the display via `frame.display.text()`, `frame.display.bitmap()`, etc write to an off-screen buffer and are not visible.  This allows you to write mutiple actions at once.  When you have completed drawing and want to show it to the user, call `frame.display.show()` which will display the buffered graphics and clear a new off-screen buffer for whatever you want to draw next.

#### frame.display.text
`frame.display.text(string, x, y)` prints the given `string` to the display with its upper-left at position `x, y`.  All positions are 1-indexed, so possible values for x are between `1` and `640`, and possible values for y are between `1` and `400`.  text is variable width, not fixed-width.  Currently is is not possible to modify the font or font size.  There is no word-wrapping performed automatically.

```lua
-- Display 'Hello world' at x = 50 and y = 100
frame.display.text('Hello world', 50, 100)
frame.display.show()
```

#### frame.display.bitmap
`frame.display.bitmap(x, y, width, num_colors, color_offset, data)` allows manually drawing to the screen.  The bitmap is positioned with its upper-left at `x, y` with width `width` and the height automatically determined by the length of the data.

`num_colors` can be one of `2`, `4`, or `16`.  By including less colors in your bitmap, you can fit more pixels into a smaller data string.  `color_offset` is a number between 1 and 16.

The `data` is a lua string which is just an array of bytes, but with multiple pixels packed in each byte based on the number of colors.  When drawing, the `color_offset` is added to palette index (wrapping around at 16).

```plaintext
Data as Lua string:
"\x01\xFE"

Data as bits:
00000001 11111110

If num_color = 16, then this maps to 4 pixels:
as bits:        0000 0001  1111 1110
palette index:     0    1    15   14

If num_color = 4, then this maps to 8 pixels:
as bits:        00 00 00 01  11 11 11 10
palette index:   0  0  0  1   3  3  3  2

If num_color = 2, then this maps to 16 pixels:
as bits:        0 0 0 0 0 0 0 1  1 1 1 1 1 1 1 0
palette index:  0 0 0 0 0 0 0 1  1 1 1 1 1 1 1 0
```

For example, to draw a red rectangle at position x = 100, y = 50, with width = 32 and height = 15:

```lua
frame.display.bitmap(100, 50, 32, 2, 3, string.rep("\xFF", 32 / 8 * 16))
                     |    |   |   |  |   |"since each byte maps to 8 pixels, we divide the width 32 by 8"
                     |    |   |   |  |   \"and multiply by the height of 16 to get the total data length"
                     |    |   |   |  \"the 3rd color in the standard palette is red"
                     |    |   |   \"we only need 2 color options, to pack 8 pixels per byte"
                     |    |   \"the width is 32, after which it rolls onto the next line"
                     |    \"top at 50px"
                     \"left at 100px"
```

#### Default Palette
From (AndroidArts: Arne Niklas Jansson)[https://www.androidarts.com/palette/16pal.htm] although the ssl cert is expired so duplicated here for easier access:
<table>
<tbody><tr>
<td bgcolor="#000000"><font color="White">#0<br> VOID</font></td>
<td bgcolor="#9D9D9D">#1<br> GRAY</td>
<td bgcolor="#FFFFFF">#2<br> WHITE</td>
<td bgcolor="#BE2633">#3<br> RED</td>
<td bgcolor="#E06F8B">#4<br> MEAT</td>
<td bgcolor="#493C2B"><font color="White">#5<br> DARKBROWN</font></td>
<td bgcolor="#A46422">#6<br> BROWN</td>
<td bgcolor="#EB8931">#7<br> ORANGE</td>
</tr>
<tr>
<td bgcolor="#F7E26B">#8<br> YELLOW</td>
<td bgcolor="#2F484E"><font color="White">#9<br> DARKGREEN</font></td>
<td bgcolor="#44891A">#10<br> GREEN</td>
<td bgcolor="#A3CE27">#11<br> SLIMEGREEN</td>
<td bgcolor="#1B2632"><font color="White">#12<br> NIGHTBLUE</font></td>
<td bgcolor="#005784"><font color="White">#13<br> SEABLUE</font></td>
<td bgcolor="#31A2F2">#14<br> SKYBLUE</td>
<td bgcolor="#B2DCEF">#15<br> CLOUDBLUE</td>
</tr>
</tbody></table>

---

### Camera

The camera capability of Frame allows for capturing and downloading of single JPEG images over Bluetooth. The sensor's full resolution is 1280x720 pixels in portrait orientation, however only square images up to 720x720 pixels can be captured at a time. The user can select which portion of the sensor's window is captured using the `pan` control. Additionally, the resolution of the capture can be cropped to either 360x360, 240x240 or 180x180 by using the `zoom` function. Smaller resolutions will increase the image quality, however the `quality` factor can be reduced to decrease the image file size, and increase download speeds of the image over Bluetooth.

| API&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
|:---------|:------------|
| `frame.camera.capture{quality_factor=50}`                                                          | Captures a single image from the camera. The `quality_factor` option can help reduce file sizes by adjusting the JPEG quality. The four possible options are `10`, `25`, `50`, and `100`. Higher values represent higher quality, but also larger file sizes.
| `frame.camera.read(num_bytes)`                                                                     | Reads out a number of bytes from the camera capture memory as a byte string. Once all bytes have been read, `nil` will be returned
| `frame.camera.auto{metering='AVERAGE', exposure=0, shutter_kp=0.1, gain_kp=1.0, gain_limit=248.0}` | Runs the automatic exposure and gain algorithm. This funtion must be called every 100ms for the best performance. `metering` can be one of three modes, `SPOT`, `CENTER_WEIGHTED`, or `AVERAGE`. `exposure` can be a value between `-2.0` and `2.0` where lower values will return slightly darker images, and higher values will return slightly brighter images. `shutter_kp` and `gain_kp` allow fine tuning of the auto exposure algorithm. Higher values can make reaching the desired exposure faster, but may result in instability and oscilliation of the control loop. These values are generally more sensitive when using the `SPOT` or `CENTER_WEIGHTED` metering modes. `gain_limit` can be used to cap the gain to below the maximum of `248`. This is useful to reduce noise in darker scenes and results in faster exposure when going from darker to brighter scenes.

#### Example
{: .no_toc }

```lua
local mtu = frame.bluetooth.max_length()

-- Auto expose for 3 seconds
for _=1, 30 do
    frame.camera.auto{}
    frame.sleep(0.1)
end

-- Capture an image using default settings
frame.camera.capture{} -- NOTE: for devices running firmware prior to v24.179.0818, the {} should be ()

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
| `frame.camera.set_exposure(shutter)`        | Sets the shutter value manually. Note that `camera.auto{}` will override this value. `shutter` can be a value between `4` and `16383`
| `frame.camera.set_gain(gain)`               | Sets the gain value manually. Note that `camera.auto{}` will override this value. `gain` can be a value between `0` and `248`
| `frame.camera.set_white_balance(r, g, b)`   | Sets the digital gains of the R, G and B channels for fine tuning white balance. `r`, `g` and `b` can be values between `0` and `1023`
| `frame.camera.set_register(address, value)` | Allows for hacking the camera's internal registers. `address` can be any 16-bit register address of the camera, and `value` any 8-bit value to write to that address

It is not recommended to manually call `frame.camera.sleep()` or `frame.camera.wake()`.

---

### Microphone

The microphone on Frame allows for streaming audio to a host device in real-time. Transfers are limited by the Bluetooth bandwith which is typically around 40kBps under good signal conditions. The audio bitrate for a given `sample_rate` and `bit_depth` is: `sample_rate * bit_depth / 8` bytes per second. An internal 32k buffer automatically compensates for additional tasks that might otherwise briefly block Bluetooth transfers. If this buffer limit is exceeded however, then discontinuities in audio might occour.

| API&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
|:---------|:------------|
| `frame.microphone.start{sample_rate=8000, bit_depth=8}` | Starts streaming mic data into the internal 32k buffer. `sample_rate` may be either `8000`, or `16000`, and `bit_depth` may be either `8`, `16`
| `frame.microphone.stop()`                               | Stops the stream
| `frame.microphone.read(num_bytes)`                      | Reads out a number of bytes from the buffer. If all bytes have been read, but streaming is still active, an empty string will be returned. Once the stream has been stopped and all bytes have been read, then `nil` will be returned

#### Example
{: .no_toc }

```lua
local mtu = frame.bluetooth.max_length()

frame.microphone.start{sample_rate=16000} -- Start streaming at 16kHz 8bit

-- Streams forever
while true do
    data = frame.microphone.read(mtu)

    -- Calling frame.microphone.stop() will allow this to break the loop
    if data == nil then
        break
    end

    -- If there's data to send then ... 
    if data ~= '' then
        -- Try to send the data as fast as possible
        while true do
            -- If the Bluetooth is busy, this simply trys again until it gets through
            if (pcall(frame.bluetooth.send, data)) then
                break
            end
        end
    end
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
| `f:read(*num_bytes)`                | Reads a number of bytes from a file. If no argument is give, the whole line is returned.
| `f:write(data)`                     | Writes data to the file. `data` must be a string and can contain any byte data
| `f:close()`                         | Closes the file. It is important to close files once done writing, otherwise they may become courrupted

#### Tips

* On many online Lua guides, the examples allow `'r'`, `'w'`, or `'a'` as shorthard for `'read'`, `'write'`, or `'append'`, however Frame does not support that.  You need to spell out the whole word.
* GitHub Copilot and ChatGPT will always generate incorrect code like `file.read()` rather than the correct `f:read()`.  Keep a close eye on the syntax.
* `f:read()` reads until the end of the line, so you need to call it multiple times to get through the whole file.  It will return `nil` when it has reached the end of the file.
* There is no function to check if a file exists.  Instead you can try to open the file for reading and see if it fails.

{: .warning }
There is (an open bug)[https://github.com/brilliantlabsAR/frame-codebase/issues/234] where `f:read(*num_bytes)` will not always respect the num_bytes limit.  Until that is resolved, your code should handle receiving up to 512 bytes at a time.


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

-- Print the file contents (this simple version will fail if a line is longer than the MTU limit)
f = frame.file.open('/my_files/log.txt', 'read')
while true do
    local line = f:read()
    if line == nil then
        break
    end
    print(line)
end
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

---

## AR Studio
{: .no_toc }

While the main way you'll use Lua on Frame is via host apps that send it over Bluetooth, it can be helpful while learning to directly write and execute Lua code on Frame using the AR Studio extension for VSCode.

AR studio is an extension for VSCode designed for both Frame and Monocle. It lets you quickly start writing apps and testing them on your device. Download it [here](https://marketplace.visualstudio.com/items?itemName=brilliantlabs.brilliant-ar-studio), or simply search for Brilliant AR Studio from within the VSCode extensions tab.

![Brilliant AR Studio for VSCode](/frame/images/frame-vs-code-extension.png)

Once you have AR Studio installed, you can try an example using the following steps:

1. Open the Command Palette using **Ctrl-Shift-P** (or **Cmd-Shift-P** on Mac)

1. Type and select **Brilliant AR Studio: Initialize new project folder**

1. Select Frame, and give your project a name

1. Copy the following example code into `main.lua`:

    ```lua
    function change_text()
        frame.display.clear()
        frame.display.text('Frame tapped!', 50, 100)
        frame.display.show()
    end

    frame.imu.tap_callback(change_text)
    frame.display.clear()
    frame.display.text('Tap the side of Frame', 50, 100)
    frame.display.show()
    ```

1. Save the file, and press the **Connect** button

1. VSCode will then connect to your Frame (You may need to accept pairing if you aren't already paired)

1. Right click on `main.lua` and select **Upload to device**

1. Your app should now be running on Frame

---