---
title: Brilliant SDK
description: A guide on how to develop your own applications for Halo.
image: /images/halo/halo-splash.png
nav_order: 2
parent: Halo
has_children: true
redirect_from:
  - /halo/building-apps
  - /halo/building-apps-sdk
  - /halo/building-apps-lua
  - /halo/building-apps-bluetooth-specs
  - /halo/sdk
---

# Building Apps with the Brilliant SDK
{: .no_toc }

---

1. TOC
{:toc}

---

## How Do Apps Run on Halo?

Halo runs a power-efficient System-on-a-Chip (SoC) with relatively limited memory and processing power compared to modern smartphones. Rather than installing apps directly on Halo, it typically functions as a peripheral accessory for "host" apps running on computers or mobile devices. These host apps communicate with Halo via Bluetooth to control features like the camera, microphone, speakers, and display.

While you may write Lua scripts that execute on Halo for specific behaviors, your host app primarily drives the logic while Halo typically runs a simple event handler loop. For example, the Noa mobile app connects to Halo, receives sensor data over Bluetooth, processes it, and sends content back to Halo for display.

Halo doesn't have its own app launcher or traditional app installation system. To share your Halo apps with others, publish your host app through normal distribution channels like App Store, Google Play, GitHub, or open source repositories. If you build something cool, let us know and we'll be happy to share it with the community.

## Getting Started

For the quickest start:

* If you're using a supported platform, begin with the SDK documentation for [Python](/halo/halo-sdk-python), [Flutter](/halo/halo-sdk-flutter), or [Web Bluetooth](/halo/halo-sdk-webbluetooth), and run the example programs. Then explore the [Lua API](/halo/halo-sdk-lua) for advanced features.
* For other platforms, use the [Lua API](/halo/halo-sdk-lua) directly over Bluetooth using the [Bluetooth LE API documentation](/halo/halo-sdk-bluetooth-specs).

## Development Options for Halo

1. **Use the Brilliant SDK** (Recommended)
    * Build with supported platforms:
        * [Python](/halo/halo-sdk-python) (Mac, Linux, Windows)
        * [Flutter](/halo/halo-sdk-flutter) (iOS/Android)
        * [Web Bluetooth](/halo/halo-sdk-webbluetooth) (Chromium browsers on desktop/Android)
    * Benefits: common tasks are simplified, many examples to follow, experimental emulator available for Python

2. **Communicate via Bluetooth LE**
    * Use any platform with Bluetooth LE capabilities
    * Offers full control but requires Bluetooth LE development experience
    * See the [Bluetooth LE API documentation](/halo/halo-sdk-bluetooth-specs)

3. **Customize Firmware** (Advanced)
    * Requires hardware development expertise
    * Provides complete control of Halo hardware
    * Find the official firmware [on GitHub](https://github.com/brilliantlabsAR/frame-2-firmware)

The typical development pattern involves creating a Python desktop application or Flutter mobile app that uses the Brilliant SDK to communicate with Halo over Bluetooth Low Energy, abstracting away the Lua and BLE details.

## Development with the Brilliant SDK

{: .note }
This recommended approach offers quick and reliable Halo app development for Python, Flutter, and Web Bluetooth platforms, all under active development.

Our platform SDKs simplify the low-level Bluetooth and Lua APIs, eliminating the need to write boilerplate code for device discovery, connection, and communication.

Familiarity with the [Lua API](/halo/halo-sdk-lua) remains useful for main application event loops, `main.lua` scripts that run at wakeup, and custom on-device processing.

Check the [Python](/halo/halo-sdk-python), [Flutter](/halo/halo-sdk-flutter), or [Web Bluetooth](/halo/halo-sdk-webbluetooth) SDK documentation for implementation details.

## Direct Bluetooth LE Development

For developers comfortable with Bluetooth LE, this approach offers maximum flexibility and requires understanding how Bluetooth LE works.

After establishing BLE communication, you'll use Lua to control Halo's functions. Halo provides a Lua 5.3 virtual machine where you can execute scripts or use the Lua REPL over the BLE interface.

Refer to the [Bluetooth LE API documentation](/halo/halo-sdk-bluetooth-specs) and the [full Lua API reference](/halo/halo-sdk-lua) for details on Halo's capabilities.

## Firmware Customization

Halo is developed by hackers for hackers, so even though we don't recommend it for most users, Halo's open-source firmware can be customized. Find the official firmware [on GitHub (coming soon)]().
