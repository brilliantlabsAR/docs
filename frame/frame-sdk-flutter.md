---
title: Flutter
description: An overview of the Frame SDK for building Flutter mobile apps that talk to Frame AR glasses.
image: /images/frame/frame-splash.png
nav_order: 2
parent: Frame SDK
grand_parent: Frame
nav_enabled: true

---

# Frame SDK for Flutter
{: .no_toc }

---

The Frame SDK for Flutter is available in a low-level library ([frame_ble](https://pub.dev/packages/frame_ble/)) for Bluetooth LE connectivity using [Flutter Blue Plus](https://pub.dev/packages/flutter_blue_plus) with a limited Lua REPL, and an application-level library ([frame_msg](https://pub.dev/packages/frame_msg/)) for passing rich objects between your host program and Frame, such as images, streamed audio, IMU data and rasterized text.

Additionally for Flutter developers the community has contributed even higher-level options for getting started quickly with single-page demo Frame applications, including specific helpers for computer vision pipelines.

---

1. TOC
{:toc}

---

## `frame_ble` package: low-level connectivity

| [![Available on pub.dev](https://img.shields.io/pub/v/frame_ble)](https://pub.dev/packages/frame_ble){:target="_blank"} | [API Reference](https://pub.dev/documentation/frame_ble/latest/){:target="_blank"} | [Source](https://github.com/CitizenOneX/frame_ble){:target="_blank"} | [Example](https://github.com/CitizenOneX/frame_ble/tree/main/example){:target="_blank"} |

The `BrilliantBluetooth` class allows a host to connect to Frame, initiating pairing if required. A sequence of Lua strings can be sent to Frame for execution, optionally returning their results as strings. Transmitted and received strings must be shorter than the Bluetooth MTU (`BrilliantDevice.maxStringLength()`).

[Frame-specific Lua APIs](frame-sdk-lua.md) can be called to draw on the display, sample the accelerometer, put Frame into firmware update mode, set the tap and user data callbacks, and more.

In addition to Lua strings, `BrilliantDevice` can also send control commands (break and reset), as well as custom user data messages that can be handled by a user-defined data handler function on Frame. See [Talking to Frame Over Bluetooth](frame-sdk-bluetooth-specs.md) for more details.

Consult the [API Reference](https://pub.dev/documentation/frame_ble/latest/){:target="_blank"} for the complete list of functions available in `frame_ble`, and the [Example](https://github.com/CitizenOneX/frame_ble/blob/main/example/lib/main.dart){:target="_blank"} to see them in action. Don't see an example you need? Ask in [Discord](https://discord.com/invite/vDS9X7gdwg){:target="_blank"} to have one added.

Note: It is expected that most application developers will prefer to use the [frame_msg package](https://pub.dev/packages/frame_msg) to make use of first-class messages and efficient transport for sprites, images, audio clips, and to avoid having to wrangle Bluetooth packet fragmentation and assembly. The `frame_ble` package, with only a dependency on the `flutter_blue_plus` library, is still a handy choice for `"Hello, World!"`, simple utilities, or as the basis of a custom application framework in Flutter.

Note: Frame SDK for Flutter is under active development and it is expected that some `frame_ble` classes may change to harmonize with the Python SDK naming, while retaining some differences due to the mobile context.

### Example usage
{: .no_toc }
```dart
  // ...
  Future<void> _showCounterOnFrame() async {
    // connect to Frame the first time
    if (_frame == null) {

      // request permission to use Bluetooth
      try {
        await BrilliantBluetooth.requestPermission();
      } catch (e) {
        print('Error requesting permission to use Bluetooth: $e');
        return;
      }

      // look for a Frame and connect to it
      BrilliantScannedDevice? scannedFrame;
      try {
        scannedFrame = await BrilliantBluetooth.scan().first;
      } catch (e) {
        print('Error scanning for Frame: $e');
        return;
      }

      try {
        // connect to the scanned Frame
        _frame = await BrilliantBluetooth.connect(scannedFrame);

        print('Found Frame: $_frame');
      }
      catch (e) {
        print('Error connecting to Frame: $e');
        return;
      }

      // send a break signal to stop any running Lua main loop
      await _frame!.sendBreakSignal();
    }

    // send the counter to Frame for display
    if (await _frame?.connectionState.first == BrilliantConnectionState.connected) {
      await _frame!.sendString(
        'frame.display.text("Hello, World! ($_counter)", 1, 1) frame.display.show()',
        awaitResponse: false
      );
    }
    else {
      print('Frame is not connected');
      _frame = null;
    }
  }
  // ...
```

| Selected Examples |
|-------------------|
| ["Hello, World!"](https://github.com/CitizenOneX/frame_ble/blob/main/example/lib/main.dart){:target="_blank"} |

---

## `frame_msg` package: application-level messaging

| [![Available on pub.dev](https://img.shields.io/pub/v/frame_msg)](https://pub.dev/packages/frame_msg){:target="_blank"} | [API Reference](https://pub.dev/documentation/frame_msg/latest/){:target="_blank"} | [Source](https://github.com/CitizenOneX/frame_msg){:target="_blank"} | Example |

`frame-msg` enables both the hostside and Frameside halves of an application to **communicate using richly typed messages** - for example transmitting Sprites to Frame with width, height, palette data and pixel data attributes. (See the code below for an example.)

Additionally, `frame-msg` uses a programming model in which **a main event loop is running on Frame**. As a result, messages are exchanged asychronously and handled in an event-driven way. This is in contrast to the "Lua REPL" model, in which single statements are sent to Frame to be executed, and the host attempts to block until execution has completed. In a REPL-style model, it would not be practical to create an application that for example continuously streams audio from Frame to host, and simultaneously sends text back for display (a live translation app). In contrast, with a main event loop running on Frame it is possible to send some audio back to the host if some is available, and check for messages indicating text is ready for display, then loop around again.

### How it works
{: .no_toc }

In order to **serialize and deserialize large objects**, use `frame_ble`'s `BrilliantDevice.send_message()` function that **fragments large payloads** into multiple Bluetooth packets marked with a matching **`msg_code`**, and **efficiently reassembles them on Frame**. After parsing the reconstructed payload into the desired type, a complete object is made available for the application's main loop in Lua.

Handling **rich message types** is done by providing symmetrical **packing code and parsing code** for standard types.

* For "Transmit" (`Tx`) message types, the packing (serialization) code is in the Dart/Flutter type (e.g. `TxSprite.pack()`) and the parsing (deserialization) code is in the corresponding Lua module (`sprite.lua` / `parse_sprite()`).

* For "Receive" (`Rx`) message types, e.g. `RxPhoto`, the serialization code is present implicitly in the Lua module `camera.lua` in `capture_and_send()`, and the deserialization code is present in the `RxPhoto` class.

This approach presents a natural extension point for user-defined types too: a custom application-specific message might contain an icon, a heading and some detailed text - and this can all be sent together and used all at once on Frame to update the display. By implementing the packing and parsing code for user-defined types, custom objects can be used in applications in the same way as the standard types.

### Startup sequence
{: .no_toc }

`frame-msg` applications tend to follow a startup sequence that ensures Frame is in a known state for the application to run, namely:
* Optionally send a break/reset/break signal sequence to ensure that Frame is in Lua REPL mode and its memory is freshly cleared
* Upload standard Lua libraries to Frame: `data` for handling all messaging, plus any others to support specific messages the application uses (e.g. `sprite`, `plain_text`, etc.)
* Upload the main Frame application Lua file (e.g. `my_frame_app.lua`). This can often be an exact copy of an example main Lua file that handles the same message types.
* Start the main application loop on Frame (after which no Lua REPL commands will be accepted by Frame).

After the Frameside application reports that it has started, the hostside and Frameside application halves begin messaging each other asynchronously: passing text, images, audio etc.


## Example usage
{: .no_toc }
`sprite_display.dart`
```dart
  // ...
  // connect to Frame using `frame-ble` in the usual way
  // frame = await BrilliantBluetooth.connect(scannedFrame);
  // ...
  Future<void> run() async {
    // Open the file picker
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['png'],
    );

    if (result != null) {
      File file = File(result.files.single.path!);
      Uint8List pngBytes = await file.readAsBytes();

      // send the Sprite to Frame
      var msg = TxSprite.fromPngBytes(pngBytes: pngBytes);
      await frame!.sendMessage(0x20, msg.pack());
    }
  }
  // ...
```

`sprite_frame_app.lua`
```lua
local data = require('data.min')
local sprite = require('sprite.min')

-- Phone to Frame flags
USER_SPRITE = 0x20

-- register the message parsers so they are automatically called when matching data comes in
data.parsers[USER_SPRITE] = sprite.parse_sprite

-- Main app loop
function app_loop()
  frame.display.text('Frame App Started', 1, 1)
  frame.display.show()

  -- tell the host program that the frameside app is ready (waiting on await_print)
  print('Frame app is running')

  while true do
    rc, err = pcall(
      function()
        -- process any raw data items, if ready
        local items_ready = data.process_raw_items()

        -- one or more full messages received
        if items_ready > 0 then

          if data.app_data[USER_SPRITE] ~= nil then
            local spr = data.app_data[USER_SPRITE]

            -- set the palette in case it's different to the standard palette
            sprite.set_palette(spr.num_colors, spr.palette_data)

            -- show the sprite
            frame.display.bitmap(1, 1, spr.width, 2^spr.bpp, 0, spr.pixel_data)
            frame.display.show()

            -- clear the object and run the garbage collector right away
            data.app_data[USER_SPRITE] = nil
            collectgarbage('collect')
          end

        end

        -- can't sleep for long, might be lots of incoming bluetooth data to process
        frame.sleep(0.001)
      end
    )
    -- Catch an error (including the break signal) here
    if rc == false then
      -- send the error back on the stdout stream and clear the display
      print(err)
      frame.display.text(' ', 1, 1)
      frame.display.show()
      break
    end
  end
end

-- run the main app loop
app_loop()
```

| Selected Examples | Flutter | Lua |
|-------------------|---------|-----|
| Display a Sprite (`simple_frame_app` example)  | [Flutter](https://github.com/CitizenOneX/frame_sprite_viewer/blob/main/lib/main.dart){:target="_blank"} | [Lua](https://github.com/CitizenOneX/frame_sprite_viewer/blob/main/assets/frame_app.lua){:target="_blank"} |

---

## Higher-level application scaffolding

In addition to `frame-msg` and `frame-ble`, the Frame developer community has provided some even higher-level scaffolding for creating demo apps and to experiment with ideas quickly, but are not recommended for production apps:

### Simple Frame App
| [![Available on pub.dev](https://img.shields.io/pub/v/simple_frame_app)](https://pub.dev/packages/simple_frame_app){:target="_blank"} | [API Reference](https://pub.dev/documentation/simple_frame_app/latest/){:target="_blank"} | [Source](https://github.com/CitizenOneX/simple_frame_app){:target="_blank"} |

Quickstart scaffolding for a single-page mobile application that handles basic connection to Frame and loading of Frameside application resources including Lua files and sprites.

| Selected Examples | Flutter | Lua |
|-------------------|---------|-----|
| [Display a Sprite](https://github.com/CitizenOneX/frame_sprite_viewer){:target="_blank"} | [Flutter](https://github.com/CitizenOneX/frame_sprite_viewer/blob/main/lib/main.dart){:target="_blank"} | [Lua](https://github.com/CitizenOneX/frame_sprite_viewer/blob/main/assets/frame_app.lua){:target="_blank"} |
| [Wikipedia Viewer](https://github.com/CitizenOneX/wiki_frame){:target="_blank"} | [Flutter](https://github.com/CitizenOneX/wiki_frame/blob/main/lib/main.dart){:target="_blank"} | [Lua](https://github.com/CitizenOneX/wiki_frame/blob/main/assets/frame_app.lua){:target="_blank"} |
| [Pollinations.AI Image Generation](https://github.com/CitizenOneX/frame_pollinations){:target="_blank"} | [Flutter](https://github.com/CitizenOneX/frame_pollinations/blob/main/lib/main.dart){:target="_blank"} | [Lua](https://github.com/CitizenOneX/frame_pollinations/blob/main/assets/frame_app.lua){:target="_blank"} |
| [Audio Clip Recorder](https://github.com/CitizenOneX/frame_audio_clip){:target="_blank"} | [Flutter](https://github.com/CitizenOneX/frame_audio_clip/blob/main/lib/main.dart){:target="_blank"} | [Lua](https://github.com/CitizenOneX/frame_audio_clip/blob/main/assets/frame_app.lua){:target="_blank"} |
| [Live Streaming Transcription](https://github.com/CitizenOneX/frame_transcribe_googlespeech){:target="_blank"} | [Flutter](https://github.com/CitizenOneX/frame_transcribe_googlespeech/blob/main/lib/main.dart){:target="_blank"} | [Lua](https://github.com/CitizenOneX/frame_transcribe_googlespeech/blob/main/assets/frame_app.lua){:target="_blank"} |

### Frame Vision App
| [![Available on pub.dev](https://img.shields.io/pub/v/simple_frame_app)](https://pub.dev/packages/simple_frame_app){:target="_blank"} | [API Reference](https://pub.dev/documentation/simple_frame_app/latest/){:target="_blank"} | [Source](https://github.com/CitizenOneX/simple_frame_app){:target="_blank"} |

Even more specialized quickstart scaffolding within the `simple_frame_app` package, designed for computer vision prototyping. In addition to handling connection and application resources on Frame, the Frame Vision App mixin conveniently provides images from the Frame camera directly to your code for custom processing.

| Selected Examples | Flutter | Lua |
|-------------------|---------|-----|
| [Live Camera Feed](https://github.com/CitizenOneX/live_camera_feed){:target="_blank"} | [Flutter](https://github.com/CitizenOneX/live_camera_feed/blob/main/lib/main.dart){:target="_blank"} | [Lua](https://github.com/CitizenOneX/live_camera_feed/blob/main/assets/frame_app.lua){:target="_blank"} |
| [Hotdog or not hotdog](https://github.com/CitizenOneX/frame_vision_hotdog){:target="_blank"} | [Flutter](https://github.com/CitizenOneX/frame_vision_hotdog/blob/main/lib/main.dart){:target="_blank"} | [Lua](https://github.com/CitizenOneX/frame_vision_hotdog/blob/main/assets/frame_app.lua){:target="_blank"} |
| [Mobile Image Classification](https://github.com/CitizenOneX/frame_vision_classification){:target="_blank"} | [Flutter](https://github.com/CitizenOneX/frame_vision_classification/blob/main/lib/main.dart){:target="_blank"} | [Lua](https://github.com/CitizenOneX/frame_vision_classification/blob/main/assets/frame_app.lua){:target="_blank"} |
| [Mobile Vision Translation](https://github.com/CitizenOneX/frame_vision_translation){:target="_blank"} | [Flutter](https://github.com/CitizenOneX/frame_vision_translation/blob/main/lib/main.dart){:target="_blank"} | [Lua](https://github.com/CitizenOneX/frame_vision_translation/blob/main/assets/frame_app.lua){:target="_blank"} |

### “Mobile app with no mobile coding”

| [Mobile App](https://github.com/CitizenOneX/frame_vision_api){:target="_blank"}  | [Sample API Backend](https://github.com/CitizenOneX/frame_vision_api_impl){:target="_blank"}

Just want to code your computer vision backend in Python, but want a mobile app experience? Use this simple mobile app as-is (or customize) and point it to your own API endpoint for image processing, sending the result back to Frame for display.


---

## Legacy SDKs

Note: The legacy SDK package is available for [frame-sdk](https://pub.dev/packages/frame_sdk) as [previously documented here](https://github.com/brilliantlabsAR/docs/blob/c33420dc55eb12b27f5a804b9a5a82247d471ae9/frame/building-apps-sdk.md).

In order to allow richer experiences on Frame including image display and audio streaming, the decision was made to move to an SDK model based on asynchronous message-passing between a main application loop running on the host, and a main event loop running on Frame. This approach is used in both the [Python](https://pypi.org/project/frame-msg/) and [Flutter](https://pub.dev/packages/frame_msg) SDKs.

While this requires a slight adjustment from the way the legacy SDKs were used, there are many examples provided (e.g. [Sprite Viewer](https://github.com/CitizenOneX/frame_sprite_viewer), [Unicode Text Display](https://github.com/CitizenOneX/frame_textspriteblock), [Teleprompter](https://github.com/CitizenOneX/frame_teleprompter), [Mobile Image Classifier](https://github.com/CitizenOneX/frame_vision_classification), [Realtime Multimodal Assistant](https://github.com/brilliantlabsAR/frame_realtime_gemini_voicevision)) and a [helpful community in Discord](https://discord.com/invite/vDS9X7gdwg) to help you build your project.
