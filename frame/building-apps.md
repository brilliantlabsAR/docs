---
title: Building Apps
description: A guide on how to develop your own applications for Frame.
image: /images/frame/frame-splash.png
nav_order: 2
parent: Frame
has_children: true
---

# Building Apps

1. TOC
{:toc}

---

## How Do Apps Run on Frame?
In case you've come to Frame development with any preconceptions from the world of wearable Android devices, let's step back and go over how Frame is different.  Unlike some other devices, Frame is not based on Android and is in fact built on a very power-efficient and somewhat low-level system on a chip.  Whereas on Android you may develop a app, package it up in an apk, send it to a device, and then launch and run it on the device, Frame is different.

In general, apps do not run on Frame, instead Frame acts as a peripheral accessory for "host" apps running on a computer or mobile device.  These apps then talk to Frame over Bluetooth to get it to do things like take photos or access the microphone or display text and graphics on its screen.  There will be many scenarios where you will write Lua scripts that execute on Frame for performance reasons, but it's your host app that is generally driving the logic.

For example, the Noa app on your phone is the "host" app, and it talks to Frame over Bluetooth.  It registers itself to be called when you wake your Frame by tapping it, and then it instructs the Frame to send over photo and microphone data which it then uses to generate a response.  It then processes the response and tells Frame exactly what to display on its screen.  Very little of the code for Noa actually runs on the Frame.  Rather, the Noa app on your phone is the one that runs the code that calls on Frame.

As such, there is no concept of an app launcher on Frame, or any other way to "install" an app on Frame.  Instead, you build the host app, and then use it to control Frame.  To share with other Frame users, publish your host app to the App Store or Google Play, or open source it or however you would normally share an app for your platform.  Of course if you build something cool, let us know and we will be happy to share it with the community.  We will eventually have a gallery of Frame apps to share with the world, although we're not quite there yet.

## A Quick Example
Here's a quick python script to take a photo and also show the time and date on the Frame.

```python
import asyncio
from frame_sdk import Frame
from frame_sdk.display import Alignment
import datetime

async def main():
    async with Frame() as f:
        # take a photo and save to disk
        await f.display.show_text("Taking photo...", align=Alignment.MIDDLE_CENTER)
        await f.camera.save_photo("frame-test-photo.jpg")

        # display battery level, time, and date
        text_to_display = f"{await f.get_battery_level()}%\n"+datetime.datetime.now().strftime("%-I:%M %p\n%a, %B %d, %Y")
        await f.display.show_text(text_to_display, align=Alignment.MIDDLE_CENTER)

asyncio.run(main())
```

For a more complete example, check out the [SDK example](/frame/building-apps-sdk#putting-it-all-together).

## How to Get Started

Read on for a better understanding of the platform and the various ways to build apps for Frame.  Or, to keep it simple:

* If you're interested in building apps for Frame, and you're using one of the platforms supported by our SDKs, then definitely start with the SDK.  Check out the [SDK documentation here](/frame/building-apps-sdk) to get started.  Then read up on the [Lua API documentation here](/frame/building-apps-lua) to do even more.
* If you're using a platform that isn't supported by our SDKs, your best bet is to use the Lua API directly over Bluetooth.  Check out the [Bluetooth LE API documentation here](/frame/building-apps-bluetooth-specs) and the [Lua API documentation here](/frame/building-apps-lua) to get started.

# Ways to Develop for Frame
Frame has several integration points you can use to create apps:

1. [Use One of Our Platform SDKs to Use Frame from Your Own Mobile or Desktop Computer App](/frame/building-apps-sdk) **(recommended)**
    * Build apps for one of our supported platforms:
        * Python from a Mac, Linux, or Windows computer
        * Swift, Kotlin, Flutter, and React Native for mobile *(coming soon)*
    * Common tasks are simplified and handled for you
    * Your app is in control and uses Frame as an accessory
    * Best way to get started
2. [Talk to the Frame Over BTLE to Run Lua on the Device](/frame/building-apps-bluetooth-specs)
    * Use any platform that can talk to Bluetooth
    * Gives you full control
    * Can be tedious to get started, best if you have experience developing with Bluetooth LE
3. [Customize the Firmware](/frame/hardware#customizing-the-firmware) **(not recommended)**
    * Very advanced, requires experience with hardware development
    * Gives you complete control

The most common structure is to build an iOS or Android mobile app which uses our SDKs to communicate with the Frame over Bluetooth.  Your app is in control and uses Frame as an accessory, with the Lua and BTLE details mostly abstracted away for you.

Let's walk through each of these options in order.


## Use One of Our Platform SDKs from Your Own Mobile or Computer App **(recommended)**


{: .note }
This is the recommended option for quickly and reliably building Frame apps.  However the platform SDKs are a work in progress and not all platforms and use cases are supported yet.  At the moment python is the first platform to launch in preview.

We've wrapped the low-level bluetooth and Lua APIs into a set of platform SDKs for a number of popular development platforms.  This allows you to build your own mobile or computer app for Frame, without having to write all the low-level boilerplate to make it work.

For example, instead of having to write code to find and connect to Frame over Bluetooth, send it Lua code, and then handle the response, you can use the SDK to do that for you.

It's still useful to [learn the Lua API](/frame/building-apps-lua), as you will occasionally need to use it directly.  For example, the `main.lua` script which runs at wakeup, or when you are doing something that isn't wrapped by the SDK.

Check out [the SDK documentation here](/frame/building-apps-sdk) to see how to use the SDK to build your own app.


## Talk to the Frame Over Bluetooth Low Energy to Run Lua on the Device

Frame is designed to be used with a host app running on a computer or mobile device.  The host app talks to Frame over Bluetooth Low Energy (BTLE) and runs Lua code on the device.

So if you're comfortable with Bluetooth LE, you can use any platform that can talk to Bluetooth to control Frame.  This is the most flexible option, and gives you complete control over your interaction with the device.  However, it can be more difficult to get started, and requires a good understanding of Bluetooth LE.

Check out the full documentation for [communicating with Frame over Bluetooth LE](/frame/building-apps-bluetooth-specs).

Once you're using BTLE to communicate with the Frame, what can you actually tell it to do?  That's where Lua comes in.  Lua is a tiny and extensible scripting language that's designed to be power efficient and quick to learn. Frame features a complete Lua virtual machine.  You can execute Lua scripts on the device, or use the Lua REPL over the BTLE interface to interact with the device.

Be sure to check out the [full Lua API reference](/frame/building-apps-lua) for more on what you can do with Lua on Frame.

While the main way you'll use Lua on Frame is via host apps that send it over Bluetooth, it can be helpful while learning to directly write and execute Lua code on Frame using the [AR Studio extension for VSCode](/frame/building-apps-lua#ar-studio).


## Customize the Firmware

Frame is developed by hackers for hackers, so even though we don't encourage it for most users, you are welcome to customize the firmware if you want.  The official Frame firmware is open source, and you can find it [on GitHub](https://github.com/brilliantlabsAR/frame-codebase).

For more details on how to customize the firmware, see the [hardware documentation](/frame/hardware#customizing-the-firmware).