# InkHUD2 — How To Use

User guide for InkHUD2 on T-Echo Plus.

---

## Buttons

T-Echo Plus has two buttons:

| Button | Short Press | Long Press |
|--------|-------------|------------|
| **User Button** (side) | Switch modules / Select in menu | Open menu / Back |
| **Touch Button** (capacitive) | Turn off backlight | Turn on backlight (latch) |

---

## Navigation

### Main Screen

After boot, **Node List** is displayed — list of nodes in the network.

**Switching between modules:**
- Short press User Button → next module
- Order: Node List → Messages → Map → Node List...

### Menu

**Open menu:** Long press User Button (from any module)

**Menu navigation:**
- Short press = select / toggle value
- Long press = back / exit

**Menu structure:**
```
├── GPS (toggle)
├── Ping (action)
├── Alerts (submenu)
│   ├── < Back
│   ├── [Channel 0] (toggle)
│   ├── [Channel 1] (toggle)
│   └── DM (toggle)
├── Screen (submenu)
│   ├── < Back
│   ├── Backlight (toggle)
│   └── Rotation (0°/90°/180°/270°)
├── System (submenu)
│   ├── < Back
│   ├── Hide PIN (toggle)
│   ├── Backup (action)
│   └── Shut Down (action)
└── Exit
```

---

## Modules

### Node List

List of Meshtastic network nodes.

**Information for each node:**
- Name (short name)
- Last contact time
- Distance (if GPS available)
- Connection indicator: ● Direct, ◐ 1 hop, ○ 2+ hops

**Sorting:** By last message time (newest first)

### Messages

View messages by channel.

**Switch channels:** Long press User Button (when not in menu)

**Tabs:**
- DM — direct messages
- Channel 0, 1, 2... — Meshtastic channels

**Display modes:**
- **List View** — list of recent messages
- **Chat View** — group chat (for channels)

### Map

Node position map.

**Displayed:**
- Own position (crosshair at center)
- Nodes with known positions
- Scale bar (auto-scaling)

**View toggle:** Long press → switch between "All nodes" / "Favorites only"

---

## Features

### Hide PIN

Hides PIN code on Bluetooth pairing screen.

**Enable:** Menu → System → Hide PIN → On

Instead of `123 456` it will display `*** ***`.

**When useful:**
- Pairing in public places
- When using fixed PIN

### Backup

Creates "golden" backup of settings.

**Create:** Menu → System → Backup

**Files:**
- `/backups/user_backup.proto` — manual backup
- `/backups/auto_backup.proto` — automatic backup

**Auto-recovery:** On boot, if main configs are corrupted, system attempts to restore from backup.

### Shut Down

Proper device shutdown.

**Execute:** Menu → System → Shut Down

**What happens:**
1. Settings and nodeDB saved
2. Auto-backup created
3. Shutdown screen displayed (logo + node name)
4. Power off

**Important:** Use Shut Down instead of disconnecting power to protect data.

### Ping

Send your position to the network.

**Execute:** Menu → Ping

Sends position broadcast to all mesh nodes.

### Alerts

Configure notifications per channel.

**Open:** Menu → Alerts

You can enable/disable notifications for each channel separately.

---

## Pairing Screen

On first Bluetooth connection, pairing screen is displayed:

```
┌─────────────────────┐
│    [BT Logo]        │
│                     │
│  Enter this code    │
│     123 456         │
│                     │
│     NodeName        │
└─────────────────────┘
```

**With Hide PIN enabled:**
```
│     *** ***         │
```

---

## Backlight

**Peek (momentary):** Touch the Touch Button
**Latch (persistent):** Hold Touch Button for 5 sec
**Turn off:** Short touch of Touch Button (after latch)

Can also be controlled via Menu → Screen → Backlight.

---

## Rotation

Rotate screen by 0°, 90°, 180°, or 270°.

**Change:** Menu → Screen → Rotation

Useful if device is mounted in non-standard orientation.

---

## Troubleshooting

### Screen flickers / ghosting

E-ink displays can accumulate "ghost" images. Solution:
- Wait — system automatically does FULL refresh during extended idle
- Reboot the device

### Node doesn't appear on map

Check current view mode — long press toggles between "All nodes" and "Favorites only". Also verify the node has a valid GPS position.

### Messages not displaying

Check:
1. Channel is enabled in Alerts
2. Device is within mesh range
3. Encryption keys match

### Device won't turn on after flashing

Try:
1. Connect USB (device may be in deep sleep)
2. Hold Reset for 10 seconds
3. Double-tap Reset to enter bootloader and reflash

---

## Tips

1. **Battery saving:** Use Shut Down instead of waiting for discharge
2. **Backup before experiments:** Menu → System → Backup
3. **GPS indoors:** Disable GPS to save power (Menu → GPS)
4. **Quick Ping:** Convenient for testing connectivity with other nodes
