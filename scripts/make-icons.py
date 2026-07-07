#!/usr/bin/env python3
"""產生浪日誌的 PWA icon（純 stdlib，不需要 PIL）：復古衝浪配色——奶油底＋丹寧藍浪線＋三色條紋。"""
import math
import struct
import zlib

CREAM_TOP = (247, 243, 232)   # #F7F3E8
CREAM_BOT = (241, 234, 218)
DENIM = (47, 74, 92)          # #2F4A5C
MUSTARD = (227, 180, 88)      # #E3B458
ORANGE = (217, 122, 80)       # #D97A50
STEEL = (143, 180, 198)       # #8FB4C6


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def pixel(x, y, size):
    t = y / size
    color = lerp(CREAM_TOP, CREAM_BOT, t)
    # 丹寧藍浪線（上半部）
    wave_y = size * (0.36 + 0.075 * math.sin(2 * math.pi * (x / size) * 1.3 + 0.6))
    d = abs(y - wave_y) / (size * 0.034)
    if d < 1:
        color = lerp(color, DENIM, (1 - d) ** 1.4)
    # 三色條紋（下半部），帶奶油間隔
    for cy, tone in [(0.66, MUSTARD), (0.75, ORANGE), (0.84, STEEL)]:
        if abs(t - cy) < 0.032:
            color = tone
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
