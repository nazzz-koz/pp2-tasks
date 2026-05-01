import pygame
import math

def draw_smooth_line(surface, color, start, end, radius):
    """Draw a smooth thick line between two points using circles."""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))

    if distance == 0:
        pygame.draw.circle(surface, color, start, radius)
        return

    for i in range(distance):
        t = i / distance
        x = int(start[0] + dx * t)
        y = int(start[1] + dy * t)
        pygame.draw.circle(surface, color, (x, y), radius)


def draw_square(surface, color, start, end, width=2):
    """Draw a square: use the shorter side to enforce equal sides."""
    side = min(abs(end[0] - start[0]), abs(end[1] - start[1]))
    sx = 1 if end[0] >= start[0] else -1
    sy = 1 if end[1] >= start[1] else -1
    rect = pygame.Rect(start[0], start[1], sx * side, sy * side)
    pygame.draw.rect(surface, color, rect.normalize(), width)


def draw_right_triangle(surface, color, start, end, width=2):
    """Draw a right triangle with the right angle at start."""
    p1 = start
    p2 = (start[0], end[1])   
    p3 = end                   
    pygame.draw.polygon(surface, color, [p1, p2, p3], width)


def draw_equilateral_triangle(surface, color, start, end, width=2):
    """Draw an equilateral triangle.
    'start' is the top-left corner of bounding box; 'end' gives the base width."""
    base_len = end[0] - start[0]
    height = int(abs(base_len) * math.sqrt(3) / 2)
    sy = 1 if end[1] >= start[1] else -1

    p1 = (start[0], start[1] + sy * height)   
    p2 = (end[0], start[1] + sy * height)     
    p3 = ((start[0] + end[0]) // 2, start[1]) 
    pygame.draw.polygon(surface, color, [p1, p2, p3], width)


def draw_rhombus(surface, color, start, end, width=2):
    """Draw a rhombus (diamond) fitted inside the bounding box of start→end."""
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2
    top    = (cx, start[1])
    bottom = (cx, end[1])
    left   = (start[0], cy)
    right  = (end[0], cy)
    pygame.draw.polygon(surface, color, [top, right, bottom, left], width)


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint App")
    clock = pygame.time.Clock()

    brush_radius = 10
    drawing = False
    mode = 'brush'           
    color = (0, 0, 255)      

    start_pos = None
    last_pos = None

    canvas = pygame.Surface(screen.get_size())
    canvas.fill((0, 0, 0))

    help_lines = [
        "B=Brush  R=Rect  C=Circle  E=Eraser",
        "Q=Square  T=Right-tri  Y=Equil-tri  U=Rhombus",
        "1=Red 2=Green 3=Blue 4=Yellow 5=White",
        "ESC=Quit",
    ]

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_b:
                    mode = 'brush'
                elif event.key == pygame.K_r:
                    mode = 'rect'
                elif event.key == pygame.K_c:
                    mode = 'circle'
                elif event.key == pygame.K_e:
                    mode = 'eraser'
                elif event.key == pygame.K_q:
                    mode = 'square'
                elif event.key == pygame.K_t:
                    mode = 'right_triangle'
                elif event.key == pygame.K_y:
                    mode = 'equil_triangle'
                elif event.key == pygame.K_u:
                    mode = 'rhombus'

                elif event.key == pygame.K_1:
                    color = (255, 0, 0)
                elif event.key == pygame.K_2:
                    color = (0, 255, 0)
                elif event.key == pygame.K_3:
                    color = (0, 0, 255)
                elif event.key == pygame.K_4:
                    color = (255, 255, 0)
                elif event.key == pygame.K_5:
                    color = (255, 255, 255)

            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                end_pos = event.pos
                last_pos = None

                if mode == 'rect':
                    pygame.draw.rect(
                        canvas, color,
                        (*start_pos,
                         end_pos[0] - start_pos[0],
                         end_pos[1] - start_pos[1]),
                        2
                    )
                elif mode == 'circle':
                    shape_radius = int(math.hypot(
                        end_pos[0] - start_pos[0],
                        end_pos[1] - start_pos[1]
                    ))
                    pygame.draw.circle(canvas, color, start_pos, shape_radius, 2)
                elif mode == 'square':
                    draw_square(canvas, color, start_pos, end_pos)
                elif mode == 'right_triangle':
                    draw_right_triangle(canvas, color, start_pos, end_pos)
                elif mode == 'equil_triangle':
                    draw_equilateral_triangle(canvas, color, start_pos, end_pos)
                elif mode == 'rhombus':
                    draw_rhombus(canvas, color, start_pos, end_pos)

            if event.type == pygame.MOUSEMOTION and drawing:
                if last_pos is not None:
                    if mode == 'brush':
                        draw_smooth_line(canvas, color, last_pos, event.pos, brush_radius)
                    elif mode == 'eraser':
                        draw_smooth_line(canvas, (0, 0, 0), last_pos, event.pos, brush_radius)
                last_pos = event.pos

        screen.fill((0, 0, 0))
        screen.blit(canvas, (0, 0))

        if drawing and start_pos:
            mouse_pos = pygame.mouse.get_pos()

            if mode == 'rect':
                pygame.draw.rect(
                    screen, color,
                    (*start_pos,
                     mouse_pos[0] - start_pos[0],
                     mouse_pos[1] - start_pos[1]),
                    1
                )
            elif mode == 'circle':
                shape_radius = int(math.hypot(
                    mouse_pos[0] - start_pos[0],
                    mouse_pos[1] - start_pos[1]
                ))
                pygame.draw.circle(screen, color, start_pos, shape_radius, 1)
            elif mode == 'square':
                draw_square(screen, color, start_pos, mouse_pos, 1)
            elif mode == 'right_triangle':
                draw_right_triangle(screen, color, start_pos, mouse_pos, 1)
            elif mode == 'equil_triangle':
                draw_equilateral_triangle(screen, color, start_pos, mouse_pos, 1)
            elif mode == 'rhombus':
                draw_rhombus(screen, color, start_pos, mouse_pos, 1)

        hud_font = pygame.font.SysFont("Arial", 14)
        mode_surf = hud_font.render(f"Mode: {mode}  Color: {color}", True, (200, 200, 200))
        screen.blit(mode_surf, (5, 460))
        for i, line in enumerate(help_lines):
            txt = hud_font.render(line, True, (150, 150, 150))
            screen.blit(txt, (5, 5 + i * 16))

        pygame.display.flip()
        clock.tick(60)


main()
