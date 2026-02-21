# Hide PIN — Protobuf Changes

Instructions for adding the `hide_pin` field to Meshtastic protobufs.

---

## config.proto

**File:** `protobufs/meshtastic/config.proto`

**Location:** Inside `message BluetoothConfig`, after `fixed_pin` field

**Find this code:**
```protobuf
message BluetoothConfig {
    enum PairingMode {
      RANDOM_PIN = 0;
      FIXED_PIN = 1;
      NO_PIN = 2;
    }

    bool enabled = 1;
    PairingMode mode = 2;
    uint32 fixed_pin = 3;
  }
```

**Change to:**
```protobuf
message BluetoothConfig {
    enum PairingMode {
      RANDOM_PIN = 0;
      FIXED_PIN = 1;
      NO_PIN = 2;
    }

    bool enabled = 1;
    PairingMode mode = 2;
    uint32 fixed_pin = 3;

    /*
     * Hide PIN code on the pairing screen (show *** *** instead)
     */
    bool hide_pin = 4;
  }
```

## Usage in Code

After adding the field, access it via:

```cpp
// Read
bool hidden = config.bluetooth.hide_pin;

// Write
config.bluetooth.hide_pin = true;
nodeDB->saveToDisk();
```

**Example in BootModule.cpp (pairing screen):**
```cpp
bool hidePin = config.bluetooth.hide_pin;

if (hidePin) {
    snprintf(pinStr, sizeof(pinStr), "*** ***");
} else {
    uint32_t first3 = pairingCode / 1000;
    uint32_t last3 = pairingCode % 1000;
    snprintf(pinStr, sizeof(pinStr), "%03lu %03lu",
             (unsigned long)first3, (unsigned long)last3);
}
```

---

## Notes

- Field number `4` is the next available in BluetoothConfig
- Default value is `false` (PIN visible)
- Setting persists in device config (survives reboot)
- No app changes required — field is ignored by older clients
