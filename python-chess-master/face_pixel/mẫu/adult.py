import pygame
import sys
import math

# Khởi tạo pygame
pygame.init()

# Kích thước cửa sổ
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Father Pixel Smiley - Eyebrows Closer")

# Định nghĩa màu
WHITE     = (255, 255, 255)
SKIN_DARK = (235, 200, 160)
BLACK     = (0, 0, 0)
BROWN     = (101,  67,  33)

PIXEL = 10   # mỗi ô pixel 10×10

# Tọa độ trung tâm mắt (pixel-coordinates)
eye_centers = [
    (13 * PIXEL + PIXEL//2, 14 * PIXEL + PIXEL//2),  # mắt trái
    (17 * PIXEL + PIXEL//2, 14 * PIXEL + PIXEL//2)   # mắt phải
]
eye_radius   = PIXEL        # bán kính lòng trắng
pupil_radius = PIXEL // 2   # bán kính con ngươi

def draw_pixel(x, y, color):
    pygame.draw.rect(screen, color, (x*PIXEL, y*PIXEL, PIXEL, PIXEL))

def draw_father(mx, my):
    screen.fill(WHITE)

    # 1. Khuôn mặt
    for gx in range(10, 20):
        for gy in range(10, 20):
            draw_pixel(gx, gy, SKIN_DARK)

    # 2. Tóc 2 mái
    hair_pixels = [
        (11,9),(12,9),(13,9), (10,10),(11,10),(12,10),
        (16,9),(17,9),(18,9), (17,10),(18,10),(19,10)
    ]
    for x,y in hair_pixels:
        draw_pixel(x, y, BROWN)

    # 3. Lông mày (cách nhau 1 pixel):
    eyebrow_pixels = [
        # bên trái: kết thúc ở x=14
        (12,12), (13,11), (14,12),
        # bên phải: bắt đầu ở x=16
        (16,12), (17,11), (18,12)
    ]
    for x, y in eyebrow_pixels:
        draw_pixel(x, y, BLACK)


    # 4. Mắt + con ngươi theo chuột
    for cx, cy in eye_centers:
        pygame.draw.circle(screen, WHITE, (cx, cy), eye_radius)
        pygame.draw.circle(screen, BLACK, (cx, cy), eye_radius, 1)
        dx, dy = mx - cx, my - cy
        dist = math.hypot(dx, dy)
        if dist:
            maxd = eye_radius - pupil_radius
            factor = min(1, maxd / dist)
            dx, dy = dx*factor, dy*factor
        pygame.draw.circle(screen, BLACK,
                           (int(cx+dx), int(cy+dy)),
                           pupil_radius)

    # 5. Miệng
    draw_pixel(13,17, BLACK)
    draw_pixel(16,17, BLACK)
    draw_pixel(14,18, BLACK)
    draw_pixel(15,18, BLACK)

    # 6. Râu
    beard_pixels = [
        (11,19),(12,19),(13,19),(14,19),(15,19),(16,19),(17,19),(18,19),
        (11,20),(12,20),(13,20),(14,20),(15,20),(16,20),(17,20),(18,20),
        (13,21),(14,21),(15,21)
    ]
    for x,y in beard_pixels:
        draw_pixel(x, y, BROWN)

    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                running = False

        draw_father(mx, my)
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
