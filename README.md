### InkHUD2 — Completely Rewritten E-Ink UI

New graphics architecture designed specifically for e-ink displays on Meshtastic devices:

- Modular architecture
- Unified CJK font with Japanese (Chinese or Korean), and Cyrillic support
- Optimized screen refresh
- Ghosting protection
- No GFX inheritance hell
- PIN hide feature
- Automatic node settings backup
- GPS position with compass

### Fully Supported Hardware:

- LilyGo T-Echo Plus (nRF52840 + GDEY0154D67 e-ink)
- Heltec Vision Master E290 (ESP32-S3 + DEPG0290BNS800 2.9" e-ink)

### User guide for InkHUD2 on T-Echo Plus: 

- Read `HOWTO.md`

### Implementation Guide: 

- Read `PATCHES.md` and `CJK_Unified_Font_Implementation`

### Release Notes: 

- Read `RELEASE_NOTES.md`

### Merge branch: 

- Japanese/Latin/Cyrillic font included by default (just replace it with Chinese/Korean one if needed): [https://github.com/kuroanji/firmware/tree/InkHUD2](https://github.com/kuroanji/firmware/tree/InkHUD2)
- Instructions for adding the `hide_pin` field to Meshtastic protobufs: `HIDE_PIN_PROTOBUF.md`
