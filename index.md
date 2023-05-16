---
title: Welcome
description: Technical documentation for Brilliant's AR devices.
image: /images/monocle-splash.png
nav_order: 1
---


![Brilliant Monocle use cases](/images/monocle-splash.png)

# Technical documentation

Monocle was designed for hackers, by hackers. Learn briefly about the Monocle [hardware](/monocle/monocle), and once you're ready to dive in, try out the [MicroPython interface](/micropython/micropython) to start building your AR application.

### How do I start my Monocle?

As soon as you take Monocle out of the case, it’ll automatically power on. You’ll see the display turn on, and be able to connect over Bluetooth. Monocle will go to sleep once you put it back into the case, and will recharge on its own.

### How do I connect to Monocle?

Connect to Monocle over Bluetooth using the WebREPL console at [repl.brilliant.xyz](https://repl.brilliant.xyz). Make sure you’re using Chrome Desktop, Chrome for Android, or [Bluefy](https://apps.apple.com/de/app/bluefy-web-ble-browser/id1492822055) in iOS.

### How can I start programming Monocle?

Monocle understands Python and exposes some intuitive APIs for you to easily access every aspect of the hardware. Using the [VSCode extension](https://marketplace.visualstudio.com/items?itemName=brilliantlabs.brilliant-ar-studio), or [WebREPL console](https://repl.brilliant.xyz), you can start building Python apps and test them directly on Monocle. Check out the examples and reference documentation [here](/micropython/micropython) for all of the details.

### How do I update the firmware?

Whenever a new firmware update is available, you’ll see an option to update within the [WebREPL console](https://repl.brilliant.xyz) once Monocle is connected. If you’re on a very early version of the firmware, you may be prompted to update manually by typing `import update;update.micropython()` and hitting enter. Subsequent updates will then be automatically shown, and you can start an update by clicking the update button within the WebREPL console.

## Join the community

Our Discord server is open to all, and is the perfect place to get help with your project. See what others are making, and share your project with the community.

[Join the Server](https://discord.gg/7w3DFxek4p){: .btn .btn-purple}
