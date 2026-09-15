import pygame
import question
import answer
import result_show
import timing
import end_screen
import coin
import progress
import profile
import daily
import settings
import player_data
import screen_manager
import ui


def draw_heart(screen, ui_system, x, y, color):
    center_x, center_y = ui_system.point(x, y)

    pygame.draw.circle(
        screen,
        color,
        (center_x - ui_system.value(4), center_y - ui_system.value(3)),
        ui_system.value(5),
    )

    pygame.draw.circle(
        screen,
        color,
        (center_x + ui_system.value(4), center_y - ui_system.value(3)),
        ui_system.value(5),
    )

    pygame.draw.polygon(
        screen,
        color,
        [
            (center_x - ui_system.value(9), center_y - ui_system.value(2)),
            (center_x + ui_system.value(9), center_y - ui_system.value(2)),
            (center_x, center_y + ui_system.value(10)),
        ],
    )


# ========================Show game func ===============================
def show_game(screen, user_name, level, total_coins):

    ui_system = ui.UI(screen)

    back_icon_source = pygame.image.load("assets/back_1.png").convert_alpha()

    back_icon = pygame.transform.smoothscale(back_icon_source, ui_system.size(24, 24))

    back_button = ui_system.rect(20, 20, 45, 38)

    level_font = ui_system.font(30)
    score_font = ui_system.font(30)
    profile_font = ui_system.font(24)
    daily_font = ui_system.font(15)

    question_box = ui_system.rect(100, 120, 440, 180)
    answer_box = ui_system.rect(260, 320, 250, 90)
    time_box = ui_system.rect(120, 330, 70, 70)
    result_show_box = ui_system.rect(560, 120, 220, 250)

    profile_button = ui_system.rect(540, 15, 120, 50)
    daily_button = ui_system.rect(680, 20, 40, 50)
    more_button = ui_system.rect(735, 20, 30, 40)

    leave_no_button = ui_system.rect(270, 330, 110, 45)
    leave_yes_button = ui_system.rect(420, 330, 110, 45)

    leave_confirm_font = ui_system.font(30)
    leave_button_font = ui_system.font(24)

    progress_y = 80

    stations = [180, 290, 400]
    finish_x = 510

    lives = 3
    max_lives = 3

    progress_percent = 0
    checkpoint_percent = 0

    station_percents = [
        (station_x - stations[0]) / (finish_x - stations[0]) * 100
        for station_x in stations[1:]
    ]

    player_answer = ""
    result_message = ""
    result_history = []
    history_scroll = 0
    earned_coins = 0

    question_text, correct_answer = question.create_question(level)

    result_color = (40, 50, 100)

    question_start_ticks = pygame.time.get_ticks()

    total_coins = coin.load_total_coins()

    mistakes = 0

    user_name = player_data.load_user_name()

    show_leave_confirm = False

    # =====================While Loop =============================================
    while True:
        screen.fill((245, 225, 255))

        # ===============bottom===============
        bottom_menu_bar = ui_system.rect(0, 440, 800, 80)

        bottom_bar_surface = pygame.Surface(
            bottom_menu_bar.size,
            pygame.SRCALPHA,
        )

        bottom_bar_surface.fill((255, 255, 255, 150))

        screen.blit(bottom_bar_surface, bottom_menu_bar.topleft)

        pygame.draw.line(
            screen,
            (255, 255, 255),
            bottom_menu_bar.topleft,
            (bottom_menu_bar.right, bottom_menu_bar.top),
            ui_system.value(1),
        )

        # =========== Back button ============

        ui.draw_button_feedback(
            screen,
            back_button,
            base_color=None,
            border_radius=ui_system.value(12),
        )

        icon_rect = back_icon.get_rect(
            center=back_button.center
        )

        screen.blit(back_icon, icon_rect)

        # ------------ Level title ------------

        level_text = level_font.render(f"Level {level}", True, (40, 50, 100))

        screen.blit(level_text, ui_system.point(110, 25))

        # --------------- Lives ---------------

        for i in range(max_lives):
            if i < lives:
                heart_color = (220, 70, 90)
            else:
                heart_color = (70, 70, 70)

            draw_heart(screen, ui_system, 110 + i * 24, 80, heart_color)

        # -------------- Total coin ------------

        coin_text = score_font.render(f"Total Coin: {total_coins}", True, (180, 120, 0))

        coin_rect = coin_text.get_rect(center=ui_system.point(400, 40))

        screen.blit(coin_text, coin_rect)

        # ---------------- Profile -------------

        profile_center = ui_system.point(640, 40)

        ui.draw_button_feedback(
            screen,
            profile_button,
            base_color=None,
            border_radius=ui_system.value(12),
        )

        pygame.draw.circle(screen, (255, 255, 255), profile_center, ui_system.value(18))

        pygame.draw.circle(
            screen,
            (40, 50, 100),
            profile_center,
            ui_system.value(18),
            ui_system.value(2),
        )

        if len(user_name) > 6:
            display_name = user_name[:6] + "..."
        else:
            display_name = user_name

        profile_text = profile_font.render(display_name, True, (40, 50, 100))

        profile_text_rect = profile_text.get_rect(midright=ui_system.point(618, 40))

        screen.blit(profile_text, profile_text_rect)

        # ---------------- Daily ---------------

        daily_center = ui_system.point(700, 40)

        ui.draw_button_feedback(
            screen,
            daily_button,
            base_color=None,
            border_radius=ui_system.value(12),
        )

        pygame.draw.circle(screen, (255, 255, 255), daily_center, ui_system.value(18))

        pygame.draw.circle(
            screen,
            (235, 180, 40),
            daily_center,
            ui_system.value(18),
            ui_system.value(2),
        )

        daily_text = daily_font.render("Daily", True, (40, 50, 100))

        daily_rect = daily_text.get_rect(center=ui_system.point(700, 65))

        screen.blit(daily_text, daily_rect)

        # ---------------- 3 dots -------------
        ui.draw_button_feedback(
            screen,
            more_button,
            base_color=None,
            border_radius=ui_system.value(12),
        )

        for dot_y in [34, 40, 46]:
            pygame.draw.circle(
                screen, (40, 50, 100), ui_system.point(750, dot_y), ui_system.value(2)
            )

        # ------------- Progress line ----------

        pygame.draw.line(
            screen,
            (100, 110, 150),
            ui_system.point(stations[0], progress_y),
            ui_system.point(finish_x, progress_y),
            ui_system.value(2),
        )

        for station_x in stations:
            pygame.draw.line(
                screen,
                (100, 110, 150),
                ui_system.point(station_x, progress_y - 10),
                ui_system.point(station_x, progress_y + 10),
                ui_system.value(2),
            )

        flag_top = progress_y - 20
        cell_width = 6
        cell_height = 6

        pygame.draw.line(
            screen,
            (50, 50, 50),
            ui_system.point(finish_x, flag_top - 5),
            ui_system.point(finish_x, progress_y + 15),
            ui_system.value(2),
        )

        flag_x = finish_x + 2
        flag_width = 20
        flag_height = 15

        flag_rect = ui_system.rect(flag_x, flag_top, flag_width, flag_height)

        pygame.draw.rect(screen, (255, 255, 255), flag_rect)

        pygame.draw.rect(screen, (50, 50, 50), flag_rect, ui_system.value(2))

        for row in range(3):
            for column in range(4):
                if (row + column) % 2 == 0:
                    color = (30, 30, 30)
                else:
                    color = (255, 255, 255)

                cell_rect = ui_system.rect(
                    flag_x + column * cell_width,
                    flag_top + row * cell_height,
                    cell_width,
                    cell_height,
                )

                pygame.draw.rect(screen, color, cell_rect)

        progress_x = stations[0] + (finish_x - stations[0]) * progress_percent / 100 #progress

        pygame.draw.line(
            screen,
            (60, 180, 100),
            ui_system.point(stations[0], progress_y),
            ui_system.point(progress_x, progress_y),
            ui_system.value(4),
        )

        # --------------question------------
        question.draw_question(screen, ui_system, question_box, question_text)

        # ---------------answer--------------
        answer.draw_answer(screen, ui_system, answer_box, player_answer)

        # ---------------timing--------------
        seconds_left = timing.get_seconds_left(question_start_ticks)

        if seconds_left == 0:
            lives = max(0, lives - 1)

            earned_coins = 0
            result_message = question_text
            result_color = (220, 70, 90)

            result_history.append((result_message, result_color, earned_coins))

            if lives == 0:
                return end_screen.show_end_screen(screen, "Game Over", (220, 70, 90))
            progress_percent = checkpoint_percent

            player_answer = ""
            history_scroll = 0

            question_text, correct_answer = question.create_question(level)

            question_start_ticks = pygame.time.get_ticks()
            seconds_left = 15

        timing.draw_time(screen, ui_system, time_box, seconds_left)

        # ---------------result show--------------
        result_show.draw_result(
            screen,
            ui_system,
            result_show_box,
            result_message,
            result_color,
            earned_coins,
            result_history,
            history_scroll,
        )

        #  =========================== EVENT ===============================
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    screen = screen_manager.toggle_display_mode()
                    ui_system = ui.UI(screen)

                    back_icon = pygame.transform.smoothscale(
                        back_icon_source,
                        ui_system.size(24, 24)
                    )

                    back_button = ui_system.rect(20, 20, 45, 38)

                    level_font = ui_system.font(30)
                    score_font = ui_system.font(30)
                    profile_font = ui_system.font(24)
                    daily_font = ui_system.font(15)

                    question_box = ui_system.rect(100, 120, 440, 180)
                    answer_box = ui_system.rect(260, 320, 250, 90)
                    time_box = ui_system.rect(120, 330, 70, 70)

                    result_show_box = ui_system.rect(
                        560, 120, 220, 250
                    )

                    profile_button = ui_system.rect(520, 15, 150, 50)
                    daily_button = ui_system.rect(680, 20, 40, 50)
                    more_button = ui_system.rect(735, 20, 30, 40)

                    leave_no_button = ui_system.rect(270, 330, 110, 45)
                    leave_yes_button = ui_system.rect(420, 330, 110, 45)

                    leave_confirm_font = ui_system.font(30)
                    leave_button_font = ui_system.font(24)

                    continue

                if event.key == pygame.K_UP:
                    previous_results = result_history[:-1]
                    max_scroll = max(0, len(previous_results) - 5)

                    history_scroll = min(max_scroll, history_scroll + 1)

                elif event.key == pygame.K_DOWN:
                    history_scroll = max(0, history_scroll - 1)
                if event.key == pygame.K_BACKSPACE:
                    player_answer = player_answer[:-1]

                elif event.key == pygame.K_RETURN:
                    if player_answer != "":
                        submitted_question = question_text.replace("?", player_answer)

                        if int(player_answer) == correct_answer:
                            result_message = submitted_question
                            result_color = (50, 170, 90)

                            earned_coins = coin.calculate_coins(question_start_ticks)

                            total_coins = coin.add_coins(total_coins, earned_coins)

                            progress_percent = progress.increase(
                                progress_percent, earned_coins
                            )

                            for station_percent in station_percents:
                                if progress_percent >= station_percent:
                                    checkpoint_percent = station_percent

                            if progress_percent >= 100:
                                return end_screen.show_end_screen(
                                    screen, "Level Complete!", (60, 180, 100), True
                                )

                        else:
                            result_message = submitted_question
                            result_color = (220, 70, 90)

                            time_percent = coin.calculate_coins(question_start_ticks)

                            progress_percent = progress.decrease(
                                progress_percent, time_percent
                            )

                            earned_coins = 0

                            mistakes += 1

                            if mistakes >= 3:
                                lives = max(0, lives - 1)
                                mistakes = 0

                                if lives > 0:
                                    progress_percent = checkpoint_percent

                        result_history.append(
                            (result_message, result_color, earned_coins)
                        )

                        if lives < 1:
                            return end_screen.show_end_screen(
                                screen, "Game Over", (220, 70, 90)
                            )

                        player_answer = ""

                        question_text, correct_answer = question.create_question(level)
                        question_start_ticks = pygame.time.get_ticks()

                elif event.unicode.isdigit():
                    if len(player_answer) < 8:

                        player_answer += event.unicode

            if event.type in (
                pygame.MOUSEBUTTONDOWN,
                pygame.FINGERDOWN
            ):
                game_position = screen_manager.get_event_game_position(
                    event
                )

                if show_leave_confirm:
                    if leave_no_button.collidepoint(game_position):
                        show_leave_confirm = False

                    elif leave_yes_button.collidepoint(game_position):
                        return "back"

                    continue

                if back_button.collidepoint(game_position):
                    show_leave_confirm = True

                if profile_button.collidepoint(game_position):
                    user_name = profile.show_profile(
                        screen, user_name, level, total_coins, can_edit=False
                    )

                if daily_button.collidepoint(game_position):
                    daily.show_daily(screen)

                if more_button.collidepoint(game_position):
                    settings.show_settings(screen)

            if event.type == pygame.MOUSEWHEEL:
                if result_show_box.collidepoint(pygame.mouse.get_pos()):
                    previous_results = result_history[:-1]

                    max_scroll = max(0, len(previous_results) - 5)

                    history_scroll = max(0, min(max_scroll, history_scroll + event.y))

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if show_leave_confirm:
            confirm_box = ui_system.rect(
                180, 190, 440, 210
            )

            pygame.draw.rect(
                screen,
                (255, 255, 255),
                confirm_box,
                border_radius=ui_system.value(15)
            )

            pygame.draw.rect(
                screen,
                (100, 110, 150),
                confirm_box,
                ui_system.value(2),
                border_radius=ui_system.value(15)
            )

            confirm_text = leave_confirm_font.render(
                "Are you sure to leave the game?",
                True,
                (40, 50, 100)
            )

            screen.blit(
                confirm_text,
                confirm_text.get_rect(
                    center=ui_system.point(400, 260)
                )
            )

            ui.draw_button_feedback(
                screen,
                leave_no_button,
                base_color=(180, 190, 220),
                hover_color=(150, 165, 205),
                pressed_color=(120, 135, 180),
                border_radius=ui_system.value(10),
            )

            ui.draw_button_feedback(
                screen,
                leave_yes_button,
                base_color=(220, 70, 90),
                hover_color=(235, 95, 110),
                pressed_color=(170, 45, 60),
                border_radius=ui_system.value(10),
            )

            no_text = leave_button_font.render(
                "No",
                True,
                (40, 50, 100)
            )

            yes_text = leave_button_font.render(
                "Yes",
                True,
                (255, 255, 255)
            )

            screen.blit(
                no_text,
                no_text.get_rect(
                    center=leave_no_button.center
                )
            )

            screen.blit(
                yes_text,
                yes_text.get_rect(
                    center=leave_yes_button.center
                )
            )

        screen_manager.present(screen)
