import pygame


def draw_result(
    screen,
    result_box,
    result_message,
    result_color,
    earned_coins,
    result_history,
    history_scroll,
):

    pygame.draw.rect(screen, (255, 255, 255), result_box, border_radius=15)

    pygame.draw.rect(screen, (100, 110, 0), result_box, 1, border_radius=15)

    coin_column_x = result_box.x + int(result_box.width * 0.7)
    header_bottom = result_box.y + 35

    pygame.draw.line(
        screen,
        (180, 190, 220),
        (result_box.x, header_bottom),
        (result_box.right, header_bottom),
        2,
    )

    pygame.draw.line(
        screen,
        (180, 190, 220),
        (coin_column_x, result_box.y),
        (coin_column_x, result_box.bottom),
        2,
    )

    title_font = pygame.font.Font(None, 20)

    recent_title = title_font.render("Recent Answers", True, (40, 50, 100))

    recent_rect = recent_title.get_rect(
        center=(result_box.x + (coin_column_x - result_box.x) // 2, result_box.y + 17)
    )

    screen.blit(recent_title, recent_rect)

    coin_title = title_font.render("Coin", True, (40, 50, 100))

    coin_rect = coin_title.get_rect(
        center=(coin_column_x + (result_box.right - coin_column_x) // 2, result_box.y + 17)
    )

    screen.blit(coin_title, coin_rect)

    latest_font = pygame.font.Font(None, 35)

    latest_text = latest_font.render(result_message, True, result_color)

    latest_rect = latest_text.get_rect(
        center=(result_box.x + (coin_column_x - result_box.x) // 2, header_bottom + 35)
    )

    screen.blit(latest_text, latest_rect)

    if result_message != "":
        if earned_coins == 0:
            coin_message = "0"
            coin_color = (50, 50, 50)
        else:
            coin_message = f"+{earned_coins}"
            coin_color = (240, 170, 50)

        latest_coin_text = latest_font.render(coin_message, True, coin_color)

        latest_coin_rect = latest_coin_text.get_rect(
            center=(
                coin_column_x + (result_box.right - coin_column_x) // 2,
                latest_rect.centery,
            )
        )

        screen.blit(latest_coin_text, latest_coin_rect)

    history_font = pygame.font.Font(None, 22)

    previous_results = result_history[:-1]

    end_index = len(previous_results) - history_scroll
    start_index = max(0, end_index - 5)

    visible_history = previous_results[start_index:end_index]

    for index, (message, color, coins) in enumerate(
        reversed(visible_history)
    ):
        history_text = history_font.render(
            message,
            True,
            color
        )

        history_y = header_bottom + 70 + index * 27

        screen.blit(
            history_text,
            (result_box.x + 12, history_y)
        )

        if coins >= 0:
            if coins == 0:
                coin_message = "0"
                coin_color = (50, 50, 50)
            else:
                coin_message = f"+{coins}"
                coin_color = (240, 170, 50)

            history_coin_text = history_font.render(coin_message, True, coin_color)

            history_coin_rect = history_coin_text.get_rect(
                center=(
                    coin_column_x
                    + (result_box.right - coin_column_x) // 2,
                    history_y + 10
                )
            )

            screen.blit(history_coin_text, history_coin_rect)
