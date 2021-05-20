import pygame
import random
import os

pygame.mixer.init()
pygame.init()

# colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# creating gameWindow
screen_width = 600
screen_height = 400
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# gameImages
welcomeimage = pygame.image.load('data/images/welcome.jpeg')
welcomeimage = pygame.transform.scale(welcomeimage, (screen_width, screen_height)).convert_alpha()
backgroundimage = pygame.image.load('data/images/background.jpg')
backgroundimage = pygame.transform.scale(backgroundimage, (screen_width, screen_height)).convert_alpha()
gameover = pygame.image.load('data/images/gameover.jpg')
gameover = pygame.transform.scale(gameover, (screen_width, screen_height)).convert_alpha()
p1image = pygame.image.load('data/images/p1.jpeg')
p1image = pygame.transform.scale(p1image, (screen_width, screen_height)).convert_alpha()
p2image = pygame.image.load('data/images/p2.jpeg')
p2image = pygame.transform.scale(p2image, (screen_width, screen_height)).convert_alpha()
p1wimage = pygame.image.load('data/images/p1w.jpeg')
p1wimage = pygame.transform.scale(p1wimage, (screen_width, screen_height)).convert_alpha()
p2wimage = pygame.image.load('data/images/p2w.jpeg')
p2wimage = pygame.transform.scale(p2wimage, (screen_width, screen_height)).convert_alpha()
mtimage = pygame.image.load('data/images/mt.jpeg')
mtimage = pygame.transform.scale(mtimage, (screen_width, screen_height)).convert_alpha()

# gameTitle
pygame.display.set_caption("PLAY SNAKE")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)


class button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, gamewindow, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(gamewindow, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(gamewindow, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font1 = pygame.font.SysFont(None, 25)
            text = font1.render(self.text, 1, (0, 0, 0))
            gamewindow.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plotsnkae(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def welcome():
    greenButton = button((0, 255, 0), 250, 320, 100, 30, 'CONTINUE')
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        gameWindow.blit(welcomeimage, (0, 0))
        greenButton.draw(gameWindow, (0, 0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                exit_game = True
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    MainMenu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(pos)
                if greenButton.isOver(pos):
                    # print("Clicked the button")
                    MainMenu()

            if event.type == pygame.MOUSEMOTION:
                # print(pos)
                if greenButton.isOver(pos):
                    greenButton.color = (255, 0, 0)
                else:
                    greenButton.color = (0, 255, 0)

        pygame.display.update()
        clock.tick(30)


def gameLoop():
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 15
    velocity_x = 0
    velocity_y = 0
    init_velocity = 5
    score = 0
    food_x = random.randint(30, 570)
    food_y = random.randint(30, 370)
    fps = 30

    snk_list = []
    snk_length = 1

    if (not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            gameWindow.blit(gameover, (0, 0))
            text_screen("Your Score = " + str(score), white, 10, 10)
            text_screen("High Score: " + str(hiscore), white, 430, 10)
            # text_screen("Game Over ! Press Enter to continue", red, 80, screen_height / 2)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                        # pygame.mixer.music.load('data/audio/turnBeep.mp3')
                        # pygame.mixer.music.play()
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                        # pygame.mixer.music.load('data/audio/turnBeep.mp3')
                        # pygame.mixer.music.play()
                    if event.key == pygame.K_UP:
                        velocity_x = 0
                        velocity_y = -init_velocity
                        # pygame.mixer.music.load('data/audio/turnBeep.mp3')
                        # pygame.mixer.music.play()
                    if event.key == pygame.K_DOWN:
                        velocity_x = 0
                        velocity_y = init_velocity
                        # pygame.mixer.music.load('data/audio/turnBeep.mp3')
                        # pygame.mixer.music.play()
                    if event.key == pygame.K_a:
                        score = score + 10
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 8 and abs(snake_y - food_y) < 8:
                score += 10

                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length = snk_length + 2
                if score > int(hiscore):
                    hiscore = score
            if 100 > score > 50:
                # init_velocity = init_velocity + 1;
                init_velocity = 7
            if 150 > score > 100:
                # init_velocity = init_velocity + 1;
                init_velocity = 10
            if 250 > score > 150:
                # init_velocity = init_velocity + 1;
                init_velocity = 12
            if 400 > score > 250:
                # init_velocity = init_velocity + 1;
                init_velocity = 14
            if score > 400:
                # init_velocity = init_velocity + 1;
                init_velocity = 16
            gameWindow.fill(white)
            gameWindow.blit(backgroundimage, (0, 0))
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
            # pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                # pygame.mixer.music.load('data/audio/accident.mp3')
                # pygame.mixer.music.play()
                game_over = True
            if head in snk_list[:-1]:
                # pygame.mixer.music.load('data/audio/accident.mp3')
                # pygame.mixer.music.play()
                game_over = True

            plotsnkae(gameWindow, black, snk_list, snake_size)
            text_screen("Score: " + str(score), white, 10, 10)
            text_screen("High Score: " + str(hiscore), white, 430, 10)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    exit()


def MainMenu():
    pygame.display.set_caption("MAIN MENU")
    mainButton1 = button((0, 255, 0), 225, 150, 150, 30, '1.Single Player')
    mainButton2 = button((0, 255, 0), 225, 200, 150, 30, '2.Multi Player')
    exit_game = False
    while not exit_game:
        gameWindow.fill((51, 255, 247))
        mainButton1.draw(gameWindow, (0, 0, 0))
        mainButton2.draw(gameWindow, (0, 0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            pos1 = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                exit_game = True
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameLoop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(pos)
                if mainButton1.isOver(pos1):
                    # print("Clicked the button")
                    gameLoop()
                if mainButton2.isOver(pos1):
                    gameLoopM()

            if event.type == pygame.MOUSEMOTION:
                # print(pos)
                if mainButton1.isOver(pos1):
                    mainButton1.color = (255, 0, 0)
                else:
                    mainButton1.color = (0, 255, 0)
                if mainButton2.isOver(pos1):
                    mainButton2.color = (255, 0, 0)
                else:
                    mainButton2.color = (0, 255, 0)

        pygame.display.update()
        clock.tick(30)


def gameLoopM():
    gameWindow1 = pygame.display.set_mode((screen_width, screen_height))
    gameWindow2 = pygame.display.set_mode((screen_width, screen_height))

    def player2():
        # pygame.display.set_caption("PLAYER 2")
        exit_game = False

        def text_screen(text, color, x, y):
            screen_text = font.render(text, True, color)
            gameWindow2.blit(screen_text, [x, y])

        while not exit_game:
            gameWindow2.fill(white)
            # text_screen("Player 2 turn Press enter to play", black, 50, 50)
            gameWindow.blit(p2image, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        loop2()
                        return
            pygame.display.update()

    def player1():
        # pygame.display.set_caption("PLAYER 1")
        exit_game = False

        def text_screen(text, color, x, y):
            screen_text = font.render(text, True, color)
            gameWindow1.blit(screen_text, [x, y])

        while not exit_game:
            gameWindow1.fill(white)
            # text_screen("Player 1 turn Press enter to play", black, 50, 50)
            gameWindow.blit(p1image, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        loop1()
                        return
            pygame.display.update()

    def loop1():
        exit_game = False
        game_over = False
        snake_x = 45
        snake_y = 55
        snake_size = 15
        velocity_x = 0
        velocity_y = 0
        init_velocity = 5
        score = 0
        food_x = random.randint(30, 570)
        food_y = random.randint(30, 370)
        fps = 30

        snk_list = []
        snk_length = 1

        if (not os.path.exists("player1.txt")):
            with open("player1.txt", "w") as f:
                f.write("0")

        with open("player1.txt", "r") as f:
            player1 = f.read()

        while not exit_game:
            if game_over:
                with open("player1.txt", "w") as f:
                    f.write(str(score))
                gameWindow.fill((51, 255, 247))
                # gameWindow.blit(gameover, (0, 0))
                # global s1
                # s1 = score
                text_screen("Score = " + str(score), black, 100, 100)
                # text_screen("High Score: " + str(hiscore), white, 430, 10)
                text_screen("Better luck next time ! Press Enter to continue", red, 80, screen_height / 2)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_game = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            return
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_game = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            velocity_x = init_velocity
                            velocity_y = 0
                            # pygame.mixer.music.load('data/audio/turnBeep.mp3')
                            # pygame.mixer.music.play()
                        if event.key == pygame.K_LEFT:
                            velocity_x = -init_velocity
                            velocity_y = 0
                            # pygame.mixer.music.load('data/audio/turnBeep.mp3')
                            # pygame.mixer.music.play()
                        if event.key == pygame.K_UP:
                            velocity_x = 0
                            velocity_y = -init_velocity
                            # pygame.mixer.music.load('data/audio/turnBeep.mp3')
                            # pygame.mixer.music.play()
                        if event.key == pygame.K_DOWN:
                            velocity_x = 0
                            velocity_y = init_velocity
                            # pygame.mixer.music.load('data/audio/turnBeep.mp3')
                            # pygame.mixer.music.play()
                        if event.key == pygame.K_a:
                            score = score + 10
                snake_x = snake_x + velocity_x
                snake_y = snake_y + velocity_y

                if abs(snake_x - food_x) < 8 and abs(snake_y - food_y) < 8:
                    score += 10

                    food_x = random.randint(20, screen_width / 2)
                    food_y = random.randint(20, screen_height / 2)
                    snk_length = snk_length + 2
                    # if score > int(hiscore):
                    #     hiscore = score
                if 100 > score > 50:
                    # init_velocity = init_velocity + 1;
                    init_velocity = 8
                if 150 > score > 100:
                    # init_velocity = init_velocity + 1;
                    init_velocity = 10
                if 250 > score > 150:
                    # init_velocity = init_velocity + 1;
                    init_velocity = 12
                if 400 > score > 250:
                    # init_velocity = init_velocity + 1;
                    init_velocity = 14
                if score > 400:
                    # init_velocity = init_velocity + 1;
                    init_velocity = 16
                gameWindow.fill(white)
                gameWindow.blit(backgroundimage, (0, 0))
                pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
                # pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])

                head = [snake_x, snake_y]
                snk_list.append(head)

                if len(snk_list) > snk_length:
                    del snk_list[0]

                if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                    # pygame.mixer.music.load('data/audio/accident.mp3')
                    # pygame.mixer.music.play()
                    game_over = True
                if head in snk_list[:-1]:
                    # pygame.mixer.music.load('data/audio/accident.mp3')
                    # pygame.mixer.music.play()
                    game_over = True

                plotsnkae(gameWindow, black, snk_list, snake_size)
                text_screen("Score: " + str(score), white, 10, 10)
                # text_screen("High Score: " + str(hiscore), white, 430, 10)
            pygame.display.update()
            clock.tick(fps)

        pygame.quit()
        exit()

    def loop2():
        exit_game = False
        game_over = False
        snake_x = 45
        snake_y = 55
        snake_size = 15
        velocity_x = 0
        velocity_y = 0
        init_velocity = 5
        score = 0
        food_x = random.randint(30, 570)
        food_y = random.randint(30, 370)
        fps = 30

        snk_list = []
        snk_length = 1

        if (not os.path.exists("player2.txt")):
            with open("player2.txt", "w") as f:
                f.write("0")

        with open("player2.txt", "r") as f:
            player2 = f.read()

        while not exit_game:
            if game_over:
                with open("player2.txt", "w") as f:
                    f.write(str(score))
                gameWindow.fill((51, 255, 247))
                # gameWindow.blit(gameover, (0, 0))
                # global s2
                # s2 = score
                text_screen("Score = " + str(score), black, 100, 100)
                # text_screen("High Score: " + str(hiscore), white, 430, 10)
                text_screen("Better luck next time ! Press Enter to continue", red, 80, screen_height / 2)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_game = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            return
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit_game = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            velocity_x = init_velocity
                            velocity_y = 0
                            # pygame.mixer.music.load('data/audio/turnBeep.mp3')
                            # pygame.mixer.music.play()
                        if event.key == pygame.K_LEFT:
                            velocity_x = -init_velocity
                            velocity_y = 0
                            # pygame.mixer.music.load('data/audio/turnBeep.mp3')
                            # pygame.mixer.music.play()
                        if event.key == pygame.K_UP:
                            velocity_x = 0
                            velocity_y = -init_velocity
                            # pygame.mixer.music.load('data/audio/turnBeep.mp3')
                            # pygame.mixer.music.play()
                        if event.key == pygame.K_DOWN:
                            velocity_x = 0
                            velocity_y = init_velocity
                            # pygame.mixer.music.load('data/audio/turnBeep.mp3')
                            # pygame.mixer.music.play()
                        if event.key == pygame.K_a:
                            score = score + 10
                snake_x = snake_x + velocity_x
                snake_y = snake_y + velocity_y

                if abs(snake_x - food_x) < 8 and abs(snake_y - food_y) < 8:
                    score += 10

                    food_x = random.randint(20, screen_width / 2)
                    food_y = random.randint(20, screen_height / 2)
                    snk_length = snk_length + 2
                    # if score > int(hiscore):
                    #     hiscore = score
                if 100 > score > 50:
                    # init_velocity = init_velocity + 1;
                    init_velocity = 8
                if 150 > score > 100:
                    # init_velocity = init_velocity + 1;
                    init_velocity = 10
                if 250 > score > 150:
                    # init_velocity = init_velocity + 1;
                    init_velocity = 12
                if 400 > score > 250:
                    # init_velocity = init_velocity + 1;
                    init_velocity = 14
                if score > 400:
                    # init_velocity = init_velocity + 1;
                    init_velocity = 16
                gameWindow.fill(white)
                gameWindow.blit(backgroundimage, (0, 0))
                pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
                # pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])

                head = [snake_x, snake_y]
                snk_list.append(head)

                if len(snk_list) > snk_length:
                    del snk_list[0]

                if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                    # pygame.mixer.music.load('data/audio/accident.mp3')
                    # pygame.mixer.music.play()
                    game_over = True
                if head in snk_list[:-1]:
                    # pygame.mixer.music.load('data/audio/accident.mp3')
                    # pygame.mixer.music.play()
                    game_over = True
                # if int(score) > int(p1):
                #     game_over = True

                plotsnkae(gameWindow, black, snk_list, snake_size)
                text_screen("Score: " + str(score), white, 10, 10)
                text_screen("Player 1 : " + str(p1), white, 430, 10)
                # text_screen("High Score: " + str(hiscore), white, 430, 10)
            pygame.display.update()
            clock.tick(fps)

        pygame.quit()
        exit()

    player1()
    with open("player1.txt", "r") as f:
        p1 = f.read()
    player2()
    with open("player2.txt", "r") as f:
        p2 = f.read()
    # print(p1)
    # print(p2)

    exit_game = False
    while not exit_game:
        if p1 > p2:
            # gameWindow3 = pygame.display.set_mode((screen_width, screen_height))

            def text_s(text, color, x, y):
                screen_text = font.render(text, True, color)
                gameWindow.blit(screen_text, [x, y])

            gameWindow.fill(white)
            text_s("Player 1 wins ! press enter to play again", black, 50, 50)
            gameWindow.blit(p1wimage, (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        if p1 < p2:
            # gameWindow3 = pygame.display.set_mode((screen_width, screen_height))

            def text_s(text, color, x, y):
                screen_text = font.render(text, True, color)
                gameWindow.blit(screen_text, [x, y])

            gameWindow.fill(white)
            text_s("Player 2 wins ! press enter to play again", black, 50, 50)
            gameWindow.blit(p2wimage, (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        if p1 == p2:
            # gameWindow3 = pygame.display.set_mode((screen_width, screen_height))

            def text_s(text, color, x, y):
                screen_text = font.render(text, True, color)
                gameWindow.blit(screen_text, [x, y])

            gameWindow.fill(white)
            text_s("Match Draw ! press enter to play again", black, 50, 50)
            gameWindow.blit(mtimage, (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        # gameWindow.fill(white)
        # gameWindow.blit(gameover, (0, 0))
        # pygame.display.update()
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         exit()
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_RETURN:
        #             welcome()

    # clock.tick(fps)


welcome()
