# InkHUD2 — How To Use

User guide for InkHUD2 on supported devices.

# TL;DR

Short press on:

- Menu → next
- Module screen → next module 

Long press on:

- Node list → open menu
- Messages → switch between channels
- Map → open map menu
- Menu → toggle/select
---

## Supported Devices

- **LilyGo T-Echo Plus** — nRF52840, 1.54" square e-ink, backlight
- **Heltec Vision Master E290** — ESP32-S3, 2.9" narrow e-ink, no backlight

---

## Buttons

### T-Echo Plus

| Button | Short Press | Long Press |
|--------|-------------|------------|
| **User Button** (side) | Switch modules / Select in menu | Open menu / Back |
| **Touch Button** (capacitive) | Turn off backlight | Turn on backlight (latch) |

### Heltec Vision Master E290

| Button | Short Press | Long Press |
|--------|-------------|------------|
| **User Button** | Switch modules / Select in menu | Open menu / Back |
| **PRG Button** (middle) | Next item in Node List | — |
| **Aux Button** | Scroll down (lists) | Scroll to top |

**Note:** E290 has no backlight. PRG button provides quick navigation in Node List without entering menu. Aux button scrolls text in messages.

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

**Navigation (E290 only):**
- PRG button (middle) — move to next node in list
- Useful for quickly browsing nodes without opening menu

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

**Navigation:**
- Short press = next option in settings
- Long press = open settings / back

**Settings menu:**
- My Position — shows your coordinates, altitude, timestamp, and compass
- Show all nodes — toggle between "Favorites only" / "All nodes with position"

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

### My Position

View your current GPS coordinates.

**Access:** Map module → Long press → My Position

**Display:**
- Latitude and longitude (DMS format)
- Altitude in meters
- Time since last GPS update
- Compass with heading (if ground track available)

**If no GPS fix:** Shows message "Waiting for GPS update..."

---

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

## Backlight (T-Echo Plus only)

**Peek (momentary):** Touch the Touch Button
**Latch (persistent):** Hold Touch Button for 5 sec
**Turn off:** Short touch of Touch Button (after latch)

Can also be controlled via Menu → Screen → Backlight.

**Note:** Heltec VM-E290 does not have a backlight.

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
