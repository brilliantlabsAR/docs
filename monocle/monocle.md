---
title: Monocle
description: A brief overview of how Monocle works under the hood.
image: /images/monocle-splash.png
nav_order: 2
---

# Monocle Hardware Manual
{: .no_toc }

---

![Monocle exploded view](/monocle/images/monocle-exploded-view.png)

Monocle is a tiny heads up display which simply clips onto your glasses. It's packed full of powerful hardware which is perfect for when you're on the go, and connects to your mobile phone over Bluetooth. It also contains a few handy sensors such as touch, camera and microphone, which will help you navigate your journey into the world of AR.

This page describes the hardware design of Monocle, as well as how you can use it's features. If you wish to go deeper, the full open source schematics are linked [below](#schematics).

## Key features:
{: .no_toc }
- 640x400 color OLED display
- 20° FOV optical body
- 5MP camera & microphone
- FPGA based acceleration for ML/CV
- Bluetooth 5.2
- 70mAh internal battery
- Touch buttons
- Wireless MicroPython based OS
- Charging case with USB & 450mAh battery

## Example uses:
{: .no_toc }
- ML based image augmentation
- Computer vision research
- QR code & barcode detection
- Heads up telemetry
- AR apps & games design

## Contents
{: .no_toc }

1. TOC
{:toc}

## Block diagram

This diagram shows a general overview of the Monocle architecture.

![Monocle block diagram](/monocle/images/monocle-hw-block-diagram.drawio.png)

---

## Bluetooth MCU

The Bluetooth MCU used is a [Nordic nRF52832](https://infocenter.nordicsemi.com/pdf/nRF52832_PS_v1.8.pdf) with **512KB of Flash** memory, and **64KB of RAM**. It supports **Bluetooth 5.2**, up to 2Mb/s.

By default, the nRF comes preloaded with our [MicroPython](/micropython/micropython) firmware, however you are able to deploy your own [custom firmware](#developing-for-the-bluetooth-mcu) if you wish to do so.

### Updating firmware over-the-air

Over the air updates can be performed via Nordic's nRFConnect software either on [Desktop](https://www.nordicsemi.com/Products/Development-tools/nrf-connect-for-desktop), or on Mobile ([iOS](https://apps.apple.com/se/app/nrf-connect-for-mobile/id1054362403)/[Android](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjbtevyrf77AhUncPEDHfjiBSEQFnoECBIQAQ&url=https%3A%2F%2Fplay.google.com%2Fstore%2Fapps%2Fdetails%3Fid%3Dno.nordicsemi.android.mcp%26hl%3Den%26gl%3DUS&usg=AOvVaw26fnMv6YUhCDOx-ZZHre94)). nRFConnect requires a `.zip` DFU file to perform the update.

**The latest MicroPython release for Monocle can be found on our [GitHub](https://github.com/Itsbrilliantlabs/monocle-micropython/releases) page.**

---

## FPGA

the FPGA used is a [Gowin GW1N-LV9MG100C6/I5](https://www.mouser.se/datasheet/2/1033/GW1N_series_of_FPGA_Products_Data_Sheet-1830682.pdf). It contains **7k LUTs**, **468kb of block RAM**, as well as **608kb of Flash** memory which is perfect for storing the FPGA bitstream.

**The FPGA can also be booted from the external [8Mb SPI Flash IC](#flash) which is also included within the Monocle.**

By default, the FPGA comes pre-loaded our [Graphics & Camera Accelerator IP](https://github.com/Itsbrilliantlabs/monocle-fpga) and is driven by a custom MicroPython driver over SPI from the nRF52. It's a perfect starting point if you decide to [create your own IP](#developing-for-the-fpga) for applications such as AI inferencing, or computer vision.

**The latest release for the FPGA IP can be updated via a [MicroPython command](/micropython/machine-fpga#update). It is also checked periodically if you are using the [Brilliant App](/mobile-app/mobile-app)**

---

## Memory

Aside from the built-in memories of the Bluetooth MCU and the FPGA, Monocle contains three additional memory ICs. One for flash, and two for RAM. The RAM is accessible by the FPGA, and is great for storing frame-buffers, buffering camera data, or working data for AI algorithms. The Flash meanwhile, is great as a secondary source for loading FPGA bitstreams, logging data, and is accessible by both the nRF52, as well as the FPGA.

### Flash

The Flash device used is the [Winbond W25Q80EWUXIE](https://www.winbond.com/hq/support/documentation/levelOne.jsp?__locale=en&DocNo=DA00-W25Q80EW). It's an 8Mb serial Flash and is connected to the FPGA and nRF52 via an SPI bus. 

### RAM

The RAM devices used are the [AP Memory APS256XXN](https://www.apmemory.com/wp-content/uploads/APM_PSRAM_OPI_Xccela-APS256XXN-OBRx-v1.0-PKG.pdf). A total of 512Mb of memory is addressable, and can be accessed at up to 800Mb/s in DDR mode.

---

## Display

The display used inside Monocle is a Sony [ECX336CN](https://www.panelook.com/ECX336CN_Sony_0.23_OLED_overview_51733.html) OLED. It features **640x400 RGB pixels**, and is permanently bonded to the optical housing which reflects the image using a prism for the user to see. The result is a floating heads up display with a **20° field of view**. About the size of a table display at arms length.

![Diagram of the Monocle display light path](/monocle/images/monocle-display-fov.png)

Much of the operation and configuration is kept private by Sony, however we include a working configuration within our [FPGA code](https://github.com/Itsbrilliantlabs/monocle-fpga) which is used to drive the display.

## Camera

![Annotation of the Monocle camera](/monocle/images/monocle-camera.png)

## Touch interface

![Annotation of the Monocle touch interface](/monocle/images/monocle-touch-interface.png)

## Microphone

![Annotation of the Monocle microphone](/monocle/images/monocle-microphone.png)

## Power

## Charging case

![Annotation of the Monocle charging case](/monocle/images/monocle-charging-case.png)

## Developing custom firmware

### Developing for the Bluetooth MCU

{: .warning }
> It's possible to damage the Monocle hardware by misconfiguring the power supply controller. We recommend that you avoid changing any of those settings as we've already fine tuned them for you.

A good place to start writing your custom nRF applications is the [Monocle MicroPython repository](https://github.com/Itsbrilliantlabs/monocle-micropython). All the hardware drivers can be found here and you can follow the `main()` flow to understand how the firmware is built.

For compiling projects, you will need to download the latest [ARM GCC compiler](https://developer.arm.com/downloads/-/gnu-rm). For Bluetooth connectivity, you will also need to download a compatible Bluetooth stack, aka the [Softdevice](https://www.nordicsemi.com/Products/Development-software/nrf5-sdk/download). The Softdevice is a proprietary library from Nordic, and is not directly included within the Monocle MicroPython repository. You will need to download it manually for your application to build. The MicroPython codebase calls the Softdevice for all Bluetooth related functions, and is well documented within the code.

### Creating custom OTA (over-the-air) update packages

{: .warning }
> It's recommended that your application is well tested and can reliably return back into OTA mode after programming. If you flash a broken application, you'll have to dismantle your Monocle and manually flash it using a programmer.

To generate the `.zip` file, you'll need to use the [nRP Util](https://www.nordicsemi.com/Products/Development-tools/nrf-util) command line application. You can read how to generate files [here](https://infocenter.nordicsemi.com/index.jsp?topic=%2Fug_nrfutils%2FUG%2Fnrfutils%2Fnrfutil_intro.html), however you will need to use the [Brilliant OTA private key](https://github.com/Itsbrilliantlabs/monocle-micropython/blob/main/bootloader/published_privkey.pem) in order to generate a compatible image. If you wish to change this key, you can create a new keypair, and add the public key within your [bootloader code](https://github.com/Itsbrilliantlabs/monocle-micropython/blob/main/bootloader/dfu_public_key.c). Subsequent updates will then require your new private key. **Note: without the key, it's not possible to do over-the-air updates, and you will need to revert to manual programming.**

### Developing for the FPGA

[GoWin's EDA](https://www.gowinsemi.com/en/support/download_eda/) can be used to develop RTL for the FPGA. You can request a free licence [here](https://www.gowinsemi.com/en/support/license/).

We recommend having a look at our [Graphics & Camera Accelerator IP](https://github.com/Itsbrilliantlabs/monocle-fpga) to see how an FPGA project is set up and built.

Generally it's convenient to use the [MicroPython FPGA module](/micropython/machine-fpga) to wirelessly program the FPGA. However this method does not allow for JTAG debugging, and can be a slow process for iterative development. It's therefore also possible to program the FPGA manually using a programmer. 

### Manually programming

{: .warning }
> The internal hardware of the Monocle is very delicate, especially the OLED flex cable. This cable contains thirty tiny wires which can be easily be broken if the cable is creased. Additionally, the OLED is bonded to the optical prism for a clear picture. It's impossible to replace this OLED if it breaks.

1. To access the programming pads, you'll first need to remove the back cover.

    ![Removing Monocle back cover](/monocle/images/monocle-back-cover.png)

1. With the back cover removed, gently extract the main board, taking care not to damage the flex cables, or shorting any of the electronics.

1. To shutdown the power, you will need to short the two pads shown below. Metal tweezers work well, but be careful not to short any other components.

    ![Enabling Monocle ship mode](/monocle/images/monocle-ship-mode.png)

1. Your device should now be off, but **note the battery pins will still be live**. If you remove any components, **take note of which way they were inserted into the connector**. Re-inserting the OLED cable or the camera module backwards will permanently damage them.

1. The programming pins for the Bluetooth MCU are shown below. It's recommended to use a J-Link compatible programmer such as the [nRF52DK](https://www.nordicsemi.com/Products/Development-hardware/nrf52-dk) as Nordic provide a helper utility which is correctly aware of important settings and flags when reprogramming. However other OpenOCD based SWD programmers may work with some careful tweaking.

    ![Monocle main board FPGA JTAG diagram](/monocle/images/monocle-swd.png)

1. The programming pins for the FPGA are shown below. You can use Gowin's GWU2X based dongles to program the FPGA directly from within the IDE. Alternatively, [openFPGAloader](https://github.com/trabucayre/openFPGALoader) works as an open source alternative and can be used with a variety of programmers, such as [FTDI FT2232 based dongles](https://www.seeedstudio.com/Sipeed-USB-JTAG-TTL-RISC-V-Debugger-ST-Link-V2-STM8-STM32-Simulator-p-2910.html).

    ![Monocle main board FPGA JTAG diagram](/monocle/images/monocle-jtag.png)

1. To re-power the device. Apply 5V to the charging pads.

    ![Monocle charging pads](/monocle/images/monocle-charging-pads.png)

1. To program the Bluetooth MCU, install the [Nordic command line tools](https://www.nordicsemi.com/Products/Development-tools/nrf-command-line-tools), and then run the command:

    ```bash
    nrfjprog --program firmware.hex --chiperase -f nrf52 --verify -r
    ```

1. To program the FPGA with openFPGAloader, run the command:

    ```bash
    openFPGALoader --cable ft2232 --fpga-part 0x0100481b --write-flash bitstream.fs
    ```

## Schematics

TODO: Venkat to generate latest schematics

[Download the PDF schematics for Monocle](/monocle/monocle-schematics.pdf)

[Download the PDF schematics for the charging case](/monocle/monocle-cc-schematics.pdf)


## Mechanical

TODO: Ben to provide mechanical drawings

### Monocle

### Charging case

## Device characteristics



## Safety

## Legal