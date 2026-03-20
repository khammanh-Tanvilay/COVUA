import pygame
import sys
import math

# Khởi tạo pygame
pygame.init()

# Kích thước cửa sổ
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grandpa Pixel Smiley - Eyebrows Harmonized")

# Màu sắc
WHITE      = (255, 255, 255)
SKIN_OLD   = (220, 190, 160)  # Da ông
BLACK      = (0, 0, 0)
GRAY_OLD   = (200, 200, 200)  # Màu râu & lông mày

PIXEL = 10  # Kích thước 1 ô

# Vị trí trung tâm hai mắt
eye_centers = [
    (13 * PIXEL + PIXEL // 2, 14 * PIXEL + PIXEL // 2),  # mắt trái
    (17 * PIXEL + PIXEL // 2, 14 * PIXEL + PIXEL // 2)   # mắt phải
]
eye_radius = PIXEL
pupil_radius = PIXEL // 2

def draw_pixel(x, y, color):
    pygame.draw.rect(screen, color, (x * PIXEL, y * PIXEL, PIXEL, PIXEL))

def draw_grandpa(mx, my):
    screen.fill(WHITE)

    # 1. Khuôn mặt
    for gx in range(10, 20):
        for gy in range(10, 20):
            draw_pixel(gx, gy, SKIN_OLD)

    # 2. Nếp nhăn trán
    wrinkle_pixels = [
        (12,11), (13,11), (14,11),
        (11,12), (15,12)
    ]
    for x, y in wrinkle_pixels:
        draw_pixel(x, y, GRAY_OLD)

    # 3. Lông mày chính (mỗi bên 3 pixel, cách nhau đúng 1 ô ở giữa)
    eyebrow_pixels = [
        # bên trái: kết thúc ở x=14
        (12,12), (13,11), (14,12),
        # bên phải: bắt đầu ở x=16
        (16,12), (17,11), (18,12)
    ]
    for x, y in eyebrow_pixels:
        draw_pixel(x, y, GRAY_OLD)

    # 4. Mắt + con ngươi
    for cx, cy in eye_centers:
        pygame.draw.circle(screen, WHITE, (cx, cy), eye_radius)
        pygame.draw.circle(screen, BLACK, (cx, cy), eye_radius, 1)
        dx, dy = mx - cx, my - cy
        dist = math.hypot(dx, dy)
        if dist != 0:
            factor = min(1, (eye_radius - pupil_radius) / dist)
            dx *= factor
            dy *= factor
        pygame.draw.circle(screen, BLACK, (int(cx + dx), int(cy + dy)), pupil_radius)

    # 5. Miệng
    draw_pixel(13, 17, BLACK)
    draw_pixel(16, 17, BLACK)
    draw_pixel(14, 18, BLACK)
    draw_pixel(15, 18, BLACK)

    # 6. Râu & quai hàm
    beard_pixels = [
        (11,19),(12,19),(13,19),(14,19),(15,19),(16,19),(17,19),(18,19),
        (11,20),(12,20),(13,20),(14,20),(15,20),(16,20),(17,20),(18,20),
        (13,21),(14,21),(15,21)
    ]
    for x, y in beard_pixels:
        draw_pixel(x, y, GRAY_OLD)

    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                running = False
        draw_grandpa(mx, my)
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
