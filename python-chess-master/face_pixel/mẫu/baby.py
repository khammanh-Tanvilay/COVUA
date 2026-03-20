import pygame
import sys
import math

# Khởi tạo pygame
pygame.init()

# Kích thước cửa sổ
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Baby Pixel Smiley - Eyes Follow Mouse")

# Định nghĩa màu
WHITE = (255, 255, 255)
SKIN  = (255, 224, 189)
BLACK = (0, 0, 0)
PINK  = (255, 192, 203)
BLUE  = (0, 191, 255)

PIXEL = 10  # kích thước mỗi ô pixel

# Tọa độ trung tâm mắt (theo lưới pixel)
eye_centers = [
    (13 * PIXEL + PIXEL//2, 14 * PIXEL + PIXEL//2),  # mắt trái
    (17 * PIXEL + PIXEL//2, 14 * PIXEL + PIXEL//2)   # mắt phải
]
eye_radius = PIXEL  # bán kính vòm mắt
pupil_radius = PIXEL // 2  # bán kính con ngươi

def draw_pixel(x, y, color):
    pygame.draw.rect(screen, color, (x * PIXEL, y * PIXEL, PIXEL, PIXEL))

def draw_face(mx, my):
    screen.fill(WHITE)
    # 1. Khuôn mặt
    for x in range(10, 20):
        for y in range(10, 20):
            draw_pixel(x, y, SKIN)

    # 2. Má hồng
    draw_pixel(11, 18, PINK)
    draw_pixel(18, 18, PINK)

    # 3. Vẽ mắt: lòng trắng + con ngươi di chuyển
    for cx, cy in eye_centers:
        # vẽ lòng trắng (hình tròn đơn giản)
        pygame.draw.circle(screen, WHITE, (cx, cy), eye_radius)
        pygame.draw.circle(screen, BLACK, (cx, cy), eye_radius, 1)

        # tính vector từ tâm mắt tới chuột
        dx, dy = mx - cx, my - cy
        dist = math.hypot(dx, dy)
        if dist != 0:
            # clamp độ dài về eye_radius - pupil_radius
            maxd = eye_radius - pupil_radius
            factor = min(1, maxd / dist)
            dx, dy = dx * factor, dy * factor

        # vẽ con ngươi
        pygame.draw.circle(
            screen,
            BLACK,
            (int(cx + dx), int(cy + dy)),
            pupil_radius
        )

    # 4. Miệng cười
    draw_pixel(13, 17, BLACK)
    draw_pixel(14, 18, BLACK)
    draw_pixel(15, 18, BLACK)
    draw_pixel(16, 17, BLACK)

    # 5. Tóc
    draw_pixel(13, 9, BLACK)
    draw_pixel(14, 9, BLACK)
    draw_pixel(15, 9, BLACK)

    # 6. Nơ xanh
    draw_pixel(10, 20, BLUE)
    draw_pixel(11, 21, BLUE)
    draw_pixel(12, 20, BLUE)

    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_face(mx, my)
        clock.tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
