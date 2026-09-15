import pygame


def draw_answer(screen, ui_system, answer_box, player_answer):
    pygame.draw.rect(
        screen, (255, 255, 255), answer_box, border_radius=ui_system.value(15)
    )

    pygame.draw.rect(
        screen,
        (100, 110, 150),
        answer_box,
        ui_system.value(2),
        border_radius=ui_system.value(15),
    )

    label_font = ui_system.font(28)

    label = label_font.render("Ans:", True, (40, 50, 100))

    screen.blit(
        label, (answer_box.x + ui_system.value(15), answer_box.y + ui_system.value(30))
    )

    answer_font = ui_system.font(45)

    answer_text = answer_font.render(player_answer, True, (40, 50, 100))

    screen.blit(
        answer_text,
        (answer_box.x + ui_system.value(80), answer_box.y + ui_system.value(30)),
    )
