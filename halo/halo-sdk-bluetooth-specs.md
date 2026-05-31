---
title: Talking to Halo Over Bluetooth
description: A reference on how to manually communicate with Halo over Bluetooth Low Energy
image: /images/halo/halo-splash.png
nav_order: 5
parent: Brilliant SDK
grand_parent: Halo
---

# Talking to Halo Over Bluetooth
{: .no_toc }

---

You may want to communicate with Halo manually over Bluetooth Low Energy if we don't yet have an SDK available for your preferred development language, or if you want full control of what's going on under the hood.

Once you're communicating with Halo over Bluetooth, you can use the [Lua API Reference](/halo/halo-sdk-lua) to see everything you can tell it to do.

1. TOC
{:toc}

---

## Pairing & Connecting

Halo uses BLE bonding and must pair with a host device before any communication can take place. When attempting to connect to Halo using an SDK, Halo will automatically initiate pairing, which the OS handles and the user will have to agree to.

**Device Naming:** Halo devices are named as `Halo XX`, where `XX` is the 4th byte (in hex) of the device's EUI-48 MAC address.

<details markdown="block">
<summary>Full Bluetooth Connection Details</summary>

### Un-Pairing

If previously paired to another device, Halo must be put into pairing mode before it can be paired to a new host device. Press and hold Halo's button for 8 seconds until the white LED on the left arm flashes, indicating that Halo is in pairing mode. Host-side devices must also remove previous bonding before a new pairing can be accepted.

### Bluetooth Connection Diagram

![Bluetooth connection sequence diagram](/halo/images/halo-bluetooth-connection-diagram.drawio.svg)
</details>

## Bluetooth Services & Characteristics

Halo implements three BLE services:

### Halo Lua Service

**Service UUID:** `7A230001-5475-A6A4-654C-8431F6AD49C4`

Characteristic names are from the **host's** perspective — TX means the host transmits to Halo, RX means the host receives from Halo.

| Characteristic | UUID | Permissions | Description |
|----------------|------|-------------|-------------|
| LUA TX | `7A230002-5475-A6A4-654C-8431F6AD49C4` | Write Without Response, Write | Host sends Lua commands and data to Halo |
| LUA RX | `7A230003-5475-A6A4-654C-8431F6AD49C4` | Notify | Host receives Lua `print()` output and data from Halo |
| AUDIO TX | `7A230005-5475-A6A4-654C-8431F6AD49C4` | Write Without Response, Write | Host streams PCM or LC3 audio to Halo's speaker |

The maximum packet size on each characteristic is the negotiated MTU (up to 512 bytes).

{: .note }
Camera images and microphone audio are **not** streamed on dedicated characteristics. Camera image chunks are sent from Halo to host over the regular **LUA RX** characteristic using `frame.bluetooth.send()`. Microphone audio is also sent back on the **LUA RX** characteristic in the same way.

### Battery Service

**Service UUID:** `0x180F` (Standard BLE Battery Service)

| Characteristic | UUID | Permissions | Description |
|----------------|------|-------------|-------------|
| Battery Level | `0x2A19` | Read, Notify | Battery level (0–100%) |

### OTA Service

**Service UUID:** `8D53DC1D-1DB7-4CD3-868B-8A527460AA84`

| Characteristic | UUID | Permissions | Description |
|----------------|------|-------------|-------------|
| SMP | `DA2E7828-FBCE-4E01-AE9E-261174997C48` | Write Without Response, Write, Notify | SMP firmware update control |

Firmware updates use the **MCU-BOOT** scheme over BLE using the [Simple Management Protocol (SMP)](https://docs.zephyrproject.org/latest/services/device_mgmt/smp_svr.html). See [Firmware Updates](#firmware-updates) below.

## Executing Lua Statements Over Bluetooth

Send Lua commands to Halo over Bluetooth using a REPL-like interaction on the **LUA TX** characteristic. Halo evaluates every message and only returns a response if it resulted in a Lua `print()` call, or if an error occurred.

```lua
print('hello world') -- Returns 'hello world' on LUA RX
print(1 + 2)         -- Returns '3'
a = 1 + 2            -- Evaluates and stores, no output
1 + 2                -- Returns an error
```

The length of data on LUA TX is limited to the negotiated MTU. To execute larger scripts, first save them to the device filesystem using `frame.file.open()` / `f:write()` / `f:close()`, then execute with `require()`.

Responses on LUA RX are also limited to the MTU. For very long strings, break them into smaller `print()` calls.

To determine the MTU in use: `frame.bluetooth.max_length()` in Lua.

### Bluetooth Lua Execution Sequence

![Bluetooth Lua execution sequence diagram](/halo/images/halo-bluetooth-sending-lua-diagram.drawio.svg)

## Sending Data

For binary payloads (e.g. image data, sprite data), prefix the payload with a byte of value `0x01` on the **LUA TX** characteristic. This triggers a callback if one was registered with `frame.bluetooth.receive_callback()`. The total payload length is therefore MTU − 4 bytes.

Raw byte data can be returned to the host using `frame.bluetooth.send()`. It is prefixed with `0x01` in the first byte of the **LUA RX** notification.

### Bluetooth Raw Data Exchange Sequence

![Bluetooth Raw Data Exchange Sequence Diagram](/halo/images/halo-bluetooth-sending-bytes-diagram.drawio.svg)

## Control Characters

While a Lua script is running, Halo will ignore additional Lua strings on LUA TX (raw data with `0x01` prefix is still processed). To interrupt a running script, send one of these single-byte control signals on LUA TX:

| Byte | Signal | Effect |
|------|--------|--------|
| `0x02` | CTRL+B | Reboot device |
| `0x03` | CTRL+C | Interrupt running script |
| `0x04` | CTRL+D | Restart Lua runtime / run `main.lua` |
| `0x05` | CTRL+E | Reset and remove `main.lua` |
| `0x06` | CTRL+F | Exit Lua runtime completely |
| `0x07` | CTRL+G | Remove all files/folders (except settings) |

**Most commonly used:**
- `0x03` (break) — terminate any running script or loop
- `0x04` (reset) — clear all variables and run `main.lua` if it exists

## Lua Main Loop — A Special Case

`require('my_module')` executes the entire file `my_module.lua`. If the file contains a main loop, it may never return. Subsequent Lua REPL commands sent on LUA TX *will not execute* because the previous command hasn't returned — however, raw data (with `0x01` prefix) will still be processed by `receive_callback()`.

**This behavior is the basis of Haloside applications:** once a Lua file is running in a main loop, all host↔Halo communication takes place through raw data messages on **LUA TX** (host→Halo) and **LUA RX** (Halo→host). The Lua loop receives messages from the host via `receive_callback()` and sends data back using `bluetooth.send()`.

Lua loops can be interrupted with the break (`0x03`) and reset (`0x04`) control signals. When first connecting to Halo, it's good practice to send a break signal to ensure the device is in REPL mode before sending new application files.

{: .note }
If `main.lua` exists on the filesystem, it is automatically run after reboot or after a reset (`0x04`) signal. If it contains a main loop, send a break (`0x03`) signal after the reboot (with a short delay) to ensure further Lua REPL commands can execute.

## Camera

Camera images are captured using the Lua camera API (`frame.camera.capture()` / `frame.camera.read()`), and the Lua app is responsible for sending image chunks back to the host using `frame.bluetooth.send()` — which delivers them on the **LUA RX** characteristic.

A typical Lua camera pattern:

```lua
frame.camera.capture({ quality = "HIGH" })
while not frame.camera.image_ready() do frame.sleep(0.05) end

local mtu = frame.bluetooth.max_length()
while true do
    local data = frame.camera.read(mtu)
    if data == nil then break end
    frame.bluetooth.send(data)  -- arrives on LUA RX
end
```

## Audio

### Sending audio to Halo (playback)

Audio data for playback is written to the **AUDIO TX** characteristic (`7A230005`). Start the speaker first using `frame.speaker.start()` over the Lua channel, then stream PCM or LC3 audio frames directly to **AUDIO TX** — bypassing the Lua VM for low-latency delivery to the speaker hardware.

### Receiving audio from Halo (recording)

There is no dedicated audio receive characteristic. Microphone audio is sent back to the host via `frame.bluetooth.send()` in Lua, which delivers it on the **LUA RX** characteristic. Start the microphone using `frame.microphone.start()`, then read chunks and send them in the main Lua loop.

LC3 format: 10ms frames (750µs or 1000µs frame duration), e.g. 16kHz 16-bit mono at 16kbps.

## Firmware Updates

Halo firmware updates use the **MCU-BOOT** bootloader scheme over BLE, using the [Simple Management Protocol (SMP)](https://docs.zephyrproject.org/latest/services/device_mgmt/smp_svr.html) on the OTA service.

The latest official firmware release is available from the [frame-2-firmware releases page](https://github.com/brilliantlabsAR/frame-2-firmware/releases).

For reference implementations of MCU-BOOT DFU over BLE:
- [mcuboot_alif port for Alif Semiconductor devices](https://github.com/alifsemi/mcuboot_alif)
