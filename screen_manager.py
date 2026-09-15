import pygame

GAME_WIDTH = 800
GAME_HEIGHT = 500

is_fullscreen = True


def create_game_surface():
    return pygame.display.get_surface()


def present(screen):
    pygame.display.update()


def to_game_position(mouse_position):
    return mouse_position


def get_event_game_position(event):
    window = pygame.display.get_surface()

    if event.type == pygame.MOUSEBUTTONDOWN:
        return event.pos

    if event.type == pygame.FINGERDOWN:
        return (int(event.x * window.get_width()), int(event.y * window.get_height()))

    return None


def toggle_display_mode():
    global is_fullscreen

    if is_fullscreen:
        pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), pygame.RESIZABLE)
    else:
        desktop_width, desktop_height = pygame.display.get_desktop_sizes()[0]

        pygame.display.set_mode((desktop_width, desktop_height), pygame.NOFRAME)

    is_fullscreen = not is_fullscreen

    return pygame.display.get_surface()
