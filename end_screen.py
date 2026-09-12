import pygame


def show_end_screen(screen, title, title_color, is_complete=False):
    title_font = pygame.font.Font(None, 60)
    button_font = pygame.font.Font(None, 30)

    screen_width = screen.get_width()

    back_button = pygame.Rect(screen_width // 2 - 180, 330, 150, 55)

    replay_button = pygame.Rect(screen_width // 2 + 30, 330, 150, 55)

    if is_complete:
        right_button_text = "NEXT"
        right_action = "next"
    else:
        right_button_text = "REPLAY"
        right_action = "replay"

    while True:
        screen.fill((245, 245, 255))

        title_text = title_font.render(title, True, title_color)

        title_rect = title_text.get_rect(center=(screen_width // 2, 200))

        screen.blit(title_text, title_rect)

        pygame.draw.rect(screen, (255, 255, 255), back_button, border_radius=15)

        pygame.draw.rect(screen, (100, 110, 150), back_button, 2, border_radius=15)

        pygame.draw.rect(screen, (60, 180, 100), replay_button, border_radius=15)

        back_text = button_font.render("BACK", True, (40, 50, 100))

        replay_text = button_font.render(right_button_text, True, (255, 255, 255))

        screen.blit(back_text, back_text.get_rect(center=back_button.center))

        screen.blit(replay_text, replay_text.get_rect(center=replay_button.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return "back"

                if replay_button.collidepoint(event.pos):
                    return right_action

        pygame.display.update()
