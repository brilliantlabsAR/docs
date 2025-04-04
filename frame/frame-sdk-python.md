---
title: Python
description: An overview of the Frame SDK for building Python apps that talk to Frame AR glasses.
image: /images/frame/frame-splash.png
nav_order: 1
parent: Frame SDK
grand_parent: Frame
nav_enabled: true

---

# Frame SDK for Python
{: .no_toc }

---

The Frame SDK for Python is available in a low-level library ([frame-ble](https://pypi.org/project/frame-ble/)) for Bluetooth LE connectivity using [Bleak](https://github.com/hbldh/bleak) with a limited Lua REPL, and an application-level library ([frame-msg](https://pypi.org/project/frame-msg/)) for passing rich objects between your host program and Frame, such as images, streamed audio, IMU data and rasterized text.

---

1. TOC
{:toc}

---

## `frame-ble` package: low-level connectivity

| [![Available on PyPI](https://img.shields.io/pypi/v/frame-ble)](https://pypi.org/project/frame-ble/){:target="_blank"} | [API Reference](https://frame-ble-python.readthedocs.io/){:target="_blank"} | [Source](https://github.com/CitizenOneX/frame_ble_python){:target="_blank"} | [Examples](https://github.com/CitizenOneX/frame_examples_python/tree/main/frame_ble){:target="_blank"} |

The `FrameBle` class allows a host to connect to Frame, initiating pairing if required. A sequence of Lua strings can be sent to Frame for execution, optionally returning their results as strings. Transmitted and received strings must be shorter than the Bluetooth MTU (`FrameBle.max_lua_payload()`).

[Frame-specific Lua APIs](frame-sdk-lua.md) can be called to draw on the display, sample the accelerometer, put Frame into firmware update mode, set the tap and user data callbacks, and more.

In addition to Lua strings, `FrameBle` can also send control commands (break and reset), as well as custom user data messages that can be handled by a user-defined data handler function on Frame. See [Talking to Frame Over Bluetooth](frame-sdk-bluetooth-specs.md) for more details.

Consult the [API Reference](https://frame-ble-python.readthedocs.io/){:target="_blank"} for the complete list of functions available in `frame-ble`, and the [Examples repo](https://github.com/CitizenOneX/frame_examples_python/tree/main/frame_ble){:target="_blank"} to see them in action. Don't see an example you need? Ask in [Discord](https://discord.com/invite/vDS9X7gdwg){:target="_blank"} to have one added.

Note: It is expected that most application developers will prefer to use `FrameMsg` from the [frame-msg package](https://pypi.org/project/frame-msg/) to make use of first-class messages and efficient transport for sprites, images, audio clips, and to avoid having to wrangle Bluetooth packet fragmentation and assembly. The `frame-ble` package, with only a dependency on the `bleak` library, is still a handy choice for `"Hello, World!"`, simple utilities, or as the basis of a custom application framework in Python.

<iframe width="720" height="405" src="https://www.youtube.com/embed/D4E8uAyt9CI" frameborder="0" allowfullscreen> </iframe>

### Example usage
{: .no_toc }
```bash
pip install frame-ble
```

```python
import asyncio
from frame_ble import FrameBle

async def main():
    frame = FrameBle()

    try:
        await frame.connect()

        await frame.send_lua("frame.display.text('Hello, Frame!', 1, 1);frame.display.show();print(nil)", await_print=True)

        await frame.disconnect()

    except Exception as e:
        print(f"Not connected to Frame: {e}")
        return

if __name__ == "__main__":
    asyncio.run(main())
```

| Selected Examples |
|-------------------|
| ["Hello, World!"](https://github.com/CitizenOneX/frame_examples_python/blob/main/frame_ble/hello_world.py){:target="_blank"} |
| [Clear the display](https://github.com/CitizenOneX/frame_examples_python/blob/main/frame_ble/clear_display.py){:target="_blank"} |
| [Echo printed outputs from Lua code executing on Frame](https://github.com/CitizenOneX/frame_examples_python/blob/main/frame_ble/echo.py){:target="_blank"} |
| [Upload and invoke a custom Lua function from a file](https://github.com/CitizenOneX/frame_examples_python/blob/main/frame_ble/custom_lua_functions.py){:target="_blank"} |
| [Upload and invoke a function demonstrating lz4 decompression on Frame](https://github.com/CitizenOneX/frame_examples_python/blob/main/frame_ble/decompression.py){:target="_blank"} |

---

## `frame-msg` package: application-level messaging

| [![Available on PyPI](https://img.shields.io/pypi/v/frame-msg)](https://pypi.org/project/frame-msg/){:target="_blank"} | [API Reference](https://frame-msg-python.readthedocs.io/){:target="_blank"} | [Source](https://github.com/CitizenOneX/frame_msg_python){:target="_blank"} | [Examples](https://github.com/CitizenOneX/frame_examples_python/tree/main/frame_msg){:target="_blank"} |

`frame-msg` enables both the hostside and Frameside halves of an application to **communicate using richly typed messages** - for example transmitting Sprites to Frame with width, height, palette data and pixel data attributes. (See the code below for an example.)

Additionally, `frame-msg` uses a programming model in which **a main event loop is running on Frame**. As a result, messages are exchanged asychronously and handled in an event-driven way. This is in contrast to the "Lua REPL" model, in which single statements are sent to Frame to be executed, and the host attempts to block until execution has completed. In a REPL-style model, it would not be practical to create an application that for example continuously streams audio from Frame to host, and simultaneously sends text back for display (a live translation app). In contrast, with a main event loop running on Frame it is possible to send some audio back to the host if some is available, and check for messages indicating text is ready for display, then loop around again.

<iframe width="720" height="405" src="https://www.youtube.com/embed/E49wf4caHKQ" frameborder="0" allowfullscreen> </iframe>

### How it works
{: .no_toc }

In order to **serialize and deserialize large objects**, `frame-msg` makes use of `FrameBle`'s `send_message()` function that **fragments large payloads** into multiple Bluetooth packets marked with a matching **`msg_code`**, and **efficiently reassembles them on Frame**. After parsing the reconstructed payload into the desired type, a complete object is made available for the application's main loop in Lua.

Handling **rich message types** is done by providing symmetrical **packing code and parsing code** for standard types.

* For "Transmit" (`Tx`) message types, the packing (serialization) code is in the Python type (e.g. `TxSprite.pack()`) and the parsing (deserialization) code is in the corresponding Lua module (`sprite.lua` / `parse_sprite()`).

* For "Receive" (`Rx`) message types, e.g. `RxPhoto`, the serialization code is present implicitly in the Lua module `camera.lua` in `capture_and_send()`, and the deserialization code is present in the `RxPhoto` class.

This approach presents a natural extension point for user-defined types too: a custom application-specific message might contain an icon, a heading and some detailed text - and this can all be sent together and used all at once on Frame to update the display. By implementing the packing and parsing code for user-defined types, custom objects can be used in applications in the same way as the standard types.

### Startup sequence
{: .no_toc }

`frame-msg` applications tend to follow a startup sequence that ensures Frame is in a known state for the application to run, namely:
* Optionally send a break/reset/break signal sequence to ensure that Frame is in Lua REPL mode and its memory is freshly cleared
* Upload standard Lua libraries to Frame: `data` for handling all messaging, plus any others to support specific messages the application uses (e.g. `sprite`, `plain_text`, etc.) Unless specified otherwise, [minified Lua code files](https://en.wikipedia.org/wiki/Minification_(programming)) are uploaded, so make sure your Frameside app includes `sprite.min` in this case.
* Upload the main Frame application Lua file (e.g. `my_frame_app.lua`). This can often be an exact copy of an example main Lua file that handles the same message types.
* Start the main application loop on Frame (after which no Lua REPL commands will be accepted by Frame).

After the Frameside application reports that it has started, the hostside and Frameside application halves begin messaging each other asynchronously: passing text, images, audio etc.

<iframe width="720" height="405" src="https://www.youtube.com/embed/y5kUzPKrFpk" frameborder="0" allowfullscreen> </iframe>

## Example usage
{: .no_toc }
```bash
pip install frame-msg
```

`sprite_display.py`
```python
import asyncio
from pathlib import Path

from frame_msg import FrameMsg, TxSprite

async def main():
    """
    Displays sample images on the Frame display.

    The images are indexed (palette) PNG images, in 2, 4,
    and 16 colors (that is, 1-, 2- and 4-bits-per-pixel).
    """
    frame = FrameMsg()
    try:
        await frame.connect()

        # Let the user know we're starting
        await frame.print_short_text('Loading...')

        # send the std lua files to Frame that handle data accumulation and sprite parsing
        await frame.upload_stdlua_libs(lib_names=['data', 'sprite'])

        # Send the main lua application from this project to Frame that will run the app
        await frame.upload_frame_app(local_filename="lua/sprite_frame_app.lua")

        # attach the print response handler so we can see stdout from Frame Lua print() statements
        frame.attach_print_response_handler()

        # "require" the main frame_app lua file to run it, and block until it has started.
        await frame.start_frame_app()

        # send the 1-bit image to Frame in chunks
        sprite = TxSprite.from_indexed_png_bytes(Path("images/logo_1bit.png").read_bytes())
        await frame.send_message(0x20, sprite.pack())

        # send a 2-bit image
        sprite = TxSprite.from_indexed_png_bytes(Path("images/street_2bit.png").read_bytes())
        await frame.send_message(0x20, sprite.pack())

        # send a 4-bit image
        sprite = TxSprite.from_indexed_png_bytes(Path("images/hotdog_4bit.png").read_bytes())
        await frame.send_message(0x20, sprite.pack())

        await asyncio.sleep(5.0)

        # unhook the print handler
        frame.detach_print_response_handler()

        # break out of the frame app loop and reboot Frame
        await frame.stop_frame_app()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # clean disconnection
        await frame.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

`sprite_frame_app.lua`
```lua
local data = require('data.min')
local sprite = require('sprite.min')

-- Phone to Frame flags
USER_SPRITE = 0x20

-- register the message parsers so they are automatically called when matching data comes in
data.parsers[USER_SPRITE] = sprite.parse_sprite

-- Main app loop
function app_loop()
  frame.display.text('Frame App Started', 1, 1)
  frame.display.show()

  -- tell the host program that the frameside app is ready (waiting on await_print)
  print('Frame app is running')

  while true do
    rc, err = pcall(
      function()
        -- process any raw data items, if ready
        local items_ready = data.process_raw_items()

        -- one or more full messages received
        if items_ready > 0 then

          if data.app_data[USER_SPRITE] ~= nil then
            local spr = data.app_data[USER_SPRITE]

            -- set the palette in case it's different to the standard palette
            sprite.set_palette(spr.num_colors, spr.palette_data)

            -- show the sprite
            frame.display.bitmap(1, 1, spr.width, 2^spr.bpp, 0, spr.pixel_data)
            frame.display.show()

            -- clear the object and run the garbage collector right away
            data.app_data[USER_SPRITE] = nil
            collectgarbage('collect')
          end

        end

        -- can't sleep for long, might be lots of incoming bluetooth data to process
        frame.sleep(0.001)
      end
    )
    -- Catch an error (including the break signal) here
    if rc == false then
      -- send the error back on the stdout stream and clear the display
      print(err)
      frame.display.text(' ', 1, 1)
      frame.display.show()
      break
    end
  end
end

-- run the main app loop
app_loop()
```

| Selected Examples | Python | Lua |
|-------------------|--------|-----|
| Display a Sprite  | [Python](https://github.com/CitizenOneX/frame_examples_python/blob/main/frame_msg/sprite_ind_png.py){:target="_blank"} | [Lua](https://github.com/CitizenOneX/frame_examples_python/blob/main/frame_msg/lua/sprite_frame_app.lua){:target="_blank"} |
| Display Unicode Text  | [Python](https://github.com/CitizenOneX/frame_examples_python/blob/main/frame_msg/text_sprite_block.py){:target="_blank"} | [Lua](https://github.com/CitizenOneX/frame_examples_python/blob/main/frame_msg/lua/text_sprite_block_frame_app.lua){:target="_blank"} |
| Take a photo (auto exposure)  | [Python](https://github.com/CitizenOneX/frame_examples_python/blob/main/frame_msg/camera.py){:target="_blank"} | [Lua](https://github.com/CitizenOneX/frame_examples_python/blob/main/frame_msg/lua/camera_frame_app.lua){:target="_blank"} |
| Take a photo (manual exposure)  | [Python](https://github.com/CitizenOneX/frame_examples_python/blob/main/frame_msg/manual_exposure.py){:target="_blank"} | [Lua](https://github.com/CitizenOneX/frame_examples_python/blob/main/frame_msg/lua/manualexp_frame_app.lua){:target="_blank"} |
| Live camera feed  | [Python](https://github.com/CitizenOneX/frame_examples_python/blob/main/frame_msg/live-camera-feed-with-params.py){:target="_blank"} | [Lua](https://github.com/CitizenOneX/frame_examples_python/blob/main/frame_msg/lua/live_camera_frame_app.lua){:target="_blank"} |
| Stream audio  | [Python](https://github.com/CitizenOneX/frame_examples_python/blob/main/frame_msg/audio_stream.py){:target="_blank"} | [Lua](https://github.com/CitizenOneX/frame_examples_python/blob/main/frame_msg/lua/audio_frame_app.lua){:target="_blank"} |

---

## Legacy SDKs

Note: Legacy SDK packages are available for [frame-sdk](https://pypi.org/project/frame-sdk/) and [frameutils](https://pypi.org/project/frame-utilities-for-python/) as [previously documented here](https://github.com/brilliantlabsAR/docs/blob/c33420dc55eb12b27f5a804b9a5a82247d471ae9/frame/building-apps-sdk.md).

In order to allow richer experiences on Frame including image display and audio streaming, the decision was made to move to an SDK model based on asynchronous message-passing between a main application loop running on the host, and a main event loop running on Frame. This approach is used in both the [Python](https://pypi.org/project/frame-msg/) and [Flutter](https://pub.dev/packages/frame_msg) SDKs.

While this requires a slight adjustment from the way the legacy SDKs were used, there are [many examples provided](https://github.com/CitizenOneX/frame_python_examples) and a [helpful community in Discord](https://discord.com/invite/vDS9X7gdwg) to help you build your project.
