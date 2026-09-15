import pygame
import math
import colorsys


def create_curve(points):
    curve = []

    for step in range(21):
        t = step / 20
        x = (
            (1 - t) ** 3 * points[0][0]
            + 3 * (1 - t) ** 2 * t * points[1][0]
            + 3 * (1 - t) * t**2 * points[2][0]
            + t**3 * points[3][0]
        )
        y = (
            (1 - t) ** 3 * points[0][1]
            + 3 * (1 - t) ** 2 * t * points[1][1]
            + 3 * (1 - t) * t**2 * points[2][1]
            + t**3 * points[3][1]
        )

        curve.append((x, y))

    return curve


def create_level_data(total_levels):
    start_x = 100
    level_spacing = 140
    center_y = 260
    wave_height = 100
    level_positions = []
    level_colors = []

    for index in range(total_levels):
        x = start_x + index * level_spacing

        y = center_y + int(math.sin(index * 1.3) * wave_height)

        level_positions.append((x, y))

        hue = (0.36 + index * 0.61803398875) % 1.0

        red, green, blue = colorsys.hsv_to_rgb(hue, 0.78, 0.92)

        level_colors.append((int(red * 255), int(green * 255), int(blue * 255)))

    final_position = (level_positions[-1][0] + 170, center_y)

    road_curves = []

    for index in range(total_levels - 1):
        start = level_positions[index]
        end = level_positions[index + 1]

        middle_x = (start[0] + end[0]) // 2

        road_curves.append([start, (middle_x, start[1]), (middle_x, end[1]), end])

    last_level = level_positions[-1]
    middle_x = (last_level[0] + final_position[0]) // 2

    road_curves.append(
        [
            last_level,
            (middle_x, last_level[1]),
            (middle_x, final_position[1]),
            final_position,
        ]
    )

    return (level_positions, final_position, level_colors, road_curves)


def get_max_path_scroll(path_box, total_levels, scale=0.5):
    start_x = 100
    level_spacing = 140
    final_space = 170
    final_radius = 50

    last_level_x = start_x + (total_levels - 1) * level_spacing
    final_x = last_level_x + final_space

    offset_x = (path_box.width - 800 * scale) // 2

    final_right = final_x * scale + offset_x + final_radius * scale

    return max(0, int(final_right - path_box.width))


def draw_level_path(
    screen, ui_system, path_box, scroll_x=0, total_levels=10, current_level=1
):

    draw_box = ui_system.rect(path_box.x, path_box.y, path_box.width, path_box.height)

    path_surface = pygame.Surface(draw_box.size, pygame.SRCALPHA)

    scale = 0.5 * ui_system.scale

    offset_x = (draw_box.width - 800 * scale) // 2 - round(scroll_x * ui_system.scale)

    offset_y = (draw_box.height - 500 * scale) // 2

    def scale_point(point):
        return (int(point[0] * scale + offset_x), int(point[1] * scale + offset_y))

    level_font = pygame.font.Font(None, max(18, round(35 * scale)))

    level_positions, final_position, level_colors, road_curves = create_level_data(
        total_levels
    )

    for curve_points in road_curves:
        scaled_curve_points = [scale_point(point) for point in curve_points]

        curve = create_curve(scaled_curve_points)

        pygame.draw.lines(
            path_surface, (145, 100, 55), False, curve, max(3, int(20 * scale))
        )

    level_radius = int(40 * scale)
    for number, (position, color) in enumerate(
        zip(level_positions, level_colors), start=1
    ):
        scaled_position = scale_point(position)

        pygame.draw.circle(path_surface, color, scaled_position, int(40 * scale))

        number_text = level_font.render(str(number), True, (255, 255, 255))

        path_surface.blit(number_text, number_text.get_rect(center=scaled_position))

        if number > current_level:

            locked_overlay = pygame.Surface(
                (level_radius * 2, level_radius * 2), pygame.SRCALPHA
            )

            pygame.draw.circle(
                locked_overlay,
                (255, 255, 255, 55),
                (level_radius, level_radius),
                level_radius,
            )

            path_surface.blit(
                locked_overlay,
                (scaled_position[0] - level_radius, scaled_position[1] - level_radius),
            )

            lock_width = max(18, int(36 * scale))
            lock_height = max(14, int(26 * scale))

            lock_center = (
                scaled_position[0] + int(18 * scale),
                scaled_position[1] + int(18 * scale),
            )

            lock_rect = pygame.Rect(
                lock_center[0] - lock_width // 2,
                lock_center[1] - lock_height // 2 + 4,
                lock_width,
                lock_height,
            )

            shackle_rect = pygame.Rect(
                lock_center[0] - lock_width // 3,
                lock_center[1] - lock_height // 2 - 5,
                lock_width * 2 // 3,
                lock_height,
            )

            pygame.draw.arc(
                path_surface, (40, 50, 100), shackle_rect, math.pi, math.pi * 2, 3
            )

            pygame.draw.rect(path_surface, (255, 255, 255), lock_rect, border_radius=3)

            pygame.draw.rect(path_surface, (40, 50, 100), lock_rect, 2, border_radius=3)

            pygame.draw.circle(path_surface, (40, 50, 100), lock_rect.center, 3)

    scaled_final_position = scale_point(final_position)

    pygame.draw.circle(
        path_surface, (255, 200, 40), scaled_final_position, int(50 * scale)
    )

    current_index = max(0, min(current_level - 1, len(level_positions) - 1))

    current_position = scale_point(level_positions[current_index])

    pygame.draw.circle(
        path_surface, (255, 255, 255), current_position, level_radius + 7, 4
    )

    marker_radius = max(12, int(28 * scale))

    marker_center = (current_position[0], current_position[1] - int(80 * scale))

    pygame.draw.circle(path_surface, (220, 70, 90), marker_center, marker_radius)

    pygame.draw.polygon(
        path_surface,
        (220, 70, 90),
        [
            (marker_center[0] - marker_radius, marker_center[1] + marker_radius // 2),
            (marker_center[0] + marker_radius, marker_center[1] + marker_radius // 2),
            (current_position[0], current_position[1] - int(23 * scale)),
        ],
    )

    pygame.draw.circle(
        path_surface, (255, 255, 255), marker_center, max(3, marker_radius // 3)
    )

    final_text = level_font.render("FINAL", True, (255, 255, 255))

    path_surface.blit(final_text, final_text.get_rect(center=scaled_final_position))

    screen.blit(path_surface, draw_box.topleft)

# --------------------------------------------
def get_current_level_scroll(
    path_box,
    total_levels,
    current_level,
    scale=0.5,
):
    level_positions, _, _, _ = create_level_data(total_levels)

    current_index = max(0, min(current_level - 1, len(level_positions) - 1))

    current_x = level_positions[current_index][0]

    offset_x = (path_box.width - 800 * scale) / 2

    target_x = path_box.width / 2

    scroll_x = current_x * scale + offset_x - target_x

    max_scroll_x = get_max_path_scroll(
        path_box,
        total_levels,
        scale,
    )

    return max(0, min(max_scroll_x, scroll_x))
