import pygame
import screen_manager
import ui


def show_settings(screen):
    ui_system = ui.UI(screen)

    back_icon_source = pygame.image.load("assets/back_1.png").convert_alpha()

    while True:
        back_button = ui_system.rect(20, 20, 45, 38)

        back_icon = pygame.transform.smoothscale(
            back_icon_source, ui_system.size(24, 24)
        )

        title_font = ui_system.font(45)

        screen.fill((245, 225, 255))

        ui.draw_button_feedback(
            screen,
            back_button,
            base_color=None,
            border_radius=ui_system.value(12),
        )

        icon_rect = back_icon.get_rect(center=back_button.center)

        screen.blit(back_icon, icon_rect)

        title_text = title_font.render("Settings", True, (40, 50, 100))

        screen.blit(title_text, ui_system.point(320, 70))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    screen = screen_manager.toggle_display_mode()
                    ui_system = ui.UI(screen)
                    continue

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                game_position = screen_manager.get_event_game_position(event)

                if back_button.collidepoint(game_position):
                    return

        pygame.display.update()
