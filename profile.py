import pygame
import player_data


def show_profile(screen, user_name, current_level, total_coins, can_edit=True):

    back_button = pygame.Rect(20, 20, 45, 38)

    title_font = pygame.font.Font(None, 45)
    info_font = pygame.font.Font(None, 30)

    avatar_box = pygame.Rect(80, 170, 130, 130)

    name_box = pygame.Rect(250, 150, 330, 45)

    editing_name = False
    name_input = user_name

    delete_button = pygame.Rect(610, 440, 160, 40)
    show_delete_confirm = False

    confirm_font = pygame.font.Font(None, 30)
    button_font = pygame.font.Font(None, 24)

    no_button = pygame.Rect(270, 330, 110, 45)
    yes_button = pygame.Rect(420, 330, 110, 45)

    warning_start_ticks = None

    while True:
        screen.fill((245, 225, 255))

        pygame.draw.rect(screen, (255, 255, 255), back_button, border_radius=12)

        arrow_color = (30, 80, 50)

        pygame.draw.line(screen, arrow_color, (55, 39), (31, 39), 4)
        pygame.draw.line(screen, arrow_color, (31, 39), (41, 29), 4)
        pygame.draw.line(screen, arrow_color, (31, 39), (41, 49), 4)

        title_text = title_font.render("Profile", True, (40, 50, 100))

        screen.blit(title_text, (330, 70))

        pygame.draw.rect(screen, (255, 255, 255), avatar_box, border_radius=20)

        pygame.draw.rect(screen, (40, 50, 100), avatar_box, 2, border_radius=20)

        level_text = info_font.render(f"Level: {current_level}", True, (40, 50, 100))

        coin_text = info_font.render(f"Total Coin: {total_coins}", True, (180, 120, 0))

        sticker_text = info_font.render("Stickers: []", True, (40, 50, 100))

        if editing_name:
            name_border_color = (60, 180, 100)
        else:
            name_border_color = (100, 110, 150)

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            name_box,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            name_border_color,
            name_box,
            2,
            border_radius=10
        )

        user_text = info_font.render(
            f"User Name: {name_input}",
            True,
            (40, 50, 100)
        )

        screen.blit(
            user_text,
            (name_box.x + 10, name_box.y + 12)
        )
        screen.blit(level_text, (260, 215))
        screen.blit(coin_text, (260, 260))
        screen.blit(sticker_text, (80, 350))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if show_delete_confirm:
                    if no_button.collidepoint(event.pos):
                        show_delete_confirm = False

                    elif yes_button.collidepoint(event.pos):
                        new_user_name = player_data.delete_account()
                        return new_user_name

                    continue

                if back_button.collidepoint(event.pos):
                    return user_name

                if name_box.collidepoint(event.pos):
                    if can_edit:
                        editing_name = True

                        if name_input == "User Name":
                            name_input = ""
                    else:
                        warning_start_ticks = pygame.time.get_ticks()

                if delete_button.collidepoint(event.pos):
                    if can_edit:
                        show_delete_confirm = True
                    else:
                        warning_start_ticks = pygame.time.get_ticks()

            if event.type == pygame.KEYDOWN:
                if editing_name:
                    if event.key == pygame.K_RETURN:
                        if 2 <= len(name_input.strip()) <= 15:
                            user_name = name_input.strip()
                            player_data.save_user_name(user_name)

                        editing_name = False

                    elif event.key == pygame.K_BACKSPACE:
                        name_input = name_input[:-1]

                    elif event.unicode.isprintable():
                        if len(name_input) < 15:
                            name_input += event.unicode

        pygame.draw.rect(
            screen,
            (220, 70, 90),
            delete_button,
            border_radius=10
        )

        # ----------------delete-------------------

        delete_text = button_font.render(
            "Delete Account",
            True,
            (255, 255, 255)
        )

        screen.blit(
            delete_text,
            delete_text.get_rect(center=delete_button.center)
        )

        # ----------delete comfirm---------------

        if show_delete_confirm:
            confirm_box = pygame.Rect(180, 190, 440, 210)

            pygame.draw.rect(
                screen,
                (255, 255, 255),
                confirm_box,
                border_radius=15
            )

            pygame.draw.rect(
                screen,
                (100, 110, 150),
                confirm_box,
                2,
                border_radius=15
            )

            line1 = confirm_font.render(
                "Do you want to delete",
                True,
                (40, 50, 100)
            )

            line2 = confirm_font.render(
                "your account?",
                True,
                (40, 50, 100)
            )

            screen.blit(line1, line1.get_rect(center=(400, 245)))
            screen.blit(line2, line2.get_rect(center=(400, 275)))

            pygame.draw.rect(screen, (180, 190, 220), no_button, border_radius=10)
            pygame.draw.rect(screen, (220, 70, 90), yes_button, border_radius=10)

            no_text = button_font.render("No", True, (40, 50, 100))
            yes_text = button_font.render("Yes", True, (255, 255, 255))

            screen.blit(no_text, no_text.get_rect(center=no_button.center))
            screen.blit(yes_text, yes_text.get_rect(center=yes_button.center))

        if (
            warning_start_ticks is not None
            and pygame.time.get_ticks() - warning_start_ticks < 3000
        ):
            warning_font = pygame.font.Font(None, 32)

            warning_text = warning_font.render(
                "You can not edit during game!",
                True,
                (220, 70, 90)
            )

            warning_rect = warning_text.get_rect(
                center=(screen.get_width() // 2, screen.get_height() // 2)
            )

            screen.blit(warning_text, warning_rect)

        pygame.display.update()
