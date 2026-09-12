import pygame
import random


def draw_question(screen, question_box, question):
    pygame.draw.rect(screen, (255, 255, 255), question_box, border_radius=20)

    pygame.draw.rect(screen, (180, 190, 220), question_box, 3, border_radius=20)

    label_font = pygame.font.Font(None, 20)
    label = label_font.render("Question:", True, (40, 50, 100))
    screen.blit(label, (question_box.x + 15, question_box.y + 15))

    question_font = pygame.font.Font(None, 55)
    question_text = question_font.render(question, True, (40, 50, 100))

    question_rect = question_text.get_rect(center=question_box.center)
    screen.blit(question_text, question_rect)


def create_question():
    operator = random.choice(["+", "-", "*", "/"])

    if operator == "+":
        number1 = random.randint(1, 10)
        number2 = random.randint(1, 10)
        correct_answer = number1 + number2

    elif operator == "-":
        number1 = random.randint(1, 10)
        number2 = random.randint(1, number1)
        correct_answer = number1 - number2

    elif operator == "*":
        number1 = random.randint(1, 10)
        number2 = random.randint(1, 10)
        correct_answer = number1 * number2

    else:
        number2 = random.randint(1, 10)
        correct_answer = random.randint(1, 10)
        number1 = number2 * correct_answer

    question_text = f"{number1} {operator} {number2} = ?"

    return question_text, correct_answer
