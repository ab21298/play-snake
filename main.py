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

# gameTitle
pygame.display.set_caption("PLAY SNAKE")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plotsnkae(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        gameWindow.blit(welcomeimage, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameLoop()

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
                        pygame.mixer.music.load('data/audio/turnBeep.mp3')
                        pygame.mixer.music.play()
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                        pygame.mixer.music.load('data/audio/turnBeep.mp3')
                        pygame.mixer.music.play()
                    if event.key == pygame.K_UP:
                        velocity_x = 0
                        velocity_y = -init_velocity
                        pygame.mixer.music.load('data/audio/turnBeep.mp3')
                        pygame.mixer.music.play()
                    if event.key == pygame.K_DOWN:
                        velocity_x = 0
                        velocity_y = init_velocity
                        pygame.mixer.music.load('data/audio/turnBeep.mp3')
                        pygame.mixer.music.play()
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
                if score > 50:
                    # init_velocity = init_velocity + 1;
                    init_velocity = 6
                if score > 100:
                    # init_velocity = init_velocity + 1;
                    init_velocity = 7
                if score > 150:
                    # init_velocity = init_velocity + 1;
                    init_velocity = 8
                if score > 250:
                    # init_velocity = init_velocity + 1;
                    init_velocity = 9
                if score > 400:
                    # init_velocity = init_velocity + 1;
                    init_velocity = 10
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
                pygame.mixer.music.load('data/audio/accident.mp3')
                pygame.mixer.music.play()
                game_over = True
            if head in snk_list[:-1]:
                pygame.mixer.music.load('data/audio/accident.mp3')
                pygame.mixer.music.play()
                game_over = True

            plotsnkae(gameWindow, black, snk_list, snake_size)
            text_screen("Score: " + str(score), white, 10, 10)
            text_screen("High Score: " + str(hiscore), white, 430, 10)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    exit()


welcome()
