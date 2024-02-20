---
title: Hardware
description: A brief overview of how Frame works under the hood.
image: /images/frame/frame-splash.png
nav_order: 1
parent: Frame
---

# Frame Hardware Manual
{: .no_toc }

---

![Frame exploded view](/frame/images/frame-exploded-view.png)

Here you'll find all the details about how Frame works under the hood. For software related information, be sure to also check out the [Building Apps](/frame/building-apps) and [Lua API](/frame/lua) pages.

## Key features
{: .no_toc }
- 640x400 color OLED display
- 20° FOV optic
- Order option for personalized prescriptions
- Thin and light 6mm lenses (not including optional prescription)
- 720p low power color camera
- Microphone
- FPGA acceleration for graphics and imaging
- Bluetooth 5.2
- 210mAh built-in rechargeable li-ion battery
- 3 axis accelerometer with tap detection
- 3 axis e-compass
- Full featured Lua based OS
- Charging dock with USB Type-C & 140mAh battery

## Example uses:
{: .no_toc }
- Generative AI on the go
- ML based image augmentation
- Computer vision research
- QR code & barcode detection
- Heads up telemetry
- AR apps & games design

## Contents
{: .no_toc }

1. TOC
{:toc}

## Block diagram

This diagram shows a general overview of the Frame internal hardware architecture.

![Frame block diagram](/frame/images/frame-hardware-block-diagram.drawio.svg)

---

## Bluetooth MCU


---

## FPGA


---

## Display


---

## Camera


---

## Microphone


---

## Motion Sensor (IMU)


---

## Power


### Regulation


### Battery charging


---

## Charging cradle (Mister Power)


---

## Developing custom firmware


### Developing for the Bluetooth MCU


### Developing for the FPGA


### Debugging


### Creating firmware updates


---

## Schematics

### Frame

<div>
    <a href="/frame/frame-schematics.pdf">
        <object data="/frame/frame-schematics.pdf" type="application/pdf" width="100%" height="525"></object>
    </a>
</div>

### Charging cradle

<div>
    <a href="/frame/charging-cradle-schematics.pdf">
        <object data="/frame/charging-cradle-schematics.pdf" type="application/pdf" width="100%" height="525"></object>
    </a>
</div>

---

## Mechanical

### Frame

[Download the 3D Model in STL format](/frame/frame.stl)

<div>
    <a href="/frame/frame-mechanical-drawing.pdf">
        <object data="/frame/frame-mechanical-drawing.pdf" type="application/pdf" width="100%" height="525"></object>
    </a>
</div>

### Charging cradle

[Download the 3D Model in STL format](/frame/charging-cradle.stl)

<div>
    <a href="/frame/charging-cradle-mechanical-drawing.pdf">
        <object data="/frame/charging-cradle-mechanical-drawing.pdf" type="application/pdf" width="100%" height="525"></object>
    </a>
</div>

---

## Device characteristics

Typical and absolute device characteristics are shown below. To get the best lifetime of your Frame, it's recommended to keep within these limits.

### Typical characteristics

|                         | Min    | Typ   | Max   |
|:------------------------|:------:|:-----:|:-----:|
| Frame operating current | 45mA   | 80mA  | 100mA |
| Frame sleep current     | -      | 580uA | -     |
| Frame shutdown current  | -      | 132uA | -     |
| Frame charging current  | 1.5mA  | -     | 225mA |
| Charging cradle current | -      | -     | 400mA |
| Bluetooth radio power   | -20dBm | -     | 8dBm  |
| Bluetooth sensitivity   | -95dBm | -     | -     |

### Maximum ratings

|                             | Min   | Typ  | Max  |
|:----------------------------|:-----:|:----:|:----:|
| Frame charging voltage      | -0.3V | 5.1V | 6.4V |
| Charging cradle USB voltage | -0.3V | 5.1V | 7V   |
| Operating temperature       | 0°C   | -    | 45°C |
| Storage temperature         | -20°C | -    | 60°C |

---

## Safety & limitation of liability

### Safety

Brilliant Labs' devices can obscure your vision and should not be used while driving or operating dangerous equipment. Additionally long periods of use may cause eye strain, headaches and motion sickness. Brilliant Labs' devices can also display bright flashing images so may not be suitable for those who are susceptible to light sensitivity.

### Critical applications

Brilliant Labs' devices are intended for consumer and R&D applications. It is not verified for use where performance and accuracy would be critical to human health, safety or mission critical use.

### Lithium batteries

Lithium batteries can be dangerous if mishandled. Do not expose Brilliant Labs' devices to excess temperatures, fire or liquids. Do not try to remove the battery as the terminals can become shorted and result in the battery overheating or catching fire. Once the product reaches the end of it's life, dispose it safely according to your local regulations, such as e-waste collection points where any volatile components can be properly contained and handled.

### Limitation of liability

Brilliant Labs provides technical data, including design resources, examples, applications, design advice, tools, safety information and other resources "as is" and disclaims all warranties, express and implied, including without limitation any implied warranties or merchantability, fitness for a particular purpose or non-infringement of third party intellectual property rights. 

These resources are intended for skilled developers. You are solely responsible for selecting the appropriate products for your application, designing, validating and testing your application, and ensuring your application meets applicable standards, and other safety, security, regulatory or other requirements.

Brilliant Labs reserves the right to change the circuitry and specifications without notice at any time. The parametric values quoted in this manual are provided for guidance only.

The resources and products are provided subject to our [terms and conditions](https://brilliant.xyz/pages/terms-conditions).
