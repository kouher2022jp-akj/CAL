import pygame


def show_settings(screen):
    back_button = pygame.Rect(20, 20, 45, 38)

    title_font = pygame.font.Font(None, 45)

    while True:
        screen.fill((245, 225, 255))

        pygame.draw.rect(screen, (255, 255, 255), back_button, border_radius=12)

        arrow_color = (30, 80, 50)

        pygame.draw.line(screen, arrow_color, (55, 39), (31, 39), 4)
        pygame.draw.line(screen, arrow_color, (31, 39), (41, 29), 4)
        pygame.draw.line(screen, arrow_color, (31, 39), (41, 49), 4)

        title_text = title_font.render("Settings", True, (40, 50, 100))

        screen.blit(title_text, (320, 70))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return

        pygame.display.update()
