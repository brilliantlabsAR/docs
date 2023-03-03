---
title: Update
description: A guide on how to update your Monocle AR device.
image: /micropython/images/monocle-micropython.png
nav_order: 4
---

# Updating your Monocle firmware
{: .no_toc }

Firmware updates should be automatic if you're using the Web REPL at [repl.brilliant.xyz](https://repl.brilliant.xyz).

Make sure you're on Google Chrome for Desktop, Android Chrome, or [Bluefy](https://apps.apple.com/us/app/bluefy-web-ble-browser/id1492822055) on iOS.

---

If that does work, you can follow this tutorial to update manually. The same steps are also described below.

<div style="display: flex; justify-content: center"> 
<iframe width="560" height="315" src="https://www.youtube.com/embed/-DYI3DfHPyw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

## Steps:

1. Make sure your Monocle is well charged before starting an update.

1. Download both the Brilliant App as well as the nRF Connect App.
    - Get the **Brilliant App** on Apple [AppStore](https://apps.apple.com/us/app/monocle-by-brilliant/id1632203938) or Google [Play Store](https://play.google.com/store/apps/details?id=com.brilliantmonocle).
    - Get the **nRF Connect App** on Apple [AppStore](https://apps.apple.com/us/app/nrf-connect-for-mobile/id1054362403) or Google [Play Store](https://play.google.com/store/apps/details?id=no.nordicsemi.android.mcp&hl=en&gl=US).

1. Download the latest firmware from our [releases page](https://github.com/brilliantlabsAR/monocle-micropython/releases), and save it to your mobile.

1. Connect to the Monocle from within the Brilliant App, and type the commands:

    ```python
    import update
    update.micropython()
    ```

1. Switch to the nRF Connect App, and connect to **"DFUTarg"**.

1. Switch to the DFU tab, select your file, and start the update.

1. Keep Monocle close, and don't switch app while the update is in progress.

Once the update is complete, Monocle will restart, and will be running the new firmware.

If the update process stops for any reason, simply put Monocle back into the case, search for **"DFUTarg"** from within the nRF Connect App, and try again.