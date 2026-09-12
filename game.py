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


def draw_heart(screen, x, y, color):
    pygame.draw.circle(screen, color, (x - 4, y - 3), 5)
    pygame.draw.circle(screen, color, (x + 4, y - 3), 5)

    pygame.draw.polygon(screen, color, [(x - 9, y - 2), (x + 9, y - 2), (x, y + 10)])


# ========================Show game func ===============================
def show_game(screen, user_name, level, total_coins):

    back_button = pygame.Rect(20, 20, 45, 38)

    level_font = pygame.font.Font(None, 30)

    progress_y = 80

    stations = [180, 290, 400]
    finish_x = 510

    score_font = pygame.font.Font(None, 30)

    lives = 3
    max_lives = 3

    progress_percent = 0
    checkpoint_percent = 0

    station_percents = [
        (station_x - stations[0]) / (finish_x - stations[0]) * 100
        for station_x in stations[1:]
    ]

    question_box = pygame.Rect(100, 120, 440, 180)
    answer_box = pygame.Rect(260, 320, 250, 90)
    time_box = pygame.Rect(120, 330, 70, 70)
    result_show_box = pygame.Rect(560, 120, 220, 250)

    player_answer = ""
    result_message = ""
    result_history = []
    history_scroll = 0
    earned_coins = 0

    question_text, correct_answer = question.create_question()

    result_color = (40, 50, 100)

    question_start_ticks = pygame.time.get_ticks()

    total_coins = coin.load_total_coins()

    profile_font = pygame.font.Font(None, 24)

    daily_font = pygame.font.Font(None, 15)

    more_button = pygame.Rect(735, 20, 30, 40)

    mistakes = 0

    user_name = player_data.load_user_name()

    profile_button = pygame.Rect(520, 15, 150, 50)

    daily_button = pygame.Rect(680, 20, 40, 50)

    show_leave_confirm = False

    leave_no_button = pygame.Rect(270, 330, 110, 45)
    leave_yes_button = pygame.Rect(420, 330, 110, 45)

    leave_confirm_font = pygame.font.Font(None, 30)
    leave_button_font = pygame.font.Font(None, 24)

    # =====================While Loop =============================================
    while True:
        screen.fill((245, 225, 255))

        # ===========back button============
        pygame.draw.rect(screen, (255, 255, 255), back_button, border_radius=12)

        arrow_color = (30, 80, 50)

        pygame.draw.line(screen, arrow_color, (55, 39), (31, 39), 4)
        pygame.draw.line(screen, arrow_color, (31, 39), (41, 29), 4)
        pygame.draw.line(screen, arrow_color, (31, 39), (41, 49), 4)

        # ------------level show-------------
        level_text = level_font.render(f"Level {level}", True, (40, 50, 100))

        screen.blit(level_text, (110, 25))

        # ---------------lives-------------
        for i in range(max_lives):
            if i < lives:
                heart_color = (220, 70, 90)
            else:
                heart_color = (70, 70, 70)

            draw_heart(screen, 110 + i * 24, 80, heart_color)

        # ----------------score ----------------
        coin_text = score_font.render(f"Total Coin: {total_coins}", True, (180, 120, 0))

        coin_rect = coin_text.get_rect(center=(400, 40))

        screen.blit(coin_text, coin_rect)

        # ----------------user profile-------------------
        profile_center = (640, 40)

        pygame.draw.circle(screen, (255, 255, 255), profile_center, 18)

        pygame.draw.circle(screen, (40, 50, 100), profile_center, 18, 2)

        if len(user_name) > 6:
            display_name = user_name[:6] + "..."
        else:
            display_name = user_name

        profile_text = profile_font.render(display_name, True, (40, 50, 100))

        profile_text_rect = profile_text.get_rect(
            midright=(profile_center[0] - 22, profile_center[1])
        )

        screen.blit(profile_text, profile_text_rect)

        # --------------daily----------------
        daily_center = (700, 40)

        pygame.draw.circle(screen, (255, 255, 255), daily_center, 18)

        pygame.draw.circle(screen, (235, 180, 40), daily_center, 18, 2)

        daily_text = daily_font.render("Daily", True, (40, 50, 100))

        daily_rect = daily_text.get_rect(center=(daily_center[0], 65))

        screen.blit(daily_text, daily_rect)

        # -----------------3 dots---------------
        for dot_y in [34, 40, 46]:
            pygame.draw.circle(screen, (40, 50, 100), (750, dot_y), 2)

        # ------------life line---------------
        pygame.draw.line(
            screen,
            (100, 110, 150),
            (stations[0], progress_y),
            (finish_x, progress_y),
            2,
        )

        for station_x in stations:
            pygame.draw.line(
                screen,
                (100, 110, 150),
                (station_x, progress_y - 10),
                (station_x, progress_y + 10),
                2,
            )

        flag_top = progress_y - 20
        cell_width = 6
        cell_height = 6

        pygame.draw.line(
            screen,
            (50, 50, 50),
            (finish_x, flag_top - 5),
            (finish_x, progress_y + 15),
            2,
        )

        flag_x = finish_x + 2
        flag_width = 20
        flag_height = 15

        pygame.draw.rect(
            screen, (255, 255, 255), (flag_x, flag_top, flag_width, flag_height)
        )

        pygame.draw.rect(
            screen, (50, 50, 50), (flag_x, flag_top, flag_width, flag_height), 2
        )

        for row in range(3):
            for column in range(4):
                if (row + column) % 2 == 0:
                    color = (30, 30, 30)
                else:
                    color = (255, 255, 255)

                pygame.draw.rect(
                    screen,
                    color,
                    (
                        flag_x + column * cell_width,
                        flag_top + row * cell_height,
                        cell_width,
                        cell_height,
                    ),
                )

        # -----------progress line-----------------
        progress_x = stations[0] + (finish_x - stations[0]) * progress_percent / 100

        pygame.draw.line(
            screen,
            (60, 180, 100),
            (stations[0], progress_y),
            (progress_x, progress_y),
            4,
        )

        # --------------question------------
        question.draw_question(screen, question_box, question_text)

        # ---------------answer--------------
        answer.draw_answer(screen, answer_box, player_answer)

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

            question_text, correct_answer = question.create_question()

            question_start_ticks = pygame.time.get_ticks()
            seconds_left = 15

        timing.draw_time(screen, time_box, seconds_left)

        # ---------------result show--------------
        result_show.draw_result(
            screen,
            result_show_box,
            result_message,
            result_color,
            earned_coins,
            result_history,
            history_scroll,
        )

        #  =========================== EVENT ===============================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if show_leave_confirm:
                    if leave_no_button.collidepoint(event.pos):
                        show_leave_confirm = False

                    elif leave_yes_button.collidepoint(event.pos):
                        return "back"

                    continue

                if back_button.collidepoint(event.pos):
                    show_leave_confirm = True

                if profile_button.collidepoint(event.pos):
                    user_name = profile.show_profile(
                        screen, user_name, level, total_coins, can_edit=False
                    )

                if daily_button.collidepoint(event.pos):
                    daily.show_daily(screen)

                if more_button.collidepoint(event.pos):
                    settings.show_settings(screen)

            if event.type == pygame.KEYDOWN:

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

                        question_text, correct_answer = question.create_question()
                        question_start_ticks = pygame.time.get_ticks()

                elif event.unicode.isdigit():
                    if len(player_answer) < 8:
                        player_answer += event.unicode

            if event.type == pygame.MOUSEWHEEL:
                if result_show_box.collidepoint(pygame.mouse.get_pos()):
                    previous_results = result_history[:-1]

                    max_scroll = max(0, len(previous_results) - 5)

                    history_scroll = max(0, min(max_scroll, history_scroll + event.y))

        if show_leave_confirm:
            confirm_box = pygame.Rect(180, 190, 440, 210)

            pygame.draw.rect(screen, (255, 255, 255), confirm_box, border_radius=15)

            pygame.draw.rect(screen, (100, 110, 150), confirm_box, 2, border_radius=15)

            confirm_text = leave_confirm_font.render(
                "Are you sure to leave the game?", True, (40, 50, 100)
            )

            screen.blit(confirm_text, confirm_text.get_rect(center=(400, 260)))

            pygame.draw.rect(screen, (180, 190, 220), leave_no_button, border_radius=10)

            pygame.draw.rect(screen, (220, 70, 90), leave_yes_button, border_radius=10)

            no_text = leave_button_font.render("No", True, (40, 50, 100))
            yes_text = leave_button_font.render("Yes", True, (255, 255, 255))

            screen.blit(no_text, no_text.get_rect(center=leave_no_button.center))
            screen.blit(yes_text, yes_text.get_rect(center=leave_yes_button.center))

        pygame.display.update()
