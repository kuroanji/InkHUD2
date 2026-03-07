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

### 2. NodeDB Save Throttle (`src/mesh/Default.h`, `src/mesh/NodeDB.cpp`)

Increased NodeDB save throttle from 1 minute to 10 minutes for flash wear protection.

```cpp
// Default.h
#define TEN_MINUTES_MS 10 * 60 * 1000

// NodeDB.cpp:1898
if (!Throttle::isWithinTimespanMs(lastNodeDbSave, TEN_MINUTES_MS)) {
    saveToDisk(SEGMENT_NODEDATABASE);
    lastNodeDbSave = millis();
}
```

**Rationale:** See `docs/FLASH_WEAR_PROTECTION.md`

**Files:**
- `src/mesh/Default.h` — added `TEN_MINUTES_MS` constant
- `src/mesh/NodeDB.cpp` — changed throttle from `ONE_MINUTE_MS` to `TEN_MINUTES_MS`

---

### 3. Backup System (`src/mesh/NodeDB.h`, `src/mesh/NodeDB.cpp`, `src/Power.cpp`)

Added backup system:

```cpp
// NodeDB.h
static constexpr const char *autoBackupFileName = "/backups/auto_backup.proto";
static constexpr const char *autoBackupPrevFileName = "/backups/auto_backup_prev.proto";
static constexpr const char *userBackupFileName = "/backups/user_backup.proto";

bool backupPreferences(meshtastic_AdminMessage_BackupLocation location);
bool backupUserPreferences();  // Manual "golden" backup
bool restorePreferences(meshtastic_AdminMessage_BackupLocation location, int restoreWhat);
```

**Functionality:**
- `backupPreferences(FLASH)` — automatic backup with rotation
- `backupUserPreferences()` — manual "golden" backup
- `restorePreferences()` — restore from backup chain
- Auto-recovery on boot if main files are corrupted
- Auto backup on any shutdown (Power.cpp integration)

**Files:**
- `src/mesh/NodeDB.h` — method declarations
- `src/mesh/NodeDB.cpp` — backup/restore implementation
- `src/Power.cpp` — auto backup on shutdown (added `backupPreferences(FLASH)` call)

---

## E-Ink Drivers

### HeltecVME290 (`src/graphics/niche/Drivers/EInk/HeltecVME290.h/cpp`)

Custom hybrid driver for Heltec Vision Master E290 panel. Fixes ghosting by combining two approaches:

**From ZJY128296_029EAAMFGN (OTP-based):**
- OTP LUT from controller memory (not custom in firmware)
- Internal temperature sensor (0x80) for automatic waveform selection
- Border waveform 0x05 (follow LUT1, drive white)
- Update sequence 0xFF (differential from OTP)

**From DEPG0290BNS800:**
- Buffer offset: 1 byte (panel wiring quirk)

**NOT used from ZJY:**
- configScanning override (not needed for this panel)

**Result:** No ghosting, faster refresh (~300ms), auto temperature adaptation.

See: `src/graphics/niche/InkHUD2/docs/DISPLAY_DRIVER_E290.md`

---

## InkHUD2 Files

### New Directories

```
src/graphics/niche/InkHUD2/
├── Core/
│   ├── Buffer.h             — Frame buffer management
│   ├── Font.h/cpp           — CJKFont wrapper
│   ├── Layout.h             — Dynamic layout calculation
│   ├── RenderContext.h/cpp  — Drawing primitives
│   ├── Logo.h/cpp           — Meshtastic logo rendering
│   ├── Settings.h           — Persistent settings (hide_pin, etc.)
│   └── BluetoothState.h/cpp — BT connection state
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
│   └── MapModule.h/cpp
├── Pipe/
│   ├── Pipe.h/cpp           — Module lifecycle
│   └── Events.h/cpp         — Meshtastic event bridge + shutdown handler
├── Text/
│   └── TextRenderer.cpp     — Text with wrapping
├── UI/
│   ├── MenuItem.h           — Menu item struct
│   ├── MenuList.h/cpp       — Menu rendering
│   ├── StatusBar.h/cpp      — Header with icon and title
│   ├── Footer.h/cpp         — Footer with hint text
│   ├── ContentArea.h        — Content area calculation
│   └── Compass.h/cpp        — Compass with heading arrow
├── Views/
│   ├── ListView.h/cpp       — Message list view
│   └── ChatView.h/cpp       — Chat-style view
├── InkHUD2.h/cpp            — Main singleton
└── Setup.h/cpp              — Common initialization (modules, menu, buttons)
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

Simplified to ~100 lines (was ~500). Device-specific only:
- E-ink driver initialization
- `InkHUD2::Config` with device pins and settings
- Single call to `InkHUD2::setup(driver, config)`

Common code moved to `Setup.h/cpp`:
- All modules creation
- Menu configuration (items, submenus, callbacks)
- Button handlers
- Event system setup

### `variants/esp32s3/heltec_vision_master_e290/nicheGraphics.h`

Support for both InkHUD (original) and InkHUD2:
- Uses `HeltecVME290` driver (fixes ghosting vs original `DEPG0290BNS800`)
- Passes reset pin to driver for deep sleep support
- Aux button used for scrolling (no backlight on this device)
- Default rotation: 270° (LoRa antenna up)

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
| `protobufs/meshtastic/config.proto` | Added `hide_pin` field to BluetoothConfig |
| `src/mesh/generated/meshtastic/config.pb.h` | Regenerated with `hide_pin` |
| `src/mesh/Default.h` | Added `TEN_MINUTES_MS` constant |
| `src/mesh/NodeDB.h` | Added backup file constants and methods |
| `src/mesh/NodeDB.cpp` | Implemented backup/restore logic + 10min throttle |
| `src/Power.cpp` | Added auto backup on shutdown |
| `src/modules/AdminModule.cpp` | Fixed incomplete backup removal code |
| `src/motion/AccelerometerThread.h` | Added `#ifdef HAS_*_LIB` guards for optional sensors |
| `variants/nrf52840/t-echo-plus/nicheGraphics.h` | Simplified to device-specific config only |
| `variants/nrf52840/t-echo-plus/platformio.ini` | Added `t-echo-plus-inkhud2` env |
| `variants/esp32s3/heltec_vision_master_e290/nicheGraphics.h` | Added InkHUD2 support, switched to HeltecVME290 driver |
| `variants/esp32s3/heltec_vision_master_e290/platformio.ini` | Added `heltec-vision-master-e290-inkhud2` env |
| `src/graphics/niche/Drivers/EInk/HeltecVME290.h` | New hybrid driver for VM-E290 |
| `src/graphics/niche/Drivers/EInk/HeltecVME290.cpp` | Driver implementation (OTP LUT + offset) |

### AccelerometerThread.h Details

Added conditional compilation guards for sensor libraries that may not be present:

```cpp
#ifdef HAS_MPU6050_LIB
case ScanI2C::DeviceType::MPU6050:
    sensor = new MPU6050Sensor(device);
    break;
#endif
#ifdef HAS_LIS3DH_LIB
case ScanI2C::DeviceType::LIS3DH:
    sensor = new LIS3DHSensor(device);
    break;
#endif
// ... similar for LSM6DS3, ICM20948, BMM150, BMX160
```

This allows builds without motion sensor libraries (saves ~17KB flash).

### AdminModule.cpp Details

Fixed incomplete backup removal code that referenced undefined `backupFileName`:

```cpp
// Before (broken):
FSCom.remove(backupFileName);

// After (fixed):
FSCom.remove(autoBackupFileName);
FSCom.remove(autoBackupPrevFileName);
FSCom.remove(userBackupFileName);
```

---

## Files Added

All files under:
- `src/graphics/niche/InkHUD2/` (entire directory)
- `src/graphics/niche/InkHUD2/Setup.h` — device config struct
- `src/graphics/niche/InkHUD2/Setup.cpp` — common initialization logic
- `src/graphics/niche/InkHUD2/docs/` — driver documentation
  - `DISPLAY_DRIVER_E290.md` — HeltecVME290 driver documentation
  - `HOWTO_ADD_EINK_DRIVER.md` — guide for adding new e-ink drivers
- `src/graphics/niche/Drivers/EInk/HeltecVME290.h/cpp` — hybrid driver
- `src/graphics/niche/Fonts/CJK/UnifiedFont18px.h`
- `src/graphics/niche/Fonts/CJK/CJKFont.h`
