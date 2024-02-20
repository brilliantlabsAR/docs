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

There's no special cables or setup needed. Lua on Frame is accessed directly over Bluetooth, such that any user created app can easily execute scripts by simply pushing Lua strings to the device.

To learn more how the underlying Bluetooth communication with Frame works, check out the Bluetooth section of the [Building Apps](/frame/building-apps#bluetooth) page.

---

## Library reference
{: .no_toc }

This page describes all of the Frame specific Lua APIs available to the developer to access with helpful examples.

1. TOC
{:toc}

---

### Display

The display engine of Frame consists of two frame buffers. While one buffer is being displayed, the other buffer is drawn to using the below commands. The `show()` command then switches the buffers such that everything that was drawn on the background buffer becomes visible on the display, and the previous displayed buffer can now be edited following a `clear()` command.

The Frame display is capable of rendering up to 16 colors at one time. Each of these colors can take on any 8bit YCbCr color value, however for convenience, the `assign_color()` API can be used to pass a color value in common 24bit RGB format.

| Function&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
|:---------|:------------|
| `frame.display.clear()`                                     | Clears the display buffer
| `frame.display.assign_color(index, red, green, blue)`       | Assigns a color the 16 color pallet. `index` can be between `1` and `16`. Pallet index `1` always represents the background (transparent) color
| `frame.display.assign_color_ycbcr(index, y, cb, cr)`        | Same as `assign_color()` but in the display's native YCbCr format. Note that `Y` will be truncated to the top 4 bits, and `Cb` and `Cr` will each be truncated to 2 bits
| `frame.display.bitmap()`                                    | *Coming soon*
| `frame.display.text(string, x, y, color, align='TOP_LEFT')` | 
| `frame.display.vector()`                                    | *Coming soon*
| `frame.display.show()`                                      | Swaps frame buffers and shows contents to the display


#### Example
{: .no_toc }

```lua
-- Display "Hello world" at x = 50 and y = 100
frame.display.clear()
frame.display.text('Hello world', 50, 100)
frame.display.show()
```

---

### Camera

| Function&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
|:---------|:------------|
| `frame.camera.capture(zoom=1, pan=0)`       |
| `frame.camera.read(bytes)`                  |
| `frame.camera.sleep()`                      |
| `frame.camera.wake()`                       |
| `frame.camera.set_register(address, value)` |

#### Example
{: .no_toc }

```lua

```

---

### Microphone

| Function&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
|:---------|:------------|
| `frame.microphone.record(seconds=inf, sample_rate=8000, bit_depth=8)` |
| `frame.microphone.read(bytes)`                                        |

#### Example
{: .no_toc }

```lua

```

---

### Motion sensor (IMU)

| Function&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
|:---------|:------------|
| `frame.imu.direction()` |
| `frame.imu.tap_callback(handler_function)` |

#### Example
{: .no_toc }

```lua

```

---

### Bluetooth

| Function&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
|:---------|:------------|
| `frame.bluetooth.address()` | Returns the device MAC address as a 17 character string. E.g. `4E:87:B5:0C:64:0F`
| `frame.bluetooth.receive_callback(handler_function)` |
| `frame.bluetooth.max_length()` |
| `frame.bluetooth.send(data)` |

#### Example
{: .no_toc }

```lua

```

---

### File system

| Function&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
|:---------|:------------|
| `frame.file.open(filename, mode)` |
| `frame.file.remove(filename)` |
| `frame.file.rename(filename, new_filename)` |
| `frame.file.listdir(directory)` |
| `frame.file.mkdir(pathname)` |
| `f:read()` |
| `f:write(data)` |
| `f:close()` |

#### Example
{: .no_toc }

```lua

```

---

### Time functions

| Function&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
|:---------|:------------|
| `frame.time.utc(*timestamp)` |
| `frame.zone(*offset)` |
| `frame.date(*timestamp)` |

#### Example
{: .no_toc }

```lua

```

---

### System functions

| Function&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;| Description |
|:---------|:------------|
| `frame.FIRMWARE_VERSION` | Returns the current firmware version as a 12 character string. E.g. `v24.046.1546`
| `frame.GIT_TAG` | Returns the current firmware git tag as a 7 character string. E.g. `4a6ea0b`
| `frame.battery_level()` | 
| `frame.sleep(*seconds)` | 
| `frame.stay_awake(enable)` | 
| `frame.fpga_write(address, data)` | 
| `frame.fpga_read(address)` | 
| `frame.update()` | 
