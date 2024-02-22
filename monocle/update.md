---
title: Firmware Updates
description: A guide on how to update your Monocle AR device.
image: /images/monocle/monocle-splash.png
nav_order: 4
parent: Monocle
redirect_from:
  - /monocle/update
---

# Updating your Monocle Firmware
{: .no_toc }

---

If you're using the [Brilliant AR Studio](/building-apps/#getting-started-with-ar-studio-for-vscode), firmware updates are automatic, and you will be prompted whenever a new update is available.

If you run into problems, you can update manually using the following steps:

1. Firstly, ensure that you're using a browser that supports Web Bluetooth such as Google Chrome for Desktop, Android Chrome, or [Bluefy](https://apps.apple.com/us/app/bluefy-web-ble-browser/id1492822055) on iOS.

1. Next, navigate to the WebREPL at [https://repl.brilliant.xyz](https://repl.brilliant.xyz)

1. Press any key to open the connection dialog box.

1. Select **monocle** from the list and hit connect. (Note, if a previous update had failed, you may see **DFUTarg** in the list. In this case, connect to that instead).

1. Once connected, check the message at the bottom of the screen. If it says `Connected.` that means that you're already on the latest firmware, if not, you will be prompted that an update is available and you can click the update button to start the update.

1. If you see a message that the current firmware could not be detected, then you can use the following commands to start the update manually:

    ```python
    import update
    update.micropython()
    ```

1. Monocle will then restart into the update mode, and you'll be prompted to reconnect. Press any key to open the connection dialog box again.

1. Select **DFUTarg** from the list, and connect.

1. The firmware update will start and Monocle will reboot. You may need to place your Monocle into the case once the update is complete to reboot it.

1. That's it! You're Monocle should now be up to date. Check it by using the commands below once connected again. The version number should match the latest release on the Monocle MicroPython [releases page](https://github.com/brilliantlabsAR/monocle-micropython/releases).

    ```python
    import device
    device.VERSION
    ```