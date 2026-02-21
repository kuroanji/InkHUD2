# Font Generator for InkHUD2

## Overview

Three specialized font generators for e-ink displays:

| Script | Languages | Output |
|--------|-----------|--------|
| `generate_font_japanese.py` | Japanese + Cyrillic + English | `JapaneseFont18px.h` |
| `generate_font_chinese.py` | Chinese (Simplified) + English | `ChineseFont18px.h` |
| `generate_font_korean.py` | Korean (Hangul) + English | `KoreanFont18px.h` |

## Quick Start

Scripts use relative paths — can be run from any directory:

```bash
# Generate Japanese/Cyrillic/English font
python3 /path/to/font-generator/generate_font_japanese.py

# Generate Chinese/English font
python3 /path/to/font-generator/generate_font_chinese.py

# Generate Korean/English font
python3 /path/to/font-generator/generate_font_korean.py
```

Output files are created in the same directory as the scripts.

## Required Source Fonts

TTF fonts are included in `fonts/` subdirectory. If missing, download and place there:

```
font-generator/
└── fonts/
    ├── JetBrainsMonoNL-Light.ttf   # Required for all
    ├── NotoSansJP-Regular.ttf      # For Japanese
    ├── NotoSansSC-Regular.ttf      # For Chinese
    └── NotoSansKR-Regular.ttf      # For Korean
```

### Download Links
- **JetBrains Mono NL Light**: https://www.jetbrains.com/mono/
- **Noto Sans JP**: https://fonts.google.com/noto/specimen/Noto+Sans+JP
- **Noto Sans SC**: https://fonts.google.com/noto/specimen/Noto+Sans+SC
- **Noto Sans KR**: https://fonts.google.com/noto/specimen/Noto+Sans+KR

## Character Lists

| File | Description | Source |
|------|-------------|--------|
| `joyo_kanji.txt` | 2136 Joyo Kanji (常用漢字) | [List of 2136 Joyo kanji (one per line) from https://github.com/scriptin/topokanji](https://github.com/scriptin/topokanji) |
| `common_hanzi.txt` | 3500 Common Chinese (GB2312 Level 1) | [Wikipedia: GB2312](https://en.wikipedia.org/wiki/GB_2312) |
| (built-in) | Korean: 2343 Hangul syllables (KS X 1001) | Algorithmic generation U+AC00–U+D7AF |

## Architecture Details

### Cell Size
- Fixed 18x18 pixel cell for all characters
- Consistent baseline alignment across scripts

### yOffset
- **Global yOffset (-18)** applies to ALL glyphs
- Per-glyph yOffset is NOT supported
- Vertical positioning is baked into bitmap during generation

### Two Rendering Paths

1. **Latin/Cyrillic** (`codepoint < 0x3000`):
   - Uses font's native metrics
   - Baseline-aligned rendering
   - Variable width (xAdvance)

2. **CJK** (`codepoint >= 0x3000` or special):
   - Centered in em-square
   - Fixed width (18px)
   - Special punctuation positioning

## Critical: Punctuation Positioning

Japanese/Chinese/Korean punctuation requires special vertical positioning.

### Bottom-aligned (baseline)
```
、。…‥，．
```
Characters: `0x3001, 0x3002, 0x2026, 0x2025, 0xFF0C, 0xFF0E`

### IMPORTANT: U+2026 Ellipsis Fix

The ellipsis character `…` (U+2026) is at codepoint `0x2026` which is **less than 0x3000**.

Without special handling, it renders CENTERED instead of at baseline.

**Required fix in is_cjk check:**
```python
# Include U+2026 and U+2025 for proper punctuation rendering
is_cjk = (codepoint >= 0x3000 or
          (0xFF00 <= codepoint <= 0xFFEF) or
          codepoint in {0x2026, 0x2025})
```

## Output Format

Generated `.h` files contain:
- Bitmap data (1-bit packed, row-major)
- Glyph table: `{ codepoint, bitmapOffset, xAdvance }`
- Font metadata struct

## Files in This Directory

```
font-generator/
├── README.md                    # This file
├── generate_font_japanese.py    # Japanese/Cyrillic/English
├── generate_font_chinese.py     # Chinese/English
├── generate_font_korean.py      # Korean/English
├── joyo_kanji.txt              # Japanese Joyo Kanji list
├── common_hanzi.txt            # Chinese character list
├── fonts/                      # Source TTF fonts (download required)
│   ├── JetBrainsMonoNL-Light.ttf
│   ├── NotoSansJP-Regular.ttf
│   ├── NotoSansSC-Regular.ttf
│   └── NotoSansKR-Regular.ttf
└── (generated output)
    ├── JapaneseFont18px.h
    ├── ChineseFont18px.h
    └── KoreanFont18px.h
```

## Troubleshooting

### Character renders in wrong position
- Check if codepoint is in correct punctuation category
- If codepoint < 0x3000 but needs CJK positioning, add to `is_cjk` check

### Character shows as □ or ?
- Verify source font contains the glyph
- Check if codepoint is in the character list

### Font file too large
- Reduce character count in the character list files
- Japanese: ~3000 chars = ~800KB
- Chinese: ~3000 chars = ~800KB
- Korean: ~2500 syllables = ~700KB

## Integration with InkHUD2

Copy generated font to:
```
src/graphics/niche/Fonts/CJK/UnifiedFont18px.h
```

The font is used via `NicheGraphics::UnifiedFont18px` in code.
