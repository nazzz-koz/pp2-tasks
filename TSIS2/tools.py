import pygame
import math
import collections
import os

_HERE       = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR  = os.path.join(_HERE, "assets")
ICONS_DIR   = os.path.join(ASSETS_DIR, "icons")
FONTS_DIR   = os.path.join(ASSETS_DIR, "fonts")


SCREEN_W  = 860
SCREEN_H  = 600
TOOLBAR_W = 180
CANVAS_W  = SCREEN_W - TOOLBAR_W
CANVAS_H  = SCREEN_H

BG_COLOR       = (30,  30,  30)
CANVAS_COLOR   = (255, 255, 255)
TOOLBAR_COLOR  = (45,  45,  45)
TOOLBAR_BORDER = (80,  80,  80)
TEXT_COLOR     = (220, 220, 220)
HIGHLIGHT      = (100, 160, 240)
PREVIEW_ALPHA  = 160   

BRUSH_SIZES = [
    ("S", 1, 1),
    ("M", 3, 3),
    ("L", 7, 7),
]

PALETTE = [
    (0,   0,   0  ),   # black
    (255, 255, 255),   # white
    (255, 0,   0  ),   # red
    (0,   200, 0  ),   # green
    (0,   0,   255),   # blue
    (255, 165, 0  ),   # orange
    (255, 255, 0  ),   # yellow
    (180, 0,   255),   # purple
    (0,   200, 200),   # cyan
    (255, 105, 180),   # pink
    (139, 69,  19 ),   # brown
    (128, 128, 128),   # gray
]

TOOLS = [
    "pencil",    "line",
    "rect",      "circle",
    "square",    "right_tri",
    "equil_tri", "rhombus",
    "eraser",    "fill",
    "text",
]

TOOL_KEYS = {
    pygame.K_p: "pencil",
    pygame.K_l: "line",
    pygame.K_r: "rect",
    pygame.K_c: "circle",
    pygame.K_q: "square",
    pygame.K_t: "right_tri",
    pygame.K_y: "equil_tri",
    pygame.K_u: "rhombus",
    pygame.K_e: "eraser",
    pygame.K_f: "fill",
    pygame.K_x: "text",
}


def draw_thick_line(surface, color, start, end, radius):
    dx       = end[0] - start[0]
    dy       = end[1] - start[1]
    distance = max(abs(dx), abs(dy))

    if distance == 0:
        pygame.draw.circle(surface, color, start, radius)
        return

    for i in range(distance + 1):
        t = i / distance
        x = int(start[0] + dx * t)
        y = int(start[1] + dy * t)
        pygame.draw.circle(surface, color, (x, y), radius)


def draw_square(surface, color, start, end, lw):
    side = min(abs(end[0] - start[0]), abs(end[1] - start[1]))
    if side == 0:
        return
    x = start[0] if end[0] >= start[0] else start[0] - side
    y = start[1] if end[1] >= start[1] else start[1] - side
    pygame.draw.rect(surface, tuple(color), (x, y, side, side), lw)


def draw_right_triangle(surface, color, start, end, lw):
    p1 = start
    p2 = (start[0], end[1])
    p3 = end
    pygame.draw.polygon(surface, tuple(color), [p1, p2, p3], lw)


def draw_equil_triangle(surface, color, start, end, lw):
    base = end[0] - start[0]
    h    = int(abs(base) * math.sqrt(3) / 2)
    sy   = 1 if end[1] >= start[1] else -1

    p1 = (start[0],                  start[1] + sy * h)   # bottom-left
    p2 = (end[0],                    start[1] + sy * h)   # bottom-right
    p3 = ((start[0] + end[0]) // 2, start[1])             # apex
    pygame.draw.polygon(surface, tuple(color), [p1, p2, p3], lw)


def draw_rhombus(surface, color, start, end, lw):
    cx     = (start[0] + end[0]) // 2
    cy     = (start[1] + end[1]) // 2
    top    = (cx,       start[1])
    bottom = (cx,       end[1])
    left   = (start[0], cy)
    right  = (end[0],   cy)
    pygame.draw.polygon(surface, tuple(color), [top, right, bottom, left], lw)


def flood_fill(surface, pos, fill_color):
    x0, y0 = int(pos[0]), int(pos[1])
    w, h   = surface.get_size()

    if not (0 <= x0 < w and 0 <= y0 < h):
        return

    target = surface.get_at((x0, y0))[:3]   
    fill3  = tuple(fill_color[:3])

    if target == fill3:
        return

    visited = set()
    queue   = collections.deque([(x0, y0)])
    visited.add((x0, y0))

    while queue:
        x, y = queue.popleft()
        surface.set_at((x, y), fill_color)

        for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if (nx, ny) not in visited and 0 <= nx < w and 0 <= ny < h:
                if surface.get_at((nx, ny))[:3] == target:
                    visited.add((nx, ny))
                    queue.append((nx, ny))


def _load_icon(tool_name, size=24):
    path = os.path.join(ICONS_DIR, f"{tool_name}.png")
    if not os.path.isfile(path):
        return None
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(img, (size, size))
    except pygame.error:
        return None


class Toolbar:
    ICON_SIZE = 24   

    def __init__(self, x, font_sm, font_tiny):
        self.x         = x
        self.font_sm   = font_sm
        self.font_tiny = font_tiny

        self.tool_rects  = {}   
        self.size_rects  = {}   
        self.color_rects = {}   

        self._icons = {tool: _load_icon(tool, self.ICON_SIZE) for tool in TOOLS}


    def draw(self, screen, active_tool, active_size_idx, active_color):
        pygame.draw.rect(screen, TOOLBAR_COLOR,
                         pygame.Rect(self.x, 0, TOOLBAR_W, SCREEN_H))
        pygame.draw.line(screen, TOOLBAR_BORDER,
                         (self.x, 0), (self.x, SCREEN_H), 2)

        y = 10   

        screen.blit(
            self.font_sm.render("TOOLS", True, (160, 160, 160)),
            (self.x + 6, y)
        )
        y += 20

        btn_w = 80          
        btn_h = 32          
        gap   = 4
        col   = 0           

        self.tool_rects.clear()
        for tool in TOOLS:
            bx   = self.x + 4 + col * (btn_w + gap)
            rect = pygame.Rect(bx, y, btn_w, btn_h)
            self.tool_rects[tool] = rect

            bg = HIGHLIGHT if tool == active_tool else (60, 60, 60)
            pygame.draw.rect(screen, bg,             rect, border_radius=4)
            pygame.draw.rect(screen, TOOLBAR_BORDER, rect, 1, border_radius=4)

            icon = self._icons.get(tool)
            if icon:
                ix = rect.x + (btn_w - self.ICON_SIZE) // 2
                iy = rect.y + 2
                screen.blit(icon, (ix, iy))
            else:
                lbl = self.font_tiny.render(tool, True, TEXT_COLOR)
                screen.blit(lbl, (
                    rect.centerx - lbl.get_width()  // 2,
                    rect.centery - lbl.get_height() // 2,
                ))

            col = 1 - col
            if col == 0:
                y += btn_h + gap

        if col == 1:   
            y += btn_h + gap
        y += 8

        screen.blit(
            self.font_sm.render("BRUSH SIZE", True, (160, 160, 160)),
            (self.x + 6, y)
        )
        y += 20

        sw = (TOOLBAR_W - 16) // 3   
        self.size_rects.clear()
        for i, (name, radius, _) in enumerate(BRUSH_SIZES):
            rect = pygame.Rect(self.x + 6 + i * (sw + 2), y, sw, 28)
            self.size_rects[i] = rect

            bg = HIGHLIGHT if i == active_size_idx else (60, 60, 60)
            pygame.draw.rect(screen, bg,             rect, border_radius=4)
            pygame.draw.rect(screen, TOOLBAR_BORDER, rect, 1, border_radius=4)

            dot_r = min(radius, 9)
            pygame.draw.circle(screen, TEXT_COLOR, rect.center, dot_r)

            screen.blit(
                self.font_tiny.render(name, True, TEXT_COLOR),
                (rect.x + 3, rect.y + 2)
            )
        y += 36

        screen.blit(
            self.font_sm.render("COLOURS", True, (160, 160, 160)),
            (self.x + 6, y)
        )
        y += 20

        sw2 = (TOOLBAR_W - 16) // 4   
        self.color_rects.clear()
        for i, col_val in enumerate(PALETTE):
            row  = i // 4
            col2 = i %  4
            rect = pygame.Rect(
                self.x + 6 + col2 * (sw2 + 2),
                y + row * (sw2 + 2),
                sw2, sw2
            )
            self.color_rects[i] = rect

            pygame.draw.rect(screen, col_val, rect, border_radius=3)

            border_col = (255, 255, 255) if col_val == active_color else TOOLBAR_BORDER
            border_w   = 2               if col_val == active_color else 1
            pygame.draw.rect(screen, border_col, rect, border_w, border_radius=3)

        y += (len(PALETTE) // 4 + 1) * (sw2 + 2) + 8

        for hint in [
            "P=Pencil  L=Line",
            "R=Rect   C=Circle",
            "Q=Square T=RTri",
            "Y=ETri   U=Rhomb",
            "E=Erase  F=Fill",
            "X=Text Tool",
            "[/] Change size",
            "Ctrl+S  Save PNG",
            "ESC  Quit",
        ]:
            screen.blit(
                self.font_tiny.render(hint, True, (120, 120, 120)),
                (self.x + 6, y)
            )
            y += 14


    def handle_click(self, pos, active_tool, active_size_idx, active_color):
        for tool, rect in self.tool_rects.items():
            if rect.collidepoint(pos):
                return tool, active_size_idx, active_color

        for i, rect in self.size_rects.items():
            if rect.collidepoint(pos):
                return active_tool, i, active_color

        for i, rect in self.color_rects.items():
            if rect.collidepoint(pos):
                return active_tool, active_size_idx, PALETTE[i]

        return active_tool, active_size_idx, active_color
