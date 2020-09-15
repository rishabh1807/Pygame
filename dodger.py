import pygame
import time
import random
import dbm
# from pygame import gfxdraw

pygame.init()
pygame.display.init()
clock = pygame.time.Clock()

# colors     R    G    B
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
SKY_BLUE = (200, 200, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
# loading images
cloud1 = pygame.image.load('cloud.png')
cloud2 = pygame.image.load('cloud2.png')
bomb_img = pygame.image.load('bomb.png')
tree = pygame.image.load('tree.png')
tank_left = pygame.image.load('tank_left.png')
tank_right = pygame.image.load('tank_right.png')
fire = pygame.image.load('explosion.png')

# loading sounds

boom = pygame.mixer.Sound('boom1.wav')
beep = pygame.mixer.Sound('beep.wav')


# Display
Display_Height = 600
Display_Width = 1000

Display = pygame.display.set_mode((Display_Width, Display_Height))
pygame.display.set_caption('Dodger')
Ground_Height = 525

# database
database = dbm.open('high_score', 'c')
high_score = database.get('high_score')



# button


def button(x, y, color, text):
    btn_len = 100
    btn_hgt = 50
    mouse = pygame.mouse.get_pos()
    clicks = pygame.mouse.get_pressed()
    fontobj = pygame.font.Font('freesansbold.ttf', 25)
    textsufobj = fontobj.render(text, True, BLACK)
    textobj = textsufobj.get_rect()
    textobj.center = x + 45, y + 25
    if (btn_len + x > mouse[0] > x) and (btn_hgt + y > mouse[1] > y):
        pygame.draw.rect(
            Display, color, (x - 10, y - 10, btn_len + 20, btn_hgt + 20))
        if clicks[0] == 1:
            if text == 'PLAY !':
                beep.play()
                main()
            elif text == 'EXIT!!':
                beep.play()
                database.close()
                pygame.quit()
        Display.blit(textsufobj, textobj)
    else:
        pygame.draw.rect(Display, color, (x, y, btn_len, btn_hgt))
        Display.blit(textsufobj, textobj)


# crash function
def crash_lost(x, y=Ground_Height - 75, last=False):
    fontobj = pygame.font.Font('freesansbold.ttf', 45)
    textsufobj = fontobj.render('YOU LOST !!', True, BLACK,)
    textobj = textsufobj.get_rect()
    textobj.center = Display_Width // 2, Display_Height // 2
    Display.blit(fire, (x, y))
    boom.play()
    if last is True:
        Display.blit(textsufobj, textobj)
        pygame.display.update()
        time.sleep(3.5)
        intro()

# health bar


def tank_health_bar(value):
    msg = "Health :- {0}".format(value)
    fontobj = pygame.font.Font('freesansbold.ttf', 30)
    fontsurfobj = fontobj.render(msg, True, BLACK)
    textobj = fontsurfobj.get_rect()
    textobj.right = Display_Width
    Display.blit(fontsurfobj, textobj)


# score

def ScoreBoard(value):
    msg = "Score :- {0}".format(value)
    fontobj = pygame.font.Font('freesansbold.ttf', 30)
    fontsurfobj = fontobj.render(msg, True, BLACK)
    textobj = fontsurfobj.get_rect()
    Display.blit(fontsurfobj, textobj)


# animation function
def bomb(x=0, y=0):
    Display.blit(bomb_img, (x, y))


def tank_mv(x, is_right=False):
    # pygame.draw.rect(Display,BLACK,(Display_Width//2 + ch_x, Ground_Height,15,15))
    if is_right:
        Display.blit(tank_left, (x, Ground_Height - 50))
    else:
        Display.blit(tank_right, (x, Ground_Height - 50))


def background():
    pygame.draw.rect(Display, GREEN, (0, Ground_Height,
                                      Display_Width, Display_Height))
    # outline
    pygame.draw.aaline(Display, BLACK, (0, Ground_Height),
                       (Display_Width, Ground_Height))

    pygame.draw.rect(Display, SKY_BLUE, (0, 0, Display_Width, Ground_Height))


def cloud_mv(x, y, z):
    x = x % (Display_Width + 300)
    y = y % (Display_Width + 300)
    z = z % (Display_Width + 300)
    Display.blit(cloud1, (x - 300, 25))
    Display.blit(cloud2, (y - 300, 30))
    Display.blit(cloud1, (z - 300, 25))


def intro():
    # database = dbm.open('high_score', 'r', )
    r = 0
    g = 0
    b = 0
    delay = 0
    while True:
        delay += 1
        if delay % 4 == 0:
            r += 1
            g += 2
            b += 3
        color_change = (r % 255, g % 255, b % 255)
        Display.fill(color_change)
        button(300, 300, GREEN, 'PLAY !')
        button(666, 300, RED, 'EXIT!!')
        Display.blit(fire, (0, 0))
        Display.blit(fire, (850, 0))
        Display.blit(fire, (0, 450))
        Display.blit(fire, (850, 450))
        fontobj = pygame.font.Font("freesansbold.ttf", 57)
        fontobj_creator = pygame.font.Font("freesansbold.ttf", 20)
        textobj = fontobj.render('__GAME__', True, WHITE)
        textsufobj = textobj.get_rect()
        textsufobj.center = Display_Width // 2, 250
        Display.blit(textobj, textsufobj)
        textobj_creator = fontobj_creator.render(
            'Created by Rishabh Soni', True, BLACK)
        textsufobj_creator = textobj_creator.get_rect()
        textsufobj_creator.center = Display_Width // 2, 585
        Display.blit(textobj_creator, textsufobj_creator)
        textobj_high_score = fontobj_creator.render(
            f"high Score :- {database['high_score'].decode()}", True, BLACK)
        textsurf_high_score = textobj_high_score.get_rect()
        textsurf_high_score.center = Display_Width // 2, 440
        Display.blit(textobj_high_score, textsurf_high_score)

        # event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                database.close()
                pygame.quit()
        pygame.display.update()


# main game loop


def main():
    # var to control tank
    tank_health = 1000
    x_pos = Display_Width // 2
    obj_x = 0
    # score
    score = 0
    tank_dir_right = False
    # trees pos
    tree_1_pos = 40
    tree_2_pos = 800
    change_tree_1 = 0
    change_tree_2 = 0
    # variables to control sun speed
    temp_cloud_mv_var = 0
    cloud_mv_var = 0
    pygame.display.init()
    bomb_mv_var_x_1 = random.randrange(Display_Width)
    bomb_mv_var_x_2 = random.randrange(Display_Width)
    bomb_mv_var_y_1 = 0
    bomb_mv_var_y_2 = 0
    Game_Running = True

    while Game_Running:

        # cloud animation variables
        temp_cloud_mv_var += 1
        if temp_cloud_mv_var % 10 == 0:  # modulus reduces the speed
            cloud_mv_var += 1

        # background

        background()
        # cloud
        cloud_mv(cloud_mv_var, cloud_mv_var * 2, cloud_mv_var * 3)
        # tree
        # Display.blit(bomb, (300, 250))
        Display.blit(tree, (tree_1_pos, 330))
        Display.blit(tree, (tree_2_pos, 330))
        # object
        tank_mv(x_pos, tank_dir_right)  # object
        # scoreboard
        ScoreBoard(score)
        # health bar
        tank_health_bar(tank_health)
        # bomb
        bomb(bomb_mv_var_x_1, bomb_mv_var_y_1)
        bomb(bomb_mv_var_x_2, bomb_mv_var_y_2)
        # event-handling
        for event in pygame.event.get():

            #           #####exit-func-handling#####
            if event.type == pygame.QUIT:
                database.close()
                pygame.quit()
#           #############################
            # handling a key down event
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT):

                    obj_x -= 1
                    change_tree_1 += 1
                    change_tree_2 += 1

                    tank_dir_right = False
                if (event.key == pygame.K_RIGHT):

                    obj_x += 1
                    change_tree_1 -= 1
                    change_tree_2 -= 1

                    tank_dir_right = True
            # handling a key up event
            if event.type == pygame.KEYUP:
                obj_x = 0
                change_tree_1 = 0
                change_tree_2 = 0

            # Game_Running = False

        # change the drawing position
        x_pos += obj_x
        tree_1_pos += change_tree_1
        tree_2_pos += change_tree_2

        # tank stays whith in boundaries|
        # if (x_pos > Display_Width):   |
        #     tree_1_pos -= 1           |
        #     tree_2_pos -= 1           |
        # if (x_pos < 0):               | Don't need this no more...
        #     tree_1_pos += 1           |
        #     tree_2_pos += 1           |
        # bomb controling variables     |

        bomb_mv_var_y_1 += 7
        bomb_mv_var_y_2 += 8
        if bomb_mv_var_y_1 > Display_Height:
            bomb_mv_var_y_1 = 0

            bomb_mv_var_x_1 = random.randrange(Display_Width)

            score += 1
        if score > int(high_score):
            database['high_score'] = f"{score}"    
        if bomb_mv_var_y_2 > Display_Height:
            bomb_mv_var_x_2 = random.randrange(Display_Width)
            bomb_mv_var_y_2 = 0
        # crashig handling
        if tank_health < 0:
            crash_lost(x_pos, last=True)
        if (x_pos + 142 >= bomb_mv_var_x_1 >= x_pos) and bomb_mv_var_y_1 >= (Ground_Height - 50):

            tank_health -= 10
            crash_lost(x_pos)

        if (x_pos + 142 >= bomb_mv_var_x_2 >= x_pos) and bomb_mv_var_y_2 >= (Ground_Height - 50):

            tank_health -= 10
            crash_lost(x_pos)

        pygame.display.update()


clock.tick(30)

intro()
database.close()
pygame.quit()
