---
title: Lua API Reference
description: A reference of Lua functionality available on your Brilliant Halo.
image: /images/halo/halo-splash.png
nav_order: 4
parent: Brilliant SDK
grand_parent: Halo
---

# Lua API
{: .no_toc }

---

Lua is a tiny and extensible scripting language that's designed to be power efficient and quick to learn. Halo features a Lua virtual machine based on Lua 5.3, with dedicated hardware APIs that allow direct access to all of Halo's peripherals.

{: .note }
The Lua virtual machine on Halo has a subset of the standard library. Lua's standard `io` and `os` libraries are not present. The global `require()` function loads modules from the device filesystem (`/lfs/<module_name>.lua`) rather than using the standard Lua search path.

There's no special cables or setup needed. Lua on Halo is accessed solely over Bluetooth, such that any user-created host app can easily execute scripts by pushing Lua strings to the device. To learn more about how the underlying Bluetooth communication with Halo works, check out the [Talking to Halo Over Bluetooth](/halo/halo-sdk-bluetooth-specs) page.

### Key differences from Frame

| Feature | Frame | Halo |
|---------|-------|------|
| Display size | 640×400 | 256×256 (round) |
| Display buffering | Double-buffered (`show()` required) | Writes directly — no `show()` needed |
| Display color format | Named palette colors | `0xRRGGBB` hex values |
| Input | IMU tap | Button (single / double / long press) |
| Audio output | — | Speaker (PCM and LC3) |
| Microphone encoding | PCM only | PCM and LC3 |
| Camera image processing | Fixed JPEG output | Configurable [libmpix](https://libmpix.org/) pipeline (`frame.camera.mpix`) |
| Sleep modes | `sleep()` deep sleep | `sleep()`, `standby()`, `light_sleep()`, `ship_mode()` |
| Firmware update | `frame.update()` → Nordic DFU | MCUboot/SMP over BLE |

---

1. TOC
{:toc}

---

## System

System-level APIs, including power management, battery, and device info.

| API | Description |
|:----|:------------|
| `frame.HARDWARE_VERSION` | Hardware version string (constant). Returns `"halo"` |
| `frame.FIRMWARE_VERSION` | Firmware version string (constant). E.g. `"0.6.2-rc"` |
| `frame.GIT_TAG` | Build git tag (constant). E.g. `"c3b76c22"` |
| `frame.SE_REVISION` | Secure Enclave firmware revision (constant) |
| `frame.get_se_revision()` | Secure Enclave firmware revision (lazy-loaded) |
| `frame.battery_level()` | Battery level as a percentage (0–100) |
| `frame.battery_voltage()` | Battery voltage in millivolts |
| `frame.battery_charging()` | `true` if battery is currently charging |
| `frame.sleep([seconds])` | Deep sleep. Disconnects BLE; wakes as a reboot |
| `frame.standby([seconds])` | Standby sleep. Keeps BLE; resumes where it left off |
| `frame.light_sleep([seconds])` | Light sleep. Keeps BLE; wakes as a reboot |
| `frame.ship_mode()` | Ultra-low power shutdown for long-term storage |
| `frame.stay_awake([enable])` | Prevent or allow sleep. Returns current state if no argument |
| `frame.charge([enable])` | Enable or disable battery charging |
| `frame.on_wakeup(callback)` | Set callback for wakeup from standby (`nil` to clear) |
| `frame.wakeup_source()` | Wakeup source string (see below) |
| `frame.yield()` | Yield execution to allow other tasks to run |
| `frame.reboot()` | Reboot the system immediately |
| `frame.get_eui()` | Device EUI-64 address as a 16-character hex string |

`frame.wakeup_source()` returns one of: `"unknown"`, `"timeout"`, `"button"`, `"ble"`, `"imu"`, or `"microphone"`.

**Sleep modes comparison:**

| Mode | BLE kept | Resumes | Use case |
|------|----------|---------|----------|
| `sleep()` | No | Reboots | Deep power saving |
| `standby()` | Yes | From where it paused | Stay connected, save power |
| `light_sleep()` | Yes | Reboots | Quick naps, BLE stays alive |
| `ship_mode()` | No | Hardware reset only | Long-term storage / shipping |

```lua
-- Print device info
print(frame.HARDWARE_VERSION)  -- halo
print(frame.FIRMWARE_VERSION)  -- 0.6.2-rc
print(frame.battery_level())   -- e.g. 87

-- Standby for 10 seconds (resumes after)
frame.standby(10)

-- Register wakeup callback
frame.on_wakeup(function()
    print("Woke from: " .. frame.wakeup_source())
end)

-- Get device identity
print(frame.get_eui())  -- e.g. "1234567890ABCDEF"
```

---

## Time

Time and date APIs for real-time clock and timezone management.

| API | Description |
|:----|:------------|
| `frame.time.utc([timestamp])` | Get or set UTC time as a Unix timestamp (seconds) |
| `frame.time.zone([offset])` | Get or set timezone offset string, e.g. `"+08:00"` |
| `frame.time.date([timestamp])` | Get local date/time as a table |

The table returned by `frame.time.date()` contains: `second`, `minute`, `hour`, `day`, `month`, `year`, `weekday` (0=Sunday), `day of year`, and `is daylight saving`.

If UTC was never set, `utc()` returns device uptime in seconds from boot.

Timezone offset rules: hours -12 to +14; minutes must be `00`, `30`, or `45`; UTC±12 and UTC+14 must have `00` minutes.

```lua
-- Set current time to 2025-01-01 00:00:00 UTC
frame.time.utc(1735689600)
frame.time.zone("+10:00")

local t = frame.time.date()
print(string.format("%04d-%02d-%02d %02d:%02d:%02d",
    t.year, t.month, t.day, t.hour, t.minute, t.second))
```

---

## File System

File system APIs for reading and writing files on the device's LittleFS storage. All file paths are relative to the `/lfs/` mount point.

| API | Description |
|:----|:------------|
| `frame.file.open(filename, [mode])` | Open a file. Mode: `"r"` (read), `"w"` (write/truncate), `"a"` (append). (`"read"`, `"write"`, `"append"` also allowed.) Default: `"r"` |
| `frame.file.remove(filename)` | Delete a file or empty directory |
| `frame.file.rename(old, new)` | Rename a file or directory |
| `frame.file.listdir(path)` | List directory contents. Returns table with `name`, `size`, `type` (1=file, 2=dir) |
| `frame.file.mkdir(path)` | Create a directory (supports nested creation) |
| `frame.file.remove_all()` | Remove all files and folders. Settings file is preserved |
| `f:read()` | Read a line from file. Returns `nil` at EOF |
| `f:write(data)` | Write string data to file |
| `f:close()` | Close file (important to call after writing) |

Use `require("modulename")` to load a Lua module from `/lfs/modulename.lua`. This replaces the standard Lua `require`.

```lua
-- Write a file
local f = frame.file.open("log.txt", "w")
f:write("Hello from Halo\n")
f:close()

-- Read it back
local f = frame.file.open("log.txt", "r")
while true do
    local line = f:read()
    if line == nil then break end
    print(line)
end
f:close()

-- List the root directory
local items = frame.file.listdir("")
for _, item in ipairs(items) do
    local type_str = item.type == 1 and "file" or "dir"
    print(item.name, item.size, type_str)
end

-- Load a module
local mymod = require("mymodule")
```

---

## Button

Button event callbacks for single click, double click, and long press.

| API | Description |
|:----|:------------|
| `frame.button.single(func)` | Set (or clear with `nil`) single-click callback |
| `frame.button.double(func)` | Set (or clear with `nil`) double-click callback |
| `frame.button.long(func)` | Set (or clear with `nil`) long-press (~1s) callback |

{: .note }
The button also has system-level behaviors that override user callbacks: a 3s press puts Halo into deep sleep, an 8s press clears Bluetooth bonding and enters pairing mode, and a 15s press clears Bluetooth bonding and enters shipping mode.

```lua
frame.button.single(function()
    print("Single click!")
end)

frame.button.double(function()
    print("Double click!")
end)

frame.button.long(function()
    print("Long press!")
end)

-- Clear a callback
frame.button.single(nil)
```

---

## Bluetooth

APIs for sending and receiving raw byte data over Bluetooth. For a full description of how this works, see [Talking to Halo Over Bluetooth](/halo/halo-sdk-bluetooth-specs).

| API | Description |
|:----|:------------|
| `frame.bluetooth.is_connected()` | Returns `true` if currently connected |
| `frame.bluetooth.address()` | MAC address as `"XX:XX:XX:XX:XX:XX"` |
| `frame.bluetooth.max_length()` | Maximum data length for a single `send()` (MTU minus 1 byte) |
| `frame.bluetooth.send(data)` | Send a string over Bluetooth. Length must be ≤ `max_length()` |
| `frame.bluetooth.receive_callback(func)` | Set (or clear with `nil`) receive callback `function(data)` |

```lua
frame.bluetooth.receive_callback(function(data)
    -- echo data back to host
    frame.bluetooth.send(data)
end)

print("MTU:", frame.bluetooth.max_length())
print("MAC:", frame.bluetooth.address())
```

---

## IMU

IMU (Inertial Measurement Unit) APIs for orientation, raw sensor data, and tap detection.

| API | Description |
|:----|:------------|
| `frame.imu.tap_callback(func)` | Set (or clear with `nil`) tap detection callback |
| `frame.imu.direction()` | Returns `{pitch, roll, heading}` angles in degrees |
| `frame.imu.raw()` | Returns `{compass={x,y,z}, accelerometer={x,y,z}}` raw data |
| `frame.imu.config(options)` | Configure sampling frequency and full scale range |

`imu.raw()` returns compass data in µT (micro-Tesla) and accelerometer data in mg (milli-g).

`imu.config(options)` accepts a table with optional `accelerometer` and `magnetometer` sub-tables, each with optional `sampling_frequency` (Hz) and `full_scale` (g or Gauss) fields.

```lua
-- Orientation
local o = frame.imu.direction()
print("Pitch:", o.pitch, "Roll:", o.roll)

-- Tap callback
frame.imu.tap_callback(function()
    print("Tapped!")
end)

-- Raw sensor data
local data = frame.imu.raw()
print("Accel X:", data.accelerometer.x, "mg")

-- Configure IMU
frame.imu.config({
    accelerometer = { sampling_frequency = 200, full_scale = 16 },
    magnetometer  = { sampling_frequency = 100, full_scale = 4  }
})
```

---

## Compression

LZ4 decompression. Only decompression is supported (compression is done on the host).

| API | Description |
|:----|:------------|
| `frame.compression.process_function(func)` | Set (or clear with `nil`) callback for decompressed data blocks |
| `frame.compression.decompress(data, block_size)` | Decompress LZ4 data. `block_size` must be 1–1,048,576 |

`process_function` must be registered before calling `decompress`. The callback is invoked once per decompressed block.

```lua
frame.compression.process_function(function(data)
    local f = frame.file.open("output.bin", "a")
    f:write(data)
    f:close()
end)

-- Decompress into 4KB blocks
frame.compression.decompress(compressed_data, 4096)
```

To compress data on the host for sending to Halo:

```sh
lz4 -9 -B4096 input.bin output.lz4
```

---

## Speaker

Audio playback from the host over Bluetooth. Supports PCM and LC3 encoded audio.

| API | Description |
|:----|:------------|
| `frame.speaker.start(cfg)` | Initialize the speaker with a configuration table |
| `frame.speaker.play(data)` | Play a binary audio string directly |
| `frame.speaker.volume([val])` | Get or set volume (0–100). Get works without initialization |
| `frame.speaker.stop()` | Stop playback and release resources |

**`frame.speaker.start(cfg)` configuration:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `encoder` | string | `"pcm"` | `"pcm"` or `"lc3"` |
| `sample_rate` | number | 8000 | 8000 or 16000 Hz |
| `channels` | number | 1 | 1 (mono) or 2 (stereo) |
| `bit_depth` | number | 16 | 16 bits (PCM only) |
| `duration` | number | 1000 | LC3 frame duration: 750 or 1000 µs |
| `bitrate` | number | 16000 | LC3 bitrate (multiple of 8000, ≤96000 bps) |
| `volume` | number | 50 | Volume (0–100%) |

```lua
-- Start PCM speaker
frame.speaker.start({
    encoder = "pcm",
    sample_rate = 16000,
    channels = 1,
    volume = 80
})

-- Start LC3 speaker
frame.speaker.start({
    encoder = "lc3",
    sample_rate = 16000,
    duration = 1000,
    bitrate = 32000,
    volume = 80
})

-- Adjust volume
frame.speaker.volume(60)

-- Stop when done
frame.speaker.stop()
```

---

## Microphone

Audio recording from Halo's microphone. Supports both PCM and LC3 encoding, with optional Audio Activity Detection (AAD).

| API | Description |
|:----|:------------|
| `frame.microphone.start(cfg)` | Initialize the microphone with a configuration table |
| `frame.microphone.read(bytes)` | Read up to `bytes` bytes from the ring buffer (must be positive, even, ≤4096) |
| `frame.microphone.gain([val])` | Get or set gain (−10 to 10). Get works without initialization |
| `frame.microphone.stop()` | Stop recording and release resources |
| `frame.microphone.aad_callback(func, [threshold], [silent_period])` | Set Audio Activity Detection callback |

**`frame.microphone.start(cfg)` configuration:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `encoder` | string | `"pcm"` | `"pcm"` or `"lc3"` |
| `sample_rate` | number | 8000 | 8000 or 16000 Hz |
| `bit_depth` | number | 16 | 16 bits (PCM only) |
| `channels` | number | 1 | 1 (mono) or 2 (stereo) |
| `duration` | number | 1000 | LC3 frame duration: 750 or 1000 µs |
| `bitrate` | number | 16000 | LC3 bitrate (multiple of 8000, ≤96000 bps) |
| `gain` | number | 0 | Gain (−10 to 10) |

**`frame.microphone.aad_callback(func, [threshold], [silent_period])`:**  
`threshold` is in dB SPL (60–100; hardware supports 60, 65, 70, 75, 80, 85, 90, 95, 97.5 dB; default 90).  
`silent_period` is in ms (0–10000; default 1000): time before next detection after triggering.

`microphone.read()` returns:
- A non-empty string if data is available
- An empty string if the microphone is running but the buffer is empty
- `nil` if not streaming (or after `stop()` has been called and all data is consumed)

```lua
local mtu = frame.bluetooth.max_length()

-- Start PCM microphone at 16kHz
frame.microphone.start({
    encoder = "pcm",
    sample_rate = 16000,
    channels = 1,
    gain = 3
})

-- Stream audio to host
while true do
    local data = frame.microphone.read(mtu)
    if data == nil then break end
    if data ~= "" then
        frame.bluetooth.send(data)
    end
    frame.yield()
end
```

```lua
-- Use AAD to start recording only when sound is detected
frame.microphone.aad_callback(function()
    print("Sound detected! Recording...")
    frame.microphone.start({ encoder = "pcm", sample_rate = 16000 })
end, 75, 2000)  -- 75 dB threshold, 2 second silent period
```

---

## Display

Display APIs for drawing text, bitmaps, and vector graphics on Halo's 256×256 circular screen.

{: .note }
Unlike Frame, Halo's display has no double-buffer. Draw calls take effect immediately — there is no `show()` call required (calling it has no effect).

| API | Description |
|:----|:------------|
| `frame.display.text(text, x, y, color)` | Draw text at `x, y`. `color` is `0xRRGGBB` (default `0xFFFFFF`) |
| `frame.display.char(codepoint, x, y, color)` | Draw a single Unicode character by codepoint |
| `frame.display.bitmap(x, y, width, format, offset, data, [opts])` | Draw indexed or RGB bitmap |
| `frame.display.set_pixel(x, y, color)` | Set a single pixel |
| `frame.display.line(x0, y0, x1, y1, color)` | Draw a line |
| `frame.display.rect(x, y, w, h, color, filled)` | Draw a rectangle (filled or outline) |
| `frame.display.circle(cx, cy, r, color, filled)` | Draw a circle (filled or outline) |
| `frame.display.polygon(points, color)` | Draw a polygon from `{x, y, x2, y2 ... }` array |
| `frame.display.clear([color])` | Clear screen to `color` (default `0x000000`) |
| `frame.display.width()` | Display width in pixels (256) |
| `frame.display.height()` | Display height in pixels (256) |
| `frame.display.brightness([value])` | Get or set brightness (0–100%) |
| `frame.display.show([enable])` | No-op — Halo renders directly without a buffer flip |

**Color palette commands:**

| API | Description |
|:----|:------------|
| `frame.display.assign_color(index, r, g, b)` | Set palette entry by index (0–15 or color name) using RGB888 |
| `frame.display.assign_color_ycbcr(index, y, cb, cr)` | Set palette entry using native YCbCr (4+3+3 bits) |

**Bitmap (`frame.display.bitmap`) parameters:**

| Parameter | Description |
|-----------|-------------|
| `x, y` | Top-left position (1–256) |
| `width` | Bitmap width in pixels |
| `color_format` | `0` = RGB888, `2` = 2bpp, `4` = 4bpp, `16` = 16bpp |
| `palette_offset` | Palette index offset (0–15) |
| `data` | Pixel data string (binary) |
| `options` | Optional table: `x_scale`, `y_scale` (scale factors), `palette_data` (custom 3-bytes-per-color RGB string) |

**Color palette names:** `VOID`, `WHITE`, `GREY`, `RED`, `PINK`, `DARKBROWN`, `BROWN`, `ORANGE`, `YELLOW`, `DARKGREEN`, `GREEN`, `LIGHTGREEN`, `NIGHTBLUE`, `SEABLUE`, `SKYBLUE`, `CLOUDBLUE`

<table>
<tbody><tr>
<td style="background-color: #000000;"><font color="White">#0<br> VOID</font></td>
<td style="background-color: #FFFFFF;"><font color="Black">#1<br> WHITE</font></td>
<td style="background-color: #9D9D9D;"><font color="Black">#2<br> GREY</font></td>
<td style="background-color: #BE2633;"><font color="Black">#3<br> RED</font></td>
<td style="background-color: #E06F8B;"><font color="Black">#4<br> PINK</font></td>
<td style="background-color: #493C2B;"><font color="White">#5<br> DARKBROWN</font></td>
<td style="background-color: #A46422;"><font color="Black">#6<br> BROWN</font></td>
<td style="background-color: #EB8931;"><font color="Black">#7<br> ORANGE</font></td>
</tr>
<tr>
<td style="background-color: #F7E26B;"><font color="Black">#8<br> YELLOW</font></td>
<td style="background-color: #2F484E;"><font color="White">#9<br> DARKGREEN</font></td>
<td style="background-color: #44891A;"><font color="Black">#10<br> GREEN</font></td>
<td style="background-color: #A3CE27;"><font color="Black">#11<br> LIGHTGREEN</font></td>
<td style="background-color: #1B2632;"><font color="White">#12<br> NIGHTBLUE</font></td>
<td style="background-color: #005784;"><font color="White">#13<br> SEABLUE</font></td>
<td style="background-color: #31A2F2;"><font color="Black">#14<br> SKYBLUE</font></td>
<td style="background-color: #B2DCEF;"><font color="Black">#15<br> CLOUDBLUE</font></td>
</tr>
</tbody></table>

**Display pan:**

| API | Description |
|:----|:------------|
| `frame.display.set_pan(x, y)` | Shift display content. Both values in range −50 to +50 |
| `frame.display.get_pan()` | Returns current `x, y` pan offset |

Pan settings are saved to non-volatile storage and restored after reboot or wakeup from sleep.

```lua
-- Draw some text
frame.display.text("Hello Halo", 50, 50)

-- Draw a filled blue circle (Halo only)
frame.display.circle(128, 128, 50, 0x0055FF, true)

-- Draw a white outline rectangle (Halo only)
frame.display.rect(20, 20, 80, 40, 0xFFFFFF, false)

-- Custom palette
frame.display.assign_color(1, 255, 128, 0)  -- orange at index 1

-- Clear screen to black (Halo only)
frame.display.clear(0x000000) -- or just frame.display.clear()

-- Display a 2bpp indexed bitmap
local pixels = string.rep("\xFF", 32 / 8 * 32)  -- 32×32 white block
frame.display.bitmap(100, 100, 32, 2, 0, pixels)
```

---

## Camera

Camera capture APIs. Halo's camera captures images in JPEG format. Only 640px resolution is supported. Camera images are read in Lua and sent to the host over the regular data channel using `frame.bluetooth.send()` (see [Bluetooth specs](/halo/halo-sdk-bluetooth-specs)).

| API | Description |
|:----|:------------|
| `frame.camera.capture([cfg])` | Start async image capture. `cfg` may include `resolution` (640) and `quality` |
| `frame.camera.image_ready()` | Returns `true` when the capture is complete and ready to read |
| `frame.camera.read(bytes)` | Read `bytes` of JPEG data. Returns `nil` when all data is consumed |
| `frame.camera.read_raw(bytes)` | Read raw sensor data (skips JPEG header) |
| `frame.camera.power_save(flag)` | `true` to sleep the camera; `false` to wake it |

Quality options: `"VERY_HIGH"`, `"HIGH"`, `"MEDIUM"`, `"LOW"`, `"VERY_LOW"`.

If the camera is in power save mode, call `camera.power_save(false)` before capturing.

```lua
local mtu = frame.bluetooth.max_length()

-- Capture a photo
frame.camera.capture({ quality = "HIGH" })

-- Wait until ready
while not frame.camera.image_ready() do
    frame.sleep(0.05)
end

-- Stream JPEG to host
while true do
    local data = frame.camera.read(mtu)
    if data == nil then break end
    frame.bluetooth.send(data)
end

-- Put camera to sleep when not needed
frame.camera.power_save(true)
```

---

## Camera Image Processing (libmpix)

Halo integrates [libmpix](https://libmpix.org/), an image signal processing library that gives Lua scripts direct control over the camera pipeline. Instead of receiving a fixed JPEG, you can compose a pipeline of operations — debayering, colour correction, denoise, resize, format conversion — before the image is encoded.

{: .note }
`frame.camera.mpix` is a Halo-only API. It has no equivalent on Frame.

The firmware automatically computes per-frame statistics (luminance histogram, per-channel averages) and uses them for auto black-level and auto white-balance. These auto values are applied through the pipeline's `correct_black_level` and `correct_white_balance` operations. The default pipeline (used if you don't call `set_pipeline`) is:

```
debayer_2x2 → correct_black_level → correct_white_balance → jpeg_encode
```

### Pipeline operations

All pipeline operations take the pipeline table as their first argument and append themselves to it. Call `frame.camera.mpix.set_pipeline(pipeline)` to install the pipeline; it takes effect on the next `frame.camera.capture()` call.

| API | Parameters | Description |
|:----|:-----------|:------------|
| `frame.camera.mpix.op.debayer_2x2(p)` | — | 2×2 binned debayer (fastest; default) |
| `frame.camera.mpix.op.debayer_1x1(p)` | — | Full-resolution 1×1 debayer |
| `frame.camera.mpix.op.debayer_3x3(p)` | — | 3×3 high-quality debayer |
| `frame.camera.mpix.op.debayer_ir_5x3(p)` | — | 5×3 debayer for IR-cut sensor patterns |
| `frame.camera.mpix.op.correct_black_level(p)` | — | Subtract black level (set via `cid.BLACK_LEVEL` or auto) |
| `frame.camera.mpix.op.correct_white_balance(p)` | — | Apply red/blue channel balance (auto or manual) |
| `frame.camera.mpix.op.correct_gamma(p)` | — | Apply gamma correction (set via `cid.GAMMA_LEVEL`) |
| `frame.camera.mpix.op.correct_color_matrix(p)` | — | Apply 3×3 color correction matrix |
| `frame.camera.mpix.op.correct_fused(p)` | — | Fused black level + gamma + color matrix in one pass |
| `frame.camera.mpix.op.convert(p, fmt)` | `fmt` — pixel format constant from `mpix.fmt` | Convert to a different pixel format |
| `frame.camera.mpix.op.crop(p, x, y, w, h)` | Pixel offset and dimensions | Crop image to a sub-region |
| `frame.camera.mpix.op.resize_subsample(p, w, h)` | Target width and height | Downsample by integer subsampling |
| `frame.camera.mpix.op.kernel_convolve_3x3(p, type)` | `type` — kernel constant from `mpix.kernel` | Apply a 3×3 convolution kernel |
| `frame.camera.mpix.op.kernel_convolve_5x5(p, type)` | `type` — kernel constant from `mpix.kernel` | Apply a 5×5 convolution kernel |
| `frame.camera.mpix.op.kernel_denoise_3x3(p)` | — | 3×3 median denoise |
| `frame.camera.mpix.op.kernel_denoise_5x5(p)` | — | 5×5 median denoise |
| `frame.camera.mpix.op.jpeg_encode(p)` | — | Encode to JPEG (quality via `cid.JPEG_QUALITY`) |
| `frame.camera.mpix.op.qoi_encode(p)` | — | Encode to QOI lossless format |
| `frame.camera.mpix.op.palette_encode(p, fmt)` | `fmt` — palette format (`mpix.fmt.PALETTE1`…`PALETTE8`) | Quantise to a colour palette |
| `frame.camera.mpix.op.palette_decode(p)` | — | Expand a palette image back to RGB |

### Controls

Controls are integer values applied to the pipeline. Balance values use Q10 fixed-point (multiply the floating-point ratio by 1024).

| API | Description |
|:----|:------------|
| `frame.camera.mpix.set_ctrl(cid, value)` | Set a control value. `cid` is a constant from `frame.camera.mpix.cid` |

| Control (`frame.camera.mpix.cid.*`) | Description |
|:-------------------------------------|:------------|
| `BLACK_LEVEL` | Subtracted from every pixel before colour processing |
| `GAMMA_LEVEL` | Gamma curve level |
| `RED_BALANCE` | Red channel multiplier in Q10 (e.g. `1229` ≈ ×1.2) |
| `BLUE_BALANCE` | Blue channel multiplier in Q10 (e.g. `1843` ≈ ×1.8) |
| `JPEG_QUALITY` | JPEG quality (higher = better quality, larger file) |
| `COLOR_MATRIX_0` … `COLOR_MATRIX_8` | 3×3 color correction matrix entries in Q10 (row-major) |

### Statistics

`frame.camera.mpix.get_stats()` returns a table populated after the previous frame was processed. The firmware calls this internally for auto-tuning; you can also use it in your own Lua logic.

| Field | Description |
|:------|:------------|
| `y_histogram` | Array of luminance histogram bin counts |
| `y_histogram_vals` | Corresponding luminance values for each bin |
| `y_histogram_total` | Total pixel count across all bins |
| `rgb_average_r/g/b` | Per-channel average pixel value |
| `rgb_min_r/g/b` | Per-channel minimum pixel value |
| `rgb_max_r/g/b` | Per-channel maximum pixel value |
| `nvals` | Number of pixels sampled for statistics |

### Kernel and format constants

**`frame.camera.mpix.kernel`** — convolution kernel presets for `kernel_convolve_*` operations:

| Constant | Effect |
|:---------|:-------|
| `edge_detect` | Highlight edges |
| `gaussian_blur` | Smooth/blur |
| `identity` | No-op (pass-through) |
| `sharpen` | Enhance edges/detail |

**`frame.camera.mpix.fmt`** — pixel format constants for `convert` and `palette_encode`:
`RGB332`, `RGB565`, `RGB24`, `XRGB32`, `YUV24`, `YUYV`, `GREY`, `JPEG`, `QOI`, `PALETTE1`–`PALETTE8`, and raw Bayer formats (`SBGGR8`, `SGBRG8`, etc.).

### Example

```lua
local mtu = frame.bluetooth.max_length()

-- Build a custom pipeline: denoise, then encode as JPEG
local pipeline = {}
frame.camera.mpix.op.debayer_2x2(pipeline)
frame.camera.mpix.op.correct_black_level(pipeline)
frame.camera.mpix.op.correct_white_balance(pipeline)
frame.camera.mpix.op.kernel_denoise_3x3(pipeline)
frame.camera.mpix.op.jpeg_encode(pipeline)
frame.camera.mpix.set_pipeline(pipeline)

-- Wake the camera and capture
frame.camera.power_save(false)
frame.camera.capture({ quality = "HIGH" })

-- Wait until processing is complete
while not frame.camera.image_ready() do
    frame.sleep(0.05)
end

-- Stream JPEG data to the host
while true do
    local data = frame.camera.read(mtu)
    if data == nil then break end
    frame.bluetooth.send(data)
end
```

You can also customise controls manually — for example to override the auto white balance:

```lua
-- Manual white balance: Q10 fixed-point (value = ratio × 1024)
frame.camera.mpix.set_ctrl(frame.camera.mpix.cid.RED_BALANCE,  math.floor(1.4 * 1024))
frame.camera.mpix.set_ctrl(frame.camera.mpix.cid.BLUE_BALANCE, math.floor(2.0 * 1024))
```

Or to use `get_stats()` from the previous frame to tune the next one:

```lua
local stats = frame.camera.mpix.get_stats()
print("Avg luminance R/G/B:", stats.rgb_average_r, stats.rgb_average_g, stats.rgb_average_b)
```

---
