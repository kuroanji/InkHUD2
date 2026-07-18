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
- **NodeDatabase backup** — automatic backup of nodes.proto on shutdown/reboot
- **Auto-recovery** — if nodes.proto is empty on boot, restores from `/backups/nodes_backup.proto`

### 4. HeltecVME290 E-Ink Driver

Custom hybrid driver for Heltec Vision Master E290:
- **OTP LUT** from controller memory (vs custom LUT in firmware)
- **Auto temperature adaptation** for optimal waveform selection
- **Fixed ghosting** that occurred with DEPG0290BNS800 driver
- **Buffer offset** preserved for panel compatibility

Technical details: `src/graphics/niche/InkHUD2/docs/DISPLAY_DRIVER_E290.md`

### 5. Minimal PCF8563 RTC Driver

Custom lightweight RTC driver replacing SensorLib dependency:
- **Header-only** — `src/gps/PCF8563_Minimal.h` (~2KB vs SensorLib ~250KB)
- **Same functionality** — read/set time, VL bit detection for clock validity
- **Conditional compilation** — PCF8563 uses minimal driver, other RTC chips (PCF85063, RV3028, RX8130CE) still use SensorLib

Affected devices:
- **T-Echo** — saves ~130KB flash
- **T-Echo Plus** — saves ~130KB flash

RTC Time Quality Hierarchy (in priority order):
1. GPS fix — most accurate
2. NTP/Phone app — network synchronized
3. Mesh time — from other nodes
4. RTC hardware — local backup

### 6. My Position View

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
- **Elecrow ThinkNode M1** (nRF52840 + GDEY0154D67 1.54" e-ink, two physical buttons)

Also built from this tree (not an InkHUD UI target):
- **Seeed SenseCAP T1000-E** (nRF52840, screenless tracker — backup system + i2c boot-loop rescue)

Based on:
- Meshtastic Firmware **2.8.0** (see `version.properties`)

> ⚠️ **Heltec Wireless Paper needs a one-line workaround to build** (toolchain packaging
> bug, not an InkHUD2 issue — the plain upstream `heltec-wireless-paper` env fails the
> same way).
>
> `framework-arduinoespressif32-libs` ships the esp32s3 slice **inconsistently**: the
> archive `esp32s3/lib/libespressif__network_provisioning.a` is present, but its headers
> `esp32s3/include/espressif__network_provisioning/` are **not** — while esp32 / s2 / c3 /
> c6 have both. The Arduino core's `NetworkEvents.h` includes
> `network_provisioning/network_config.h`, so any esp32s3 board that compiles the
> Network/WiFi libraries fails to build.
>
> **Workaround** (headers are portable; same package, same version):
> ```bash
> L=~/.platformio/packages/framework-arduinoespressif32-libs
> cp -R "$L/esp32/include/espressif__network_provisioning" "$L/esp32s3/include/"
> ```
> Verified: the target builds cleanly afterwards. Note this lives in the PlatformIO
> package cache, so it must be reapplied if that package is reinstalled. A proper fix
> belongs upstream (in the libs packaging, or by pinning a platform/core version whose
> esp32s3 slice is complete).

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

### Elecrow ThinkNode M1 Notes

- **Same display as T-Echo** — GDEY0154D67 (200x200), so the layout needed no changes
- **No controllable backlight** — the light runs off the peripheral power rail and is on
  whenever the device is powered; `PIN_EINK_EN` is a hardware dimmer, not an on/off gate.
  The aux button is therefore used for scrolling instead.
- **Rotation 0** (unlike T-Echo's 3)
- **Slim build** — uses `nrf52_base`, not `nrf52840_base`: the board has no onboard
  environmental sensors, so skipping those drivers saves ~124 KB (94.5% → 78.9% flash)
- Bootloader volume is `ELECROWBOOT`

Button mapping for ThinkNode M1:

| Button | Short Press | Long Press |
|--------|-------------|------------|
| **Top** (circle, "Page Turn") | Select / Next module | Open menu / Back |
| **Bottom** (triangle, "Function") | Scroll down | Scroll to top |

Full port notes and gotchas: `docs/PORT_THINKNODE_M1.md`

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

- Additional device support (LilyGo T3 S3 E-Paper) — *Elecrow ThinkNode M1 is done, see above*
- Restore the **Heltec Wireless Paper** build (blocked upstream, not by InkHUD2 — see the
  note under Compatibility)
- BHI260AP PDR Integration (T-Echo Plus has BHI260AP IMU which supports Pedestrian Dead Reckoning (PDR) with GPS fusion)

## Credits

InkHUD2 is built on the excellent work of the Meshtastic community. Special thanks to:
- Meshtastic firmware developers
- NicheGraphics e-ink driver authors
- Noto Fonts and JetBrains Mono projects
