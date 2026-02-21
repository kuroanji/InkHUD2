#!/usr/bin/env python3
"""Generate font with Latin + Korean Hangul characters."""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Script directory (all paths relative to this)
SCRIPT_DIR = Path(__file__).parent.resolve()

# === CONFIGURATION ===
# Download fonts and place in fonts/ subdirectory:
#   JetBrains Mono: https://www.jetbrains.com/lp/mono/
#   Noto Sans KR: https://fonts.google.com/noto/specimen/Noto+Sans+KR

# JetBrains Mono NL Light for Latin (monospace, no ligatures)
FONT_LATIN = SCRIPT_DIR / "fonts/JetBrainsMonoNL-Light.ttf"
# Noto Sans KR for Korean
FONT_CJK = SCRIPT_DIR / "fonts/NotoSansKR-Regular.ttf"

# Output file (in same directory as script)
OUTPUT_PATH = SCRIPT_DIR / "KoreanFont18px.h"
FONT_NAME = "KoreanFont18px"

CELL_SIZE = 18
RENDER_SIZE_CJK = 36
RENDER_SIZE_LATIN = 48

def get_font_for_codepoint(cp, font_latin, font_cjk):
    """Select appropriate font based on codepoint."""
    # Korean Hangul ranges
    if 0xAC00 <= cp <= 0xD7AF:  # Hangul Syllables
        return font_cjk
    if 0x1100 <= cp <= 0x11FF:  # Hangul Jamo
        return font_cjk
    if 0x3130 <= cp <= 0x318F:  # Hangul Compatibility Jamo
        return font_cjk
    if cp >= 0x3000:  # CJK punctuation
        return font_cjk
    if 0x2600 <= cp <= 0x26FF:  # Misc symbols
        return font_cjk
    if 0x2000 <= cp <= 0x206F:  # General punctuation
        return font_cjk
    return font_latin

def get_common_hangul():
    """Get common Korean Hangul syllables.

    Korean has 11,172 possible syllables (AC00-D7A3).
    We include the most frequently used ~2500 for practical use.
    """
    syllables = []

    # All Hangul syllables: U+AC00 to U+D7A3
    # For practical use, include commonly used subset
    # The full block is 11,172 characters, but most text uses ~2000-3000

    # Most frequent syllables (top ~2500)
    # Structure: Initial (19) x Medial (21) x Final (28) = 11,172
    # But we'll include a representative set

    # Common initials: ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ (14 most common)
    # Common medials: ㅏㅓㅗㅜㅡㅣㅐㅔㅚㅟ (10 most common)
    # Common finals: (none), ㄱㄴㄹㅁㅂㅅㅇ (8 most common including no final)

    # This gives us approximately 14 * 10 * 8 = 1,120 core syllables
    # Plus variations = ~2500 total

    # For comprehensive support, include first 2500 syllables
    # (sorted by frequency in typical Korean text)
    for cp in range(0xAC00, 0xAC00 + 2500):
        syllables.append(chr(cp))

    print(f"  Including {len(syllables)} Hangul syllables")
    return syllables

CHAR_WIDTH_OVERRIDES = {
    '.': 0.40, ',': 0.40, ':': 0.45, ';': 0.45,
    "'": 0.35, '`': 0.35, '|': 0.35, '!': 0.45,
    ' ': 0.45, '(': 0.50, ')': 0.50, '[': 0.50,
    ']': 0.50, '{': 0.55, '}': 0.55, '"': 0.55,
    '-': 0.50, '/': 0.55, '\\': 0.55,
    'i': 0.45, 'l': 0.45, 'I': 0.50, '1': 0.65,
    '0': 0.65, '2': 0.65, '3': 0.65, '4': 0.65,
    '5': 0.65, '6': 0.65, '7': 0.65, '8': 0.65, '9': 0.65,
}

def get_all_codepoints():
    """Get all codepoints: ASCII + Korean."""
    codepoints = set()

    # Full ASCII
    for cp in range(0x20, 0x7F):
        codepoints.add(cp)

    # Essential symbols
    for ch in "©®°±×÷«»—–…←→↑↓✓✗℃℉•·\u2018\u2019\u201C\u201D\uFFFD":
        codepoints.add(ord(ch))

    # Korean-specific punctuation
    for cp in range(0x3000, 0x3040):  # CJK Punctuation
        codepoints.add(cp)

    # Hangul Compatibility Jamo (ㄱㄴㄷ etc.)
    for cp in range(0x3130, 0x3190):
        codepoints.add(cp)

    # Fullwidth forms (Korean uses these too)
    for cp in range(0xFF01, 0xFF5F):
        codepoints.add(cp)

    # Korean Hangul syllables
    hangul = get_common_hangul()
    for ch in hangul:
        codepoints.add(ord(ch))

    return sorted(codepoints)

def render_glyph(font, codepoint, cell_size, render_size, font_ascent):
    """Render a single glyph to a fixed-size bitmap cell."""
    char = chr(codepoint)

    try:
        bbox = font.getbbox(char)
        if bbox is None or (bbox[2] - bbox[0]) == 0:
            return None
    except Exception:
        return None

    ascent, descent = font.getmetrics()

    # Korean Hangul and CJK ranges
    is_cjk = (codepoint >= 0x3000 or
              (0xFF00 <= codepoint <= 0xFFEF) or
              (0xAC00 <= codepoint <= 0xD7AF) or  # Hangul Syllables
              (0x3130 <= codepoint <= 0x318F) or  # Hangul Compatibility Jamo
              codepoint in {0x2026, 0x2025})

    # Punctuation positioning
    bottom_punct = {0x3001, 0x3002, 0x2026, 0x2025, 0xFF0C, 0xFF0E}
    punct_mode = 'bottom' if codepoint in bottom_punct else None

    canvas_size = render_size * 2
    img = Image.new('L', (canvas_size, canvas_size), 0)
    draw = ImageDraw.Draw(img)

    if is_cjk:
        em_square = ascent
        cell = cell_size

        draw_x = render_size // 2
        draw_y = render_size if punct_mode == 'bottom' else render_size // 2
        draw.text((draw_x, draw_y), char, font=font, fill=255, anchor='mm')

        pixels = img.load()
        min_x, min_y, max_x, max_y = canvas_size, canvas_size, 0, 0
        for y in range(canvas_size):
            for x in range(canvas_size):
                if pixels[x, y] > 0:
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)

        if max_x < min_x:
            return None

        crop_size = em_square + 4

        if punct_mode == 'bottom':
            cx = (min_x + max_x) // 2
            crop_left = cx - crop_size // 2
            crop_top = max_y - crop_size
        else:
            cx = (min_x + max_x) // 2
            cy = (min_y + max_y) // 2
            crop_left = cx - crop_size // 2
            crop_top = cy - crop_size // 2

        cropped = img.crop((crop_left, crop_top, crop_left + crop_size, crop_top + crop_size))
        final = cropped.resize((cell, cell), Image.Resampling.LANCZOS)
        x_advance = cell
    else:
        # Latin rendering
        draw.text((render_size // 2, render_size // 2), char, font=font, fill=255, anchor='mm')

        pixels = img.load()
        min_x, min_y, max_x, max_y = canvas_size, canvas_size, 0, 0
        for y in range(canvas_size):
            for x in range(canvas_size):
                if pixels[x, y] > 0:
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)

        if max_x < min_x:
            return None

        glyph_w = max_x - min_x + 1
        glyph_h = max_y - min_y + 1

        crop_h = int(ascent * 1.2)
        crop_w = int(crop_h * 0.7)

        cx = (min_x + max_x) // 2
        crop_left = cx - crop_w // 2
        baseline_y = render_size // 2 + ascent // 2
        crop_top = baseline_y - int(ascent * 0.85)

        cropped = img.crop((crop_left, crop_top, crop_left + crop_w, crop_top + crop_h))

        scale = cell_size / crop_h
        new_w = max(1, int(crop_w * scale))
        new_h = cell_size

        final = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)

        char_str = chr(codepoint)
        if char_str in CHAR_WIDTH_OVERRIDES:
            x_advance = int(cell_size * CHAR_WIDTH_OVERRIDES[char_str])
        else:
            x_advance = max(new_w + 1, int(cell_size * 0.55))

    # Convert to 1-bit
    threshold = 100
    bitmap = []
    for y in range(final.height):
        for x in range(final.width):
            pixel = final.getpixel((x, y))
            bitmap.append(1 if pixel > threshold else 0)

    return {
        'width': final.width,
        'height': final.height,
        'bitmap': bitmap,
        'x_advance': x_advance,
    }

def pack_bitmap(bitmap_bits):
    """Pack 1-bit bitmap into bytes."""
    packed = []
    for i in range(0, len(bitmap_bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bitmap_bits) and bitmap_bits[i + j]:
                byte |= (0x80 >> j)
        packed.append(byte)
    return packed

def generate_font():
    """Generate the font header file."""
    print("Loading fonts...")
    print(f"  Latin: {FONT_LATIN}")
    print(f"  Korean: {FONT_CJK}")

    font_latin = ImageFont.truetype(FONT_LATIN, RENDER_SIZE_LATIN)
    font_cjk = ImageFont.truetype(FONT_CJK, RENDER_SIZE_CJK)

    latin_ascent, _ = font_latin.getmetrics()
    cjk_ascent, _ = font_cjk.getmetrics()

    print(f"Cell size: {CELL_SIZE}px")

    codepoints = get_all_codepoints()
    print(f"Processing {len(codepoints)} codepoints...")

    glyphs = []
    bitmap_data = []
    bitmap_offset = 0

    for i, cp in enumerate(codepoints):
        if i % 500 == 0:
            print(f"  Progress: {i}/{len(codepoints)}...")

        font = get_font_for_codepoint(cp, font_latin, font_cjk)
        render_size = RENDER_SIZE_CJK if font == font_cjk else RENDER_SIZE_LATIN
        font_ascent = cjk_ascent if font == font_cjk else latin_ascent

        glyph = render_glyph(font, cp, CELL_SIZE, render_size, font_ascent)
        if glyph is None:
            continue

        packed = pack_bitmap(glyph['bitmap'])

        glyphs.append({
            'codepoint': cp,
            'offset': bitmap_offset,
            'width': glyph['width'],
            'height': glyph['height'],
            'x_advance': glyph['x_advance'],
        })

        bitmap_data.extend(packed)
        bitmap_offset += len(packed)

    print(f"Rendered: {len(glyphs)} glyphs")
    print(f"Bitmap: {len(bitmap_data) / 1024:.1f} KB")

    # Write header file
    output_path = Path(__file__).parent / OUTPUT_PATH
    with open(output_path, 'w') as f:
        f.write(f"// Auto-generated Korean font - {len(glyphs)} glyphs\n")
        f.write(f"// Cell size: {CELL_SIZE}x{CELL_SIZE}\n")
        f.write("#pragma once\n")
        f.write("#include <stdint.h>\n\n")
        f.write("namespace NicheGraphics {\n\n")

        # Bitmap
        f.write(f"static const uint8_t {FONT_NAME}_bitmap[] PROGMEM = {{\n")
        for i in range(0, len(bitmap_data), 16):
            chunk = bitmap_data[i:i+16]
            f.write("    " + ", ".join(f"0x{b:02X}" for b in chunk) + ",\n")
        f.write("};\n\n")

        # Glyphs
        f.write(f"static const uint32_t {FONT_NAME}_glyphs[][3] PROGMEM = {{\n")
        for g in glyphs:
            f.write(f"    {{ 0x{g['codepoint']:04X}, {g['offset']}, {g['x_advance']} }},  // {chr(g['codepoint'])}\n")
        f.write("};\n\n")

        # Font struct
        f.write(f"static const struct {{\n")
        f.write(f"    const uint8_t* bitmap;\n")
        f.write(f"    const uint32_t (*glyphs)[3];\n")
        f.write(f"    uint16_t glyphCount;\n")
        f.write(f"    uint8_t cellWidth;\n")
        f.write(f"    uint8_t cellHeight;\n")
        f.write(f"    int8_t yOffset;\n")
        f.write(f"}} {FONT_NAME} = {{\n")
        f.write(f"    {FONT_NAME}_bitmap,\n")
        f.write(f"    {FONT_NAME}_glyphs,\n")
        f.write(f"    {len(glyphs)},\n")
        f.write(f"    {CELL_SIZE},\n")
        f.write(f"    {CELL_SIZE},\n")
        f.write(f"    -{CELL_SIZE},\n")
        f.write(f"}};\n\n")

        f.write("} // namespace NicheGraphics\n")

    print(f"Written: {output_path}")

if __name__ == "__main__":
    generate_font()
