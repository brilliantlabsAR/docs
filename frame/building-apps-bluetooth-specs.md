---
title: Talking to the Frame Over Bluetooth
description: A reference on how to manually communicate with the Frame over Bluetooth Low Energy
image: /images/frame/frame-splash.png
nav_order: 3
parent: Building Apps
grand_parent: Frame
---

# Talking to the Frame Over Bluetooth
{: .no_toc }

---

You may want to communicate with the Frame manually over Bluetooth Low Energy if we don't yet have an SDK available for your preferred development language, or if you just want to understand what's going on under the hood.

Once you're communicating with the Frame over Bluetooth, you can use the [Lua API Reference](/frame/building-apps-lua) to see everything you can tell it to do.

1. TOC
{:toc}

---

## Pairing & Connecting

Frame uses BLE bonding and must pair with a host device before any communication can take place.  When attempting to connect to the Frame using an SDK, the Frame will automatically initiate pairing, which the OS handles and the user will have to agree to.

<details markdown="block">
<summary>Full Bluetooth Connection Details</summary>

### Un-Pairing
If already paired, Frame must be reset using the pinhole button on the charging dock before it can be paired to a new host side device. Host-side devices must also remove bonding before a new bonding can be accepted.

### Bluetooth Connection Technical Diagram

![Bluetooth connection sequence diagram](/frame/images/frame-bluetooth-connection-diagram.drawio.svg)
</details>

## Bluetooth Service & Characteristics

Frame has a single BLE service containing two characteristics. One for transmitting and one for receiving data.

Lua strings can be sent on the TX characteristic as UTF-8 strings, and responses are returned back on the RX characteristic. The host device must enable notification on the RX characteristic in order to receive data.

- Service UUID: 7A230001-5475-A6A4-654C-8431F6AD49C4
- RX characteristic UUID: 7A230002-5475-A6A4-654C-8431F6AD49C4
- TX characteristic UUID: 7A230003-5475-A6A4-654C-8431F6AD49C4

## Executing Lua Over Bluetooth

You can run Lua commands on the Frame over Bluetooth using a REPL-like interaction.  Frame does not contain a complete Lua REPL, but rather evaluates every message and only returns a message if it resulted in the Lua `print()` function being called, or an error.

```lua
print('hello world') -- Returns 'hello world' on the RX characteristic

print(1 + 2) -- Returns 3

a = 1 + 2 -- Evaluates 1 + 2 and stores it in a, but does not return anything

1 + 2 -- Returns an error because 1 + 2 hasn't been assigned to anything
```

The length of TX data is limited to a maximum size of the host's chosen MTU length. This number also determines the maximum length of a Lua string that can be evaluated at a time. For larger scripts, they must first be saved to the device using the [file system API](/frame/building-apps-lua#file-system) using several `f:write()` operations, and then executed using `require()`. (If you are using [the SDK](/frame/building-apps-sdk/#sending-lua-to-the-frame), you can instead use [`frame.run_lua()`](/frame/building-apps-sdk/#sending-lua-to-the-frame) and it will automatically handle sending the data in multiple chunks if needed.)

Responses are also limited to the MTU length. Should you want to return very long strings, they should be broken up into smaller `print()` statements.  (If you are using [the SDK](/frame/building-apps-sdk/), you can use the `prntLng()` function in place of `print()` to automatically send the data in multiple chunks.  Note that this functionality only exists in the SDK, so if you are manually sending data over Bluetooth, you will need to implement your own logic to handle multiple chunks.)

Common MTU lengths are from 27 to 251 bytes, depending on OS version, BT version, and more.  To determine the MTU length that applies to your connection, use the following Lua function on the Frame: `frame.bluetooth.max_length()`.  More details in the [Lua Bluetooth API reference](/frame/building-apps-lua#bluetooth).  To determine the MTU length on the host side, consult the documentation for your bluetooth library, or use the `frame.bluetooth.max_lua_payload()` function in the SDK.

### Bluetooth Lua Execution Sequence Diagram

![Bluetooth Lua execution sequence diagram](/frame/images/frame-bluetooth-sending-lua-diagram.drawio.svg)

## Sending Data

Sometimes it may be more efficient to send raw byte data rather than strings. For example when transmitting graphical or microphone data. These can be sent on the same TX characteristic by simply prepending a byte of value `1` at the start of the payload. This will trigger a callback function if one has already been assigned by `frame.bluetooth.receive_callback()`. The total length of byte data that can be transmitted is therefore MTU - 4 bytes.

Raw byte data can also be returned to the host device using the `frame.bluetooth.send()` function. This data is also limited to MTU - 4 bytes in length, and will be prepended by a value of `1` in the first byte of the payload.

If you are using the SDK and want to await multiple chunks of data from the Frame sent via `frame.bluetooth.send()`, you can use the [`frame.bluetooth.wait_for_data()` function](/frame/building-apps-sdk/#wait-for-data).  In that case, prepend each chunk with a value of `1` in the first byte (`'\001'` or `'\x01'`) and send a final chunk with a value of `2` (`'\002'` or `'\x02'`).  You can optionally include the total chunk count in the final message for reliability checking (for example, if you send 3 data chunks, then the final message should be `'\0023'`).  Note that this functionality only exists in the SDK, so if you are manually sending data over Bluetooth, you will need to implement your own logic to handle multiple chunks.

### Bluetooth Raw Data Exchange Sequence Diagram

![Bluetooth Raw Data Exchange Sequence Diagram](/frame/images/frame-bluetooth-sending-bytes-diagram.drawio.svg)

## Control Characters

While a Lua script is running, Frame will ignore any other Lua strings that are sent over Bluetooth (except [raw byte data](#sending-data) which can still be sent to trigger callbacks in the user logic).  To interrupt a running script, the following control signals can be sent on the TX characteristic to exit or restart the script:

- Sending a single byte of value `3` will terminate any running script or loop.
- Sending a single byte of value `4` will clear all variables, and run `main.lua` if it exists. Same as a reboot.

## Firmware Updates

Frame contains a mechanism for updating the complete system firmware via a built in bootloader. To enter the bootloader, call `frame.update()`. The device will then reboot and advertise with the name "Frame update".

To understand how the bootloader process works in closer detail, visit the [Nordic DFU documentation](https://infocenter.nordicsemi.com/topic/sdk_nrf5_v17.1.0/lib_bootloader_modules.html).

If no activity commences on the bootloader for more than 5 minutes, it will timeout and return back to the application firmware. If the firmware update process is interrupted, and the application firmware becomes invalid, the bootloader will wait forever until a valid firmware update is completed.

Unlike the application firmware, the bootloader will continue to operate even while Frame is on charge. It's therefore possible to update while the device is docked to the charging cradle. In this case, once the update completes, the firmware will reload and then go to sleep right away.

The latest release file of the official firmware is available from the [Frame codebase releases page](https://github.com/brilliantlabsAR/frame-codebase/releases) which you can include in your own host apps along with the DFU mechanism.
