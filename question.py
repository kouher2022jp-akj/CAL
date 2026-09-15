import pygame
import random


def draw_question(screen, ui_system, question_box, question):
    pygame.draw.rect(
        screen, (255, 255, 255), question_box, border_radius=ui_system.value(20)
    )

    pygame.draw.rect(
        screen,
        (180, 190, 220),
        question_box,
        ui_system.value(3),
        border_radius=ui_system.value(20),
    )

    label_font = ui_system.font(20)

    label = label_font.render("Question:", True, (40, 50, 100))

    screen.blit(
        label,
        (question_box.x + ui_system.value(15), question_box.y + ui_system.value(15)),
    )

    question_font = ui_system.font(55)

    question_text = question_font.render(question, True, (40, 50, 100))

    question_rect = question_text.get_rect(center=question_box.center)

    screen.blit(question_text, question_rect)


def create_question(level):
    if level <= 2:
        operators = ["+"]
        minimum, maximum = 1, 9

    elif level <= 5:
        operators = ["+", "-"]
        minimum, maximum = 1, 9

    elif level <= 10:
        operators = ["+", "-", "*"]
        minimum, maximum = 1, 9

    elif level <= 20:
        operators = ["+", "-", "*", "/"]
        minimum, maximum = 1, 9

    elif level <= 30:
        operators = ["+", "-", "*", "/", "^"]
        minimum, maximum = 1, 9

    elif level <= 40:
        operators = ["+", "-", "*", "/", "^", "sqrt"]
        minimum, maximum = 1, 9

    elif level <= 50:
        operators = ["+", "-", "*", "/", "^", "sqrt"]
        minimum, maximum = 1, 19

    else:
        operators = ["+", "-", "*", "/", "^", "sqrt"]
        minimum, maximum = 10, 50

    operator = random.choice(operators)

    if operator == "+":
        number1 = random.randint(minimum, maximum)
        number2 = random.randint(minimum, maximum)
        correct_answer = number1 + number2
        question_text = f"{number1} + {number2} = ?"

    elif operator == "-":
        number1 = random.randint(minimum, maximum)
        number2 = random.randint(minimum, number1)
        correct_answer = number1 - number2
        question_text = f"{number1} - {number2} = ?"

    elif operator == "*":
        number1 = random.randint(minimum, maximum)
        number2 = random.randint(minimum, maximum)
        correct_answer = number1 * number2
        question_text = f"{number1} × {number2} = ?"

    elif operator == "/":
        number2 = random.randint(minimum, maximum)
        correct_answer = random.randint(minimum, maximum)
        number1 = number2 * correct_answer
        question_text = f"{number1} ÷ {number2} = ?"

    elif operator == "^":
        number1 = random.randint(minimum, maximum)
        number2 = random.choice([2, 3])
        correct_answer = number1**number2
        question_text = f"{number1} ^ {number2} = ?"

    else:  # sqrt
        correct_answer = random.randint(minimum, maximum)
        number1 = correct_answer**2
        question_text = f"√{number1} = ?"

    return question_text, correct_answer
