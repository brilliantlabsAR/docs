---
title: Python
description: An overview of the Brilliant SDK for building Python apps that talk to Brilliant Halo.
image: /images/halo/halo-splash.png
nav_order: 1
parent: Brilliant SDK
grand_parent: Halo
nav_enabled: true
---

# Brilliant SDK for Python
{: .no_toc }

---

The Brilliant SDK for Python is available in a low-level library ([brilliant-ble](https://pypi.org/project/brilliant-ble/)) for Bluetooth LE connectivity using [Bleak](https://github.com/hbldh/bleak), an application-level library ([brilliant-msg](https://pypi.org/project/brilliant-msg/)) for passing rich objects between your host program and Halo — such as images, streamed audio, and rasterized text — and an experimental software emulator ([halo-emulator](https://github.com/brilliantlabsAR/brilliant_sdk/tree/halo/python/packages/halo_emulator)) for developing and testing Halo apps without any hardware.

The Brilliant SDK for Python also supports **Frame** devices. `brilliant-ble` automatically detects whether the connected device is a Halo or a Frame at connection time.

---

1. TOC
{:toc}

---

## `brilliant-ble` package: low-level connectivity

| [![Available on PyPI](https://img.shields.io/pypi/v/brilliant-ble)](https://pypi.org/project/brilliant-ble/){:target="_blank"} | [Source](https://github.com/brilliantlabsAR/brilliant_sdk/tree/main/python/packages/brilliant_ble){:target="_blank"} |

The `BrilliantBle` class connects to Halo (or Frame), initiating pairing if required. Lua strings can be sent for execution, optionally returning their results. Transmitted strings must be shorter than `BrilliantBle.max_lua_payload()`.

[Halo-specific Lua APIs](/halo/halo-sdk-lua) can be called to draw on the display, sample the IMU, set button and data callbacks, control the microphone and speaker, and more.

In addition to Lua strings, `BrilliantBle` can send control commands (break, reset, remove) and custom user data messages handled by a data callback on Halo. See [Talking to Halo Over Bluetooth](/halo/halo-sdk-bluetooth-specs) for more details.

**Halo-specific features in `brilliant-ble` 2.0.0:**
- `BrilliantBle.type` — detected `BrilliantDeviceType` (`FRAME`, `HALO`, or `UNKNOWN`) after connection
- `send_audio(data)` — writes LC3 or PCM audio to the Halo audio characteristic
- `send_remove_signal()` — sends `0x05` to remove `main.lua` and reset the Lua VM
- `send_data(await_data=True)` — receiver-paced flow control using ACK bytes from the device

### Example usage
{: .no_toc }

```bash
uv add brilliant-ble
# or: pip install brilliant-ble
```

```python
import asyncio
from brilliant_ble import BrilliantBle

async def main():
    frame = BrilliantBle()

    try:
        await frame.connect()

        print(f"Connected to: {frame.type}")  # BrilliantDeviceType.HALO

        await frame.send_lua(
            "frame.display.text('Hello, Halo!', 50, 50); print(nil)",
            await_print=True
        )

        await frame.disconnect()

    except Exception as e:
        print(f"Not connected to Halo: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## `brilliant-msg` package: application-level messaging

| [![Available on PyPI](https://img.shields.io/pypi/v/brilliant-msg)](https://pypi.org/project/brilliant-msg/){:target="_blank"} | [Source](https://github.com/brilliantlabsAR/brilliant_sdk/tree/main/python/packages/brilliant_msg){:target="_blank"} |

`brilliant-msg` enables the host and Halo-side halves of an application to **communicate using richly typed messages** — for example transmitting sprites to Halo with width, height, palette data, and pixel data as a single object.

`brilliant-msg` uses a programming model in which **a main event loop runs on Halo**. Messages are exchanged asynchronously and handled in an event-driven way. This makes it practical to build applications that simultaneously stream audio from Halo to the host *and* send display content back to Halo.

### How it works
{: .no_toc }

Large objects are serialized into multiple Bluetooth packets marked with a `msg_code`, and **efficiently reassembled on the device**. After parsing, the complete object is delivered to the Lua main loop.

* **`Tx` message types** — packing (Python) + parsing (Lua) — e.g. `TxSprite.pack()` + `sprite.lua`
* **`Rx` message types** — parsing (Python) + implicit serialization in Lua — e.g. `RxPhoto` + `camera.lua`

**Key changes for Halo in `brilliant-msg` 6.0.0:**
- `RxClick` — Halo button click events (`single`, `double`, `long`), msg code `0x0B`
- `data.lua` — queue-based message ordering with ACK byte flow control
- `imu.lua` — 6 × `float32` IMU values with Halo-specific axis mapping
- `sprite.lua` — Halo uses integer palette indices (0–15); Frame uses named color strings
- `audio.lua` — updated for Halo audio streaming

### Startup sequence
{: .no_toc }

`brilliant-msg` applications follow a standard sequence:

1. Send break/reset/break signals to ensure Halo is in Lua REPL mode
2. Upload standard Lua libraries (`data`, `sprite`, `plain_text`, etc.)
3. Upload the main Lua application file
4. Start the Halo-side event loop (after which, no REPL commands are accepted)
5. Exchange messages asynchronously

### Example usage
{: .no_toc }

```bash
uv add brilliant-msg
# or: pip install brilliant-msg
```

`sprite_display.py`
```python
import asyncio
from pathlib import Path
from brilliant_msg import BrilliantMsg, TxSprite

async def main():
    frame = BrilliantMsg()
    try:
        await frame.connect()

        await frame.print_short_text('Loading...')

        # Upload Lua libraries and main app
        await frame.upload_stdlua_libs(lib_names=['data', 'sprite'])
        await frame.upload_frame_app(local_filename="lua/halo_app.lua")

        frame.attach_print_response_handler()
        await frame.start_frame_app()

        # Send a 4-bit indexed PNG sprite to Halo
        sprite = TxSprite.from_indexed_png_bytes(Path("images/logo_4bit.png").read_bytes())
        await frame.send_message(0x20, sprite.pack())

        await asyncio.sleep(5.0)

        frame.detach_print_response_handler()
        await frame.stop_frame_app()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await frame.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

`lua/halo_app.lua`
```lua
local data = require('data.min')
local sprite = require('sprite.min')

USER_SPRITE = 0x20

function app_loop()
  frame.display.power_save(false)
  frame.display.clear()
  print('Halo app is running')

  while true do
    rc, err = pcall(function()
      local items = data.process_raw_items()

      for _, item in ipairs(items) do
        local msg_code, raw = item[1], item[2]

        if msg_code == USER_SPRITE then
          local spr = sprite.parse_sprite(raw)
          frame.display.bitmap(1, 1, spr.width, 2^spr.bpp, 0, spr.pixel_data, {palette_data=spr.palette_data})
        end
      end

      frame.sleep(0.001)
    end)
    if rc == false then
      print(err)
      frame.display.clear()
      break
    end
  end
end

app_loop()
```

| Selected Message Types | Description |
|------------------------|-------------|
| `TxSprite` | Send an indexed-color PNG image for display |
| `TxCaptureSettings` | Request a photo from the camera |
| `RxPhoto` | Receive a JPEG photo from the camera |
| `RxAudio` | Receive a PCM or LC3 audio stream |
| `RxIMU` | Receive accelerometer and magnetometer readings |
| `RxClick` | Receive Halo button click events (single / double / long) |

---

## `halo-emulator` package: develop without hardware (experimental)

| [Source](https://github.com/brilliantlabsAR/brilliant_sdk/tree/halo/python/packages/halo_emulator){:target="_blank"} |

The `halo-emulator` package embeds a full Lua 5.3 runtime and replaces all `frame.*` calls with Python stubs, rendering display output to a 256×256 pixel buffer. This lets you develop, test, and debug Halo Lua apps entirely in software — no hardware required.

**Key features:**
- Full Lua 5.3 runtime via [lupa](https://github.com/scoder/lupa) — run unmodified Halo Lua scripts
- Virtual 256×256 display — all drawing primitives, palette, text, and bitmap rendering
- Event injection — trigger BLE data, button presses, and IMU taps from Python
- Test-friendly — inspect the framebuffer as a PIL `Image`, capture `bluetooth.send()` calls
- Interactive REPL — `halo-emulator ./app/` opens a live pygame window and Python REPL
- Sandboxed filesystem — `frame.file.*` operations run against a real directory

### Installation
{: .no_toc }

`halo-emulator` is not published to PyPI. Install it by cloning the `brilliant_sdk` repository — see [Installing from source](#installing-from-source) below.

### Quick start
{: .no_toc }

```python
from halo_emulator import HaloEmulator

with HaloEmulator(sandbox_dir='./my_app') as emu:
    emu.load_directory('./my_app')  # copy .lua files into sandbox
    emu.start('main.lua')
    emu.wait(timeout=5.0)

    img = emu.get_framebuffer()     # PIL Image (256×256 RGBA)
    img.save('output.png')
```

### Interactive REPL
{: .no_toc }

```bash
halo-emulator ./my_app/
```

Opens a 512×512 pygame window (2× scaled) with a Python REPL. Keyboard shortcuts:

| Key | Action |
|-----|--------|
| `Space` | Button single click |
| `D` | Button double click |
| `L` | Button long press |
| `T` | IMU tap |

```bash
halo-emulator ./my_app/ --script frame_app.lua   # specify entry point
halo-emulator ./my_app/ --headless               # REPL only, no window
```

### Event injection
{: .no_toc }

```python
emu.inject_bluetooth_data(b'\x0a\x00\x05Hello')   # triggers receive_callback
emu.inject_button_single()                          # triggers button.single callback
emu.inject_button_double()                          # triggers button.double callback
emu.inject_button_long()                            # triggers button.long callback
emu.inject_imu_tap()                               # triggers imu.tap_callback
```

### State configuration
{: .no_toc }

```python
emu.set_battery_level(42)
emu.set_battery_charging(True)
emu.set_imu_direction(pitch=15.0, roll=-5.0, heading=0.0)
emu.set_imu_raw(compass=(10, 20, 30), accel=(0, 0, 1000))
```

### Writing automated tests
{: .no_toc }

```python
import time, pytest
from halo_emulator import HaloEmulator

@pytest.fixture
def emulator(tmp_path):
    emu = HaloEmulator(sandbox_dir=tmp_path, print_handler=None)
    yield emu
    if emu.is_running():
        emu.stop()

def test_display_shows_text(emulator, tmp_path):
    (tmp_path / 'main.lua').write_text("""
        frame.display.text('Hello', 10, 10, 0xFFFFFF)
    """)
    emulator.start()
    emulator.wait(timeout=3.0)

    img = emulator.get_framebuffer()
    pixels = list(img.getdata())
    bright = sum(1 for r, g, b, a in pixels if r + g + b > 30)
    assert bright > 0

def test_button_press_triggers_callback(emulator, tmp_path):
    (tmp_path / 'main.lua').write_text("""
        frame.button.single(function()
            frame.bluetooth.send('\x01')
        end)
        frame.sleep(5.0)
    """)
    emulator.start()
    time.sleep(0.1)
    emulator.inject_button_single()
    time.sleep(0.2)
    assert b'\x01' in emulator.get_bluetooth_sent()
```

Run tests from the workspace root:

```bash
cd python
uv sync --all-packages --all-extras
uv run pytest packages/brilliant_msg/tests/ packages/halo_emulator/tests/
```

---

## Installing from source

When working from the `brilliant_sdk` repository, install all packages as editable installs so local changes are immediately reflected:

```bash
git clone https://github.com/brilliantlabsAR/brilliant_sdk.git
cd brilliant_sdk/python
uv sync --all-packages
```

The `uv` workspace configuration ensures `brilliant-ble` and `brilliant-msg` resolve to local packages rather than PyPI.
