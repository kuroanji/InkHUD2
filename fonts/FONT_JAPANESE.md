# Japanese Font (UnifiedFont18px)

## Overview

Full Japanese language support with Cyrillic and Latin characters.

## Statistics

| Metric | Value |
|--------|-------|
| **Total Glyphs** | 2932 |
| **File Size** | ~120 KB |
| **Cell Size** | 18×18 px |

## Character Coverage

| Category | Unicode Range | Count |
|----------|---------------|-------|
| ASCII | U+0020–U+007E | 95 |
| Latin-1 Supplement | U+00A0–U+00FF (subset) | 11 |
| Cyrillic | U+0400–U+04FF (Russian + Ukrainian) | 74 |
| Symbols | Various | 144 |
| CJK Punctuation | U+3000–U+303F | 64 |
| Hiragana | U+3040–U+309F | 96 |
| Katakana | U+30A0–U+30FF | 96 |
| Fullwidth Forms | U+FF00–U+FFEF | 169 |
| **Kanji (Joyo)** | Various | **2138** |

## Kanji Details

Complete Joyo Kanji (常用漢字) set — 2136 characters officially designated for everyday use in Japan, plus 2 additional common variants.

**Education levels covered:**
- Grade 1: 80 kanji
- Grade 2: 160 kanji
- Grade 3: 200 kanji
- Grade 4: 202 kanji
- Grade 5: 193 kanji
- Grade 6: 191 kanji
- Secondary: 1110 kanji

## Source Fonts

| Script | Font | Style | Render Size |
|--------|------|-------|-------------|
| Latin/Cyrillic | JetBrains Mono NL | Light | 48px |
| Japanese | Noto Sans JP | Regular | 36px |

## Special Handling

### Punctuation Positioning

Japanese punctuation rendered at baseline (not centered):
- `、` (U+3001) — Ideographic comma
- `。` (U+3002) — Ideographic full stop
- `…` (U+2026) — Horizontal ellipsis
- `‥` (U+2025) — Two dot leader
- `，` (U+FF0C) — Fullwidth comma
- `．` (U+FF0E) — Fullwidth full stop

### Proportional Spacing

Latin characters use per-glyph xAdvance for readability:
- Narrow: `.` `,` `'` `|` `!` (40-45% of cell)
- Medium: `()` `[]` `-` `/` (50-55% of cell)
- Wide: digits, letters (55-65% of cell)
- Full width: CJK characters (100% of cell)

## Usage

```cpp
#include "graphics/niche/Fonts/CJK/UnifiedFont18px.h"

// Initialize InkHUD2 with Japanese font
hud.init(adapter, &NicheGraphics::UnifiedFont18px);
```

## Generation

```bash
cd font-generator
python3 generate_font_japanese.py
```

**Output:** `JapaneseFont18px.h` (rename to `UnifiedFont18px.h` for use)

## Limitations

- No Traditional Chinese characters (use Chinese font)
- Limited Korean (basic Jamo only, no Hangul syllables)
- No emoji support
