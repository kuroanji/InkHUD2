# CJK Font Implementation

## Overview

InkHUD2 uses a unified bitmap font system supporting multiple languages. All characters are rendered through a single CJKFont structure with automatic codepoint detection.

## Available Fonts

| Font | Languages | Glyphs | Size | Documentation |
|------|-----------|--------|------|---------------|
| **UnifiedFont18px** | Japanese + Cyrillic + Latin | 2932 | 120 KB | [FONT_JAPANESE.md](fonts/FONT_JAPANESE.md) |
| **ChineseFont18px** | Chinese + Latin | 3810 | 156 KB | [FONT_CHINESE.md](fonts/FONT_CHINESE.md) |
| **KoreanFont18px** | Korean + Latin | 2749 | 113 KB | [FONT_KOREAN.md](fonts/FONT_KOREAN.md) |

Default: **UnifiedFont18px** (Japanese)

## Architecture

### Font Structure

```cpp
struct CJKFont {
    const uint8_t *bitmap;      // Packed 1-bit glyph data
    const CJKGlyph *glyphs;     // Glyph lookup table (sorted by codepoint)
    uint16_t glyphCount;        // Number of glyphs
    uint8_t width;              // Cell width (18px)
    uint8_t height;             // Cell height (18px)
    uint8_t xAdvance;           // Default advance width
    int8_t yOffset;             // Baseline offset (-18)
};

struct CJKGlyph {
    uint32_t codepoint;         // Unicode codepoint
    uint32_t bitmapOffset;      // Offset into bitmap array
    uint8_t xAdvance;           // Per-glyph advance width
};
```

### Glyph Lookup

Binary search by codepoint (O(log n)):

```cpp
const CJKGlyph* findGlyph(const CJKFont* font, uint32_t codepoint) {
    int low = 0, high = font->glyphCount - 1;
    while (low <= high) {
        int mid = (low + high) / 2;
        uint32_t midCp = font->glyphs[mid].codepoint;
        if (midCp == codepoint) return &font->glyphs[mid];
        if (midCp < codepoint) low = mid + 1;
        else high = mid - 1;
    }
    return nullptr;  // Glyph not found
}
```

### UTF-8 Decoding

Standard UTF-8 decoding in RenderContext:

```cpp
uint32_t decodeUTF8(const char*& str) {
    uint8_t c = *str++;
    if (c < 0x80) return c;                    // ASCII
    if ((c & 0xE0) == 0xC0) {                  // 2-byte
        return ((c & 0x1F) << 6) | (*str++ & 0x3F);
    }
    if ((c & 0xF0) == 0xE0) {                  // 3-byte
        uint32_t cp = (c & 0x0F) << 12;
        cp |= (*str++ & 0x3F) << 6;
        cp |= (*str++ & 0x3F);
        return cp;
    }
    // 4-byte sequences not commonly needed for CJK
    return 0xFFFD;  // Replacement character
}
```

## Rendering Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ UTF-8 Text  │────►│ Decode UTF-8 │────►│ Find Glyph  │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
┌─────────────┐     ┌──────────────┐     ┌──────▼──────┐
│   Buffer    │◄────│ Draw Pixels  │◄────│ Read Bitmap │
└─────────────┘     └──────────────┘     └─────────────┘
```

## Font Generation

### Prerequisites

```bash
pip install pillow
```

### Source Fonts Required

| Script | Font | Download |
|--------|------|----------|
| Latin/Cyrillic | JetBrains Mono NL Light | [jetbrains.com/mono](https://www.jetbrains.com/mono/) |
| Japanese | Noto Sans JP Regular | [Google Fonts](https://fonts.google.com/noto/specimen/Noto+Sans+JP) |
| Chinese | Noto Sans SC Regular | [Google Fonts](https://fonts.google.com/noto/specimen/Noto+Sans+SC) |
| Korean | Noto Sans KR Regular | [Google Fonts](https://fonts.google.com/noto/specimen/Noto+Sans+KR) |

### Generation Commands

```bash
cd font-generator

# Japanese (default)
python3 generate_font_japanese.py

# Chinese
python3 generate_font_chinese.py

# Korean
python3 generate_font_korean.py
```

### Output

Generated `.h` files contain:
- Bitmap data (1-bit packed, row-major, PROGMEM)
- Glyph table (codepoint, offset, xAdvance)
- CJKFont metadata struct

## Switching Fonts

### Compile-time

Edit `variants/.../nicheGraphics.h`:

```cpp
// Japanese (default)
#include "graphics/niche/Fonts/CJK/UnifiedFont18px.h"
hud.init(adapter, &NicheGraphics::UnifiedFont18px);

// Chinese
#include "graphics/niche/Fonts/CJK/ChineseFont18px.h"
hud.init(adapter, &NicheGraphics::ChineseFont18px);

// Korean
#include "graphics/niche/Fonts/CJK/KoreanFont18px.h"
hud.init(adapter, &NicheGraphics::KoreanFont18px);
```

### File Replacement

Or simply replace the font file:
```bash
cp font-generator/ChineseFont18px.h \
   src/graphics/niche/Fonts/CJK/UnifiedFont18px.h
```

## Technical Details

### Cell Size

All fonts use 18×18 pixel cells:
- Optimal for 200×200 e-ink displays
- ~11 characters per line
- Clear readability at arm's length

### Rendering Sizes

| Script | Render Size | Final Size | Notes |
|--------|-------------|------------|-------|
| Latin/Cyrillic | 48px | 18px | 2.67x downscale for smoothing |
| CJK | 36px | 18px | 2x downscale |

### Proportional vs Monospace

- **CJK characters**: Full cell width (18px xAdvance)
- **Latin characters**: Proportional (7-12px xAdvance)
- **Punctuation**: Narrow (4-8px xAdvance)

### Special Punctuation

Characters requiring baseline positioning (not centered):

```python
bottom_punct = {0x3001, 0x3002, 0x2026, 0x2025, 0xFF0C, 0xFF0E}
```

These are handled specially in the font generator to render at baseline instead of vertically centered.

## Memory Usage

| Font | Flash | RAM |
|------|-------|-----|
| Japanese | 120 KB | 0 (PROGMEM) |
| Chinese | 156 KB | 0 (PROGMEM) |
| Korean | 113 KB | 0 (PROGMEM) |

All bitmap data stored in PROGMEM (flash), no RAM allocation required.

## Troubleshooting

### Character shows as □ or missing

1. Check if codepoint is in font's character set
2. Verify font file is correctly included
3. Check UTF-8 encoding of source text

### Text alignment off

- Verify `yOffset` is `int8_t` (signed), not `uint8_t`
- Check padding compensation in alignment code

### Punctuation centered instead of baseline

- Ensure codepoint is in `bottom_punct` set in generator
- Regenerate font after adding new punctuation

## Files

```
src/graphics/niche/
├── Fonts/CJK/
│   ├── CJKFont.h           # Font interface
│   └── UnifiedFont18px.h   # Active font (Japanese by default)
└── InkHUD2/
    └── Core/
        ├── Font.h/cpp      # Font wrapper class
        └── RenderContext.cpp # Text rendering
```

## License

Font data: SIL Open Font License (Noto), Apache 2.0 (JetBrains Mono)
Code: GPL-3.0
