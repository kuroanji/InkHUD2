# Korean Font (KoreanFont18px)

## Overview

Korean language support with Latin characters.

## Statistics

| Metric | Value |
|--------|-------|
| **Total Glyphs** | 2749 |
| **File Size** | ~113 KB |
| **Cell Size** | 18×18 px |

## Character Coverage

| Category | Unicode Range | Count |
|----------|---------------|-------|
| ASCII | U+0020–U+007E | 95 |
| Symbols | Various | 46 |
| CJK Punctuation | U+3000–U+303F | 64 |
| Fullwidth Forms | U+FF00–U+FFEF | 94 |
| Hangul Jamo | U+3130–U+318F | 95 |
| **Hangul Syllables** | U+AC00–U+D7AF | **2343** |

## Hangul Details

KS X 1001 standard character set — 2343 pre-composed Hangul syllables covering common Korean text.

**Structure:**
- Korean uses 11,172 possible syllable combinations
- KS X 1001 includes the most frequently used ~2350
- Covers 99%+ of modern Korean text

**Jamo (components):**
- Consonants (자음): ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ...
- Vowels (모음): ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟ...
- Used for display of individual components

## Source Fonts

| Script | Font | Style | Render Size |
|--------|------|-------|-------------|
| Latin | JetBrains Mono NL | Light | 48px |
| Korean | Noto Sans KR | Regular | 36px |

## Special Handling

### Punctuation Positioning

Korean uses same CJK punctuation as Chinese/Japanese:
- `、` (U+3001) — Ideographic comma (rare in Korean)
- `。` (U+3002) — Ideographic full stop (rare in Korean)
- `.` and `,` — More commonly used in modern Korean

## Usage

Replace the default font in `nicheGraphics.h`:

```cpp
#include "graphics/niche/Fonts/CJK/KoreanFont18px.h"

// Initialize with Korean font
hud.init(adapter, &NicheGraphics::KoreanFont18px);
```

## Generation

```bash
cd font-generator
python3 generate_font_korean.py
```

**Output:** `KoreanFont18px.h`

## Limitations

- No Cyrillic support
- No Japanese Kanji/Kana
- No Chinese Hanzi
- Some rare syllables may be missing (use Jamo fallback)
