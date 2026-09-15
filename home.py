import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ["SDL_VIDEO_CENTERED"] = "1"

import pygame
import sys

import level
import profile
import daily
import settings
import coin
import player_data
import game
import screen_manager
import ui

pygame.init()

display_info = pygame.display.Info()

pygame.display.set_mode(
    (display_info.current_w, display_info.current_h), pygame.NOFRAME
)

screen = screen_manager.create_game_surface()

pygame.display.set_caption("Cal Game")

# =========================home background=================================
def load_home_background(screen):
    background = pygame.image.load("assets/home_background_2.png").convert()  

    return pygame.transform.smoothscale(background, screen.get_size())


def create_layout(ui_system):
    return {
        "exit_no_button": ui_system.rect(270, 330, 110, 40),
        "exit_yes_button": ui_system.rect(420, 330, 110, 40),
        "exit_button": ui_system.rect(20, 20, 40, 40),
        "play_button": ui_system.rect(620, 375, 140, 50),
        "profile_button": ui_system.rect(470, 20, 190, 40),
        "daily_button": ui_system.rect(680, 20, 40, 40),
        "more_button": ui_system.rect(735, 20, 30, 40),
        "level_path_box": pygame.Rect(150, 190, 450, 200),
        "level_path_screen_box": ui_system.rect(150, 190, 450, 200),
        "profile_center": ui_system.point(640, 40),
        "daily_center": ui_system.point(700, 40),
        "bottom_menu_bar": ui_system.rect(0, 440, 800, 80),
    }


ui_system = ui.UI(screen)
home_background = load_home_background(screen)
layout = create_layout(ui_system)

exit_icon_source = pygame.image.load("assets/exit_game.png").convert_alpha()

path_scroll_x = 0
dragging_path = False
drag_start_x = 0
drag_start_scroll = 0

total_levels = 100
current_level = player_data.load_current_level()
total_coins = coin.load_total_coins()

max_path_scroll_x = level.get_max_path_scroll(
    layout["level_path_box"],
    total_levels,
)

path_scroll_x = level.get_current_level_scroll(
    layout["level_path_box"],
    total_levels,
    current_level,
)

user_name = player_data.load_user_name()

show_exit_confirm = False

# ====================== While loop ======================

while True:
    screen.blit(home_background, (0, 0))

    # --------------bottom menu bar--------------
    bottom_menu_bar = layout["bottom_menu_bar"]

    bottom_bar_surface = pygame.Surface(
        bottom_menu_bar.size,
        pygame.SRCALPHA,
    )

    bottom_bar_surface.fill((20, 35, 60, 210))

    screen.blit(bottom_bar_surface, bottom_menu_bar.topleft)

    pygame.draw.line(
        screen,
        (255, 255, 255),
        bottom_menu_bar.topleft,
        (bottom_menu_bar.right, bottom_menu_bar.top),
        ui_system.value(1),
    )

    # ------------exit button-------------

    exit_button = layout["exit_button"]

    ui.draw_button_feedback(
        screen,
        exit_button,
        base_color=None,
        hover_color=(220, 70, 90),
        pressed_color=(170, 45, 60),
        border_radius=ui_system.value(12),
    )

    exit_icon = pygame.transform.smoothscale(
        exit_icon_source,
        ui_system.size(24, 24)
    )

    exit_icon_rect = exit_icon.get_rect(
        center=exit_button.center
    )

    screen.blit(exit_icon, exit_icon_rect)

    # ---------------------------------------
    level_path_background = pygame.Surface(
        layout["level_path_screen_box"].size,
        pygame.SRCALPHA,
    )

    level_path_background.fill((0, 0, 0, 120))

    screen.blit(
        level_path_background,
        layout["level_path_screen_box"].topleft,
    )

    # ---------------level path---------------

    level.draw_level_path(
        screen,
        ui_system,
        layout["level_path_box"],
        path_scroll_x,
        total_levels,
        current_level,
    )

    pygame.draw.rect(
        screen,
        (255, 255, 255),
        layout["level_path_screen_box"],
        ui_system.value(4),
        border_radius=ui_system.value(18),
    )

    # ---------------- Profile ----------------

    profile_center = layout["profile_center"]

    ui.draw_button_feedback(
        screen,
        layout["profile_button"],
        base_color=None,
        border_radius=ui_system.value(12),
    )

    pygame.draw.circle(
        screen,
        (255, 255, 255),
        profile_center,
        ui_system.value(18),
    )

    pygame.draw.circle(
        screen,
        (40, 50, 100),
        profile_center,
        ui_system.value(18),
        ui_system.value(2),
    )

    profile_font = ui_system.font(24)

    profile_text = profile_font.render(
        user_name,
        True,
        (40, 50, 100),
    )

    profile_text_rect = profile_text.get_rect(
        midright=ui_system.point(618, 40)
    )

    screen.blit(profile_text, profile_text_rect)

    # ---------------- Daily ----------------

    daily_center = layout["daily_center"]

    ui.draw_button_feedback(
        screen,
        layout["daily_button"],
        base_color=None,
        border_radius=ui_system.value(12),
    )

    pygame.draw.circle(screen, (255, 255, 255), daily_center, ui_system.value(18))

    pygame.draw.circle(
        screen, (235, 180, 40), daily_center, ui_system.value(18), ui_system.value(2)
    )

    daily_font = ui_system.font(15)

    daily_text = daily_font.render("Daily", True, (40, 50, 100))

    daily_rect = daily_text.get_rect(center=ui_system.point(700, 65))

    screen.blit(daily_text, daily_rect)

    # ---------------- More dots ----------------

    ui.draw_button_feedback(
        screen,
        layout["more_button"],
        base_color=None,
        border_radius=ui_system.value(12),
    )

    for dot_y in [34, 40, 46]:
        pygame.draw.circle(
            screen, (40, 50, 100), ui_system.point(750, dot_y), ui_system.value(2)
        )

    # ---------------- Play ----------------

    play_button = layout["play_button"]

    ui.draw_button_feedback(
        screen,
        play_button,
        base_color=(255, 0, 0),
        hover_color=(165, 10, 15),
        pressed_color=(240, 125, 85),
        border_radius=ui_system.value(10),
    )

    button_font = ui_system.font(30)

    pygame.draw.rect(
        screen,
        (255, 255, 255),  # ขอบเขียวเข้ม
        play_button,
        ui_system.value(2),
        border_radius=ui_system.value(10),
    )

    play_text = button_font.render("PLAY", True, (255, 255, 255))

    screen.blit(play_text, play_text.get_rect(center=play_button.center))

    # ------------exit------------
    if show_exit_confirm:
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

        confirm_font = ui_system.font(30)

        confirm_text = confirm_font.render(
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

        no_button = layout["exit_no_button"]
        yes_button = layout["exit_yes_button"]

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

        button_font = ui_system.font(24)

        no_text = button_font.render(
            "No",
            True,
            (40, 50, 100)
        )

        yes_text = button_font.render(
            "Yes",
            True,
            (255, 255, 255)
        )

        screen.blit(
            no_text,
            no_text.get_rect(center=no_button.center)
        )

        screen.blit(
            yes_text,
            yes_text.get_rect(center=yes_button.center)
        )

    pygame.display.update()

    # ================= Events =================

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                screen = screen_manager.toggle_display_mode()

                ui_system = ui.UI(screen)
                home_background = load_home_background(screen)
                layout = create_layout(ui_system)

                continue

            if event.key == pygame.K_RIGHT:
                path_scroll_x = min(max_path_scroll_x, path_scroll_x + 25)

            elif event.key == pygame.K_LEFT:
                path_scroll_x = max(0, path_scroll_x - 25)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
            game_position = screen_manager.get_event_game_position(event)

            if show_exit_confirm:
                if layout["exit_no_button"].collidepoint(
                    game_position
                ):
                    show_exit_confirm = False

                elif layout["exit_yes_button"].collidepoint(
                    game_position
                ):
                    pygame.quit()
                    sys.exit()

                continue

            if layout["exit_button"].collidepoint(game_position):
                show_exit_confirm = True
                continue

            if layout["profile_button"].collidepoint(game_position):
                total_coins = coin.load_total_coins()

                user_name = profile.show_profile(
                    screen, user_name, current_level, total_coins
                )

                current_level = player_data.load_current_level()
                total_coins = coin.load_total_coins()

            if layout["daily_button"].collidepoint(game_position):
                daily.show_daily(screen)

            if layout["more_button"].collidepoint(game_position):
                settings.show_settings(screen)

            if play_button.collidepoint(game_position):
                while True:
                    action = game.show_game(
                        screen, user_name, current_level, coin.load_total_coins()
                    )

                    if action == "replay":
                        continue

                    if action == "next":
                        if current_level < total_levels:
                            current_level += 1

                            player_data.save_current_level(current_level)

                            continue

                        break

                    break

        # ---------------- Touch scroll ----------------

        if event.type == pygame.FINGERDOWN:
            finger_x = int(event.x * screen.get_width())
            finger_y = int(event.y * screen.get_height())

            if layout["level_path_screen_box"].collidepoint(finger_x, finger_y):
                dragging_path = True
                drag_start_x = finger_x
                drag_start_scroll = path_scroll_x

        if event.type == pygame.FINGERMOTION and dragging_path:
            finger_x = int(event.x * screen.get_width())

            move_x = (drag_start_x - finger_x) / ui_system.scale

            path_scroll_x = drag_start_scroll + move_x

            path_scroll_x = max(0, min(max_path_scroll_x, path_scroll_x))

        if event.type == pygame.FINGERUP:
            dragging_path = False

        # ---------------- Mouse scroll ----------------

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if layout["level_path_screen_box"].collidepoint(event.pos):
                    dragging_path = True
                    drag_start_x = event.pos[0]
                    drag_start_scroll = path_scroll_x

        if event.type == pygame.MOUSEMOTION and dragging_path:
            mouse_x = event.pos[0]

            move_x = (drag_start_x - mouse_x) / ui_system.scale

            path_scroll_x = drag_start_scroll + move_x

            path_scroll_x = max(
                0,
                min(max_path_scroll_x, path_scroll_x)
            )

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging_path = False
