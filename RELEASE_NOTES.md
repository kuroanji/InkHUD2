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

### 3. Auto-Backup System
- Automatic settings backup
- Recovery from corrupted configs
- Manual "golden" backup: Menu → System → Backup


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
- LilyGo T-Echo Plus (nRF52840 + GDEY0154D67 e-ink)

Based on:
- Meshtastic Firmware 2.7.20

## What's Next

- Additional device support (Elecrow ThinkNode M1, LilyGo T3 S3 E-Paper, LilyGo T-Echo, Heltec MeshPocket, Heltec Vision Master E213, Heltec Vision Master E290, Heltec Wireless Paper)
- BHI260AP PDR Integration (T-Echo Plus has BHI260AP IMU which supports Pedestrian Dead Reckoning (PDR) with GPS fusion)

## Credits

InkHUD2 is built on the excellent work of the Meshtastic community. Special thanks to:
- Meshtastic firmware developers
- NicheGraphics e-ink driver authors
- Noto Fonts and JetBrains Mono projects
