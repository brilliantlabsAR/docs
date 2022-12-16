---
title: Monocle
description: A brief overview of how Monocle works under the hood.
image: /images/monocle-splash.png
nav_order: 2
---

# Monocle Hardware
{: .no_toc }

![Monocle exploded view](/images/monocle/exploded-annotated-view.png)

Monocle is a tiny heads up display which you can clip onto your glasses. It's packed full of powerful hardware which is perfect for when you're on the go. It can connect to your mobile phone, or other devices over Bluetooth, and contains a few handy sensors such as touch, camera and microphone, which can help you expand your uses.

This page briefly describes the hardware design of Monocle, and if you need specific details, the full, open source schematic is linked [below](#schematics).

1. TOC
{:toc}

## Block diagram

The image below shows a general view of the Monocle architecture.

![Monocle block diagram](/images/monocle/hw-block-diagram.drawio.png)

---

## Bluetooth MCU

The Bluetooth MCU used is a [Nordic nRF52832](https://infocenter.nordicsemi.com/pdf/nRF52832_PS_v1.8.pdf) with **512KB of Flash** memory, and **64KB of RAM**. It supports **Bluetooth 5.2**, up to 2Mb/s.

By default, the nRF comes preloaded with our [MicroPython](/micropython/micropython) firmware, however you are able to deploy your own custom firmware if you wish to do so.

### Flashing using over-the-air (OTA) device firmware updates (DFU)


Over the air updates can be performed via Nordic's nRFConnect software either on [Desktop](https://www.nordicsemi.com/Products/Development-tools/nrf-connect-for-desktop), or on Mobile ([iOS](https://apps.apple.com/se/app/nrf-connect-for-mobile/id1054362403)/[Android](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjbtevyrf77AhUncPEDHfjiBSEQFnoECBIQAQ&url=https%3A%2F%2Fplay.google.com%2Fstore%2Fapps%2Fdetails%3Fid%3Dno.nordicsemi.android.mcp%26hl%3Den%26gl%3DUS&usg=AOvVaw26fnMv6YUhCDOx-ZZHre94)). nRFConnect requires a `.zip` DFU file to perform the update.

**The latest MicroPython release for Monocle can be found on our [GitHub](https://github.com/Itsbrilliantlabs/monocle-micropython/releases) page.**

### Creating custom DFU images

{: .warning }
> It's recommended that you tell your application is well tested and can reliably return back into OTA mode after programming. If you flash a broken application, you'll have to dismantle your Monocle andmanually flash it using a programmer.

To generate the `.zip` file, you'll need to use the [nRP Util](https://www.nordicsemi.com/Products/Development-tools/nrf-util) command line application. You can read how to generate files [here](https://infocenter.nordicsemi.com/index.jsp?topic=%2Fug_nrfutils%2FUG%2Fnrfutils%2Fnrfutil_intro.html), however you will need to use the [Brilliant OTA private key](https://github.com/Itsbrilliantlabs/monocle-micropython/blob/main/bootloader/published_privkey.pem) in order to generate a compatible image. If you wish to change this key, you can create a new keypair, and add the public key within your [bootloader code](https://github.com/Itsbrilliantlabs/monocle-micropython/blob/main/bootloader/dfu_public_key.c). Subsequent updates will then require your new private key. **Note: without the key, it's not possible to do over-the-air updates, and you will need to revert to manual programming.**

### Flashing manually with a programmer

{: .warning }
> The internal hardware of the Monocle is very delicate, especially the OLED flex cable. This cable contains thirty tiny wires which can be easily be broken if the cable is creased. Additionally, the OLED is bonded to the optical prism for a clear picture. It's impossible to replace this OLED if it breaks.

1. To access the programming pads of the nRF52, you'll first need to remove the back cover.

    ![Removing Monocle back cover](/images/monocle/removing-back-cover.png)

1. With the back cover removed, gently extract the main board, taking care not to damage the flex cables, or shorting any of the electronics. **The lithium battery will still be active**.

1. To shutdown the battery, you will need to short the pad JX. Metal tweezers work great, but be careful not to short any other components.

1. Your device should now be off, and it's safe to disconnect the flex cables and camera module. **Note the battery pins will still be live**. Additionally, **take note of which way the cables and camera**. Re-inserting them backwards will damage the OLED or the camera module.

1. The programming pins are described below. It's recommended to use a J-Link programmer, or nRF52DK to reprogram the Monocle.

1. To flash a binary file, ensure you have the [Nordic command line tools](https://www.nordicsemi.com/Products/Development-tools/nrf-command-line-tools) installed, and then run the command:

    ```bash
    nrfjprog --program firmware_file.hex --chiperase -f nrf52 --verify -r
    ```

### Developing a custom firmware

{: .warning }
> It's possible to damage the Monocle hardware by misconfiguring the power supply controller. We recommend that you avoid changing those settings as we've already fine tuned them for you.

A good place to start writing your custom nRF applications is the [Monocle MicroPython repository](https://github.com/Itsbrilliantlabs/monocle-micropython). All the hardware drivers can be found here and you can follow the `main()` flow to understand how the firmware is built.

For compiling projects, you will need to download the latest [ARM GCC compiler](https://developer.arm.com/downloads/-/gnu-rm). For Bluetooth connectivity, you will also need to download a compatible Bluetooth stack, aka the [Softdevice](https://www.nordicsemi.com/Products/Development-software/nrf5-sdk/download). The Softdevice is a proprietary library from Nordic, and is not directly included within the Monocle MicroPython repository. You will need to download it manually for your application to build. The MicroPython codebase calls the Softdevice for all Bluetooth related functions, and is well documented within the code.

---

## FPGA

the FPGA used is a [Gowin GW1N-LV9MG100C6/I5](https://www.mouser.se/datasheet/2/1033/GW1N_series_of_FPGA_Products_Data_Sheet-1830682.pdf). It contains **~7k LUTs**, **<TODO>Mb of block RAM**, as well as **<TODO>Mb of Flash** memory.

### Developing custom applications

### Flashing the FPGA

---

## Memory

Aside from the built-in memories of the Bluetooth MCU and the FPGA, Monocle contains additional 

### Flash

### RAM

---

## Display

Example of the display FOV

## Camera

![](/images/monocle/camera-fov.png)

## Touch interface

![](/images/monocle/touch-interface.png)

## Microphone

## Power

## Schematics

## Mechanical

## Maximum ratings

## Safety

## Legal