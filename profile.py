import pygame
import player_data
import screen_manager
import ui


def show_profile(screen, user_name, current_level, total_coins, can_edit=True):
    ui_system = ui.UI(screen)

    back_icon_source = pygame.image.load("assets/back_1.png").convert_alpha()

    editing_name = False
    name_input = user_name
    show_delete_confirm = False
    warning_start_ticks = None

    while True:
        back_button = ui_system.rect(20, 20, 45, 38)

        avatar_box = ui_system.rect(80, 170, 130, 130)
        name_box = ui_system.rect(250, 150, 330, 45)

        delete_button = ui_system.rect(610, 440, 160, 40)

        no_button = ui_system.rect(270, 330, 110, 45)
        yes_button = ui_system.rect(420, 330, 110, 45)

        back_icon = pygame.transform.smoothscale(
            back_icon_source, ui_system.size(24, 24)
        )

        title_font = ui_system.font(45)
        info_font = ui_system.font(30)
        confirm_font = ui_system.font(30)
        button_font = ui_system.font(24)

        screen.fill((245, 225, 255))

        # ---------------- Back ----------------

        ui.draw_button_feedback(
            screen,
            back_button,
            base_color=None,
            border_radius=ui_system.value(12),
        )

        icon_rect = back_icon.get_rect(center=back_button.center)

        screen.blit(back_icon, icon_rect)

        # ---------------- Title ----------------

        title_text = title_font.render("Profile", True, (40, 50, 100))

        screen.blit(title_text, ui_system.point(330, 70))

        # ---------------- Avatar ---------------

        pygame.draw.rect(
            screen, (255, 255, 255), avatar_box, border_radius=ui_system.value(20)
        )

        pygame.draw.rect(
            screen,
            (40, 50, 100),
            avatar_box,
            ui_system.value(2),
            border_radius=ui_system.value(20),
        )

        # ---------------- Information ----------

        if editing_name:
            name_border_color = (60, 180, 100)
        else:
            name_border_color = (100, 110, 150)

        pygame.draw.rect(
            screen, (255, 255, 255), name_box, border_radius=ui_system.value(10)
        )

        pygame.draw.rect(
            screen,
            name_border_color,
            name_box,
            ui_system.value(2),
            border_radius=ui_system.value(10),
        )

        user_text = info_font.render(f"User Name: {name_input}", True, (40, 50, 100))

        screen.blit(
            user_text,
            (name_box.x + ui_system.value(10), name_box.y + ui_system.value(12)),
        )

        level_text = info_font.render(f"Level: {current_level}", True, (40, 50, 100))

        coin_text = info_font.render(f"Total Coin: {total_coins}", True, (180, 120, 0))

        sticker_text = info_font.render("Stickers: []", True, (40, 50, 100))

        screen.blit(level_text, ui_system.point(260, 215))
        screen.blit(coin_text, ui_system.point(260, 260))
        screen.blit(sticker_text, ui_system.point(80, 350))

        # ------------- Delete button ----------

        ui.draw_button_feedback(
            screen,
            delete_button,
            base_color=(220, 70, 90),
            hover_color=(235, 95, 110),
            pressed_color=(170, 45, 60),
            border_radius=ui_system.value(10),
        )

        delete_text = button_font.render("Delete Account", True, (255, 255, 255))

        screen.blit(delete_text, delete_text.get_rect(center=delete_button.center))

        # -------- Delete confirmation ----------

        if show_delete_confirm:
            confirm_box = ui_system.rect(180, 190, 440, 210)

            pygame.draw.rect(
                screen, (255, 255, 255), confirm_box, border_radius=ui_system.value(15)
            )

            pygame.draw.rect(
                screen,
                (100, 110, 150),
                confirm_box,
                ui_system.value(2),
                border_radius=ui_system.value(15),
            )

            line1 = confirm_font.render("Do you want to delete", True, (40, 50, 100))

            line2 = confirm_font.render("your account?", True, (40, 50, 100))

            screen.blit(line1, line1.get_rect(center=ui_system.point(400, 245)))

            screen.blit(line2, line2.get_rect(center=ui_system.point(400, 275)))

            ui.draw_button_feedback(
                screen,
                no_button,
                base_color=(180, 190, 220),
                hover_color=(150, 165, 205),
                pressed_color=(120, 135, 180),
                border_radius=ui_system.value(10),
            )

            ui.draw_button_feedback(
                screen,
                yes_button,
                base_color=(220, 70, 90),
                hover_color=(235, 95, 110),
                pressed_color=(170, 45, 60),
                border_radius=ui_system.value(10),
            )

            no_text = button_font.render("No", True, (40, 50, 100))

            yes_text = button_font.render("Yes", True, (255, 255, 255))

            screen.blit(no_text, no_text.get_rect(center=no_button.center))

            screen.blit(yes_text, yes_text.get_rect(center=yes_button.center))

        # ---------------- Warning --------------

        if (
            warning_start_ticks is not None
            and pygame.time.get_ticks() - warning_start_ticks < 3000
        ):
            warning_font = ui_system.font(32)

            warning_text = warning_font.render(
                "You can not edit during game!", True, (220, 70, 90)
            )

            warning_rect = warning_text.get_rect(center=ui_system.point(400, 250))

            screen.blit(warning_text, warning_rect)

        # ---------------- Events ---------------

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

                if show_delete_confirm:
                    if no_button.collidepoint(game_position):
                        show_delete_confirm = False

                    elif yes_button.collidepoint(game_position):
                        new_user_name = player_data.delete_account()

                        return new_user_name

                    continue

                if back_button.collidepoint(game_position):
                    return user_name

                if name_box.collidepoint(game_position):
                    if can_edit:
                        editing_name = True

                        if name_input == "User Name":
                            name_input = ""

                    else:
                        warning_start_ticks = pygame.time.get_ticks()

                if delete_button.collidepoint(game_position):
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

        pygame.display.update()
