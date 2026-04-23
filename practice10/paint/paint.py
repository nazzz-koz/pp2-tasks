import pygame
import math

def draw_smooth_line(surface, color, start, end, radius):
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


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Smooth Paint App")
    clock = pygame.time.Clock()

    brush_radius = 10
    drawing = False
    mode = 'brush'
    color = (0, 0, 255)

    start_pos = None
    last_pos = None

    canvas = pygame.Surface(screen.get_size())
    canvas.fill((0, 0, 0))

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                # Tools
                if event.key == pygame.K_b:
                    mode = 'brush'
                elif event.key == pygame.K_r:
                    mode = 'rect'
                elif event.key == pygame.K_c:
                    mode = 'circle'
                elif event.key == pygame.K_e:
                    mode = 'eraser'

                # Colors
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
                        canvas,
                        color,
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

            if event.type == pygame.MOUSEMOTION and drawing:
                if last_pos is not None:
                    if mode == 'brush':
                        draw_smooth_line(canvas, color, last_pos, event.pos, brush_radius)

                    elif mode == 'eraser':
                        draw_smooth_line(canvas, (0, 0, 0), last_pos, event.pos, brush_radius)

                last_pos = event.pos

        screen.fill((0, 0, 0))
        screen.blit(canvas, (0, 0))

        # Preview shapes
        if drawing and start_pos:
            mouse_pos = pygame.mouse.get_pos()

            if mode == 'rect':
                pygame.draw.rect(
                    screen,
                    color,
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

        pygame.display.flip()
        clock.tick(60)


main()