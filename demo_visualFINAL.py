import pygame
import numpy as np

pygame.init()

# Window
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RAC Cube Traversal (Full 3D + Inside Access)")

# Fonts
font = pygame.font.SysFont(None, 28)
small_font = pygame.font.SysFont(None, 22)

# Colors
BG = (10, 10, 10)
EDGE = (180, 180, 180)
ACTIVE_COLOR = (0, 255, 0, 220)
DEFAULT_COLOR = (80, 80, 180, 70)

# Grid
GRID = 3
cube_spacing = 60
origin_x = WIDTH // 2 - 100
origin_y = HEIGHT // 2 - 150

# Signal position
pos = [0, 0, 0]  # x, y, z

def iso_coords(x, y, z):
    """Convert 3D coords to isometric screen position"""
    iso_x = origin_x + (x - z) * cube_spacing
    iso_y = origin_y + (x + z - 2 * y) * cube_spacing // 2
    return iso_x, iso_y

def draw_cube(x, y, z, is_active=False):
    iso_x, iso_y = iso_coords(x, y, z)
    size = 40
    h = size // 2

    top = [
        (iso_x, iso_y),
        (iso_x + size, iso_y - h),
        (iso_x + 2 * size, iso_y),
        (iso_x + size, iso_y + h)
    ]
    left = [
        (iso_x, iso_y),
        (iso_x + size, iso_y + h),
        (iso_x + size, iso_y + size + h),
        (iso_x, iso_y + size)
    ]
    right = [
        (iso_x + size, iso_y + h),
        (iso_x + 2 * size, iso_y),
        (iso_x + 2 * size, iso_y + size),
        (iso_x + size, iso_y + size + h)
    ]

    surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    color = ACTIVE_COLOR if is_active else DEFAULT_COLOR

    pygame.draw.polygon(surf, color, left)
    pygame.draw.polygon(surf, color, right)
    pygame.draw.polygon(surf, color, top)

    pygame.draw.polygon(surf, EDGE, top, 1)
    pygame.draw.polygon(surf, EDGE, left, 1)
    pygame.draw.polygon(surf, EDGE, right, 1)

    screen.blit(surf, (0, 0))

def draw_scene():
    screen.fill(BG)

    # Painter's algorithm — draw from back to front
    for y in range(GRID):
        for z in range(GRID):
            for x in range(GRID):
                active = (x, y, z) == tuple(pos)
                draw_cube(x, y, z, is_active=active)

    # Labels
    screen.blit(font.render(f"RAC Signal Position → X:{pos[0]}  Y:{pos[1]}  Z:{pos[2]}", True, (255, 255, 255)), (40, 30))

    info = [
        "← ↑ ↓ → : Move in X and Y",
        "I = Forward Z (into screen),  O = Backward Z (out of screen)",
        "Green cube = active RAC | Translucent = inactive nodes",
        "You're now traversing inside the full 3D grid — not just its surface"
    ]
    for i, line in enumerate(info):
        screen.blit(small_font.render(line, True, (200, 200, 200)), (40, HEIGHT - 150 + i * 24))

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    draw_scene()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Full X/Y/Z traversal
    if keys[pygame.K_LEFT]:
        pos[0] = max(0, pos[0] - 1)
    if keys[pygame.K_RIGHT]:
        pos[0] = min(GRID - 1, pos[0] + 1)
    if keys[pygame.K_UP]:
        pos[1] = max(0, pos[1] - 1)
    if keys[pygame.K_DOWN]:
        pos[1] = min(GRID - 1, pos[1] + 1)
    if keys[pygame.K_i]:
        pos[2] = min(GRID - 1, pos[2] + 1)
    if keys[pygame.K_o]:
        pos[2] = max(0, pos[2] - 1)
            # Diagonal traversals
    if keys[pygame.K_7]:  # inward (toward cube center)
        pos[0] = min(GRID - 1, pos[0] + 1)
        pos[1] = min(GRID - 1, pos[1] + 1)
        pos[2] = min(GRID - 1, pos[2] + 1)

    if keys[pygame.K_9]:  # outward (away from cube center)
        pos[0] = max(0, pos[0] - 1)
        pos[1] = max(0, pos[1] - 1)
        pos[2] = max(0, pos[2] - 1)

    if keys[pygame.K_u]:  # diagonal up + into screen
        pos[1] = max(0, pos[1] - 1)
        pos[2] = min(GRID - 1, pos[2] + 1)

    if keys[pygame.K_j]:  # diagonal down + out of screen
        pos[1] = min(GRID - 1, pos[1] + 1)
        pos[2] = max(0, pos[2] - 1)


    pygame.display.flip()
    clock.tick(10)

    

pygame.quit()
