import pygame
import math
from datetime import datetime

from tools import (
    SCREEN_W, SCREEN_H, TOOLBAR_W, CANVAS_W, CANVAS_H,
    BG_COLOR, CANVAS_COLOR, TOOLBAR_BORDER,
    BRUSH_SIZES, PALETTE, TOOLS, TOOL_KEYS, PREVIEW_ALPHA,
    draw_thick_line,
    draw_square, draw_right_triangle, draw_equil_triangle, draw_rhombus,
    flood_fill,
    Toolbar,
)


def commit_shape(canvas, active_tool, active_color, start_pos, end_pos, lw):
    if active_tool == 'rect':
        pygame.draw.rect(
            canvas, active_color,
            (*start_pos,
             end_pos[0] - start_pos[0],
             end_pos[1] - start_pos[1]),
            lw
        )
    elif active_tool == 'circle':
        r = int(math.hypot(end_pos[0] - start_pos[0],
                           end_pos[1] - start_pos[1]))
        pygame.draw.circle(canvas, active_color, start_pos, r, lw)

    elif active_tool == 'line':
        pygame.draw.line(canvas, active_color,
                         start_pos, end_pos, max(1, lw * 2))

    elif active_tool == 'square':
        draw_square(canvas, active_color, start_pos, end_pos, lw)

    elif active_tool == 'right_tri':
        draw_right_triangle(canvas, active_color, start_pos, end_pos, lw)

    elif active_tool == 'equil_tri':
        draw_equil_triangle(canvas, active_color, start_pos, end_pos, lw)

    elif active_tool == 'rhombus':
        draw_rhombus(canvas, active_color, start_pos, end_pos, lw)


def draw_preview(screen, active_tool, active_color, start_pos, end_pos, lw):
    ghost = pygame.Surface((CANVAS_W, CANVAS_H), pygame.SRCALPHA)
    gc    = (*active_color, PREVIEW_ALPHA)   
    lw    = max(1, lw)

    if active_tool == 'rect':
        pygame.draw.rect(
            ghost, gc,
            (*start_pos,
             end_pos[0] - start_pos[0],
             end_pos[1] - start_pos[1]),
            lw
        )
    elif active_tool == 'circle':
        r = int(math.hypot(end_pos[0] - start_pos[0],
                           end_pos[1] - start_pos[1]))
        if r > 0:
            pygame.draw.circle(ghost, gc, start_pos, r, lw)

    elif active_tool == 'line':
        pygame.draw.line(ghost, gc, start_pos, end_pos, max(1, lw * 2))

    elif active_tool == 'square':
        draw_square(ghost, gc, start_pos, end_pos, lw)

    elif active_tool == 'right_tri':
        draw_right_triangle(ghost, gc, start_pos, end_pos, lw)

    elif active_tool == 'equil_tri':
        draw_equil_triangle(ghost, gc, start_pos, end_pos, lw)

    elif active_tool == 'rhombus':
        draw_rhombus(ghost, gc, start_pos, end_pos, lw)

    screen.blit(ghost, (0, 0))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Paint App — TSIS2")
    clock = pygame.time.Clock()

    font_sm   = pygame.font.SysFont("Arial", 13, bold=True)
    font_tiny = pygame.font.SysFont("Arial", 11)
    font_text = pygame.font.SysFont("Arial", 22)   

    canvas = pygame.Surface((CANVAS_W, CANVAS_H))
    canvas.fill(CANVAS_COLOR)

    toolbar = Toolbar(CANVAS_W, font_sm, font_tiny)

    active_tool     = "pencil"
    active_size_idx = 1            
    active_color    = (0, 0, 0)    

    drawing   = False
    start_pos = None
    last_pos  = None

    text_mode   = False   
    text_pos    = None    
    text_buffer = ""      

    notify_msg   = ""
    notify_timer = 0      

    SHAPE_TOOLS = {'rect', 'circle', 'line', 'square',
                   'right_tri', 'equil_tri', 'rhombus'}


    def brush_r():
        return BRUSH_SIZES[active_size_idx][1]

    def shape_lw():
        return BRUSH_SIZES[active_size_idx][2]

    def in_canvas(pos):
        return 0 <= pos[0] < CANVAS_W and 0 <= pos[1] < CANVAS_H


    running = True
    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if text_mode:
                    if event.key == pygame.K_RETURN:
                        surf = font_text.render(text_buffer, True, active_color)
                        canvas.blit(surf, text_pos)
                        text_mode   = False
                        text_buffer = ""
                        text_pos    = None

                    elif event.key == pygame.K_ESCAPE:
                        text_mode   = False
                        text_buffer = ""
                        text_pos    = None

                    elif event.key == pygame.K_BACKSPACE:
                        text_buffer = text_buffer[:-1]

                    elif event.unicode and event.unicode.isprintable():
                        text_buffer += event.unicode

                    continue   

                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"canvas_{ts}.png"
                    pygame.image.save(canvas, filename)
                    notify_msg   = f"Saved: {filename}"
                    notify_timer = 180   
                    continue

                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key in TOOL_KEYS:
                    active_tool = TOOL_KEYS[event.key]
                    text_mode   = False   

                if event.key == pygame.K_LEFTBRACKET:
                    active_size_idx = max(0, active_size_idx - 1)
                if event.key == pygame.K_RIGHTBRACKET:
                    active_size_idx = min(len(BRUSH_SIZES) - 1,
                                         active_size_idx + 1)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos

                if pos[0] >= CANVAS_W:
                    active_tool, active_size_idx, active_color = \
                        toolbar.handle_click(pos, active_tool,
                                             active_size_idx, active_color)
                    text_mode = False
                    continue

                if not in_canvas(pos):
                    continue

                if active_tool == 'fill':
                    flood_fill(canvas, pos, active_color)

                elif active_tool == 'text':
                    text_mode   = True
                    text_pos    = pos
                    text_buffer = ""

                else:
                    drawing   = True
                    start_pos = pos
                    last_pos  = pos

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drawing and start_pos and in_canvas(event.pos):
                    if active_tool in SHAPE_TOOLS:
                        commit_shape(canvas, active_tool, active_color,
                                     start_pos, event.pos, shape_lw())
                drawing  = False
                last_pos = None

            if event.type == pygame.MOUSEMOTION and drawing:
                pos = event.pos

                if active_tool == 'pencil' and last_pos:
                    draw_thick_line(canvas, active_color,
                                    last_pos, pos, brush_r())

                elif active_tool == 'eraser' and last_pos:
                    draw_thick_line(canvas, CANVAS_COLOR,
                                    last_pos, pos, brush_r())

                last_pos = pos   

        screen.fill(BG_COLOR)
        screen.blit(canvas, (0, 0))   

        mouse_pos = pygame.mouse.get_pos()
        if drawing and start_pos and active_tool in SHAPE_TOOLS:
            draw_preview(screen, active_tool, active_color,
                         start_pos, mouse_pos, shape_lw())

        if text_mode and text_pos:
            preview_surf = font_text.render(text_buffer + "|", True, active_color)
            bg_box = pygame.Surface(
                (preview_surf.get_width() + 4, preview_surf.get_height() + 4),
                pygame.SRCALPHA
            )
            bg_box.fill((200, 200, 200, 120))
            screen.blit(bg_box,       (text_pos[0] - 2, text_pos[1] - 2))
            screen.blit(preview_surf, text_pos)

        toolbar.draw(screen, active_tool, active_size_idx, active_color)

        if notify_timer > 0:
            notify_timer -= 1
            ns   = font_sm.render(notify_msg, True, (50, 220, 100))
            nbox = pygame.Surface(
                (ns.get_width() + 10, ns.get_height() + 6),
                pygame.SRCALPHA
            )
            nbox.fill((30, 30, 30, 200))
            screen.blit(nbox, (CANVAS_W // 2 - nbox.get_width() // 2, 8))
            screen.blit(ns,   (CANVAS_W // 2 - ns.get_width()  // 2, 11))

        status = (f"Tool: {active_tool}  |  "
                  f"Size: {BRUSH_SIZES[active_size_idx][0]}  |  "
                  f"[ / ] to resize brush   Ctrl+S to save")
        screen.blit(font_tiny.render(status, True, (180, 180, 180)),
                    (6, SCREEN_H - 18))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
