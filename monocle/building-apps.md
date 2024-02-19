---
title: Building Apps
description: A guide on how to develop your own applications for Monocle.
image: /images/monocle/monocle-splash.png
nav_order: 3
parent: Monocle
redirect_from:
  - /building-apps
---

# Building Apps
{: .no_toc }

---

## Getting started with AR Studio for VSCode
{: .no_toc }

AR Studio for VSCode lets you develop, test and save apps directly onto your Monocle. Download it today from the [VSCode Marketplace](https://marketplace.visualstudio.com/items?itemName=brilliantlabs.brilliant-ar-studio) and start developing your Monocle projects.

![Brilliant AR Studio for VSCode](/monocle/images/vs-code-extension.png)

- Once installed, connect to Monocle with `Ctrl-Shift-P` → `Brilliant AR Studio: Connect`.
- Copy the example below, and save the file as `main.py`.

```python
import touch
import display

def change_text(button):
    new_text = display.Text(f"Button {button} touched!", 0, 0, display.WHITE)
    display.show(new_text)

touch.callback(touch.EITHER, change_text)

initial_text = display.Text("Tap a touch button", 0, 0, display.WHITE)
display.show(initial_text)
```

- Upload `main.py` by right clicking on the file in the Explorer and clicking `Brilliant AR Studio: Upload File to Device`. Ensure that you have a workspace or folder open in the Explorer so that you can see the file.
- When prompted for the on-device name, keep it as `main.py` and press Enter.
- Run main.py with `Ctrl-Shift-P` → `Brilliant AR Studio: Build`.
- You should be able to touch each of the touch pads on Monocle, and see the display update.

---

## Connecting to the wider world

MicroPython on Monocle simplifies the usage of complex protocols typically employed in Bluetooth devices. Just like Python on desktop, Monocle can be conveniently interacted with using the REPL (Read Evaluate Print Loop) interface. The key difference? It's completely wireless!

This wireless functionality not only allows for effortless testing and application development on Monocle, but also enables Python commands to control Monocle from your customized iOS, Android, or Desktop app.

![Diagram of Monocle network flow](/images/monocle-network-flow.png)

Below are some templates to help you get started building your own apps.

### iOS & Android

Noa is our ChatGPT client for Monocle. Check out the source code for [iOS](https://github.com/brilliantlabsAR/noa-for-ios), as well as for [Android](https://github.com/brilliantlabsAR/noa-for-android) and use it as a template for your own mobile app.

![Brilliant Noa for iOS App](/images/noa-for-ios-screens.png)

### Javascript

The [WebREPL](https://repl.brilliant.xyz) is a good starting point building your own web apps. Try it from Google Chrome on your PC, Mac, Android, or a Web Bluetooth compatible web browser on your iOS device such as [Bluefy](https://apps.apple.com/us/app/bluefy-web-ble-browser/id1492822055).

Check out the full instructions and the source code [here](https://github.com/siliconwitchery/web-bluetooth-repl/).

![Accessing MicroPython on Monocle using the WebREPL interface](/monocle/images/micropython-web-repl.png)

### Community projects

For more application examples and ideas, check out the [community projects](/community) section to see what others have built.