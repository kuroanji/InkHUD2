# Chinese Font (ChineseFont18px)

## Overview

Simplified Chinese language support with Latin characters.

## Statistics

| Metric | Value |
|--------|-------|
| **Total Glyphs** | 3810 |
| **File Size** | ~156 KB |
| **Cell Size** | 18×18 px |

## Character Coverage

| Category | Unicode Range | Count |
|----------|---------------|-------|
| ASCII | U+0020–U+007E | 95 |
| Symbols | Various | 45 |
| CJK Punctuation | U+3000–U+303F | 64 |
| Fullwidth Forms | U+FF00–U+FFEF | 94 |
| **Hanzi (Level 1)** | CJK Unified | **3500** |

## Hanzi Details

GB2312 Level 1 characters (一级字) — 3500 most frequently used Simplified Chinese characters.

**Coverage:**
- 99.7% of modern Chinese text
- All HSK 1-6 vocabulary
- Common names, places, technical terms

**Not included:**
- Level 2 characters (3000 less common)
- Traditional Chinese variants
- Rare/archaic characters

## Source Fonts

| Script | Font | Style | Render Size |
|--------|------|-------|-------------|
| Latin | JetBrains Mono NL | Light | 48px |
| Chinese | Noto Sans SC | Regular | 36px |

## Special Handling

### Punctuation Positioning

Chinese punctuation rendered at baseline:
- `、` (U+3001) — Ideographic comma
- `。` (U+3002) — Ideographic full stop
- `…` (U+2026) — Horizontal ellipsis
- `，` (U+FF0C) — Fullwidth comma
- `．` (U+FF0E) — Fullwidth full stop

## Usage

Replace the default font in `nicheGraphics.h`:

```cpp
#include "graphics/niche/Fonts/CJK/ChineseFont18px.h"

// Initialize with Chinese font
hud.init(adapter, &NicheGraphics::ChineseFont18px);
```

## Generation

```bash
cd font-generator
python3 generate_font_chinese.py
```

**Output:** `ChineseFont18px.h`

**Character list:** `common_hanzi.txt` (edit to customize)

## Limitations

- No Cyrillic support
- No Japanese Kana (Hiragana/Katakana)
- No Korean Hangul
- Simplified Chinese only (no Traditional)
