---
title: Flutter
description: An overview of the Brilliant SDK for building Flutter mobile apps that talk to Brilliant Halo.
image: /images/halo/halo-splash.png
nav_order: 2
parent: Brilliant SDK
grand_parent: Halo
nav_enabled: true
---

# Brilliant SDK for Flutter
{: .no_toc }

---

The Brilliant SDK for Flutter is available in a low-level library ([brilliant_ble](https://pub.dev/packages/brilliant_ble/)) for Bluetooth LE connectivity, and an application-level library ([brilliant_msg](https://pub.dev/packages/brilliant_msg/)) for passing rich objects between your host app and Halo — such as images, streamed audio, and rasterized text.

For rapid app development, the [simple_brilliant_app](https://pub.dev/packages/simple_brilliant_app) package provides scaffolding for single-page Flutter apps that work with both Halo and Frame. A convenience meta-package ([brilliant_sdk](https://pub.dev/packages/brilliant_sdk)) bundles `brilliant_ble` and `brilliant_msg` together.

The Brilliant SDK for Flutter also supports **Frame** devices. `brilliant_ble` automatically detects whether the connected device is a Halo or a Frame at connection time.

---

1. TOC
{:toc}

---

## `brilliant_ble` package: low-level connectivity

| [![Available on pub.dev](https://img.shields.io/pub/v/brilliant_ble)](https://pub.dev/packages/brilliant_ble){:target="_blank"} | [API Reference](https://pub.dev/documentation/brilliant_ble/latest/){:target="_blank"} | [Source](https://github.com/brilliantlabsAR/brilliant_sdk/tree/main/flutter/packages/brilliant_ble){:target="_blank"} |

The `BrilliantBluetooth` class connects to Halo (or Frame), initiating pairing if required. A sequence of Lua strings can be sent to the device for execution, optionally returning their results. Transmitted strings must be shorter than the Bluetooth MTU (`BrilliantDevice.maxStringLength()`).

[Halo-specific Lua APIs](/halo/halo-sdk-lua) can be called to draw on the display, sample the IMU, set button and data callbacks, control the microphone and speaker, and more.

In addition to Lua strings, `BrilliantDevice` can send control commands (break, reset, remove) and custom user data messages handled by a callback on the device.

**Halo-specific features in `brilliant_ble` 4.0.0:**
- `BrilliantDeviceType` enum (`frame`, `halo`, `unknown`) — detected automatically at connection time
- `BrilliantDevice.type` getter
- `BrilliantDevice.audioTxChannel` — Halo-specific BLE characteristic for audio output
- `BrilliantDevice.isLuaInReplState()` — probe to check if the Lua REPL is active
- `BrilliantBluetooth.getSystemConnectedDevice(uuid)` — check for an existing OS-level connection
- Android: MTU 517 negotiation, high connection priority, 2M PHY, bond creation
- Android: fixed spurious reconnects after user-initiated disconnects

### Example usage
{: .no_toc }

```dart
import 'package:brilliant_ble/brilliant_ble.dart';

// Scan and connect
BrilliantScannedDevice? scannedDevice = await BrilliantBluetooth.scan().first;
BrilliantDevice device = await BrilliantBluetooth.connect(scannedDevice);

print('Connected to: ${device.type}');  // BrilliantDeviceType.halo

// Send a break signal to stop any running Lua loop
await device.sendBreakSignal();

// Send Lua to draw text and print confirmation
await device.sendString(
  'frame.display.text("Hello, Halo!", 50, 100, 0xFFFFFF); print("done")',
  awaitResponse: true,
);
```

---

## `brilliant_msg` package: application-level messaging

| [![Available on pub.dev](https://img.shields.io/pub/v/brilliant_msg)](https://pub.dev/packages/brilliant_msg){:target="_blank"} | [API Reference](https://pub.dev/documentation/brilliant_msg/latest/){:target="_blank"} | [Source](https://github.com/brilliantlabsAR/brilliant_sdk/tree/main/flutter/packages/brilliant_msg){:target="_blank"} |

`brilliant_msg` enables the host and Haloside halves of an application to **communicate using richly typed messages** — for example transmitting sprites to Halo with width, height, palette data, and pixel data as a single object.

`brilliant_msg` uses a programming model in which **a main event loop runs on Halo**. Messages are exchanged asynchronously and handled in an event-driven way, making it practical to build applications that simultaneously stream audio from Halo to the host *and* send display content back to Halo.

### How it works
{: .no_toc }

Large objects are serialized into multiple Bluetooth packets marked with a `msgCode`, and **efficiently reassembled on the device**. After parsing, the complete object is delivered to the Lua main loop.

* **`Tx` message types** — packing (Dart) + parsing (Lua) — e.g. `TxSprite.pack()` + `sprite.lua`
* **`Rx` message types** — parsing (Dart) + implicit serialization in Lua — e.g. `RxPhoto` + `camera.lua`

**Key changes for Halo in `brilliant_msg` 3.0.0:**
- `RxClick` + `ClickType` enum — Halo button click events (`single`, `double`, `long`), msg code `0x0B`
- `TxTextPage` with `CircularTextLayout` — text rendered within Halo's circular 256×256 display
- `data.lua` — queue-based message ordering with ACK byte flow control
- `imu.lua` — 6 × `float32` values with Halo-specific axis scaling and mapping
- `sprite.lua` / `image_sprite_block.lua` — Halo uses integer palette indices (0–15)
- `TxSprite` wire format — `compressed` flag byte added at header offset 5

### Startup sequence
{: .no_toc }

`brilliant_msg` applications follow a standard sequence:

1. Send break/reset/break signals to ensure Halo is in Lua REPL mode
2. Upload standard Lua libraries (`data`, `sprite`, `plain_text`, etc.)
3. Upload the main Lua application file
4. Start the Haloside event loop
5. Exchange messages asynchronously

### Example usage
{: .no_toc }

`sprite_display.dart`
```dart
import 'package:brilliant_ble/brilliant_ble.dart';
import 'package:brilliant_msg/brilliant_msg.dart';

// connect using brilliant_ble...
// BrilliantDevice frame = await BrilliantBluetooth.connect(scannedDevice);

Future<void> run(BrilliantDevice frame) async {
  // Pick an image file
  FilePickerResult? result = await FilePicker.platform.pickFiles(
    type: FileType.custom,
    allowedExtensions: ['png'],
  );

  if (result != null) {
    final pngBytes = await File(result.files.single.path!).readAsBytes();
    final sprite = TxSprite.fromPngBytes(pngBytes: pngBytes);
    await frame.sendMessage(0x20, sprite.pack());
  }
}
```

`lua/halo_app.lua`
```lua
local data = require('data.min')
local sprite = require('sprite.min')

USER_SPRITE = 0x20

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

app_loop()
```

| Selected Message Types | Description |
|------------------------|-------------|
| `TxSprite` | Send an indexed-color PNG image for display |
| `TxTextPage` | Send a page of text with `CircularTextLayout` for Halo's round display |
| `TxCaptureSettings` | Request a photo from the camera |
| `RxPhoto` | Receive a JPEG photo from the camera |
| `RxAudio` | Receive a PCM or LC3 audio stream |
| `RxIMU` | Receive accelerometer and magnetometer readings |
| `RxClick` | Receive Halo button click events (single / double / long) |

---

## `brilliant_sdk` meta-package

| [![Available on pub.dev](https://img.shields.io/pub/v/brilliant_sdk)](https://pub.dev/packages/brilliant_sdk){:target="_blank"} | [Source](https://github.com/brilliantlabsAR/brilliant_sdk/tree/main/flutter/packages/brilliant_sdk){:target="_blank"} |

The `brilliant_sdk` meta-package bundles `brilliant_ble` and `brilliant_msg` as a single dependency for apps that use both packages. Add it to your `pubspec.yaml`:

```yaml
dependencies:
  brilliant_sdk: ^1.0.0
```

---

## `simple_brilliant_app` scaffolding

| [![Available on pub.dev](https://img.shields.io/pub/v/simple_brilliant_app)](https://pub.dev/packages/simple_brilliant_app){:target="_blank"} | [Source](https://github.com/brilliantlabsAR/brilliant_sdk/tree/main/flutter/packages/simple_brilliant_app){:target="_blank"} |

`simple_brilliant_app` provides quickstart scaffolding for single-page Flutter applications that connect to Halo or Frame. It handles Bluetooth connection lifecycle, uploading Lua libraries and app files to the device, and provides mixins for common application patterns.

`simple_brilliant_app` 8.0.0 adds full Halo support:
- Device-aware startup: uses `frame.display.clear()` on Halo, bitmap fill on Frame
- `FrameVisionAppState` mixin: uses `RxClick` for Halo button input and `RxTap` for Frame tap input

### Getting started with `simple_brilliant_app`
{: .no_toc }

```bash
flutter pub add simple_brilliant_app
```

Follow the [flutter_blue_plus setup instructions](https://pub.dev/packages/flutter_blue_plus#getting-started){:target="_blank"} to configure your Android and iOS projects for Bluetooth LE.

Copy the template files from the package into your project:
- `template/main.dart` → `lib/main.dart`
- `template/frame_app.lua` → `assets/frame_app.lua`

Declare the Lua library assets in `pubspec.yaml`:

```yaml
flutter:
  assets:
    - packages/brilliant_msg/lua/data.min.lua
    - packages/brilliant_msg/lua/sprite.min.lua
    - packages/brilliant_msg/lua/plain_text.min.lua
    - packages/brilliant_msg/lua/camera.min.lua
    - packages/brilliant_msg/lua/audio.min.lua
    - packages/brilliant_msg/lua/imu.min.lua
    - assets/frame_app.lua
```

### `FrameVisionAppState` mixin — for camera and click/tap input
{: .no_toc }

The `FrameVisionAppState` mixin handles the differences between Halo and Frame input:

```dart
class _MyAppState extends State<MyApp>
    with SimpleFrameAppState, FrameVisionAppState {

  // Called when Halo button is clicked
  @override
  Future<void> onClick(ClickType type) async {
    if (type == ClickType.single) {
      await capturePhoto();
    }
  }

  // Called when Frame is tapped (tap count provided)
  @override
  Future<void> onTap(int taps) async {
    await capturePhoto();
  }
}
```

---

## Installing from source

When working from the `brilliant_sdk` repository:

```bash
git clone https://github.com/brilliantlabsAR/brilliant_sdk.git
cd brilliant_sdk/flutter

# Install Melos
dart pub global activate melos
export PATH="$PATH":"$HOME/.pub-cache/bin"

# Bootstrap all packages
melos bootstrap
```

Common workspace commands:

| Command | Description |
|---------|-------------|
| `melos bootstrap` | Get dependencies for all packages |
| `melos analyze` | Run `flutter analyze` across all packages |
| `melos format` | Format all Dart files |
| `melos test` | Run tests across all packages |
