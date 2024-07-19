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

The Frame display is capable of rendering up to 16 colors at one time. These colors are preset by default, however each color can be overridden.

| API&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
|:---------|:------------|
| `frame.display.text(string, x, y, {color='WHITE', spacing=4})` | Prints the given `string` to the display at co-ordinates `x` and `y`. A `color` can optionally be provided to print the text in one of the palette colors. Valid options for `color` are: `WHITE` ,`GREY` ,`RED` ,`PINK` ,`DARKBROWN` ,`BROWN` ,`ORANGE` ,`YELLOW` ,`DARKGREEN` ,`GREEN` ,`LIGHTGREEN` ,`NIGHTBLUE` ,`SEABLUE` ,`SKYBLUE` or `CLOUDBLUE`. `spacing` can optionally be provided to adjust the character spacing of the printed text.
| `frame.display.vector()`                                       | *Details coming soon*
| `frame.display.show()`                                         | Shows the drawn objects on the display

#### Example
{: .no_toc }

```lua
-- Display 'Hello world' at x = 50 and y = 100
frame.display.text('Hello world', 50, 100)
frame.display.show()
```

| Low&nbsp;level&nbsp;functions&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
|:---------|:------------|
| `frame.display.assign_color(color, r, g, b)`                            | Changes the rendered color in slot `color` with a new color given by the components `r`, `g,` and `b`. Valid options for `color` are: `VOID`, `WHITE` ,`GREY` ,`RED` ,`PINK` ,`DARKBROWN` ,`BROWN` ,`ORANGE` ,`YELLOW` ,`DARKGREEN` ,`GREEN` ,`LIGHTGREEN` ,`NIGHTBLUE` ,`SEABLUE` ,`SKYBLUE` or `CLOUDBLUE`. Note that changing the `VOID` color will change the rendered background color of the display. The RGB components are internally converted to a 10bit YCbCr value that represents the true colorspace of the display. There may therefore be rounding errors for certain RGB combinations.
| `frame.display.assign_color_ycbcr(color, y, cb, cr)`                    | Same as above, however the `y`, `cb`, and `cr` represent the true 10bit colorspace of the display. Each component has a range of 4, 3, and 3 bits respectively.
| `frame.display.bitmap(x, y, width, color_format, palette_offset, data)` | Prints raw bitmap data to the display at co-ordinates `x` and `y`. `width` should be the width of the bitmap. `color_format` represents the total colors users, and should be either `2`, `4`, or `16`. `palette_offset` offsets the colors indexed from the palette. If no offset is desired, set this to `0`. `data` should be a string containing the bitmap data.

#### Color Palette
{: .no_toc }

The Frame display is capable of rendering up to 16 colors at a time. Each color is indexed 0-15, and are named in the following order: `VOID`, `WHITE` ,`GREY` ,`RED` ,`PINK` ,`DARKBROWN` ,`BROWN` ,`ORANGE` ,`YELLOW` ,`DARKGREEN` ,`GREEN` ,`LIGHTGREEN` ,`NIGHTBLUE` ,`SEABLUE` ,`SKYBLUE` or `CLOUDBLUE`. `VOID` represents the background (normally black) color. Each color can be overridden per frame to any 10bit YCbCr color from the colorspace shown below. This space contains a total of 1024 possible colors.

![Frame display YCbCr colorspace](/frame/images/frame-ycbcr-colorspace.png)

The `assign_color()` function simplifies color selection by allowing the user to enter regular 24bit RGB values which are internally converted to the YCbCr colorspace. Note however that the color actually rendered will be rounded to one of the above colors.

#### Sprite Engine
{: .no_toc }

The sprite engine in Frame is capable of quickly rendering bitmap data to anywhere on the screen. Sprites data can be stored in one of three different color formats. 2 color, 4 color, and 16 color. 2 color mode will only use the first two colors in the color palette, but allows storing 8 pixels per byte of sprite data. 4 color will use the first four colors in the palette, but requires twice as much data per pixel. Finally, 16 color mode allows accessing the entire color palette, but requires 4 bits per pixel. Pixel data in Lua is simply represented as a long string of all the pixels. The `width` parameter tells the sprite engine when to move to the next line when rendering out each pixel from the string.

Each pixel represented by the pixel data simply indexes one of the colors from the color palette. For 2 color mode, a bit (pixel) value of `1` will print a pixel of color `WHITE`. The internal font glyphs used by the `text()` function are essentially all 2 color sprites.

To achieve different color text, the `palette_offset` feature is used. This value offsets how the colors are indexed during the render. Using the same 2 color example as above, but combined with a `palette_offset` value of 3, now indexes `PINK` instead of `WHITE` for all pixel values of `1`. The same works for all the other color modes. Note that the `VOID` color is never shifted. A pixel value of `0` will always index `VOID`, no matter the `palette_offset`.

The example below shows how a single sprite can be shown in different colors using the `palette_offset` feature. Note how the color palette has been adjusted to repeat the same colors after index 5, but with red changed to green.

![Frame display sprite engine example](/frame/images/frame-sprite-engine.drawio.png)

---

### Camera

The camera capability of Frame allows for capturing and downloading of single JPEG images over Bluetooth. The sensor's full resolution is 1280x720 pixels in portrait orientation, however only square images up to 720x720 pixels can be captured at a time. The user can select which portion of the sensor's window is captured using the `pan` control. Additionally, the resolution of the capture can be cropped to either 360x360, 240x240 or 180x180 by using the `zoom` function. Smaller resolutions will increase the image quality, however the `quality` factor can be reduced to decrease the image file size, and increase download speeds of the image over Bluetooth.

| API&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
|:---------|:------------|
| `frame.camera.capture{quality_factor=50}`                                                          | Captures a single image from the camera. The `quality_factor` option can help reduce file sizes by adjusting the JPEG quality. The four possible options are `10`, `25`, `50`, and `100`. Higher values represent higher quality, but also larger file sizes.
| `frame.camera.read(num_bytes)`                                                                     | Reads out a number of bytes from the camera capture memory as a byte string. Once all bytes have been read, `nil` will be returned
| `frame.camera.auto{metering='AVERAGE', exposure=0, shutter_kp=0.1, gain_kp=1.0, gain_limit=248.0}` | Runs the automatic exposure and gain algorithm. This function must be called every 100ms for the best performance. `metering` can be one of three modes, `SPOT`, `CENTER_WEIGHTED`, or `AVERAGE`. `exposure` can be a value between `-2.0` and `2.0` where lower values will return slightly darker images, and higher values will return slightly brighter images. `shutter_kp` and `gain_kp` allow fine tuning of the auto exposure algorithm. Higher values can make reaching the desired exposure faster, but may result in instability and oscillation of the control loop. These values are generally more sensitive when using the `SPOT` or `CENTER_WEIGHTED` metering modes. `gain_limit` can be used to cap the gain to below the maximum of `248`. This is useful to reduce noise in darker scenes and results in faster exposure when going from darker to brighter scenes.

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

---

### Microphone

The microphone on Frame allows for streaming audio to a host device in real-time. Transfers are limited by the Bluetooth bandwidth which is typically around 40kBps under good signal conditions. The audio bitrate for a given `sample_rate` and `bit_depth` is: `sample_rate * bit_depth / 8` bytes per second. An internal 32k buffer automatically compensates for additional tasks that might otherwise briefly block Bluetooth transfers. If this buffer limit is exceeded however, then discontinuities in audio might occur.

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
| `frame.imu.tap_callback(handler)` | Assigns a callback to the tap gesture. `handler` must be a function, or can be `nil` to deactivate the callback

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
| `frame.bluetooth.receive_callback(handler)` | Assigns a callback to handle received Bluetooth data. `handler` must be a function, or can be `nil` to deactivate the callback
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
| `f:close()`                         | Closes the file. It is important to close files once done writing, otherwise they may become corrupted

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
| `frame.stay_awake(enable)`            | Prevents Frame from going to sleep while it's docked onto the charging cradle. This can help during development where continuous power is needed, however may degrade the display or cause burn-in if used for extended periods of time
| `frame.fpga_read(address, num_bytes)` | Reads a number of bytes from the FPGA at the given address
| `frame.fpga_write(address, data)`     | Writes data to the FPGA at a given address. `data` can be a string containing any byte values
