import pygame


def draw_answer(screen, answer_box, player_answer):
    pygame.draw.rect(screen, (255, 255, 255), answer_box, border_radius=15)

    pygame.draw.rect(screen, (100, 110, 150), answer_box, 2, border_radius=15)

    label_font = pygame.font.Font(None, 28)

    label = label_font.render(
        "Ans:",
        True,
        (40, 50, 100)
    )

    screen.blit(
        label,
        (answer_box.x + 15, answer_box.y + 30)
    )

    answer_font = pygame.font.Font(None, 45)

    answer_text = answer_font.render(player_answer, True, (40, 50, 100))

    screen.blit(answer_text, (answer_box.x + 80, answer_box.y + 30))
