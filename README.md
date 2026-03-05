# Custom Multi-Purpose Macropad (jzspad)

A multi-purpose macropad featuring 9 customizable LED-backlit keys, 1 rotary encoder, and an OLED display. Powered by the Seeed Studio XIAO RP2040, The keys change depending on the program, but for now they are copy, paste, undo, mute, cam off, close tab, play / pause, screenshot, and most important- show Desktop :)

![Macropad Render](assets/[schematic.jpg])

## ✨ Features
* **Brain:** Seeed Studio XIAO RP2040
* **Inputs:** 3x3 Key Matrix (9 Keys) + 1 Rotary Encoder (Volume/Scroll)
* **Visuals:** 128x32 I2C OLED Display for real-time dynamic status updates
* **Lighting:** 13 WS2812B RGB LEDs (capped at 50% brightness for USB power safety)
* **Firmware:** Event-driven KMK framework (CircuitPython) with zero-blocking UI hooks

---

## 🛠️ Hardware & PCB Design
The PCB was designed using KiCad. It uses a highly efficient matrix routing to save pins on the RP2040, ensuring all peripherals (OLED, LEDs, Encoder, Matrix) fit perfectly within the 11 available GPIO pins.

![PCB Schematic](images/[TERI_SCHEMATIC_KI_PHOTO.png])
![PCB 3D View](images/[TERE_KICAD_3D_VIEW_KI_PHOTO.png])

* **Col Pins:** D0, D1, D2
* **Row Pins:** D10, D9, D8
* **I2C (OLED):** D4 (SDA), D5 (SCL)
* **Encoder:** D6 (A), D3 (B)
* **LED (Din):** D7

---

## 📦 Mechanical Design (3D Case)
The custom enclosure was modeled in **Onshape**. It features snap-fit or screw-mounted standoffs designed perfectly for the custom PCB layout and keycaps.

![3D Case View](images/[TERE_ONSHAPE_CASE_KI_PHOTO.png])

> *Note for Reviewers: The original CAD source files (.STEP) are included in the `/Mechanical` folder. The Onshape public link can be provided upon request for full design history.*

---

## 💻 Firmware & Deployment
The firmware is written in Python using the **KMK Framework**. It features a custom `AdvancedUI` module that updates the OLED screen dynamically based on key presses (e.g., displaying "MIC MUTED" or a dynamic Volume Bar) without blocking the matrix scanning loop.

### How to Flash:
1. Double-tap the `Boot` button on the XIAO RP2040 to mount it as a drive.
2. Drag and drop the CircuitPython `.uf2` file.
3. Copy the `kmk` framework folder and the required `lib` files (neopixel, adafruit_displayio_ssd1306) to the `CIRCUITPY` drive.
4. Copy the `code.py` from this repository's `/Firmware` folder into the drive. The pad will reboot and work instantly.

---

## 📄 License
This project is open-source and available under the **MIT License**.
