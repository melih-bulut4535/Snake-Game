# Name&Surname: Melih Bulut
# Date: 07.09.2022
# SNAKE GAME

import random
import sys
import mysql.connector
import pygame
from pygame.math import Vector2
import speech_recognition as sr
import pyttsx3

connection = mysql.connector.connect(host='localhost', user='root', port='3306',
                                     password='We1ih.Bu1ut', database='pythongui')

pygame.init()
cell_size = 38
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load("apple1.png").convert_alpha()
cup = pygame.image.load("cup.png").convert_alpha()
trap = pygame.image.load("trap.png").convert_alpha()
trap1 = pygame.image.load("trap.png").convert_alpha()
trap2 = pygame.image.load("trap.png").convert_alpha()
game_font = pygame.font.Font('PoetsenOne-Regular.ttf', 25)
bg = pygame.image.load("bg.jpg")
snake_page = pygame.image.load("snake_page.png")

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (245, 130, 32)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
WINDOW_WIDTH = cell_number * cell_size
WINDOW_HEIGHT = cell_number * cell_size
SPEED_SNAKE = 150
TOP_WIDTH = 35
small_font = pygame.font.SysFont('forte', 25)
medium_font = pygame.font.SysFont('showcard gothic', 30, True)
large_font = pygame.font.SysFont('chiller', 60, True, True)
pause_font = medium_font.render('II', True, RED)

recording = sr.Recognizer()
engine = pyttsx3.init()


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    global command
    while 1:
        try:
            with sr.Microphone() as source:
                recording.adjust_for_ambient_noise(source)
                print("Listening....")
                voice = recording.listen(source)
                command = recording.recognize_google(voice)
                command = command.lower()
        except Exception as e:
            print(e)
        return command


def speak():
    global counter, mode, command
    command = take_command()
    print(command)
    if "play" in command:
        difficulty_mode()
        talk("choose difficulty mode")
    elif "easy" in command:
        f_mode = open("mode.txt", "w")
        mode = f_mode.writelines("0")
        f_mode.close()
        game_loop()
    elif "medium" in command:
        f_mode = open("mode.txt", "w")
        mode = f_mode.writelines("1")
        f_mode.close()
        game_loop()
    elif "hard" in command:
        f_mode = open("mode.txt", "w")
        mode = f_mode.writelines("2")
        f_mode.close()
        game_loop()
    elif "rules" or "blues" in command:
        start_inst()
    elif "score table" in command:
        score_table()
    elif "back" in command:
        start_game()
    elif "quit" in command:
        writehighscore1 = open("score.txt", "w")
        writehighscore1.write("0")
        writehighscore1.close()
        f8 = open("counter.txt", "r")
        i = int(f8.readline())
        f8.close()
        f = open("counter.txt", "w")
        counter = f.writelines(str(i + 1))
        f.close()
        pygame.quit()
        sys.exit()
    else:
        talk("I did not understand your question, please say it again")


class SNAKE(object):
    def __init__(self):
        self.tail = None
        self.head = None
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        self.head_up = pygame.image.load("head_up.png").convert_alpha()
        self.head_down = pygame.image.load("head_down.png").convert_alpha()
        self.head_right = pygame.image.load("head_right.png").convert_alpha()
        self.head_left = pygame.image.load("head_left.png").convert_alpha()

        self.tail_up = pygame.image.load("tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("tail_down.png").convert_alpha()
        self.tail_right = pygame.image.load("tail_right.png").convert_alpha()
        self.tail_left = pygame.image.load("tail_left.png").convert_alpha()

        self.body_vertical = pygame.image.load("body_vertical.png").convert_alpha()
        self.body_horizontal = pygame.image.load("body_horizontal.png").convert_alpha()

        self.body_tr = pygame.image.load("body_tr.png").convert_alpha()
        self.body_tl = pygame.image.load("body_tl.png").convert_alpha()
        self.body_br = pygame.image.load("body_br.png").convert_alpha()
        self.body_bl = pygame.image.load("body_bl.png").convert_alpha()

        self.crunch_sound = pygame.mixer.Sound("Sound_crunch.wav")

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

        # for block in self.body:
        # x_pos = int(block.x * cell_size)
        # y_pos = int(block.y * cell_size)
        # block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        # pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_sound_crunch(self):
        self.crunch_sound.play()


class FRUIT:
    def __init__(self):
        self.pos = None
        self.y = None
        self.x = None
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(1, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class TRAP:
    def __init__(self):
        self.pos = None
        self.y = None
        self.x = None
        f_mode = open("mode.txt", "r")
        mode = int(f_mode.readline())
        f_mode.close()
        if mode == 1:
            self.randomize()
        if mode == 2:
            self.randomize()

    def draw_trap(self):
        trap_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(trap, trap_rect)

    def draw_trap1(self):
        trap1_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(trap1, trap1_rect)
        trap2_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(trap2, trap2_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(1, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


def draw_grass():
    grass_color = (167, 209, 61)

    for row in range(cell_number):
        if row % 2 == 0:
            for col in range(cell_number):
                if col % 2 == 0:
                    grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)
        else:
            for col in range(cell_number):
                if col % 2 != 0:
                    grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)

        if row == 0:
            for col in range(cell_number):
                grass_rect = pygame.Rect(col * cell_size, 0, cell_size, cell_size)
                pygame.draw.rect(screen, (255, 127, 0), grass_rect)


def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()


def print_score():
    # opening both files in read only mode to read first contents
    global counter
    f2 = open("score.txt", 'r')
    f1 = open("counter.txt", "r")
    counter = int(f1.readline())
    # appending the contents of the second file to the first file
    replace_line("user_score.txt", counter, f2.read() + "\n")

    # f1.writelines(f2.read() + "\n")

    # relocating the cursor of the files at the beginning

    f2.seek(0)

    # closing the files
    f1.close()
    f2.close()


def game_over():
    print_score()
    global counter
    font_gameover1 = large_font.render('GAME OVER', True, RED)
    font_gameover2 = medium_font.render("Play Again", True, RED, YELLOW)
    font_gameover5 = medium_font.render("Difficulty Mode Page", True, RED, YELLOW)
    font_gameover3 = medium_font.render("Quit", True, RED, YELLOW)
    font_gameover4 = medium_font.render("Main Menu", True, RED, YELLOW)

    font_gameover1_rect = font_gameover1.get_rect()
    font_gameover2_rect = font_gameover2.get_rect()
    font_gameover3_rect = font_gameover3.get_rect()
    font_gameover4_rect = font_gameover4.get_rect()
    font_gameover5_rect = font_gameover5.get_rect()

    font_gameover1_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100)
    font_gameover2_rect.center = (WINDOW_WIDTH / 2 + 150, WINDOW_HEIGHT / 2 + 20)
    font_gameover3_rect.center = (WINDOW_WIDTH / 2 + 150, WINDOW_HEIGHT / 2 + 170)
    font_gameover4_rect.center = (WINDOW_WIDTH / 2 + 150, WINDOW_HEIGHT / 2 + 120)
    font_gameover5_rect.center = (WINDOW_WIDTH / 2 + 150, WINDOW_HEIGHT / 2 + 70)

    screen.blit(font_gameover1, font_gameover1_rect)
    screen.blit(font_gameover2, font_gameover2_rect)
    screen.blit(font_gameover3, font_gameover3_rect)
    screen.blit(font_gameover4, font_gameover4_rect)
    screen.blit(font_gameover5, font_gameover5_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                writehighscore1 = open("score.txt", "w")
                writehighscore1.write("0")
                f8 = open("counter.txt", "r")
                i = int(f8.readline())
                f8.close()
                f = open("counter.txt", "w")
                counter = f.writelines(str(i + 1))
                f.close()
                writehighscore1.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    speak()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if font_gameover2_rect.left < x < font_gameover2_rect.right:
                    if font_gameover2_rect.top < y < font_gameover2_rect.bottom:
                        game_loop()
                if font_gameover3_rect.left < x < font_gameover3_rect.right:
                    if font_gameover3_rect.top < y < font_gameover3_rect.bottom:
                        writehighscore1 = open("score.txt", "w")
                        writehighscore1.write("0")
                        writehighscore1.close()
                        f8 = open("counter.txt", "r")
                        i = int(f8.readline())
                        f8.close()
                        f = open("counter.txt", "w")
                        counter = f.writelines(str(i + 1))
                        f.close()
                        pygame.quit()
                        sys.exit()
                if font_gameover4_rect.left < x < font_gameover4_rect.right:
                    if font_gameover4_rect.top < y < font_gameover4_rect.bottom:
                        start_game()
                if font_gameover5_rect.left < x < font_gameover5_rect.right:
                    if font_gameover5_rect.top < y < font_gameover5_rect.bottom:
                        difficulty_mode()

        pygame.display.update()


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.trap = TRAP()
        self.trap1 = TRAP()
        self.trap2 = TRAP()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        draw_grass()
        f_mode = open("mode.txt", "r")
        mode = int(f_mode.readline())
        f_mode.close()
        if mode == 1:
            self.trap.draw_trap()
        if mode == 2:
            self.trap.draw_trap()
            self.trap1.draw_trap1()
            self.trap2.draw_trap1()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        global mode
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            f_mode = open("mode.txt", "r")
            mode = int(f_mode.readline())
            f_mode.close()
            if mode == 1:
                self.trap.randomize()
            if mode == 2:
                self.trap.randomize()
                self.trap1.randomize()
                self.trap2.randomize()
            self.snake.add_block()
            self.snake.play_sound_crunch()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

        if mode == 1 or mode == 2:
            if self.trap.pos == self.fruit.pos:
                self.trap.randomize()
        if mode == 2:
            if self.trap1.pos == self.fruit.pos:
                self.trap1.randomize()
            if self.trap2.pos == self.fruit.pos:
                self.trap2.randomize()

        if mode == 1 or mode == 2:
            for block in self.snake.body[1:]:
                if block == self.trap.pos:
                    self.trap.randomize()
        if mode == 2:
            for block in self.snake.body[1:]:
                if block == self.trap1.pos:
                    self.trap1.randomize()
            for block in self.snake.body[1:]:
                if block == self.trap2.pos:
                    self.trap2.randomize()

    def check_fail(self):
        # check if snake is outside the screen.

        f_mode = open("mode.txt", "r")
        mode = int(f_mode.readline())
        f_mode.close()
        if mode == 1 or mode == 0:
            if self.snake.body[0].x < 0:
                self.snake.body[0].x += 20
            elif self.snake.body[0].x >= 20:
                self.snake.body[0].x -= 20
            if self.snake.body[0].y < 1:
                self.snake.body[0].y += 20
            elif self.snake.body[0].y >= 20:
                self.snake.body[0].y -= 19
        elif mode == 2:
            if not 0 <= self.snake.body[0].x < cell_number or not 1 <= self.snake.body[0].y < cell_number:
                game_over()

        # check if snake hits a trap.
        if self.trap.pos == self.snake.body[0]:
            game_over()
        f_mode = open("mode.txt", "r")
        mode = int(f_mode.readline())
        f_mode.close()
        if mode == 2:
            if self.trap1.pos == self.snake.body[0]:
                game_over()
            if self.trap2.pos == self.snake.body[0]:
                game_over()

        # check if snake hits itself.
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                game_over()

    def draw_score(self):
        global score_text
        f_mode = open("mode.txt", "r")
        mode = int(f_mode.readline())
        f_mode.close()
        if mode == 1:
            score_text = str(int(len(self.snake.body) - 3) * 2)
        elif mode == 2:
            score_text = str(int(len(self.snake.body) - 3) * 5)
        else:
            score_text = str(len(self.snake.body) - 3)

        readhighscore = open("score.txt", "r")
        best_score = readhighscore.read()
        readhighscore.close()
        if int(score_text) > int(best_score):
            writehighscore = open("score.txt", "w")
            writehighscore.write(str(score_text))

            writehighscore.close()

        score_surface = game_font.render(score_text, True, (56, 74, 12))
        best_surface = game_font.render(best_score, True, (56, 74, 12))
        score_x = int(WINDOW_WIDTH - (WINDOW_WIDTH - 52))
        score_y = int(WINDOW_WIDTH - (WINDOW_WIDTH - 20))
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(center=((WINDOW_WIDTH - 455), (WINDOW_WIDTH - 460)))
        best_rect = best_surface.get_rect(center=((WINDOW_WIDTH - 630), (WINDOW_WIDTH - 740)))
        cup_rect = cup.get_rect(center=((WINDOW_WIDTH - 655), (WINDOW_WIDTH - 742)))
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        screen.blit(cup, cup_rect)
        screen.blit(best_surface, best_rect)
        pygame.draw.line(screen, BLACK, (0, TOP_WIDTH + 2), (WINDOW_WIDTH, TOP_WIDTH + 2))
        pygame.draw.line(screen, YELLOW, (WINDOW_WIDTH - 60, 0), (WINDOW_WIDTH - 60, TOP_WIDTH))
        pygame.draw.rect(screen, YELLOW, (WINDOW_WIDTH - 60, 0, 60, TOP_WIDTH + 2))
        screen.blit(pause_font, (WINDOW_WIDTH - 45, 7))
        pygame.display.update()


def multilineRender(screen, text, x, y, the_font, colour=(128, 128, 128), justification="left"):
    justification = justification[0].upper()
    # text = text.strip().replace('\r', '').split('\n')
    max_width = 0
    text_bitmaps = []
    # Convert all the text into bitmaps, calculate the justification width
    for t in text:
        text_bitmap = the_font.render(t, True, colour)
        text_width = text_bitmap.get_width()
        text_bitmaps.append((text_width, text_bitmap))
        if max_width < text_width:
            max_width = text_width
    # Paint all the text bitmaps to the screen with justification
    for (width, bitmap) in text_bitmaps:
        xpos = x
        width_diff = max_width - width
        if justification == 'R':  # right-justify
            xpos = x + width_diff
        elif justification == 'C':  # centre-justify
            xpos = x + (width_diff // 2)
        screen.blit(bitmap, (xpos, y))
        y += bitmap.get_height()


def score_table():
    global counter
    # screen.fill((0, 177, 64))
    screen.blit(bg, (0, 0))
    score_print1 = medium_font.render("Score Table", True, BLUE)
    score_print1_rect = score_print1.get_rect()
    score_print1_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 300)
    screen.blit(score_print1, score_print1_rect)

    with open("username_score.txt") as f1, open("user_score.txt") as f2, open("score_table.txt", "w") as f3:
        for x, y in zip(f1, f2):
            f3.write(x.strip() + "----> " + y.strip() + "\n")

    f1.close()
    f2.close()
    f3.close()

    file1 = open('score_table.txt', 'r')
    # Lines = file1.readlines()
    myfont = pygame.font.Font(None, 50)
    multilineRender(screen, file1, 100, 200, myfont, BLACK)
    # Strips the newline character
    # for line in Lines:
    #     score_print2 = small_font.render(line.strip(), True, BLUE)
    #     screen.blit(score_print2, (WINDOW_WIDTH / 8 + 100, WINDOW_HEIGHT / 2 + 50))

    file1.close()

    start_inst5 = medium_font.render("<<BACK", True, BLUE, YELLOW)
    start_inst5_rect = start_inst5.get_rect()
    start_inst5_rect.center = (WINDOW_WIDTH - 100, WINDOW_HEIGHT - 100)
    screen.blit(start_inst5, start_inst5_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f8 = open("counter.txt", "r")
                i = int(f8.readline())
                f8.close()
                f = open("counter.txt", "w")
                counter = f.writelines(str(i + 1))
                f.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    speak()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if start_inst5_rect.left < x < start_inst5_rect.right:
                    if start_inst5_rect.top < y < start_inst5_rect.bottom:
                        start_game()
        pygame.display.update()


def start_inst():
    global counter
    # screen.fill((0, 177, 64))
    screen.blit(bg, (0, 0))
    start_inst1 = small_font.render("--> There are 3 game modes, Easy, Medium and Hard.", True, BLACK)
    start_inst2 = small_font.render("--> There is 1 apple in easy mode, you must try to eat the apple with", True,
                                    BLACK)
    start_inst3 = small_font.render(" the snake.There is no hitting the walls, you come out in the same", True, BLACK)
    start_inst4 = small_font.render(" direction across the wall you passed.", True, BLACK)
    start_inst5 = small_font.render("--> In medium difficulty mode, there is 1 apple and 1 trap. The trap will", True,
                                    BLACK)
    start_inst6 = small_font.render(" be randomly replaced every time an apple is eaten. You have to try to eat", True,
                                    BLACK)
    start_inst7 = small_font.render(" the apple without hitting the trap, in this mode you will get 2x points.", True,
                                    BLACK)
    start_inst8 = small_font.render("There is no hitting the wall in this mode either.", True, BLACK)
    start_inst9 = small_font.render("--> In hard mode, there are 1 apple and 3 traps. Traps move randomly", True, BLACK)
    start_inst10 = small_font.render("and you must avoid hitting walls. In this mode you get 5 times points.", True,
                                     BLACK)
    start_inst11 = medium_font.render("<<BACK", True, ORANGE, YELLOW)
    start_inst11_rect = start_inst11.get_rect()
    start_inst12 = large_font.render("RULES", True, BLUE)
    start_inst11_rect.center = (WINDOW_WIDTH - 100, WINDOW_HEIGHT - 70)
    screen.blit(start_inst1, (WINDOW_WIDTH / 8 - 90, WINDOW_HEIGHT / 2 - 40))
    screen.blit(start_inst2, (WINDOW_WIDTH / 8 - 90, WINDOW_HEIGHT / 2 - 10))
    screen.blit(start_inst3, (WINDOW_WIDTH / 8 - 90, WINDOW_HEIGHT / 2 + 20))
    screen.blit(start_inst4, (WINDOW_WIDTH / 8 - 90, WINDOW_HEIGHT / 2 + 50))
    screen.blit(start_inst5, (WINDOW_WIDTH / 8 - 90, WINDOW_HEIGHT / 2 + 80))
    screen.blit(start_inst6, (WINDOW_WIDTH / 8 - 90, WINDOW_HEIGHT / 2 + 110))
    screen.blit(start_inst7, (WINDOW_WIDTH / 8 - 90, WINDOW_HEIGHT / 2 + 140))
    screen.blit(start_inst8, (WINDOW_WIDTH / 8 - 90, WINDOW_HEIGHT / 2 + 170))
    screen.blit(start_inst9, (WINDOW_WIDTH / 8 - 90, WINDOW_HEIGHT / 2 + 200))
    screen.blit(start_inst10, (WINDOW_WIDTH / 8 - 90, WINDOW_HEIGHT / 2 + 230))
    screen.blit(start_inst12, (WINDOW_WIDTH / 8+200, WINDOW_HEIGHT / 2-150))
    screen.blit(start_inst11, start_inst11_rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f8 = open("counter.txt", "r")
                i = int(f8.readline())
                f8.close()
                f = open("counter.txt", "w")
                counter = f.writelines(str(i + 1))
                f.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    speak()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if start_inst11_rect.left < x < start_inst11_rect.right:
                    if start_inst11_rect.top < y < start_inst11_rect.bottom:
                        start_game()
        pygame.display.update()


def difficulty_mode():
    global counter, mode
    # screen.fill((0, 177, 64))
    screen.blit(bg, (0, 0))
    mode_easy = medium_font.render("Easy Difficulty Mode", True, GREEN, YELLOW)
    mode_medium = medium_font.render("Medium Difficulty Mode", True, BLUE, YELLOW)
    mode_hard = medium_font.render("Hard Difficulty Mode", True, RED, YELLOW)
    start_inst5 = medium_font.render("<<BACK", True, ORANGE, YELLOW)

    start_inst5_rect = start_inst5.get_rect()
    mode_easy_rect = mode_easy.get_rect()
    mode_medium_rect = mode_medium.get_rect()
    mode_hard_rect = mode_hard.get_rect()

    mode_easy_rect.center = (WINDOW_WIDTH / 2 + 10, WINDOW_HEIGHT / 2 + 50)
    mode_medium_rect.center = (WINDOW_WIDTH / 2 + 10, WINDOW_HEIGHT / 2 + 100)
    mode_hard_rect.center = (WINDOW_WIDTH / 2 + 10, WINDOW_HEIGHT / 2 + 150)
    start_inst5_rect.center = (WINDOW_WIDTH - 100, WINDOW_HEIGHT - 100)

    screen.blit(mode_easy, mode_easy_rect)
    screen.blit(mode_medium, mode_medium_rect)
    screen.blit(mode_hard, mode_hard_rect)
    screen.blit(start_inst5, start_inst5_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                writehighscore1 = open("score.txt", "w")
                writehighscore1.write("0")
                writehighscore1.close()
                f8 = open("counter.txt", "r")
                i = int(f8.readline())
                f8.close()
                f = open("counter.txt", "w")
                counter = f.writelines(str(i + 1))
                f.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    speak()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if mode_easy_rect.left < x < mode_easy_rect.right:
                    if mode_easy_rect.top < y < mode_easy_rect.bottom:
                        f_mode = open("mode.txt", "w")
                        mode = f_mode.writelines("0")
                        f_mode.close()
                        game_loop()
                if mode_medium_rect.left < x < mode_medium_rect.right:
                    if mode_medium_rect.top < y < mode_medium_rect.bottom:
                        f_mode = open("mode.txt", "w")
                        mode = f_mode.writelines("1")
                        f_mode.close()
                        game_loop()
                if mode_hard_rect.left < x < mode_hard_rect.right:
                    if mode_hard_rect.top < y < mode_hard_rect.bottom:
                        f_mode = open("mode.txt", "w")
                        mode = f_mode.writelines("2")
                        f_mode.close()
                        game_loop()
                if start_inst5_rect.left < x < start_inst5_rect.right:
                    if start_inst5_rect.top < y < start_inst5_rect.bottom:
                        start_game()
        pygame.display.update()


def start_game():
    global counter
    # screen.fill((0, 177, 64))
    screen.blit(bg, (0, 0))
    screen.blit(snake_page, (500, 400))
    read_username = open("username.txt", "r")
    start_font5 = large_font.render("USER {}".format(read_username.read()), True, BLACK)
    read_username.close()
    start_font1 = large_font.render("WELCOME TO SNAKE GAME", True, BLUE)
    start_font2 = medium_font.render("Play Game", True, ORANGE, YELLOW)
    start_font3 = medium_font.render("Rules", True, ORANGE, YELLOW)
    start_font6 = medium_font.render("Score Table", True, ORANGE, YELLOW)
    start_font4 = medium_font.render("Quit", True, RED, YELLOW)

    start_font1_rect = start_font1.get_rect()
    start_font2_rect = start_font2.get_rect()
    start_font3_rect = start_font3.get_rect()
    start_font4_rect = start_font4.get_rect()
    start_font5_rect = start_font5.get_rect()
    start_font6_rect = start_font6.get_rect()

    start_font1_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100)
    start_font2_rect.center = (WINDOW_WIDTH / 2 - 250, WINDOW_HEIGHT / 2 + 50)
    start_font3_rect.center = (WINDOW_WIDTH / 2 - 290, WINDOW_HEIGHT / 2 + 100)
    start_font6_rect.center = (WINDOW_WIDTH / 2 - 230, WINDOW_HEIGHT / 2 + 150)
    start_font4_rect.center = (WINDOW_WIDTH / 2 - 295, WINDOW_HEIGHT / 2 + 250)
    start_font5_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 200)

    screen.blit(start_font1, start_font1_rect)
    screen.blit(start_font2, start_font2_rect)
    screen.blit(start_font3, start_font3_rect)
    screen.blit(start_font4, start_font4_rect)
    screen.blit(start_font5, start_font5_rect)
    screen.blit(start_font6, start_font6_rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                writehighscore1 = open("score.txt", "w")
                writehighscore1.write("0")
                writehighscore1.close()
                f8 = open("counter.txt", "r")
                i = int(f8.readline())
                f8.close()
                f = open("counter.txt", "w")
                counter = f.writelines(str(i + 1))
                f.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_loop()
                if event.key == pygame.K_q:
                    f8 = open("counter.txt", "r")
                    i = int(f8.readline())
                    f8.close()
                    f = open("counter.txt", "w")
                    counter = f.writelines(str(i + 1))
                    f.close()
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_m:
                    talk("welcome to snake game")
                    speak()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if start_font6_rect.left < x < start_font6_rect.right:
                    if start_font6_rect.top < y < start_font6_rect.bottom:
                        score_table()
                if start_font3_rect.left < x < start_font3_rect.right:
                    if start_font3_rect.top < y < start_font3_rect.bottom:
                        start_inst()
                if start_font2_rect.left < x < start_font2_rect.right:
                    if start_font2_rect.top < y < start_font2_rect.bottom:
                        difficulty_mode()
                if start_font4_rect.left < x < start_font4_rect.right:
                    if start_font4_rect.top < y < start_font4_rect.bottom:
                        writehighscore1 = open("score.txt", "w")
                        writehighscore1.write("0")
                        writehighscore1.close()
                        f8 = open("counter.txt", "r")
                        i = int(f8.readline())
                        f8.close()
                        f = open("counter.txt", "w")
                        counter = f.writelines(str(i + 1))
                        f.close()
                        pygame.quit()
                        sys.exit()

        pygame.display.update()


def game_paused():
    # canvas.fill(BLACK)
    global counter
    paused_font1 = large_font.render("Game Paused", True, RED)
    paused_font_rect1 = paused_font1.get_rect()
    paused_font_rect1.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    screen.blit(paused_font1, paused_font_rect1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                writehighscore1 = open("score.txt", "w")
                writehighscore1.write("0")
                writehighscore1.close()
                f8 = open("counter.txt", "r")
                i = int(f8.readline())
                f8.close()
                f = open("counter.txt", "w")
                counter = f.writelines(str(i + 1))
                f.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    writehighscore1 = open("score.txt", "w")
                    writehighscore1.write("0")
                    f8 = open("counter.txt", "r")
                    i = int(f8.readline())
                    f8.close()
                    f = open("counter.txt", "w")
                    counter = f.writelines(str(i + 1))
                    f.close()
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pause_xy = event.pos
                if (WINDOW_WIDTH - 50) < pause_xy[0] < WINDOW_WIDTH:
                    if 0 < pause_xy[1] < 50:
                        return
        pygame.display.update()


def game_loop():
    global APPLE_X, APPLE_Y, score, counter, SPEED_SNAKE, ballrect, sprite_group
    f_mode = open("mode.txt", "r")
    mode = int(f_mode.readline())
    f_mode.close()
    if mode == 0:
        SPEED_SNAKE = 150
    elif mode == 1:
        SPEED_SNAKE = 100
    elif mode == 2:
        SPEED_SNAKE = 80

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, SPEED_SNAKE)
    main_game = MAIN()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                writehighscore1 = open("score.txt", "w")
                writehighscore1.write("0")
                f8 = open("counter.txt", "r")
                i = int(f8.readline())
                f8.close()
                f = open("counter.txt", "w")
                counter = f.writelines(str(i + 1))
                f.close()
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    if main_game.snake.direction.y != 1:  # prevent going down when going up
                        main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    if main_game.snake.direction.x != -1:  # prevent going right when going left
                        main_game.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    if main_game.snake.direction.y != -1:  # prevent going up when going down
                        main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    if main_game.snake.direction.x != 1:  # prevent left right when going right
                        main_game.snake.direction = Vector2(-1, 0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pause_xy = event.pos
                if (WINDOW_WIDTH - 50) < pause_xy[0] < WINDOW_WIDTH:
                    if 0 < pause_xy[1] < 50:
                        game_paused()

        pygame.display.update()
        pygame.display.flip()
        screen.fill((175, 215, 70))
        main_game.draw_elements()
        clock.tick(120)


start_game()
game_loop()
