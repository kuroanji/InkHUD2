#!/usr/bin/env python3
"""Generate unified font with JetBrains Mono (Latin/Cyrillic) + Noto Sans JP (Japanese)."""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Script directory (all paths relative to this)
SCRIPT_DIR = Path(__file__).parent.resolve()

# === CONFIGURATION ===
# Download fonts and place in fonts/ subdirectory:
#   JetBrains Mono: https://www.jetbrains.com/lp/mono/
#   Noto Sans JP: https://fonts.google.com/noto/specimen/Noto+Sans+JP

# JetBrains Mono NL Light for Latin and Cyrillic (monospace, no ligatures)
FONT_LATIN = SCRIPT_DIR / "fonts/JetBrainsMonoNL-Light.ttf"
# Noto Sans JP for Japanese (Hiragana, Katakana, Kanji)
FONT_NOTO_JP = SCRIPT_DIR / "fonts/NotoSansJP-Regular.ttf"

# Output file (in same directory as script)
OUTPUT_PATH = SCRIPT_DIR / "JapaneseFont18px.h"

# Joyo kanji list
JOYO_KANJI_PATH = SCRIPT_DIR / "joyo_kanji.txt"

# Codepoint aliases: map new codepoint to existing one (e.g., new 𠮟 U+20B9F -> old 叱 U+53F1)
CODEPOINT_ALIASES = {
    0x20B9F: 0x53F1,  # 𠮟 -> 叱 (shikaru - new Joyo form to old form)
}

CELL_SIZE = 18
RENDER_SIZE_CJK = 36
RENDER_SIZE_LATIN = 48  # Larger to make Latin visually match CJK size

def get_font_for_codepoint(cp, font_latin, font_noto):
    """Select appropriate font based on codepoint."""
    # Japanese ranges -> Noto Sans JP
    if cp >= 0x3000:  # CJK punctuation, Hiragana, Katakana, Kanji, etc.
        return font_noto
    # Miscellaneous Symbols (U+2600-U+26FF) including ♪ ♫ ★ etc. -> Noto Sans JP
    if 0x2600 <= cp <= 0x26FF:
        return font_noto
    # General Punctuation (U+2000-U+206F) - curly quotes, dashes, ellipsis -> Noto Sans JP
    # JetBrains Mono doesn't have these
    if 0x2000 <= cp <= 0x206F:
        return font_noto
    # APL Symbols (U+2336-U+237A) including ⍰ placeholder -> Noto Sans JP
    if 0x2336 <= cp <= 0x237A:
        return font_noto
    # Everything else (ASCII, Cyrillic, symbols) -> JetBrains Mono
    return font_latin

def get_joyo_kanji():
    """Load all 2136 Joyo kanji from file."""
    kanji_file = Path(__file__).parent / JOYO_KANJI_PATH
    if not kanji_file.exists():
        print(f"ERROR: {kanji_file} not found!")
        return []

    all_kanji = []
    with open(kanji_file, 'r', encoding='utf-8') as f:
        for line in f:
            ch = line.strip()
            if ch and len(ch) == 1:
                all_kanji.append(ch)

    print(f"  Loaded {len(all_kanji)} Joyo kanji")
    return all_kanji

# Manual xAdvance overrides for e-ink readability
CHAR_WIDTH_OVERRIDES = {
    # Punctuation
    '.': 0.40,   # Period
    ',': 0.40,   # Comma
    ':': 0.45,   # Colon
    ';': 0.45,   # Semicolon
    "'": 0.35,   # Single quote
    '`': 0.35,   # Backtick
    '|': 0.35,   # Pipe
    '!': 0.45,   # Exclamation
    # Space
    ' ': 0.45,   # Space
    # Brackets/parens
    '(': 0.50,
    ')': 0.50,
    '[': 0.50,
    ']': 0.50,
    '{': 0.55,
    '}': 0.55,
    # Other
    '"': 0.55,
    '-': 0.50,   # Hyphen
    '/': 0.55,
    '\\': 0.55,
    # Narrow letters
    'i': 0.45,
    'l': 0.45,
    'I': 0.50,
    '1': 0.65,
    # Digits - wider for better spacing with CJK
    '0': 0.65,
    '2': 0.65,
    '3': 0.65,
    '4': 0.65,
    '5': 0.65,
    '6': 0.65,
    '7': 0.65,
    '8': 0.65,
    '9': 0.65,
}

def get_all_codepoints():
    """Get all codepoints: Full ASCII + Full Cyrillic + Full Japanese + symbols."""
    codepoints = set()

    # === FULL ASCII (0x20-0x7E) - 95 printable chars ===
    for cp in range(0x20, 0x7F):
        codepoints.add(cp)

    # === LATIN-1 SUPPLEMENT (essential symbols only) ===
    for ch in "©®°±×÷«»":
        codepoints.add(ord(ch))

    # === CYRILLIC (Russian + Ukrainian only) ===
    # Russian: А-Я, а-я (U+0410-U+044F)
    for cp in range(0x0410, 0x0450):
        codepoints.add(cp)
    # Ё, ё
    codepoints.add(0x0401)  # Ё
    codepoints.add(0x0451)  # ё
    # Ukrainian: Є, є, І, і, Ї, ї, Ґ, ґ
    codepoints.add(0x0404)  # Є
    codepoints.add(0x0454)  # є
    codepoints.add(0x0406)  # І
    codepoints.add(0x0456)  # і
    codepoints.add(0x0407)  # Ї
    codepoints.add(0x0457)  # ї
    codepoints.add(0x0490)  # Ґ
    codepoints.add(0x0491)  # ґ

    # === ESSENTIAL SYMBOLS ONLY ===
    # Essential punctuation & symbols (hand-picked, not full blocks)
    essential_symbols = (
        "№€£¥©®™°±×÷«»—–…"  # Common symbols
        "←→↑↓↔"              # Basic arrows
        "♪♫"                 # Musical notes (for Japanese)
        "★☆♥♦♣♠"            # Common decorative
        "✓✗"                 # Check/cross marks
        "℃℉"                 # Temperature
        "\u2018\u2019\u201C\u201D\u201E\u201A"  # Typographic quotes: '' "" „ ‚ (iOS uses these!)
        "•·"                 # Bullets
        "…"                  # Ellipsis (already in, but ensure)
        "\uFFFD"             # U+FFFD - REPLACEMENT CHARACTER (standard Unicode)
    )
    for ch in essential_symbols:
        codepoints.add(ord(ch))

    # === KAOMOJI SYMBOLS ===
    # Greek letters used in kaomoji (ω, etc.)
    kaomoji_greek = "ωΩαβγδεζηθικλμνξοπρστυφχψΔΣΠ"
    for ch in kaomoji_greek:
        codepoints.add(ord(ch))

    # Math symbols used in kaomoji
    kaomoji_math = "∀∃∇∂∞∫∮√∝∠∧∨∩∪∈∋⊂⊃⊆⊇⊕⊗⊥∅≡≠≤≥"
    for ch in kaomoji_math:
        codepoints.add(ord(ch))

    # Geometric shapes for kaomoji
    kaomoji_shapes = "○●◎◇◆□■△▲▽▼◯◉◐◑◒◓▷◁▶◀☐☑☒"
    for ch in kaomoji_shapes:
        codepoints.add(ord(ch))

    # CJK decorative characters for kaomoji (彡, etc.)
    kaomoji_cjk = (
        "彡"    # U+5F61 - decorative strokes
        "ノ"    # U+30CE - katakana no (used as line)
        "ヾ"    # U+30FE - iteration mark
        "ゞ"    # U+309E - hiragana iteration
        "〃"    # U+3003 - ditto mark
        "々"    # U+3005 - ideographic iteration
        "〆"    # U+3006 - closing mark
        "〇"    # U+3007 - ideographic number zero
        "〈〉"  # U+3008-3009 - angle brackets
        "《》"  # U+300A-300B - double angle brackets
        "〒"    # U+3012 - postal mark
        "〓"    # U+3013 - geta mark
        "〔〕"  # U+3014-3015 - tortoise shell brackets
        "〖〗"  # U+3016-3017 - white lenticular brackets
        "〘〙"  # U+3018-3019 - white tortoise shell
        "〚〛"  # U+301A-301B - white square brackets
        "〜"    # U+301C - wave dash
        "〝〞"  # U+301D-301E - double prime quotes
        "゛゜"  # U+309B-309C - dakuten, handakuten
        "ゝゟ"  # U+309D, 309F - iteration marks
        "ヽヿ"  # U+30FD, 30FF - katakana iteration
    )
    for ch in kaomoji_cjk:
        codepoints.add(ord(ch))

    # Miscellaneous symbols for kaomoji
    misc_kaomoji = (
        "☆★☾☽☀☁☂☃"  # Weather/celestial
        "♀♂"           # Gender
        "♩♪♫♬♭♮♯"    # Music
        "❤❥❦❧"        # Hearts
        "✿❀❁❂❃❄❅❆"  # Flowers/snowflakes
        "✦✧✩✪✫✬✭✮✯"  # Stars
        "☺☻☹"         # Faces
        "✌✍✎✏"        # Hands/writing
        "☠☢☣"         # Warning
        "⌒"           # Arc (for smiles)
        "∩∪"          # Set operations (for faces)
        "ε"           # Epsilon (for mouths)
        "Д"           # Cyrillic De (for shocked faces)
        "益"          # CJK for kaomoji faces
        "皿"          # CJK for kaomoji
        "罒"          # CJK for kaomoji eyes
        "ﾟ"           # Halfwidth handakuten
        "ω"           # Already included but ensure
    )
    for ch in misc_kaomoji:
        codepoints.add(ord(ch))

    # Box drawing light (for simple borders)
    box_drawing = "─│┌┐└┘├┤┬┴┼━┃┏┓┗┛"
    for ch in box_drawing:
        codepoints.add(ord(ch))

    # === FULLWIDTH FORMS (U+FF00-U+FF5E) ===
    # Japanese fullwidth ASCII (！ " ＃ etc.)
    for cp in range(0xFF01, 0xFF5F):
        codepoints.add(cp)

    # Halfwidth Katakana (U+FF65-U+FF9F) - used in some kaomoji
    for cp in range(0xFF65, 0xFFA0):
        codepoints.add(cp)

    # Additional fullwidth symbols (U+FFE0-U+FFEF)
    # ￣ (macron), ￠￡￢￣￤￥￦ etc.
    for cp in range(0xFFE0, 0xFFF0):
        codepoints.add(cp)

    # === JAPANESE ===

    # CJK Punctuation & Symbols: U+3000-U+303F (。、・「」『』【】〜ー etc.)
    for cp in range(0x3000, 0x3040):
        codepoints.add(cp)

    # Hiragana: U+3040-U+309F (full block)
    for cp in range(0x3040, 0x30A0):
        codepoints.add(cp)

    # Katakana: U+30A0-U+30FF (full block)
    for cp in range(0x30A0, 0x3100):
        codepoints.add(cp)

    # Katakana Phonetic Extensions: U+31F0-U+31FF (small katakana for Ainu)
    for cp in range(0x31F0, 0x3200):
        codepoints.add(cp)

    # ALL 2136 Joyo Kanji
    joyo_kanji = get_joyo_kanji()
    for ch in joyo_kanji:
        codepoints.add(ord(ch))

    # Add the old form of 叱 (U+53F1) explicitly for alias support
    codepoints.add(0x53F1)  # 叱 - old form that 𠮟 maps to

    # Halfwidth/Fullwidth Forms: REMOVED - not needed, regular ASCII suffices

    # CJK Symbols (U+3200-U+32FF) and CJK Compatibility (U+3300-U+33FF): REMOVED

    return sorted(codepoints)


def render_glyph(font, codepoint, cell_size, render_size, font_ascent):
    """Render a single glyph to a fixed-size bitmap cell.

    Different strategies for Latin vs CJK:
    - Latin/Cyrillic: use consistent baseline for proper alignment
    - CJK: center in cell for uniform appearance
    """
    char = chr(codepoint)

    try:
        bbox = font.getbbox(char)
        if bbox is None or (bbox[2] - bbox[0]) == 0:
            return None
    except Exception:
        return None

    # Get font metrics
    ascent, descent = font.getmetrics()

    # For CJK (codepoint >= 0x3000), use centered approach
    # Also include U+2026 (…) and U+2025 (‥) for proper Japanese punctuation rendering
    is_cjk = codepoint >= 0x3000 or (0xFF00 <= codepoint <= 0xFFEF) or codepoint in {0x2026, 0x2025}

    # Punctuation positioning categories
    # Bottom: 、。…‥＿_ (comma, period, ellipsis, underscore)
    bottom_punct = {0x3001, 0x3002, 0x2026, 0x2025, 0xFF3F, 0x005F, 0xFF0C, 0xFF0E}
    # Opening brackets (align to top-left): 「『（【〔〈《
    open_brackets = {0x300C, 0x300E, 0xFF08, 0x3010, 0x3014, 0x3008, 0x300A}
    # Closing brackets (align to bottom-right): 」』）】〕〉》
    close_brackets = {0x300D, 0x300F, 0xFF09, 0x3011, 0x3015, 0x3009, 0x300B}
    # Top: ｀ " ' " ' (quotes, backtick)
    top_punct = {0xFF40, 0x201C, 0x2018, 0x201D, 0x2019, 0xFF02, 0xFF07}
    # Center: ー〜-~−＞＜・＊*；：（）＝＋≠≒｜ and most others
    center_punct = {0x30FC, 0x301C, 0x002D, 0x007E, 0x2212, 0xFF1E, 0xFF1C,
                    0x30FB, 0xFF0A, 0x002A, 0xFF1B, 0xFF1A, 0xFF1D, 0xFF0B,
                    0x2260, 0x2252, 0xFF5C, 0xFF0D}

    # Determine positioning mode
    punct_mode = None
    if codepoint in bottom_punct:
        punct_mode = 'bottom'
    elif codepoint in open_brackets:
        punct_mode = 'open'
    elif codepoint in close_brackets:
        punct_mode = 'close'
    elif codepoint in top_punct:
        punct_mode = 'top'
    elif codepoint in center_punct:
        punct_mode = 'center'
    elif 0x3000 <= codepoint <= 0x303F:
        punct_mode = 'center'  # Default for other CJK punctuation

    # Create canvas
    canvas_size = render_size * 2
    img = Image.new('L', (canvas_size, canvas_size), 0)
    draw = ImageDraw.Draw(img)

    if is_cjk:
        # Em-square size from font metrics
        em_square = ascent  # Use ascent as reference (typically equals em-square for CJK)
        cell = cell_size  # Target cell size (18px)

        # Draw character position depends on punctuation mode
        draw_x = render_size // 2
        if punct_mode == 'bottom':
            # Draw lower on canvas so there's room for crop_top to be positive
            draw_y = render_size  # Lower position
        else:
            draw_y = render_size // 2
        draw.text((draw_x, draw_y), char, font=font, fill=255, anchor='mm')  # middle-middle

        # Find actual bbox
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

        # Fixed crop size for consistent scaling
        crop_size = em_square + 4

        if punct_mode == 'bottom':
            # Position glyph at very bottom of cell (like Latin punctuation)
            cx = (min_x + max_x) // 2
            crop_left = cx - crop_size // 2
            crop_top = max_y - crop_size  # Align to absolute bottom edge
        elif punct_mode == 'top':
            # Position glyph at top of cell
            cx = (min_x + max_x) // 2
            crop_left = cx - crop_size // 2
            crop_top = min_y - 2  # Align top
        elif punct_mode == 'open':
            # Opening bracket: align right edge to reduce gap after bracket
            crop_left = max_x - crop_size + 6  # Push bracket to right side of cell
            crop_top = min_y - 4
        elif punct_mode == 'close':
            # Closing bracket: align to bottom-right
            crop_left = min_x - 6  # Push bracket to left side of cell
            crop_top = max_y - crop_size + 4
        elif punct_mode == 'center':
            # Center the glyph
            cx = (min_x + max_x) // 2
            cy = (min_y + max_y) // 2
            crop_left = cx - crop_size // 2
            crop_top = cy - crop_size // 2
        else:
            # Kanji/Kana: tight crop centered on glyph
            crop_size = max(glyph_w, glyph_h) + 4
            cx = (min_x + max_x) // 2
            cy = (min_y + max_y) // 2
            crop_left = cx - crop_size // 2
            crop_top = cy - crop_size // 2
    else:
        # Latin/Cyrillic: render at larger size, fixed baseline
        # Draw at LEFT side of canvas (not centered) so narrow glyphs align left
        draw_x = 24  # Fixed left position (with small margin)
        baseline_y = 40  # Position baseline to fit cap height + descender in crop

        draw.text((draw_x, baseline_y), char, font=font, fill=255, anchor='ls')  # left-baseline

        # Find actual glyph bounds
        pixels = img.load()
        min_x, max_x = canvas_size, 0
        for y in range(canvas_size):
            for x in range(canvas_size):
                if pixels[x, y] > 0:
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)

        # Smaller crop = larger character after scaling to 18px
        # CJK uses ~40-46px crop, Latin should match
        crop_size = 48
        # Crop from LEFT edge of glyph (with small margin) so narrow chars align left
        crop_left = min_x - 2 if max_x >= min_x else draw_x - 2
        crop_top = 0

    # Ensure bounds
    crop_left = max(0, crop_left)
    crop_top = max(0, crop_top)
    crop_right = min(canvas_size, crop_left + crop_size)
    crop_bottom = min(canvas_size, crop_top + crop_size)

    crop = img.crop((crop_left, crop_top, crop_right, crop_bottom))

    # Scale to cell_size
    result = crop.resize((cell_size, cell_size), Image.LANCZOS)

    # Threshold - lower value = thicker lines
    result = result.point(lambda p: 1 if p > 48 else 0, '1')

    # Pack to bytes
    bitmap = []
    byte_val = 0
    bit = 7
    result_pixels = result.load()
    for y in range(cell_size):
        for x in range(cell_size):
            if result_pixels[x, y]:
                byte_val |= (1 << bit)
            bit -= 1
            if bit < 0:
                bitmap.append(byte_val)
                byte_val = 0
                bit = 7

    if bit < 7:
        bitmap.append(byte_val)

    return bytes(bitmap)


def main():
    print(f"Loading fonts...")
    print(f"  JetBrains Mono (Latin/Cyrillic): {FONT_LATIN}")
    print(f"  Noto Sans JP (Japanese): {FONT_NOTO_JP}")

    # Load fonts at same size
    font_latin = ImageFont.truetype(FONT_LATIN, RENDER_SIZE_LATIN)
    font_noto = ImageFont.truetype(FONT_NOTO_JP, RENDER_SIZE_CJK)

    # Get font metrics
    ascent_latin, descent_latin = font_latin.getmetrics()
    ascent_cjk, descent_cjk = font_noto.getmetrics()
    print(f"Latin metrics (size {RENDER_SIZE_LATIN}): ascent={ascent_latin}, descent={descent_latin}")
    print(f"CJK metrics (size {RENDER_SIZE_CJK}): ascent={ascent_cjk}, descent={descent_cjk}")
    print(f"Cell size: {CELL_SIZE}px")

    codepoints = get_all_codepoints()
    print(f"Processing {len(codepoints)} codepoints...")

    # Force blank for ideographic space
    force_blank = {0x3000, 0x0020}

    glyphs = []
    skipped = 0

    # Scale factors
    scale_latin = CELL_SIZE / RENDER_SIZE_LATIN
    scale_cjk = CELL_SIZE / RENDER_SIZE_CJK

    for i, cp in enumerate(codepoints):
        if i % 1000 == 0:
            print(f"  Progress: {i}/{len(codepoints)}...")

        char = chr(cp)

        # Determine if CJK or Latin and select appropriate font/size
        is_cjk = cp >= 0x3000 or (0xFF00 <= cp <= 0xFFEF)
        if is_cjk:
            font = font_noto
            render_size = RENDER_SIZE_CJK
            scale = scale_cjk
            ascent = ascent_cjk
        else:
            font = get_font_for_codepoint(cp, font_latin, font_noto)
            render_size = RENDER_SIZE_LATIN
            scale = scale_latin
            ascent = ascent_latin

        if cp in force_blank:
            # Make blank glyph with appropriate space width
            total_bytes = (CELL_SIZE * CELL_SIZE + 7) // 8
            if char in CHAR_WIDTH_OVERRIDES:
                space_advance = int(CELL_SIZE * CHAR_WIDTH_OVERRIDES[char] + 0.5)
            else:
                space_advance = max(1, int(font.getlength(' ') * scale + 0.5))
            glyphs.append((cp, bytes(total_bytes), space_advance))
            continue

        result = render_glyph(font, cp, CELL_SIZE, render_size, ascent)
        if result is not None:
            if char in CHAR_WIDTH_OVERRIDES:
                advance = int(CELL_SIZE * CHAR_WIDTH_OVERRIDES[char] + 0.5)
            else:
                try:
                    advance_render = font.getlength(char)
                    advance = int(advance_render * scale + 0.5)
                    advance = max(1, min(CELL_SIZE, advance))
                except:
                    advance = CELL_SIZE


            glyphs.append((cp, result, advance))
        else:
            skipped += 1

    print(f"Rendered: {len(glyphs)} glyphs, skipped: {skipped}")

    # Count categories
    ascii_count = len([g for g in glyphs if 0x20 <= g[0] < 0x80])
    latin1_count = len([g for g in glyphs if 0xA0 <= g[0] < 0x100])
    cyrillic = len([g for g in glyphs if 0x400 <= g[0] < 0x530])
    greek = len([g for g in glyphs if 0x370 <= g[0] < 0x400])
    symbols = len([g for g in glyphs if 0x2000 <= g[0] < 0x2800])
    math_sym = len([g for g in glyphs if 0x2200 <= g[0] < 0x2300])
    hiragana = len([g for g in glyphs if 0x3040 <= g[0] < 0x30A0])
    katakana = len([g for g in glyphs if 0x30A0 <= g[0] < 0x3100])
    kanji = len([g for g in glyphs if 0x4E00 <= g[0] < 0xA000])
    fullwidth = len([g for g in glyphs if 0xFF00 <= g[0] < 0xFFF0])

    print(f"  ASCII: {ascii_count}, Latin-1: {latin1_count}, Cyrillic: {cyrillic}, Greek: {greek}")
    print(f"  Symbols: {symbols}, Math: {math_sym}, Hiragana: {hiragana}, Katakana: {katakana}")
    print(f"  Kanji: {kanji}, Fullwidth: {fullwidth}")

    # Sort by codepoint
    glyphs.sort(key=lambda g: g[0])

    # Build bitmap and glyph table (now includes xAdvance)
    bitmap_data = bytearray()
    glyph_entries = []
    for cp, bmp, xadv in glyphs:
        offset = len(bitmap_data)
        bitmap_data.extend(bmp)
        glyph_entries.append((cp, offset, xadv))

    # Size: 4 (codepoint) + 4 (offset) + 1 (xAdvance) = 9 bytes per glyph (padded to 12)
    total_kb = (len(bitmap_data) + len(glyph_entries) * 12) / 1024
    print(f"Bitmap: {len(bitmap_data) / 1024:.1f} KB, total: {total_kb:.1f} KB")

    # Write header file
    with open(OUTPUT_PATH, 'w') as f:
        f.write(f"// Unified font: JetBrains Mono NL (Latin/Cyrillic) + Noto Sans JP (Japanese)\n")
        f.write(f"// ASCII: {ascii_count}, Latin-1: {latin1_count}, Cyrillic: {cyrillic}, Symbols: {symbols}\n")
        f.write(f"// Hiragana: {hiragana}, Katakana: {katakana}, Kanji: {kanji}, Fullwidth: {fullwidth}\n")
        f.write(f"// Render: Latin {RENDER_SIZE_LATIN}px, CJK {RENDER_SIZE_CJK}px -> {CELL_SIZE}px\n")
        f.write(f"// Total: {len(glyphs)} glyphs, {len(bitmap_data)} bytes\n\n")
        f.write("#pragma once\n\n")
        f.write("#include <stdint.h>\n")
        f.write("#ifdef __AVR__\n")
        f.write("#include <avr/pgmspace.h>\n")
        f.write("#else\n")
        f.write("#define PROGMEM\n")
        f.write("#endif\n\n")
        f.write("#include \"graphics/niche/Fonts/CJK/CJKFont.h\"\n\n")
        f.write("namespace NicheGraphics {\n\n")

        f.write("const uint8_t UnifiedFont18px_Bitmap[] PROGMEM = {\n")
        for i in range(0, len(bitmap_data), 16):
            chunk = bitmap_data[i:i + 16]
            f.write("    " + ", ".join(f"0x{b:02X}" for b in chunk) + ",\n")
        f.write("};\n\n")

        f.write("const CJKGlyph UnifiedFont18px_Glyphs[] PROGMEM = {\n")
        for cp, offset, xadv in glyph_entries:
            ch = chr(cp) if cp >= 0x20 and cp != 0x5C else '?'
            f.write(f"    {{ 0x{cp:04X}, {offset:6d}, {xadv:2d} }},  // {ch}\n")
        f.write("};\n\n")

        f.write("const CJKFont UnifiedFont18px PROGMEM = {\n")
        f.write("    UnifiedFont18px_Bitmap,\n")
        f.write("    UnifiedFont18px_Glyphs,\n")
        f.write(f"    {len(glyphs)},   // glyphCount\n")
        f.write(f"    {CELL_SIZE},     // width\n")
        f.write(f"    {CELL_SIZE},     // height\n")
        f.write(f"    {CELL_SIZE + 1}, // xAdvance\n")
        f.write(f"    -{CELL_SIZE},    // yOffset\n")
        f.write("};\n\n")

        # Write codepoint aliases (e.g., new Joyo 𠮟 -> old 叱)
        if CODEPOINT_ALIASES:
            f.write("// Codepoint aliases: map unsupported codepoints to existing glyphs\n")
            f.write("// Used for characters like 𠮟 (U+20B9F) which should display as 叱 (U+53F1)\n")
            f.write("struct CJKAlias {\n")
            f.write("    uint32_t from;  // Requested codepoint\n")
            f.write("    uint32_t to;    // Codepoint to use instead\n")
            f.write("};\n\n")
            f.write(f"const CJKAlias UnifiedFont18px_Aliases[] PROGMEM = {{\n")
            for from_cp, to_cp in CODEPOINT_ALIASES.items():
                from_char = chr(from_cp) if from_cp < 0x10000 else f"U+{from_cp:05X}"
                to_char = chr(to_cp)
                f.write(f"    {{ 0x{from_cp:05X}, 0x{to_cp:04X} }},  // {from_char} -> {to_char}\n")
            f.write("};\n")
            f.write(f"const uint16_t UnifiedFont18px_AliasCount = {len(CODEPOINT_ALIASES)};\n\n")

        f.write("} // namespace NicheGraphics\n")

    print(f"Written: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
