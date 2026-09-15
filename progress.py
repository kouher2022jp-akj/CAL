def calculate_change(time_percent):
    return time_percent / 4


def increase(current_progress, time_percent):
    change = calculate_change(time_percent)

    return min(100, current_progress + change)


def decrease(current_progress, time_percent):
    change = calculate_change(time_percent)

    return max(0, current_progress - change)
