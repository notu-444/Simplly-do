#!/usr/bin/env python3
"""
Create a 32x32 PNG favicon with a double-tick design.
Uses only standard library modules: struct, zlib.
"""
import struct
import zlib

def create_png(width, height, pixels):
    """Create a PNG file from pixel data."""
    def png_chunk(chunk_type, data):
        chunk = chunk_type + data
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', zlib.crc32(chunk) & 0xffffffff)
    
    # PNG header
    header = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)  # 8-bit RGBA
    ihdr = png_chunk(b'IHDR', ihdr_data)
    
    # IDAT chunk (image data)
    raw_data = b''
    for row in pixels:
        raw_data += b'\x00'  # Filter type: None
        for r, g, b, a in row:
            raw_data += bytes([r, g, b, a])
    
    compressed = zlib.compress(raw_data)
    idat = png_chunk(b'IDAT', compressed)
    
    # IEND chunk
    iend = png_chunk(b'IEND', b'')
    
    return header + ihdr + idat + iend

def draw_double_tick():
    """Create a 32x32 image with a double-tick design."""
    width, height = 32, 32
    # Initialize with transparent pixels
    pixels = [[(0, 0, 0, 0) for _ in range(width)] for _ in range(height)]
    
    # Colors
    green = (34, 197, 94, 255)  # #22c55e
    dark_green = (22, 163, 74, 255)  # #16a34a
    
    # Draw first checkmark (left)
    check1_points = [
        (6, 18), (7, 19), (8, 20), (9, 21), (10, 22), (11, 21), (12, 20), (13, 19), (14, 18), (15, 17), (16, 16), (17, 15), (18, 14)
    ]
    
    # Draw second checkmark (right, slightly offset)
    check2_points = [
        (14, 18), (15, 19), (16, 20), (17, 21), (18, 22), (19, 21), (20, 20), (21, 19), (22, 18), (23, 17), (24, 16), (25, 15), (26, 14)
    ]
    
    # Draw thick lines for checkmarks
    def draw_thick_line(pixels, points, color, thickness=2):
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            # Draw a thick line between points
            for t in range(10):
                x = int(x1 + (x2 - x1) * t / 9)
                y = int(y1 + (y2 - y1) * t / 9)
                # Draw thickness
                for dx in range(-thickness//2, thickness//2 + 1):
                    for dy in range(-thickness//2, thickness//2 + 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            pixels[ny][nx] = color
    
    # Draw the two checkmarks
    draw_thick_line(pixels, check1_points, green, 2)
    draw_thick_line(pixels, check2_points, dark_green, 2)
    
    return create_png(width, height, pixels)

def main():
    png_data = draw_double_tick()
    
    with open('favicon.png', 'wb') as f:
        f.write(png_data)
    
    print(f"Created favicon.png ({len(png_data)} bytes)")

if __name__ == "__main__":
    main()
