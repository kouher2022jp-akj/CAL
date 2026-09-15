import pygame
import screen_manager
import ui


def show_end_screen(screen, title, title_color, is_complete=False):
    ui_system = ui.UI(screen)

    if is_complete:
        right_button_text = "NEXT"
        right_action = "next"
    else:
        right_button_text = "REPLAY"
        right_action = "replay"

    while True:
        screen.fill((245, 245, 255))

        title_font = ui_system.font(60)
        button_font = ui_system.font(30)

        back_button = ui_system.rect(220, 330, 150, 55)
        replay_button = ui_system.rect(430, 330, 150, 55)

        title_text = title_font.render(title, True, title_color)

        title_rect = title_text.get_rect(center=ui_system.point(400, 200))

        screen.blit(title_text, title_rect)

        ui.draw_button_feedback(
            screen,
            back_button,
            base_color=(255, 255, 255),
            border_radius=ui_system.value(15),
        )

        pygame.draw.rect(
            screen,
            (100, 110, 150),
            back_button,
            ui_system.value(2),
            border_radius=ui_system.value(15),
        )

        ui.draw_button_feedback(
            screen,
            replay_button,
            base_color=(60, 180, 100),
            hover_color=(75, 195, 115),
            pressed_color=(45, 140, 75),
            border_radius=ui_system.value(15),
        )

        back_text = button_font.render("BACK", True, (40, 50, 100))

        replay_text = button_font.render(right_button_text, True, (255, 255, 255))

        screen.blit(back_text, back_text.get_rect(center=back_button.center))

        screen.blit(replay_text, replay_text.get_rect(center=replay_button.center))

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
                    return "back"

                if replay_button.collidepoint(game_position):
                    return right_action

        pygame.display.update()
