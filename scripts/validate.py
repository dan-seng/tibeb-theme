#!/usr/bin/env python3
"""Validate the distributable theme using Python 3.11+ (no dependencies)."""

from pathlib import Path
import re
import struct
import sys
import tomllib
import zlib

ROOT = Path(__file__).resolve().parent.parent
COLORS = """accent selection muted background dark_background darker_background
lighter_background foreground dark_foreground light_foreground bright_foreground
red yellow orange green cyan blue magenta brown bright_red bright_yellow
bright_green bright_cyan bright_blue bright_magenta""".split()


def check_png(path):
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path.name}: invalid PNG signature")
    offset = 8
    chunks = []
    pixels = bytearray()
    while offset < len(data):
        length, kind = struct.unpack_from(">I4s", data, offset)
        payload = data[offset + 8:offset + 8 + length]
        crc = struct.unpack_from(">I", data, offset + 8 + length)[0]
        if zlib.crc32(kind + payload) != crc:
            raise ValueError(f"{path.name}: corrupt PNG chunk")
        chunks.append(kind)
        if kind == b"IDAT":
            pixels.extend(payload)
        offset += length + 12
    if not chunks or chunks[0] != b"IHDR" or chunks[-1] != b"IEND":
        raise ValueError(f"{path.name}: incomplete PNG")
    width, height = struct.unpack_from(">II", data, 16)
    if not width or not height or not pixels or not zlib.decompress(pixels):
        raise ValueError(f"{path.name}: missing image data")
    print(f"OK {path.relative_to(ROOT)} ({width} × {height})")


def main():
    with (ROOT / "colors.toml").open("rb") as source:
        palette = tomllib.load(source)
    if palette.get("mode") != "dark":
        raise ValueError("Tibeb requires mode = \"dark\"")
    for key in COLORS:
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", str(palette.get(key, ""))):
            raise ValueError(f"Missing or invalid palette color: {key}")
    print(f"OK colors.toml ({len(COLORS)} colors)")
    if (ROOT / "icons.theme").read_text().strip() != "Yaru-olive":
        raise ValueError("Expected Yaru-olive in icons.theme")
    print("OK icons.theme")
    check_png(ROOT / "preview.png")
    check_png(ROOT / "backgrounds/tibeb-highlands.png")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, struct.error, zlib.error) as error:
        sys.exit(f"Theme validation failed: {error}")
