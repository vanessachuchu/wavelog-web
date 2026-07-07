#!/usr/bin/env python3
"""產生浪日誌的 PWA icon（純 stdlib，不需要 PIL）：深海漸層＋白色浪線。"""
import math
import struct
import zlib

BG_TOP = (10, 22, 34)      # #0A1622
BG_BOT = (18, 54, 66)      # 深海青
FOAM = (79, 209, 197)      # #4FD1C5
WHITE = (234, 242, 247)


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def pixel(x, y, size):
    t = y / size
    color = lerp(BG_TOP, BG_BOT, t)
    # 三條浪線，往下漸淡
    for i, (cy, amp, thick, tone) in enumerate([
        (0.52, 0.055, 0.030, WHITE),
        (0.64, 0.045, 0.022, FOAM),
        (0.76, 0.035, 0.016, lerp(FOAM, BG_BOT, 0.45)),
    ]):
        wave_y = size * (cy + amp * math.sin(2 * math.pi * (x / size) * 1.4 + i * 1.1))
        d = abs(y - wave_y) / (size * thick)
        if d < 1:
            a = (1 - d) ** 1.5
            color = lerp(color, tone, a)
    return color


def make_png(size, path):
    raw = bytearray()
    for y in range(size):
        raw.append(0)
        for x in range(size):
            raw.extend(pixel(x, y, size))

    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(bytes(raw), 9))
           + chunk(b'IEND', b''))
    with open(path, 'wb') as f:
        f.write(png)
    print(f'{path} ({size}x{size})')


if __name__ == '__main__':
    make_png(512, 'icons/icon-512.png')
    make_png(192, 'icons/icon-192.png')
    make_png(180, 'icons/apple-touch-icon.png')
