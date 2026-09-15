import pygame

BASE_WIDTH = 800
BASE_HEIGHT = 500


class UI:
    def __init__(self, screen):
        self.screen = screen

        self.scale = min(
            screen.get_width() / BASE_WIDTH, screen.get_height() / BASE_HEIGHT
        )

        self.draw_width = int(BASE_WIDTH * self.scale)
        self.draw_height = int(BASE_HEIGHT * self.scale)

        self.offset_x = (screen.get_width() - self.draw_width) // 2

        self.offset_y = (screen.get_height() - self.draw_height) // 2

    def point(self, x, y):
        return (
            round(self.offset_x + x * self.scale),
            round(self.offset_y + y * self.scale),
        )

    def size(self, width, height):
        return (max(1, round(width * self.scale)), max(1, round(height * self.scale)))

    def rect(self, x, y, width, height):
        scaled_x, scaled_y = self.point(x, y)
        scaled_width, scaled_height = self.size(width, height)

        return pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)

    def font(self, size):
        return pygame.font.Font(None, max(1, round(size * self.scale)))

    def value(self, number):
        return max(1, round(number * self.scale))


def draw_button_feedback(
    screen,
    button_rect,
    base_color=None,
    border_radius=10,
    hover_color=(175, 190, 215),
    pressed_color=(135, 155, 190),
):
    mouse_position = pygame.mouse.get_pos()

    is_hovered = button_rect.collidepoint(mouse_position)
    is_pressed = is_hovered and pygame.mouse.get_pressed()[0]

    color = base_color

    if is_pressed:
        color = pressed_color
    elif is_hovered:
        color = hover_color

    if color is not None:
        pygame.draw.rect(screen, color, button_rect, border_radius=border_radius)


def draw_circle_feedback(
    screen,
    center,
    radius,
    normal_color=(255, 255, 255),
    hover_color=(175, 190, 215),
    pressed_color=(135, 155, 190),
):
    mouse_x, mouse_y = pygame.mouse.get_pos()

    distance_x = mouse_x - center[0]
    distance_y = mouse_y - center[1]

    is_hovered = distance_x**2 + distance_y**2 <= radius**2

    is_pressed = is_hovered and pygame.mouse.get_pressed()[0]

    if is_pressed:
        color = pressed_color
    elif is_hovered:
        color = hover_color
    else:
        color = normal_color

    pygame.draw.circle(screen, color, center, radius)
