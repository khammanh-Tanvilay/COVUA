import pygame
import math

def draw_baby_face(surface, mx, my, x, y, pixel_size=8, abs_x=0, abs_y=0):
    WHITE = (255, 255, 255)
    SKIN  = (255, 224, 189)
    BLACK = (0, 0, 0)
    PINK  = (255, 192, 203)
    BLUE  = (0, 191, 255)
    def draw_pixel(px, py, color):
        pygame.draw.rect(surface, color, (x + px * pixel_size, y + py * pixel_size, pixel_size, pixel_size))
    # 1. Khuôn mặt (10x10 pixel, bắt đầu từ (0,0))
    for px in range(0, 10):
        for py in range(0, 10):
            draw_pixel(px, py, SKIN)
    # 2. Má hồng
    draw_pixel(1, 8, PINK)
    draw_pixel(8, 8, PINK)
    # 3. Mắt (vị trí và bán kính như mẫu)
    eye_centers = [
        (3 * pixel_size + pixel_size//2, 4 * pixel_size + pixel_size//2),
        (7 * pixel_size + pixel_size//2, 4 * pixel_size + pixel_size//2)
    ]
    eye_radius = int(pixel_size * 1.0)
    pupil_radius = int(pixel_size * 0.5)
    for cx, cy in eye_centers:
        cx, cy = x + cx, y + cy
        pygame.draw.circle(surface, WHITE, (cx, cy), eye_radius)
        pygame.draw.circle(surface, BLACK, (cx, cy), eye_radius, 1)
        dx = mx - (abs_x + cx)
        dy = my - (abs_y + cy)
        dist = math.hypot(dx, dy)
        maxd = eye_radius - pupil_radius
        if dist != 0:
            factor = min(1, maxd / dist)
            dx, dy = dx * factor, dy * factor
        else:
            dx, dy = 0, 0
        pygame.draw.circle(surface, BLACK, (int(cx + dx), int(cy + dy)), pupil_radius)
    # 4. Miệng
    draw_pixel(3, 7, BLACK)
    draw_pixel(4, 8, BLACK)
    draw_pixel(5, 8, BLACK)
    draw_pixel(6, 7, BLACK)
    # 5. Tóc (3 pixel trên cùng)
    draw_pixel(3, 0, BLACK)
    draw_pixel(4, 0, BLACK)
    draw_pixel(5, 0, BLACK)
    # 6. Nơ xanh (dưới cùng)
    draw_pixel(0, 9, BLUE)
    draw_pixel(1, 10, BLUE)
    draw_pixel(2, 9, BLUE)

def draw_adult_face(surface, mx, my, x, y, pixel_size=8, abs_x=0, abs_y=0):
    WHITE     = (255, 255, 255)
    SKIN_DARK = (235, 200, 160)
    BLACK     = (0, 0, 0)
    BROWN     = (101,  67,  33)
    def draw_pixel(px, py, color):
        pygame.draw.rect(surface, color, (x + px * pixel_size, y + py * pixel_size, pixel_size, pixel_size))
    # 1. Khuôn mặt (10x10 pixel)
    for px in range(0, 10):
        for py in range(0, 10):
            draw_pixel(px, py, SKIN_DARK)
    # 2. Tóc 2 mái
    hair_pixels = [
        (1, -1),(2, -1),(3, -1), (0,0),(1,0),(2,0),
        (6, -1),(7, -1),(8, -1), (7,0),(8,0),(9,0)
    ]
    for px, py in hair_pixels:
        draw_pixel(px, py, BROWN)
    # 3. Lông mày
    eyebrow_pixels = [
        (2,2), (3,1), (4,2),
        (6,2), (7,1), (8,2)
    ]
    for px, py in eyebrow_pixels:
        draw_pixel(px, py, BLACK)
    # 4. Mắt
    eye_centers = [
        (3 * pixel_size + pixel_size//2, 4 * pixel_size + pixel_size//2),
        (7 * pixel_size + pixel_size//2, 4 * pixel_size + pixel_size//2)
    ]
    eye_radius = int(pixel_size * 1.0)
    pupil_radius = int(pixel_size * 0.5)
    for cx, cy in eye_centers:
        cx, cy = x + cx, y + cy
        pygame.draw.circle(surface, WHITE, (cx, cy), eye_radius)
        pygame.draw.circle(surface, BLACK, (cx, cy), eye_radius, 1)
        dx = mx - (abs_x + cx)
        dy = my - (abs_y + cy)
        dist = math.hypot(dx, dy)
        maxd = eye_radius - pupil_radius
        if dist != 0:
            factor = min(1, maxd / dist)
            dx, dy = dx * factor, dy * factor
        else:
            dx, dy = 0, 0
        pygame.draw.circle(surface, BLACK, (int(cx + dx), int(cy + dy)), pupil_radius)
    # 5. Miệng
    draw_pixel(3,7, BLACK)
    draw_pixel(6,7, BLACK)
    draw_pixel(4,8, BLACK)
    draw_pixel(5,8, BLACK)
    # 6. Râu
    beard_pixels = [
        (1,9),(2,9),(3,9),(4,9),(5,9),(6,9),(7,9),(8,9),
        (1,10),(2,10),(3,10),(4,10),(5,10),(6,10),(7,10),(8,10),
        (3,11),(4,11),(5,11)
    ]
    for px, py in beard_pixels:
        draw_pixel(px, py, BROWN)

def draw_old_face(surface, mx, my, x, y, pixel_size=8, abs_x=0, abs_y=0):
    WHITE      = (255, 255, 255)
    SKIN_OLD   = (220, 190, 160)
    BLACK      = (0, 0, 0)
    GRAY_OLD   = (200, 200, 200)
    def draw_pixel(px, py, color):
        pygame.draw.rect(surface, color, (x + px * pixel_size, y + py * pixel_size, pixel_size, pixel_size))
    # 1. Khuôn mặt (10x10 pixel)
    for px in range(0, 10):
        for py in range(0, 10):
            draw_pixel(px, py, SKIN_OLD)
    # 2. Nếp nhăn trán
    wrinkle_pixels = [
        (2,1), (3,1), (4,1),
        (1,2), (5,2)
    ]
    for px, py in wrinkle_pixels:
        draw_pixel(px, py, GRAY_OLD)
    # 3. Lông mày
    eyebrow_pixels = [
        (2,2), (3,1), (4,2),
        (6,2), (7,1), (8,2)
    ]
    for px, py in eyebrow_pixels:
        draw_pixel(px, py, GRAY_OLD)
    # 4. Mắt
    eye_centers = [
        (3 * pixel_size + pixel_size//2, 4 * pixel_size + pixel_size//2),
        (7 * pixel_size + pixel_size//2, 4 * pixel_size + pixel_size//2)
    ]
    eye_radius = int(pixel_size * 1.0)
    pupil_radius = int(pixel_size * 0.5)
    for cx, cy in eye_centers:
        cx, cy = x + cx, y + cy
        pygame.draw.circle(surface, WHITE, (cx, cy), eye_radius)
        pygame.draw.circle(surface, BLACK, (cx, cy), eye_radius, 1)
        dx = mx - (abs_x + cx)
        dy = my - (abs_y + cy)
        dist = math.hypot(dx, dy)
        maxd = eye_radius - pupil_radius
        if dist != 0:
            factor = min(1, maxd / dist)
            dx, dy = dx * factor, dy * factor
        else:
            dx, dy = 0, 0
        pygame.draw.circle(surface, BLACK, (int(cx + dx), int(cy + dy)), pupil_radius)
    # 5. Miệng
    draw_pixel(3,7, BLACK)
    draw_pixel(6,7, BLACK)
    draw_pixel(4,8, BLACK)
    draw_pixel(5,8, BLACK)
    # 6. Râu & quai hàm
    beard_pixels = [
        (1,9),(2,9),(3,9),(4,9),(5,9),(6,9),(7,9),(8,9),
        (1,10),(2,10),(3,10),(4,10),(5,10),(6,10),(7,10),(8,10),
        (3,11),(4,11),(5,11)
    ]
    for px, py in beard_pixels:
        draw_pixel(px, py, GRAY_OLD) 