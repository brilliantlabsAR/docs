---
title: Talking to Frame Over Bluetooth
description: A reference on how to manually communicate with Frame over Bluetooth Low Energy
image: /images/frame/frame-splash.png
nav_order: 4
parent: Frame SDK
grand_parent: Frame
---

# Talking to Frame Over Bluetooth
{: .no_toc }

---

You may want to communicate with Frame manually over Bluetooth Low Energy if we don't yet have an SDK available for your preferred development language, or if you just want to have full control of what's going on under the hood.

Once you're communicating with Frame over Bluetooth, you can use the [Lua API Reference](/frame/frame-sdk-lua) to see everything you can tell it to do.

1. TOC
{:toc}

---

## Pairing & Connecting

Frame uses BLE bonding and must pair with a host device before any communication can take place.  When attempting to connect to Frame using an SDK, Frame will automatically initiate pairing, which the OS handles and the user will have to agree to.

<details markdown="block">
<summary>Full Bluetooth Connection Details</summary>

### Un-Pairing
If already paired, Frame must be reset using the pinhole button on the charging dock before it can be paired to a new host side device. Host-side devices must also remove previous bonding before a new bonding can be accepted.

### Bluetooth Connection Technical Diagram

![Bluetooth connection sequence diagram](/frame/images/frame-bluetooth-connection-diagram.drawio.svg)
</details>

## Bluetooth Service & Characteristics

Frame has a single BLE service containing two characteristics: one for transmitting and one for receiving data.

Lua strings can be sent on the TX characteristic as UTF-8 strings, and responses are returned back on the RX characteristic. The host device must enable notification on the RX characteristic in order to receive data.

- Service UUID: 7A230001-5475-A6A4-654C-8431F6AD49C4
- TX characteristic UUID: 7A230002-5475-A6A4-654C-8431F6AD49C4
- RX characteristic UUID: 7A230003-5475-A6A4-654C-8431F6AD49C4

## Executing Lua Statements Over Bluetooth

You can run Lua commands on Frame over Bluetooth using a REPL-like interaction.  Frame does not contain a complete Lua REPL, but rather evaluates every message and only returns a message if it resulted in the Lua `print()` function being called, or an error.

```lua
print('hello world') -- Returns 'hello world' on the RX characteristic

print(1 + 2) -- Returns 3

a = 1 + 2 -- Evaluates 1 + 2 and stores it in a, but does not return anything

1 + 2 -- Returns an error because 1 + 2 hasn't been assigned to anything
```

The length of TX data is limited to a maximum size of the host's chosen MTU length. This number also determines the maximum length of a Lua string that can be evaluated at a time. For larger scripts, they must first be saved to the device using the [file system API](/frame/frame-sdk-lua#file-system) using several `f:write()` operations, and then executed using `require()`.

Responses are also limited to the MTU length. Should you want to return very long strings, they should be broken up into smaller `print()` statements.

Common MTU lengths are from 27 to 251 bytes, depending on OS version, BT version, and more.  To determine the MTU length that applies to your connection, use the following Lua function on Frame: `frame.bluetooth.max_length()`.  More details in the [Lua Bluetooth API reference](/frame/frame-sdk-lua#bluetooth).  To determine the MTU length on the host side, consult the documentation for your bluetooth library.

### Bluetooth Lua Execution Sequence Diagram

![Bluetooth Lua execution sequence diagram](/frame/images/frame-bluetooth-sending-lua-diagram.drawio.svg)

## Sending Data

Sometimes it may be more efficient to send raw byte data rather than strings: for example, when transmitting graphical or microphone data. These can be sent on the same TX characteristic by simply prepending a byte of value `0x01` at the start of the payload. This will trigger a callback function if one has already been assigned by `frame.bluetooth.receive_callback()`. The total length of byte data that can be transmitted is therefore MTU - 4 bytes.

Raw byte data can also be returned to the host device using the `frame.bluetooth.send()` function. This data is also limited to MTU - 4 bytes in length, and will be prepended by a value of `0x01` in the first byte of the payload.

### Bluetooth Raw Data Exchange Sequence Diagram

![Bluetooth Raw Data Exchange Sequence Diagram](/frame/images/frame-bluetooth-sending-bytes-diagram.drawio.svg)

## Control Characters

While a Lua script is running, Frame will ignore any other Lua strings that are sent over Bluetooth (except [raw byte data](#sending-data) which can still be sent to trigger callbacks in the user logic - see below).  To interrupt a running script, the following control signals can be sent on the TX characteristic to exit or restart the script:

- Sending a single byte of value `0x03` ("break signal") will terminate any running script or loop.
- Sending a single byte of value `0x04` ("reset signal") will clear all variables, and run `main.lua` if it exists. Equivalent to a reboot, or dipping in and out of the charging cradle.

## Lua Main Loop - A Special Case

The Lua command `require('my_module')` executes the whole file `my_module.lua`.  If this file contains a main loop, it may never return. Any subsequent Lua command sent on the TX characteristic *will not execute in the REPL* because the previous command has not returned - however raw data transmitted (with the `0x01` prefix) will still be handled by the `receive_callback()`.

**This behavior is the basis of Frameside applications**: when a Lua file is sent to Frame and then run (`require`d), Frame no longer accepts individual Lua REPL commands, but thereafter all communication between the Host and Frame takes place with raw data messages on the TX characteristic (with the `0x01` prefix). The primary purpose of the Lua main loop (in conjunction with the data characteristic `receive_callback()`) is to receive messages from the Host and trigger corresponding Frameside behavior. In addition, data from Frame can be sent back on the RX characteristic (RX from the point of view of the Host) to trigger its action.

For example, an application that takes photos from Frame's camera, sends them to the Host, runs a vision model, and then sends a text caption to Frame, might require a main Lua loop that receives 2 message types from the host: (1) capture a photo (and send to Host), and (2) display the specified text. The `frame-msg` package in the Frame SDK works precisely in this way.

Lua loops can be interrupted with the break and reset signals outlined in the section above: [Control Characters](#control-characters). When first connecting to Frame, it may not be known in advance if a main loop is already running, so a program may need to send a break signal to break out of any running loop to ensure that subsequent Lua REPL statements execute (e.g. to send new application files.)

Note: if a file named `main.lua` exists on the filesystem, it will automatically be run (`require`d) after reboot (or reset signal). If that file has a main loop, a break control character will need to be sent after the reboot (and after a short delay) to ensure that further Lua commands can be successfully executed.

## Firmware Updates

Frame contains a mechanism for updating the complete system firmware via a built in bootloader. To enter the bootloader, call `frame.update()`. The device will then reboot and advertise with the name "Frame Update".

To understand how the bootloader process works in more detail, visit the [Nordic DFU documentation](https://infocenter.nordicsemi.com/topic/sdk_nrf5_v17.1.0/lib_bootloader_modules.html).

If no activity commences on the bootloader for more than 5 minutes, it will timeout and return back to the application firmware. If the firmware update process is interrupted, and the application firmware becomes invalid, the bootloader will wait forever until a valid firmware update is completed.

Unlike the application firmware, the bootloader will continue to operate even while Frame is on charge. It's therefore possible to update while the device is docked to the charging cradle. In this case, once the update completes, the firmware will reload and then go to sleep right away.

The latest release file of the official firmware is available from the [Frame codebase releases page](https://github.com/brilliantlabsAR/frame-codebase/releases) which you can include in your own host apps along with the DFU mechanism.
