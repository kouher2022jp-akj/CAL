import pygame


def get_seconds_left(start_ticks, limit_seconds=15):
    elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000

    return max(0, limit_seconds - elapsed_seconds)


def draw_time(screen, ui_system, time_box, seconds_left):
    if seconds_left >= 8:
        border_color = (60, 180, 100)

    elif seconds_left >= 4:
        border_color = (240, 170, 50)

    else:
        border_color = (220, 70, 90)

    pygame.draw.rect(
        screen, (255, 255, 255), time_box, border_radius=ui_system.value(15)
    )

    pygame.draw.rect(
        screen,
        border_color,
        time_box,
        ui_system.value(4),
        border_radius=ui_system.value(15),
    )

    time_font = ui_system.font(35)

    time_text = time_font.render(f"{seconds_left}", True, (40, 50, 100))

    time_rect = time_text.get_rect(center=time_box.center)

    screen.blit(time_text, time_rect)
