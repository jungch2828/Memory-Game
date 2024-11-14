import pygame
import sys
import random
import math

pygame.init()

while True:
    LEVEL = input("Enter the level of the game (1 ~ 3): ")
    if LEVEL.isnumeric() and 1 <= int(LEVEL) and int(LEVEL) <= 3:
        LEVEL = int(LEVEL)
        break
    print("Please enter again.\n")

BOARD_SIZE = BOARD_WIDTH, BOARD_HEIGHT = LEVEL + 1, LEVEL + 1
NUM_BUTTONS = BOARD_WIDTH * BOARD_HEIGHT

BUTTON_SIZE = int(500 / (BOARD_WIDTH + 1))
BUTTON_GAP = int(500 / (BOARD_WIDTH + 1) ** 2)

SCREEN_SIZE = \
    BOARD_WIDTH * (BUTTON_SIZE + BUTTON_GAP) + BUTTON_GAP, \
    BOARD_HEIGHT * (BUTTON_SIZE + BUTTON_GAP) + BUTTON_GAP

SCREEN = pygame.display.set_mode(SCREEN_SIZE)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

TIME_LIMIT = NUM_BUTTONS * 2
CLOCK = pygame.time.Clock()
TICK = 40

clicked_nums = []


# button objects
class Button:

    # initialize attributes
    def __init__(self, index, num):
        self.index = index
        self.num = num

        def r(): return random.randint(80, 255)
        self.color = (r(), r(), r())
        self.opened = False

        self.rect_x = (self.index % BOARD_WIDTH) * (BUTTON_SIZE + BUTTON_GAP) + BUTTON_GAP
        self.rect_y = (self.index // BOARD_WIDTH) * (BUTTON_SIZE + BUTTON_GAP) + BUTTON_GAP
        self.rect = pygame.Rect(
            (self.rect_x, self.rect_y, BUTTON_SIZE, BUTTON_SIZE))

        font = pygame.font.Font(
            'freesansbold.ttf', int(64 * (BUTTON_SIZE / 150)))
        self.text_color = [x - 50 for x in self.color]
        self.text = font.render(str(self.num + 1), True, self.text_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    # draw number on a button
    def display_num(self):
        SCREEN.blit(self.text, self.text_rect)

    # draw button square
    def display_button(self, color=None):
        if color is None:
            color = self.color
        pygame.draw.rect(SCREEN, color, self.rect)

    # check if a button is clicked
    def is_clicked(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.opened:
                self.opened = True
                clicked_nums.append(self.index)

    #draw O on a button
    def draw_o(self):
        pygame.draw.circle(SCREEN, self.text_color, self.rect.center, int(
            BUTTON_SIZE / 2.2), int(BUTTON_SIZE / 16))

    # draw X on a button
    def draw_x(self):
        pygame.draw.line(SCREEN, self.text_color,
            (self.rect.centerx - self.rect.width / 3, self.rect.centery - self.rect.height / 3),
            (self.rect.centerx + self.rect.width / 3, self.rect.centery + self.rect.height / 3),
            int(BUTTON_SIZE / 13))
        pygame.draw.line(SCREEN, self.text_color,
            (self.rect.centerx + self.rect.width / 3, self.rect.centery - self.rect.height / 3),
            (self.rect.centerx - self.rect.width / 3, self.rect.centery + self.rect.height / 3),
            int(BUTTON_SIZE / 13))


# draw bar to show time left
def draw_timer(time_limit, time_left):
    ratio = time_left / time_limit
    color = (255 * (1 - ratio), 255 * ratio, 0)
    pygame.draw.line(SCREEN, color, (0, SCREEN.get_height()),
        (SCREEN.get_width() * ratio, SCREEN.get_height()), BUTTON_GAP * 2)


# test if a time is spent since a particular moment
def time_spent(start_time, wait_time, sec):
    if sec >= start_time + wait_time:
        return True
    return False


# initialize lists
nums = list(range(NUM_BUTTONS))
random.shuffle(nums)
answer = [nums.index(i) for i in range(NUM_BUTTONS)]
buttons = [Button(i, n) for i, n in zip(range(NUM_BUTTONS), nums)]


def main():
    # initialize variables
    gaming = False
    won = False
    lost = False
    sec = 0

    # main loop
    while True:

        # quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # checks if user pressed spacebar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not (won or lost):
                        gaming = True

            # checks if user clicked a button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not (won or lost) and gaming:
                    for button in buttons:
                        button.is_clicked()

        SCREEN.fill(WHITE)

        # if game is not ended
        if not (won or lost):
            
            # if game is started
            if gaming:

                # draw opened buttons
                for button in buttons:
                    if button.opened:
                        button.display_button()
                        button.display_num()
                    else:
                        button.display_button(GRAY)

                # check if user won or lost the game
                if clicked_nums != answer[:len(clicked_nums)]:
                    time_lost = sec
                    lost = True

                elif clicked_nums == answer:
                    time_won = sec
                    won = True

            # if game is not started yet
            else:

                # show all the buttons
                for button in buttons:
                    button.display_button()
                    button.display_num()

                # show text to show that user can press spacebar
                font = pygame.font.Font('freesansbold.ttf', 28)
                text = font.render("Press SPACE when you're ready", True, BLACK)
                text.set_alpha(int(255 * (math.sin(sec * 3))))
                text_rect = text.get_rect()
                text_rect.center = SCREEN.get_rect().center
                SCREEN.blit(text, text_rect)

                draw_timer(TIME_LIMIT, TIME_LIMIT - sec)

                # start the game after time limit
                if sec >= TIME_LIMIT:
                    gaming = True

        elif lost:

            for button in buttons:

                # draw opened buttons
                if button.opened:
                    button.display_button()
                    button.display_num()
                else:
                    button.display_button(GRAY)

                # draw O on correct button
                if button.index == answer[len(clicked_nums) - 1]:
                    button.display_button()
                    button.display_num()
                    button.draw_o()

                # draw X on clicked button
                if button.index == clicked_nums[-1]:
                    button.display_num()
                    button.draw_x()

            # display losing message
            font = pygame.font.Font('freesansbold.ttf', 28)
            text = font.render("You failed!", True, BLACK)
            text_rect = text.get_rect()
            text_rect.center = SCREEN.get_rect().center
            SCREEN.blit(text, text_rect)

            # end the program after 3 seconds
            if time_spent(time_lost, 3, sec):
                pygame.quit()
                sys.exit()

        elif won:

            # draw all the buttons
            for button in buttons:
                button.display_button()
                button.display_num()

            # display winning message
            font = pygame.font.Font('freesansbold.ttf', 28)
            text = font.render("Perfect!", True, BLACK)
            text_rect = text.get_rect()
            text_rect.center = SCREEN.get_rect().center
            SCREEN.blit(text, text_rect)

            # end the program after 3 seconds
            if time_spent(time_won, 3, sec):
                pygame.quit()
                sys.exit()

        # game tick & update sec value
        CLOCK.tick(TICK)
        sec += 1 / TICK

        pygame.display.flip()


if __name__ == '__main__':
    main()