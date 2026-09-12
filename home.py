import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"


import pygame
import sys
import level
import profile
import daily
import settings
import coin
import player_data
import game

pygame.init()

screen = pygame.display.set_mode((800, 500))  # w/h
pygame.display.set_caption("Cal Game")

title_font = pygame.font.Font(None, 70)  # None= no font

play_button = pygame.Rect(
    screen.get_width() - 180, screen.get_height() - 130, 140, 50
)  # (x, y, ความกว้าง, ความสูง)

button_font = pygame.font.Font(None, 30)

profile_font = pygame.font.Font(None, 24)
daily_font = pygame.font.Font(None, 15)

user_name = player_data.load_user_name()
profile_center = (640, 40)

current_level = player_data.load_current_level()

total_coins = coin.load_total_coins()

profile_button = pygame.Rect(430, 15, 230, 50)
daily_button = pygame.Rect(680, 20, 40, 50)
more_button = pygame.Rect(735, 20, 30, 40)


level_path_box = pygame.Rect(50, 150, 650, 250)

path_scroll_x = 0
max_path_scroll_x = 250

dragging_path = False
drag_start_x = 0
drag_start_scroll = 0

total_levels = 100

path_scroll_x = 0

max_path_scroll_x = level.get_max_path_scroll(level_path_box, total_levels)


# =======================================While loop========================================
while True:
    screen.fill((240, 245, 255))  # note: how to set it with image or animation

    level.draw_level_path(
        screen, level_path_box, path_scroll_x, total_levels, current_level
    )

    pygame.draw.circle(screen, (255, 255, 255), profile_center, 18)

    pygame.draw.circle(screen, (40, 50, 100), profile_center, 18, 2)

    profile_text = profile_font.render(user_name, True, (40, 50, 100))

    profile_text_rect = profile_text.get_rect(
        midright=(profile_center[0] - 22, profile_center[1])
    )

    screen.blit(profile_text, profile_text_rect)

    daily_center = (700, 40)

    pygame.draw.circle(screen, (255, 255, 255), daily_center, 18)

    pygame.draw.circle(screen, (235, 180, 40), daily_center, 18, 2)

    daily_text = daily_font.render("Daily", True, (40, 50, 100))

    daily_rect = daily_text.get_rect(center=(daily_center[0], 65))

    screen.blit(daily_text, daily_rect)

    for dot_y in [34, 40, 46]:
        pygame.draw.circle(screen, (40, 50, 100), (750, dot_y), 2)

    pygame.draw.rect(
        screen, (50, 150, 100), play_button, border_radius=10
    )  # rounded corners

    play_text = button_font.render("PLAY", True, (255, 255, 255))
    screen.blit(play_text, play_text.get_rect(center=play_button.center))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if profile_button.collidepoint(event.pos):
                total_coins = coin.load_total_coins()

                user_name = profile.show_profile(
                    screen, user_name, current_level, total_coins
                )

                current_level = player_data.load_current_level()

                total_coins = coin.load_total_coins()

            if daily_button.collidepoint(event.pos):
                daily.show_daily(screen)

            if more_button.collidepoint(event.pos):
                settings.show_settings(screen)

            if play_button.collidepoint(
                event.pos
            ):  # `collidepoint()`` = ตรวจว่ากดอยู่ในพื้นที่ปุ่มไหม
                while True:
                    action = game.show_game(
                        screen,
                        user_name,
                        current_level,
                        coin.load_total_coins()
                    )

                    if action == "replay":
                        continue

                    if action == "next":
                        if current_level < total_levels:
                            current_level += 1

                            player_data.save_current_level(
                                current_level
                            )

                            continue

                        break

                    break

        # -------------------------ket touch----------------------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                path_scroll_x = min(max_path_scroll_x, path_scroll_x + 25)

            elif event.key == pygame.K_LEFT:
                path_scroll_x = max(0, path_scroll_x - 25)

        # -------------------finger touch-------------------------
        if event.type == pygame.FINGERDOWN:
            finger_x = int(event.x * screen.get_width())
            finger_y = int(event.y * screen.get_height())

            if level_path_box.collidepoint(finger_x, finger_y):
                dragging_path = True
                drag_start_x = finger_x
                drag_start_scroll = path_scroll_x

        if event.type == pygame.FINGERMOTION and dragging_path:
            finger_x = int(event.x * screen.get_width())

            path_scroll_x = drag_start_scroll + (drag_start_x - finger_x)

            path_scroll_x = max(0, min(max_path_scroll_x, path_scroll_x))

        if event.type == pygame.FINGERUP:
            dragging_path = False
