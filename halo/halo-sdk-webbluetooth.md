---
title: Web Bluetooth
description: An overview of the Brilliant SDK for building browser-based TypeScript/JavaScript apps that talk to Brilliant Halo.
image: /images/halo/halo-splash.png
nav_order: 3
parent: Brilliant SDK
grand_parent: Halo
nav_enabled: true
---

# Brilliant SDK for Web Bluetooth
{: .no_toc }

---

The Brilliant SDK for Web Bluetooth is a TypeScript/JavaScript SDK for building browser-based applications that connect to Halo (or Frame). It is available in two npm packages:

- **[brilliant-ble](https://www.npmjs.com/package/brilliant-ble)** — low-level [Web Bluetooth API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Bluetooth_API) interface
- **[brilliant-msg](https://www.npmjs.com/package/brilliant-msg)** — application-level message types (sprites, text, audio, IMU, photos, clicks)

{: .warning }
Web Bluetooth is only available in Chromium-based browsers (Chrome, Edge, Opera) on desktop and Android. It is **not** available in Firefox or Safari.

---

1. TOC
{:toc}

---

## `brilliant-ble` package: low-level connectivity

| [npm](https://www.npmjs.com/package/brilliant-ble){:target="_blank"} | [Source](https://github.com/brilliantlabsAR/brilliant_sdk/tree/main/webbluetooth/packages/brilliant-ble){:target="_blank"} |

The `BrilliantBle` class connects to Halo (or Frame) via the browser's Web Bluetooth API. Device type is detected automatically at connection time.

**Halo-specific features in `brilliant-ble` 0.4.0:**
- `BrilliantBle.type` getter — `BrilliantDeviceType` enum (`FRAME`, `HALO`, or `UNKNOWN`)
- `sendAudio(data, awaitBtResponse?)` — writes to the Halo audio characteristic
- `sendRemoveSignal()` — sends `0x05` to remove `main.lua` from Halo
- `sendData()` / `sendMessage()` — new `awaitBtResponse` option for write-with/without-response

### Installation
{: .no_toc }

```bash
npm install brilliant-ble
```

Or import from a CDN in your HTML:

```html
<script type="module">
  import { BrilliantBle } from 'https://unpkg.com/brilliant-ble/dist/brilliant-ble.es.js';
</script>
```

### Example usage
{: .no_toc }

```typescript
import { BrilliantBle, BrilliantDeviceType } from 'brilliant-ble';

const frame = new BrilliantBle();

// Connect — opens the browser's device picker
await frame.connect();

console.log('Connected to:', frame.type); // BrilliantDeviceType.HALO

// Send a Lua command
await frame.sendLua(
  "frame.display.text('Hello, Halo!', 50, 100, 0xFFFFFF); print('done')",
  { awaitPrint: true }
);

await frame.disconnect();
```

---

## `brilliant-msg` package: application-level messaging

| [npm](https://www.npmjs.com/package/brilliant-msg){:target="_blank"} | [Source](https://github.com/brilliantlabsAR/brilliant_sdk/tree/main/webbluetooth/packages/brilliant-msg){:target="_blank"} |

`brilliant-msg` enables the host and Haloside halves of an application to **communicate using richly typed messages**.

`brilliant-msg` uses the same programming model as the Python and Flutter SDKs: a **main event loop runs on Halo**, and messages are exchanged asynchronously. Large objects are fragmented into multiple Bluetooth packets and efficiently reassembled on the device.

**Halo-specific features in `brilliant-msg` 1.1.0:**
- `RxClick` + `ClickType` enum — Halo button click events (`SINGLE`, `DOUBLE`, `LONG`), msg code `0x0B`
- `TxTextPage` with `CircularTextLayout` — text rendered within Halo's circular 256×256 display
- Updated Lua libraries (synced with Python and Flutter SDKs):
  - `data.lua` — queue-based message ordering with ACK byte flow control
  - `imu.lua` — 6 × `float32` values with device-specific axis scaling
  - `sprite.lua` — Halo uses integer palette indices; Frame uses colour name strings
  - `audio.lua` — reserves 1 byte for the leading flag byte
- `RxIMU` — decodes 6 `float32` values (was `int16`)
- `TxTextSpriteBlock` — updated `lineHeight` header format

### Installation
{: .no_toc }

```bash
npm install brilliant-ble brilliant-msg
```

### Example usage
{: .no_toc }

```typescript
import { BrilliantBle } from 'brilliant-ble';
import { BrilliantMsg, TxSprite, RxClick, ClickType } from 'brilliant-msg';

const ble = new BrilliantBle();
const frame = new BrilliantMsg(ble);

await ble.connect();

// Upload Lua libraries and main app
await frame.uploadStdluaLibs(['data', 'sprite']);
await frame.uploadFrameApp('./lua/halo_app.lua');
await frame.startFrameApp();

// Listen for button clicks from Halo
const rxClick = new RxClick({
  callback: (type: ClickType) => {
    console.log('Button:', type);  // ClickType.SINGLE, .DOUBLE, or .LONG
    if (type === ClickType.SINGLE) {
      capturePhoto();
    }
  }
});
frame.attach(rxClick);

// Send a sprite to Halo
const imageBytes = await fetch('images/logo.png').then(r => r.arrayBuffer());
const sprite = await TxSprite.fromPngBytes(new Uint8Array(imageBytes));
await frame.sendMessage(0x20, sprite.pack());
```

`lua/halo_app.lua`
```lua
local data = require('data.min')
local sprite = require('sprite.min')

USER_SPRITE = 0x20
CLICK_MSG = 0x0B

function app_loop()
  frame.display.clear(0x000000)
  print('Halo app is running')

  while true do
    rc, err = pcall(function()
      local items = data.process_raw_items()

      for _, item in ipairs(items) do
        local msg_code, raw = item[1], item[2]

        if msg_code == USER_SPRITE then
          local spr = sprite.parse_sprite(raw)
          sprite.set_palette(spr.num_colors, spr.palette_data)
          frame.display.bitmap(1, 1, spr.width, 2^spr.bpp, 0, spr.pixel_data)
        end
      end

      frame.sleep(0.001)
    end)
    if rc == false then
      print(err)
      frame.display.clear(0x000000)
      break
    end
  end
end

-- Send click events back to host
frame.button.single(function()
  frame.bluetooth.send('\x0b\x01')  -- msg code 0x0B, ClickType SINGLE
end)
frame.button.double(function()
  frame.bluetooth.send('\x0b\x02')  -- msg code 0x0B, ClickType DOUBLE
end)
frame.button.long(function()
  frame.bluetooth.send('\x0b\x03')  -- msg code 0x0B, ClickType LONG
end)

app_loop()
```

### Circular text layout for Halo's round display
{: .no_toc }

Use `CircularTextLayout` to constrain multi-line text within Halo's circular 256×256 display:

```typescript
import { TxTextPage, CircularTextLayout } from 'brilliant-msg';

const layout = new CircularTextLayout({
  diameter: 256,
  fontSizePx: 24,
  lineSpacingPx: 4,
});

const page = new TxTextPage({
  text: 'The quick brown fox jumps over the lazy dog',
  layout,
});

// Send first page of text
const pages = page.getPages();
await frame.sendMessage(0x12, pages[0].pack());
```

---

## Building from source

```bash
git clone https://github.com/brilliantlabsAR/brilliant_sdk.git
cd brilliant_sdk/webbluetooth

# Install and build brilliant-ble first (brilliant-msg depends on it)
cd packages/brilliant-ble
npm install
npm run build

# Then build brilliant-msg
cd ../brilliant-msg
npm install
npm run build
```

Common commands (run from inside each package directory):

| Command | Description |
|---------|-------------|
| `npm run build` | Build the library to `dist/` |
| `npm run dev` | Start Vite dev server for the example app |
| `npm run docs:api` | Generate TypeDoc API documentation |
