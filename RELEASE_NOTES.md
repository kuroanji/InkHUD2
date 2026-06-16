### InkHUD2 — Completely Rewritten E-Ink UI

## New Features

### 1. Unified CJK Font System

Three interchangeable fonts, one active at compile time:

| Font | Glyphs | Size | Languages |
|------|--------|------|-----------|
| **Japanese** (default) | 2932 | 120 KB | ASCII, Cyrillic, Hiragana, Katakana, 2138 Joyo Kanji |
| **Chinese** | 3810 | 156 KB | ASCII, 3500 Hanzi (GB2312 Level 1) |
| **Korean** | 2749 | 113 KB | ASCII, 2343 Hangul syllables (KS X 1001) |

- Cell size: 18×18 pixels
- Proportional Latin, monospace CJK
- Sources: JetBrains Mono NL Light + Noto Sans family
- See [docs/fonts/](docs/fonts/) for detailed character coverage

### 2. Hide PIN
- Hides PIN code on Bluetooth pairing screen
- Setting: Menu → System → Hide PIN
- Stored in `config.bluetooth.hide_pin`

### 3. Backup & Restore System
- Automatic settings backup on shutdown
- Backup rotation (auto_backup → auto_backup_prev)
- Recovery from corrupted configs on boot
- Manual "golden" backup: Menu → System → Backup
- Restore from backup: Menu → System → Restore

### 4. HeltecVME290 E-Ink Driver

Custom hybrid driver for Heltec Vision Master E290:
- **OTP LUT** from controller memory (vs custom LUT in firmware)
- **Auto temperature adaptation** for optimal waveform selection
- **Fixed ghosting** that occurred with DEPG0290BNS800 driver
- **Buffer offset** preserved for panel compatibility

Technical details: `src/graphics/niche/InkHUD2/docs/DISPLAY_DRIVER_E290.md`

### 5. My Position View

View your GPS position with compass:
- Coordinates in degrees/minutes/seconds format
- Altitude in meters
- Time since last GPS update
- Compass with heading arrow (when ground track available)

Access: Map → Long press → My Position

---

## Architecture

```
Meshtastic Firmware
        │
   ┌────▼────┐
   │ InkHUD2 │  ← Singleton
   └────┬────┘
        │
   ┌────▼────┐
   │  Pipe   │  ← Event routing
   └────┬────┘
        │
   ┌────▼─────────┐
   │RenderContext │  ← Drawing API
   └────┬─────────┘
        │
   ┌────▼────┐     ┌────────┐
   │ Buffer  │────►│ Driver │
   └─────────┘     └────────┘
```
## Compatibility

Supported Hardware:
- **LilyGo T-Echo** (nRF52840 + GDEY0154D67 1.54" e-ink, capacitive touch)
- **LilyGo T-Echo Plus** (nRF52840 + GDEY0154D67 1.54" e-ink)
- **Heltec Vision Master E290** (ESP32-S3 + DEPG0290BNS800 2.9" e-ink)
- **Heltec Vision Master E213** (ESP32-S3 + 2.13" e-ink, 250x122, two buttons)
- **Heltec Wireless Paper** (ESP32-S3 + 2.13" e-ink, 250x122, no GPS)
- **Heltec Mesh Pocket Qi2** (nRF52840 + LCMEN2R13ECC1 2.13" e-ink, 122x250, single button)

Based on:
- Meshtastic Firmware 2.7.25

### LilyGo T-Echo Notes

- **Same display as T-Echo Plus** — GDEY0154D67 (200x200)
- **Minimal RTC driver** — uses PCF8563_Minimal.h (saves ~130KB vs SensorLib)
- **Capacitive touch button** — controls backlight (peek/latch)
- **5 second latch** — limited by T-Echo's capacitive touch IC

Button mapping for T-Echo:

| Button | Short Press | Long Press |
|--------|-------------|------------|
| **User Button** (side) | Select / Next module | Open menu / Back |
| **Touch Button** (capacitive) | Turn off backlight | Turn on backlight (latch) |

### Heltec VM-E290 Notes

- **Narrow screen (128x296)** — UI automatically adapts with smaller fonts
- **No backlight** — Aux button used for scrolling instead
- **Custom driver** — `HeltecVME290` driver built to fix ghosting (see docs)

Button mapping for VM-E290:

| Button | Short Press | Long Press |
|--------|-------------|------------|
| **User Button** | Select / Next module | Open menu / Back |
| **Aux Button** | Scroll down | Scroll to top |

### Heltec Vision Master E213 Notes

- **Screen: 250x122** — same 2.13" e-ink as Wireless Paper
- **Runtime display detection** — auto-detects LCMEN213EFC1 (V1) or E0213A367 (V1.1)
- **Two buttons** — User + Aux (GPIO 21) for scrolling
- **GPS support** — full map features available

Button mapping for VM-E213:

| Button | Short Press | Long Press |
|--------|-------------|------------|
| **User Button** | Select / Next module | Open menu / Back |
| **Aux Button** | Scroll down | Scroll to top |

### Heltec Wireless Paper Notes

- **Screen: 250x122** — 2.13" e-ink, landscape aspect ratio similar to VM-E290
- **Runtime display detection** — auto-detects LCMEN213EFC1 (V1.1) or E0213A367 (V1.1.1, V1.2)
- **Single button only** — no Aux button, no backlight
- **No GPS** — map features require position data from other mesh nodes
- **ADC calibration** — corrected ADC_MULTIPLIER (2.68) for accurate battery readings

Button mapping for Wireless Paper:

| Button | Short Press | Long Press |
|--------|-------------|------------|
| **User Button** | Select / Next module | Open menu / Back |

### Heltec Mesh Pocket Qi2 Notes

- **Screen: 122x250** — 2.13" e-ink (LCMEN2R13ECC1, SSD1680 controller)
- **Landscape orientation** — rotation = 3 (250x122 logical)
- **Single button** — no Aux button, no backlight
- **Ghosting mitigation** — idle maintenance FULL refresh after 60s of inactivity
- **Hardware limitation** — display has poor OTP waveform, ghosting is inherent to this panel

Button mapping for Mesh Pocket Qi2:

| Button | Short Press | Long Press |
|--------|-------------|------------|
| **User Button** | Select / Next module | Open menu / Back |

## What's Next

- Additional device support (Elecrow ThinkNode M1, LilyGo T3 S3 E-Paper)
- BHI260AP PDR Integration (T-Echo Plus has BHI260AP IMU which supports Pedestrian Dead Reckoning (PDR) with GPS fusion)

## Credits

InkHUD2 is built on the excellent work of the Meshtastic community. Special thanks to:
- Meshtastic firmware developers
- NicheGraphics e-ink driver authors
- Noto Fonts and JetBrains Mono projects
