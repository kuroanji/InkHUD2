# InkHUD2 Patches & Modifications

Documentation of all changes relative to base Meshtastic firmware.

---

## Core Firmware Changes

### 1. Bluetooth Hide PIN (`protobufs/meshtastic/config.proto`)

Added field for PIN hiding:

```protobuf
message BluetoothConfig {
    // ... existing fields ...
    bool hide_pin = 4;  // NEW: Hide PIN on pairing screen
}
```

**Files:**
- `protobufs/meshtastic/config.proto` — field definition
- `src/mesh/generated/meshtastic/config.pb.h` — generated header

---

### 2. Backup System (`src/mesh/NodeDB.h`, `src/mesh/NodeDB.cpp`)

Added backup system:

```cpp
// NodeDB.h
static constexpr const char *autoBackupFileName = "/backups/auto_backup.proto";
static constexpr const char *autoBackupPrevFileName = "/backups/auto_backup_prev.proto";
static constexpr const char *userBackupFileName = "/backups/user_backup.proto";

bool backupPreferences(meshtastic_AdminMessage_BackupLocation location);
bool backupUserPreferences();  // Manual "golden" backup
```

**Functionality:**
- `backupPreferences(FLASH)` — automatic backup on shutdown
- `backupUserPreferences()` — manual "golden" backup
- Auto-recovery on boot if main files are corrupted

---

## InkHUD2 Files

### New Directories

```
src/graphics/niche/InkHUD2/
├── Core/
│   ├── Buffer.h/cpp         — Frame buffer management
│   ├── Font.h/cpp           — CJKFont wrapper
│   ├── Layout.h/cpp         — Dynamic layout calculation
│   ├── RenderContext.h/cpp  — Drawing primitives
│   ├── Settings.h           — Persistent settings (hide_pin, etc.)
│   └── BluetoothState.h     — BT connection state
├── Drivers/
│   └── EInkAdapter.h/cpp    — Adapter for e-ink driver
├── Fonts/
│   ├── UnifiedFont18px.h/cpp — Placeholder (not used)
├── Modules/
│   ├── Module.h             — Base module interface
│   ├── BatteryModule.h/cpp
│   ├── BootModule.h/cpp
│   ├── MenuModule.h/cpp
│   ├── MessageModule.h/cpp
│   ├── NodeListModule.h/cpp
│   ├── NotificationModule.h/cpp
│   └── MapModule.h/cpp
├── Pipe/
│   ├── Pipe.h/cpp           — Module lifecycle
│   └── Events.h/cpp         — Meshtastic event bridge
├── Text/
│   └── TextRenderer.cpp     — Text with wrapping
├── UI/
│   ├── MenuItem.h           — Menu item struct
│   └── MenuList.h/cpp       — Menu rendering
├── Views/
│   ├── ListView.h/cpp       — Message list view
│   └── ChatView.h/cpp       — Chat-style view
├── InkHUD2.h/cpp            — Main singleton
└── Events.h/cpp             — Event definitions
```

---

## CJK Font

### Location
```
src/graphics/niche/Fonts/CJK/
├── CJKFont.h                — Font interface
└── UnifiedFont18px.h        — Japanese + Cyrillic + Latin (2932 glyphs)
```

### Generation
Font generator: `/font-generator/`
- `generate_font_japanese.py` — Japanese + Cyrillic + Latin
- `generate_font_chinese.py` — Chinese + Latin
- `generate_font_korean.py` — Korean + Latin

---

## Variant Configuration

### `variants/nrf52840/t-echo-plus/nicheGraphics.h`

Completely rewritten for InkHUD2:
- InkHUD2 singleton initialization
- All modules creation
- Menu configuration (items, submenus, callbacks)
- Button configuration

## PlatformIO Configuration

### `platformio.ini`

Added environment for InkHUD2:

```ini
[env:t-echo-plus-inkhud2]
extends = nrf52840_base
board = t-echo
build_flags =
    ${nrf52840_base.build_flags}
    -DUSE_INKHUD2
    -DMESHTASTIC_INCLUDE_NICHE_GRAPHICS
    # ... other flags
```

---

## Files Modified (Summary)

| File | Change |
|------|--------|
| `protobufs/meshtastic/config.proto` | Added `hide_pin` field |
| `src/mesh/NodeDB.h` | Added backup methods |
| `src/mesh/NodeDB.cpp` | Implemented backup/restore |
| `src/mesh/generated/meshtastic/config.pb.h` | Regenerated with `hide_pin` |
| `variants/nrf52840/t-echo-plus/nicheGraphics.h` | InkHUD2 initialization |
| `platformio.ini` | Added `t-echo-plus-inkhud2` env |

---

## Files Added

All files under:
- `src/graphics/niche/InkHUD2/` (entire directory)
- `src/graphics/niche/Fonts/CJK/UnifiedFont18px.h`
- `docs/CJK_UNIFIED_Implementation.md`
