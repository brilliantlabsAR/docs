---
title: Building Apps
description: A guide on how to develop your own applications for Frame.
image: /images/frame/frame-splash.png
nav_order: 2
parent: Frame
---

# Building Apps
{: .no_toc }

---

## AR Studio
{: .no_toc }

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

## Bluetooth

Once you're ready to start making your own host side apps, it's useful to understand how Frame's Bluetooth works under the hood.

### Pairing & connecting

Frame uses BLE bonding and must pair with a host device before any communication can take place.

If already paired, Frame must be reset using the pinhole button on the charging dock before it can be paired to a new host side device. Host side devices must also remove bonding before a new bonding can be accepted.

![Bluetooth connection sequence diagram](/frame/images/frame-bluetooth-connection-diagram.drawio.svg)

### Sending Lua

Frame has a single BLE service containing two characteristics. One for transmitting and one for receiving data.

- Service UUID: 7A230001-5475-A6A4-654C-8431F6AD49C4
- TX characteristic UUID: 7A230002-5475-A6A4-654C-8431F6AD49C4
- RX characteristic UUID: 7A230003-5475-A6A4-654C-8431F6AD49C4

Lua strings can be sent on the TX characteristic as UTF-8 strings, and responses are returned back on the RX characteristic. The host device must enable notification on the RX characteristic in order to receive data.

Frame does not contain a complete Lua REPL, but rather evaluates every message and only returns a message if it resulted in the Lua `print()` function being called, or an error. This keeps the RX channel free of excess messages and echoed characters that would otherwise need to be filtered by the host side app.

```lua
print('hello world') -- Returns 'hello world' on the RX characteristic

print(1 + 2) -- Returns 3

a = 1 + 2 -- Evaluates 1 + 2 and stores it in a, but does not return anything

1 + 2 -- Returns an error because 1 + 2 hasn't been assigned to anything
```

The length of TX data is limited to a maximum size of the host's chosen MTU length - 3 bytes. This number also determines the maximum length of a Lua string that can be evaluated at a time. For larger scripts, they must first be saved to the device using the [file system API](/frame/lua#file-system) using several `f:write()` operations, and then executed using `require()`.

Responses are also limited to the MTU length. Should you want to return very long strings, they should be broken up into smaller `print()` statements.

![Bluetooth connection sequence diagram](/frame/images/frame-bluetooth-sending-lua-diagram.drawio.svg)

### Sending Data

Sometimes it may be more efficient to send raw byte data rather than strings. For example when transmitting graphical or microphone data. These can be sent on the same TX characteristic by simply appending a byte of value `1` at the start of the payload. This will trigger a callback function if one has already been assigned by `frame.bluetooth.receive_callback()`. The total length of byte data that can be transmitted is therefore MTU - 4 bytes.

Raw byte data can also be returned to the host device using the `frame.bluetooth.send()` function. This data is also limited to MTU - 4 bytes in length, and will be prepended by a value of `1` in the first byte of the payload.

![Bluetooth connection sequence diagram](/frame/images/frame-bluetooth-sending-bytes-diagram.drawio.svg)

### Control characters

While a Lua script is running, Frame will ignore any other Lua strings that are sent over Bluetooth (note that raw byte data can still be sent to trigger callbacks in the user logic). The following control signals can be sent on the TX characteristic to exit or restart the script:

- Sending a single byte of value `3` will terminate any running script or loop.
- Sending a single byte of value `4` will clear all variables, and run `main.lua` if it exists. Same as a reboot.

### Firmware updates

Frame contains a mechanism for updating the complete system firmware via a built in bootloader. To enter the bootloader, call `frame.update()`. The device will then reboot and advertise with the name "Frame update".

To understand how the bootloader process works in closer detail, visit the [Nordic DFU documentation](https://infocenter.nordicsemi.com/topic/sdk_nrf5_v17.1.0/lib_bootloader_modules.html).

If no activity commences on the bootloader for more than 5 minutes, it will timeout and return back to the application firmware. If the firmware update process is interrupted, and the application firmware becomes invalid, the bootloader will wait forever until a valid firmware update is completed.

Unlike the application firmware, the bootloader will continue to operate even while Frame is on charge. It's therefore possible to update while the device is docked to the charging cradle. In this case, once the update completes, the firmware will reload and then go to sleep right away.

The latest release file of the official firmware is available from the [Frame codebase releases page](https://github.com/brilliantlabsAR/frame-codebase/releases) which you can include in your own host apps along with the DFU mechanism.

---

## Frame utilities for Python

[frameutils](https://github.com/brilliantlabsAR/frame-utilities-for-python/tree/main) for Python is a handy library for communicating with Frame and provides several tools for creating graphics that you can use in your Frame apps.

Install it with pip:

```
pip3 install frameutils
```

### Bluetooth library

The Bluetooth module of frameutils can be used to communicate with Frame from any Python desktop app. It makes use of [Bleak](https://github.com/hbldh/bleak) under the hood.

```python
import asyncio
from frameutils import Bluetooth

async def main():
    bluetooth = Bluetooth()
    await bluetooth.connect()

    print(await bluetooth.send_lua('print('hello world')', await_print=True))
    print(await bluetooth.send_lua('print(1 + 2)', await_print=True))

    await bluetooth.disconnect()

asyncio.run(main())
```

### Font & graphics generation tool

**Details coming soon**