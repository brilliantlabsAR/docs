---
title: Frame SDK
description: A guide on how to develop your own applications for Frame.
image: /images/frame/frame-splash.png
nav_order: 2
parent: Frame
has_children: true
redirect_from:
  - /frame/building-apps
  - /frame/building-apps-sdk
  - /frame/building-apps-lua
  - /frame/building-apps-bluetooth-specs
  - /frame/sdk
---

# Building Apps with the Frame SDK
{: .no_toc }

---

1. TOC
{:toc}

---

## How Do Apps Run on Frame?

Frame runs a power-efficient System-on-a-Chip (SoC) with relatively limited memory and processing power compared to modern smartphones. Rather than installing apps directly on Frame, it typically functions as a peripheral accessory for "host" apps running on computers or mobile devices. These host apps communicate with Frame via Bluetooth to control features like the camera, microphone, and display.

While you may write Lua scripts that execute on Frame for specific behaviors, your host app primarily drives the logic while Frame runs a simple event handler loop. For example, the Noa mobile app connects to Frame, receives sensor data over Bluetooth, processes it, and sends content back to Frame for display.

Frame doesn't have its own app launcher or traditional app installation system. To share your Frame apps with others, publish your host app through normal distribution channels like App Store, Google Play, or open source repositories. Of course if you build something cool, let us know and we will be happy to share it with the community.

## Getting Started

For the quickest start:

* If you're using a supported platform, begin with our SDK documentation for [Python](/frame/frame-sdk-python) or [Flutter](/frame/frame-sdk-python), then explore the [Lua API](/frame/frame-sdk-lua) for advanced features.
* For other platforms, use the [Lua API](/frame/frame-sdk-lua) directly over Bluetooth with the [Bluetooth LE API documentation](/frame/frame-sdk-bluetooth-specs).
* Note: Legacy SDKs ([frame-sdk-python](https://pypi.org/project/frame-sdk/), [frame-sdk-flutter](https://pub.dev/packages/frame_sdk), [frameutils-python](https://pypi.org/project/frameutils/)) remain functional, but new projects should use the updated SDK to access new features like image display and realtime streaming.

# Development Options for Frame

1. Use Platform SDKs **(Recommended)**
    * Build with supported platforms:
        * [Python](/frame/frame-sdk-python) (Mac, Linux, Windows)
        * [Flutter](/frame/frame-sdk-flutter) (iOS/Android)
    * Benefits: Common tasks are simplified, many examples to follow
2. Communicate via Bluetooth LE
    * Use any platform with Bluetooth LE capabilities
    * Offers full control but requires Bluetooth LE development experience
    * See [Bluetooth LE API documentation](/frame/frame-sdk-bluetooth-specs)
3. Customize Firmware **(Advanced)**
    * Requires hardware development expertise
    * Provides complete control of Frame hardware
    * See [firmware customization and hardware documentation](/frame/hardware#customizing-the-firmware)

The typical development pattern involves creating a Python desktop application or Flutter mobile app that uses the Frame SDK to communicate with Frame over Bluetooth, abstracting away many Lua and BTLE details.

## Platform SDK Development

{: .note }
This recommended approach offers quick and reliable Frame app development for Python and Flutter platforms, with each of these platform SDKs under active development.

Our platform SDKs simplify the low-level Bluetooth and Lua APIs, eliminating the need to write boilerplate code for device discovery, connection, and communication.

Familiarity with the [Lua API](/frame/frame-sdk-lua) remains useful for main application event loops, `main.lua` scripts that run at wakeup, or custom on-device processing.

Check the [Python](/frame/frame-sdk-python) or [Flutter](/frame/frame-sdk-flutter) SDK documentation for implementation details.


## Direct Bluetooth LE Development

For developers comfortable with Bluetooth LE, this approach offers maximum flexibility but requires a greater understanding of Bluetooth technology.

After establishing BTLE communication, you'll use Lua to control Frame's functions. Frame provides a Lua virtual machine where you can execute scripts or use the Lua REPL over the BTLE interface.

Refer to the [Bluetooth LE API documentation](/frame/frame-sdk-bluetooth-specs) and the [full Lua API reference](/frame/frame-sdk-lua) for details on Frame's capabilities.

During development, you can also use the [AR Studio extension for VSCode](/frame/frame-sdk-lua#ar-studio) to directly write and execute Lua code on Frame.

## Firmware Customization

Frame is developed by hackers for hackers, so even though we don't recommend it for most users, Frame's open-source firmware can be customized.  Find the official firmware [on GitHub](https://github.com/brilliantlabsAR/frame-codebase).

For more details on how to customize the firmware, see the [hardware documentation](/frame/hardware#customizing-the-firmware).