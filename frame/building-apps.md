---
title: Building Apps
description: A guide on how to develop your own applications for Frame.
image: /images/frame/frame-splash.png
nav_order: 2
parent: Frame
---

# Building Apps
{: .no_toc }

---

## AR Studio for VSCode
{: .no_toc }

![Brilliant AR Studio for VSCode](/frame/images/frame-vs-code-extension.png)

```lua
function change_text()
    frame.display.clear()
    frame.display.text("Frame tapped!", 50, 100)
    frame.display.show()
end

frame.imu.tap_callback(change_text)
frame.display.clear()
frame.display.text("Tap the side of Frame", 50, 100)
frame.display.show()
```

---

## Bluetooth

### Pairing & connecting

![Bluetooth connection sequence diagram](/frame/images/frame-bluetooth-connection-diagram.drawio.svg)

### Sending Lua

![Bluetooth connection sequence diagram](/frame/images/frame-bluetooth-sending-lua-diagram.drawio.svg)

### Sending Data

![Bluetooth connection sequence diagram](/frame/images/frame-bluetooth-sending-lua-diagram.drawio.svg)

### Firmware updates



---

## Frame utilities for Python

### Bluetooth library

### Font & graphics generation tool