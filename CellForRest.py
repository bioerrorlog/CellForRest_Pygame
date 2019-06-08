import pygame
import time
import random
import os
import math
from pygame.locals import *

pygame.init()

GAME_TITLE = 'CellForRest'
POINT_NAME = 'Leaf' # Game currency
DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 800

game_point = 1000000 # Default game currency

cave_power = 1 # Used by cell layer to increase cell power

CELL_LAYER_NAME = 'Cell'
TREE_LAYER_NAME = 'Forest'
CAVE_LAYER_NAME = 'Cave'

# Each game layer ON/OFF
menu_on = False
cell_layer = True
tree_layer = False
cave_layer = False
intro = True

black = (0, 0, 0)
white = (255, 255, 255)
up_white = (205, 198, 169)
red = (200, 0, 0)
bright_red = (255, 0, 0)

game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

clock = pygame.time.Clock()

init_map = pygame.image.load(os.path.join('images', 'start.png')) # Start screen
cell_map = pygame.image.load(os.path.join('images', 'cell_map.png')) # Cell layer background
tree_map = pygame.image.load(os.path.join('images', 'tree_map.png')) # Tree layer background
cave_map = pygame.image.load(os.path.join('images', 'cave_map.png')) # Cave layer background
menu_background = pygame.image.load(os.path.join('images', 'menu_background.png')) # Menu screen

button_up_white = pygame.image.load(os.path.join('images', 'button_up_white.png'))
button_white = pygame.image.load(os.path.join('images', 'button_white.png'))
button_black = pygame.image.load(os.path.join('images', 'button_black.png'))

icon_img = pygame.image.load(os.path.join('images', 'icon.png'))
pygame.display.set_icon(icon_img)

FONT = 'JKG-L_3.ttf' # http://font.cutegirl.jp


# Init start menu
# Start button: init gameLoop()
# x / quit button: quit game
def gameInit():
    global intro
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()
        game_display.blit(init_map, (0,0))
        textDisplay(GAME_TITLE, FONT, 150, white, (DISPLAY_WIDTH/2), (DISPLAY_HEIGHT / 8)*3)

        button("Start",20,black,(DISPLAY_WIDTH/4),(DISPLAY_HEIGHT/4)*3,100,50,button_white,button_up_white, gameLoop)
        button("Quit", 20, black, (DISPLAY_WIDTH / 4)*3-50, (DISPLAY_HEIGHT / 4)*3, 100, 50, button_white, button_up_white, gameQuit)

        pygame.display.update()
        clock.tick(60)


# Game loop: event.get() -> update() -> draw() -> display.update() -> clear()
# x button: Quit game
# m button: Menu
# Left click: Inform each game layer via setMouseEventUp()
def gameLoop():
    global intro
    intro = False
    game_exit = False

    cellLayerManager = CellLayerManager()
    treeLayerManager = TreeLayerManager()
    caveLayerManager = CaveLayerManager()

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    menu()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # cellLayerManeger uses pygame.mouse.get_pressed()
                treeLayerManager.setMouseEventUp(True)
                caveLayerManager.setMouseEventUp(True)

        cellLayerManager.update()
        treeLayerManager.update()
        caveLayerManager.update()

        if cell_layer == True:
            cellLayerManager.draw()
        elif tree_layer == True:
            treeLayerManager.draw()
        elif cave_layer == True:
            caveLayerManager.draw()

        pygame.display.update()
        clock.tick(60)

        treeLayerManager.clear()
        caveLayerManager.clear()


def gameQuit():
    pygame.quit()
    quit()


def menu():
    global menu_on
    menu_on = True

    game_display.blit(menu_background, (0, 0))
    textDisplay('PAUSE', FONT, 100, black, (DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2))

    while menu_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()

        button("Back", 20, white, (DISPLAY_WIDTH / 4), (DISPLAY_HEIGHT / 4)*3, 100, 50, button_black, button_up_white, quitMenu)
        button("Quit", 20, white, (DISPLAY_WIDTH / 4)*3, (DISPLAY_HEIGHT / 4)*3, 100, 50, button_black, button_up_white, gameQuit)

        pygame.display.update()
        clock.tick(60)


def quitMenu():
    global menu_on
    menu_on = False


# Create a button
# Button pressed: Execute action()
# msg: Text displayed on the button
# if mouseover: ac drawed
#   else: ic drawed
def button(msg, size, msg_color, x, y, w, h, ic, ac, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        game_display.blit(ac,(x,y))
        if click[0] == 1 and action != None:
            action()
    else:
        game_display.blit(ic,(x,y))

    textDisplay(msg, FONT, size, msg_color, (x+(w/2)), (y+(h/2)))


def textDisplay(text, font, size, color, center_x, center_y):
    textFont = pygame.font.Font(font, size)
    TextSurf = textFont.render(text, True, color)
    TextRect = TextSurf.get_rect()
    TextRect.center = (center_x, center_y)
    game_display.blit(TextSurf, TextRect)


def goToCellLayer():
    global cell_layer
    global tree_layer
    global cave_layer
    cell_layer = True
    tree_layer = False
    cave_layer = False


def goToTreeLayer():
    global cell_layer
    global tree_layer
    global cave_layer
    cell_layer = False
    tree_layer = True
    cave_layer = False


def goToCaveLayer():
    global cell_layer
    global tree_layer
    global cave_layer
    cell_layer = False
    tree_layer = False
    cave_layer = True


# Manage cell layer instances: gate and cell
class CellLayerManager:
    def __init__(self):
        self.gate = Gate(DISPLAY_WIDTH/2-60, DISPLAY_HEIGHT/2-60)

    def update(self):
        global game_point

        self.gate.update()

        for i in Cell.cell_list:
            i.update()
            if i.cell_age % i.divide_per == 0 and i.divide_limit > 0:
                self.genCell('SON',i.cell_x,i.cell_y,random.randrange(0, 8))
                i.divide_limit -= 1
            if i.cell_age > i.budding_time:
                i.budding()
                Cell.bud_list.append(i)
                Cell.cell_list.remove(i)

        for i in Cell.bud_list:
            if i.is_harvested == True:
                Cell.bud_list.remove(i)
                game_point += i.cell_power * cave_power

    # TODO: Improve draw speed
    def draw(self):
        game_display.blit(cell_map, (0, 0))

        self.gate.draw()

        for i in Cell.cell_list:
            i.draw()
        for i in Cell.bud_list:
            i.draw()

        if self.gate.is_generating == True:
                self.cellgenerating()

        game_display.blit(Cell.cell_gen_img_list[Cell.cell_gen_count], (self.gate.gate_x, self.gate.gate_y))

        textDisplay(POINT_NAME+': '+str(math.floor(game_point)),FONT,30,black,DISPLAY_WIDTH/2,20)

        button(CELL_LAYER_NAME,20,white,0,0,100,50,button_up_white,button_up_white,goToCellLayer)
        button(TREE_LAYER_NAME,20,white,110,0,100,50,button_black,button_up_white,goToTreeLayer)
        button(CAVE_LAYER_NAME,20,white,220,0,100,50,button_black,button_up_white,goToCaveLayer)

    def cellgenerating(self):
        global game_point

        if game_point > 0:
            game_point -= 1
            if Cell.cell_gen_count < Cell.cell_gen_img_list_size:
                Cell.cell_gen_count += 1
            else:
                self.genCell('NEW',self.gate.gate_x+20,self.gate.gate_y+40,6)
                Cell.cell_gen_count = 0
        else:
            textDisplay('NO '+POINT_NAME+'!',FONT,20,red,self.gate.gate_x+self.gate.gate_width/2,self.gate.gate_y-20)

    def genCell(self,name,x,y,dir):
        cell = Cell(name,x,y,dir)
        Cell.cell_list.append(cell)


# While Gate pressed, generate a cell gradually
# Cell generation process is executed in CellLayerManager
class Gate:
    def __init__(self, x, y):
        self.gate_act = pygame.image.load(os.path.join('images', 'gate_act.png'))
        self.gate_inact = pygame.image.load(os.path.join('images', 'gate_inact.png'))

        self.gate_width = self.gate_act.get_width()
        self.gate_height = self.gate_act.get_height()
        self.gate_x = x
        self.gate_y = y

        self.is_generating = False

    def update(self):
        self.is_generating = False

    # if mouseover: gate_act drawed
    #     else: gate_inact drawed
    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.gate_x+self.gate_width > mouse[0] > self.gate_x and self.gate_y+self.gate_height > mouse[1] > self.gate_y:
            game_display.blit(self.gate_act, (self.gate_x, self.gate_y))
            if click[0] == 1:
                self.is_generating = True
        else:
            game_display.blit(self.gate_inact, (self.gate_x, self.gate_y))


# Cells move around
# After while (budding_time), cell changes to bud
# Buds can be harvested by clicking
class Cell:
    # Instance list
    cell_list = []
    bud_list = []

    # Cell generation image list
    cell_gen_img_list = []
    cell_gen_img_list_size = 74
    cell_gen_count = 0

    for i in range(cell_gen_img_list_size+1):
        cell_gen_img_list.append(pygame.image.load(os.path.join('images', 'generate_' + str(i) + '.png')))

    def __init__(self,name,x,y,dir):
        self.cell_img_stay = pygame.image.load(os.path.join('images', 'cell_img_stay.png'))
        self.cell_img_left = pygame.image.load(os.path.join('images', 'cell_img_left.png'))
        self.cell_img_right = pygame.image.load(os.path.join('images', 'cell_img_right.png'))
        self.cell_img_down = pygame.image.load(os.path.join('images', 'cell_img_down.png'))
        self.cell_img_up = pygame.image.load(os.path.join('images', 'cell_img_up.png'))
        self.bud_img = pygame.image.load(os.path.join('images', 'bud.png'))
        self.bud_act_img = pygame.image.load(os.path.join('images', 'bud_act.png'))
        self.cell_img = self.cell_img_stay # Store a image to display

        self.cell_width = self.cell_img.get_width()
        self.cell_height = self.cell_img.get_height()
        self.cell_x = x
        self.cell_y = y

        self.divide_limit = 1 # times
        self.divide_per = 200 # frames
        self.cell_age = 0 # frames
        self.budding_time = 500 # frames
        self.cell_power = 40 # Added to game_point when harvested
        self.is_budded = False
        self.is_harvested = False

        self.is_moving = True
        self.move_count = 0 # frames after started to move
        self.cell_speed = 1 # pixel
        self.cell_dir = dir

        self.cell_name = name

    def update(self):
        if self.is_budded == False:
            self.move()
        self.cell_age += 1

    def draw(self):
        click = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()

        if self.is_budded == False:
            game_display.blit(self.cell_img, (self.cell_x, self.cell_y))
        else:
            if self.cell_x+self.cell_width > mouse[0] > self.cell_x and self.cell_y+self.cell_height > mouse[1] > self.cell_y:
                game_display.blit(self.bud_act_img, (self.cell_x, self.cell_y))
                if click[0] == 1:
                    self.is_harvested = True
            else:
                game_display.blit(self.bud_img, (self.cell_x, self.cell_y))

    def move(self):
        if self.is_moving:

            # Wall collision: Stop moving
            if self.cell_x < 0:
                self.cell_x = 0
                self.is_moving = False
            elif self.cell_x > DISPLAY_WIDTH - self.cell_width:
                self.cell_x = DISPLAY_WIDTH - self.cell_width
                self.is_moving = False
            elif self.cell_y < 0:
                self.cell_y = 0
                self.is_moving = False
            elif self.cell_y > DISPLAY_HEIGHT - self.cell_height:
                self.cell_y = DISPLAY_HEIGHT - self.cell_height
                self.is_moving = False

            # Normal move: Stay or move random dirction
            else:
                if self.move_count > 100:
                    self.is_moving = False
                    self.cell_img = self.cell_img_stay
                    self.move_count = 0
                else:
                    if self.cell_dir == 0: # Move to right
                        self.cell_img = self.cell_img_right
                        self.cell_x += self.cell_speed
                    elif self.cell_dir == 1: # Move to left
                        self.cell_img = self.cell_img_left
                        self.cell_x -= self.cell_speed
                    elif self.cell_dir == 2: # Move down
                        self.cell_img = self.cell_img_down
                        self.cell_y += self.cell_speed
                    elif self.cell_dir == 3: # Move up
                        self.cell_img = self.cell_img_up
                        self.cell_y -= self.cell_speed
                    elif self.cell_dir == 4: # Move to right faster
                        self.cell_img = self.cell_img_right
                        self.cell_x += self.cell_speed * 2
                    elif self.cell_dir == 5: # Move to left faster
                        self.cell_img = self.cell_img_left
                        self.cell_x -= self.cell_speed * 2
                    elif self.cell_dir == 6: # Move down faster
                        self.cell_img = self.cell_img_down
                        self.cell_y += self.cell_speed * 2
                    elif self.cell_dir == 7: # Move up faster
                        self.cell_img = self.cell_img_up
                        self.cell_y -= self.cell_speed * 2

                    self.move_count += 1

        else: # Stopping
            if self.move_count > 100:
                self.is_moving = True
                self.cell_dir = random.randrange(0, 8)
                self.move_count = 0
            else:
                self.cell_img = self.cell_img_stay
                self.move_count += 1

    def budding(self):
        self.is_budded = True


# Manage tree layer instances: tree and humans
class TreeLayerManager:
    def __init__(self):
        self.tree = Tree()
        self.house = House()
        self.mouseEventUp = False

    # Get left click from gameLoop()
    def setMouseEventUp(self,is_clicked):
        self.mouseEventUp = is_clicked

    # Increase game_point every frame by tree_power * human
    def update(self):
        global game_point

        self.tree.update()
        self.house.update()
        for i in Human.human_list:
            i.update()

        game_point += self.tree.tree_power[self.tree.tree_level] * (self.house.gen_count + 1)

    def draw(self):
        game_display.blit(tree_map, (0, 0))

        self.tree.draw(self.mouseEventUp)
        self.house.draw(self.mouseEventUp)
        for i in Human.human_list:
            i.draw()

        textDisplay(POINT_NAME+': '+str(math.floor(game_point)),FONT,30,black,DISPLAY_WIDTH/2,20)

        button(CELL_LAYER_NAME,20,white,0,0,100,50,button_black,button_up_white,goToCellLayer)
        button(TREE_LAYER_NAME,20,white,110,0,100,50,button_up_white,button_up_white,goToTreeLayer)
        button(CAVE_LAYER_NAME,20,white,220,0,100,50,button_black,button_up_white,goToCaveLayer)

    def clear(self):
        self.setMouseEventUp(False)


# They walk around
# And increase tree_power
class Human:
    # Instance list
    human_list = []

    def __init__(self, name, x):
        self.human_stay = pygame.image.load(os.path.join('images', 'human_stay.png'))
        self.human_left = pygame.image.load(os.path.join('images', 'human_left.png'))
        self.human_right = pygame.image.load(os.path.join('images', 'human_right.png'))
        self.human_img = self.human_left # Store image to display

        self.human_width = self.human_img.get_width()
        self.human_height = self.human_img.get_height()
        self.human_x = x
        self.human_y = DISPLAY_HEIGHT - self.human_height

        self.human_moving = True
        self.move_count = 0 # frame
        self.human_speed = 2 # pixels
        self.human_dir = 2 # Left

        self.human_name = name

    def move(self):
        if self.human_moving:

            # Wall collision: Stop moveing
            if self.human_x < 0:
                self.human_x = 0
                self.human_moving = False
            elif self.human_x > DISPLAY_WIDTH - self.human_width:
                self.human_x = DISPLAY_WIDTH - self.human_width
                self.human_moving = False

            # Normal move: Stay or move random dirction (left / right)
            else:
                if self.move_count > 20:
                    self.human_moving = False
                    self.human_img = self.human_stay
                    self.move_count = 0
                else:
                    if self.human_dir == 0:#Go left
                        self.human_img = self.human_left
                        self.human_x -= self.human_speed
                    elif self.human_dir == 1:#Go right
                        self.human_img = self.human_right
                        self.human_x += self.human_speed
                    elif self.human_dir == 2:#Go left faster
                        self.human_img = self.human_left
                        self.human_x -= self.human_speed * 2
                    elif self.human_dir == 3:#Go right
                        self.human_img = self.human_right
                        self.human_x += self.human_speed * 2

                    self.move_count +=1
        else:
            if self.move_count > 15:
                self.human_moving = True
                self.human_dir = random.randrange(0, 4)
                self.move_count = 0
            else:
                self.human_img = self.human_stay
                self.move_count += 1

    def update(self):
        self.move()

    def draw(self):
        game_display.blit(self.human_img, (self.human_x, self.human_y))


# Tree increases game_point by tree_power every frame
# if Tree clicked: treeShopping window appears
#     if "Level Up" button clicked: Tree level up
class Tree:
    def __init__(self):
        self.tree_img_list_num = 8
        self.tree_level = 0

        self.tree_img_list = []
        self.tree_ac_img_list = []
        self.tree_width_list = []
        self.tree_height_list = []
        self.tree_xy_list = []

        self.tree_cost =[100, 500, 1000, 3000, 10000, 50000, 100000]
        self.tree_power =[0, 0.1, 1, 11, 111, 1111, 11111, 111111]

        self.tree_shop = False

        for i in range(self.tree_img_list_num):
            self.tree_img_list.append(pygame.image.load(os.path.join('images','tree_' + str(i) + '.png')))
            self.tree_ac_img_list.append(pygame.image.load(os.path.join('images','tree_ac_' + str(i) + '.png')))
            self.tree_width_list.append(self.tree_img_list[i].get_width())
            self.tree_height_list.append(self.tree_img_list[i].get_height())
            self.tree_xy_list.append((DISPLAY_WIDTH/2-self.tree_width_list[i]/2,DISPLAY_HEIGHT-self.tree_height_list[i]))

    def update(self):
        pass

    # if mouseover: tree_ac_img_list drawed
    #     else: tree_img_list drawed
    # Click out of tree: disappear treeShopping button
    def draw(self,mouseEventUp):
        mouse = pygame.mouse.get_pos()

        if self.tree_xy_list[self.tree_level][0]+self.tree_width_list[self.tree_level] > mouse[0] > self.tree_xy_list[self.tree_level][0] and self.tree_xy_list[self.tree_level][1]+self.tree_height_list[self.tree_level] > mouse[1] > self.tree_xy_list[self.tree_level][1]:
            if mouseEventUp == True:
                self.tree_shop = True
            game_display.blit(self.tree_ac_img_list[self.tree_level],self.tree_xy_list[self.tree_level])
        else:
            if mouseEventUp == True:
                self.closeTreeShopping()
            game_display.blit(self.tree_img_list[self.tree_level],self.tree_xy_list[self.tree_level])

        if self.tree_shop == True:
            if self.tree_level < len(self.tree_img_list) - 1:
                self.treeShopping()
            else:
                # If tree_level reaches max level...
                pass

    def treeShopping(self):
        textDisplay('Cost: '+str(self.tree_cost[self.tree_level])+'Leaf',FONT,20,black,DISPLAY_WIDTH/2,self.tree_xy_list[self.tree_level][1]-70)
        button("Level Up",20,white,DISPLAY_WIDTH/2-50,self.tree_xy_list[self.tree_level][1]-50,100,50,button_black,button_up_white,self.treeGrowth)

    def treeGrowth(self):
        global game_point
        if game_point >= self.tree_cost[self.tree_level]:
            game_point -= self.tree_cost[self.tree_level]
            self.tree_level += 1
            self.closeTreeShopping()
        else:
            textDisplay('NO Leaf!',FONT,20,red,DISPLAY_WIDTH/2,self.tree_xy_list[self.tree_level][1]-100)

    def closeTreeShopping(self):
        self.tree_shop = False


# House creates humans
# if House clicked: Shopping window appears
#     if "Human +1" button clicked: Create a human
class House:
    def __init__(self):
        self.act_img = pygame.image.load(os.path.join('images', 'house_act.png'))
        self.inact_img = pygame.image.load(os.path.join('images', 'house_inact.png'))

        self.width = self.act_img.get_width()
        self.height = self.act_img.get_height()
        self.x = DISPLAY_WIDTH - self.width
        self.y = DISPLAY_HEIGHT - self.height

        # Human creation cost
        self.cost =[100, 500, 1000, 3000, 10000, 50000, 100000]

        self.gen_count = 0

        self.is_shopping = False
        self.is_generating = False

    def update(self):
        pass

    # if mouseover: act_img drawed
    #     else: inact_img drawed
    # Click out of house: disappear shopping button
    def draw(self,mouseEventUp):
        mouse = pygame.mouse.get_pos()

        if self.x+self.width > mouse[0] > self.x and self.y+self.height > mouse[1] > self.y:
            if mouseEventUp == True:
                self.is_shopping = True
            game_display.blit(self.act_img, (self.x, self.y))
        else:
            if mouseEventUp == True:
                self.closeShop()
            game_display.blit(self.inact_img, (self.x, self.y))

        if self.is_shopping == True:
            if self.gen_count < len(self.cost):
                self.shopping()
            else:
                textDisplay('No more human!',FONT,20,red,self.x-20,self.y-50)

    def shopping(self):
        textDisplay('Cost: '+str(self.cost[self.gen_count])+'Leaf',FONT,20,black,self.x-20,self.y-70)
        button("Human +1",20,white,self.x-70,self.y-50,100,50,button_black,button_up_white,self.genHuman)

    def closeShop(self):
        self.is_shopping = False

    def genHuman(self):
        global game_point
        if(game_point >= self.cost[self.gen_count]):
            game_point -= self.cost[self.gen_count]
            Human.human_list.append(Human("name",DISPLAY_WIDTH-self.width))
            self.gen_count += 1
            self.closeShop()
        else:
            textDisplay('NO Leaf!',FONT,20,red,self.house.y-20,self.house.y-100)


# Manage cave layer instance: blueGem
class CaveLayerManager:
    def __init__(self):
        self.blueGem = BlueGem()
        self.mouseEventUp = False

    # Get left click from gameLoop()
    def setMouseEventUp(self,is_clicked):
        self.mouseEventUp = is_clicked

    def update(self):
        global game_point
        self.blueGem.update()

    def draw(self):
        game_display.blit(cave_map, (0, 0))

        self.blueGem.draw(self.mouseEventUp)

        textDisplay(POINT_NAME+': '+str(math.floor(game_point)),FONT,30,white,DISPLAY_WIDTH/2,20)

        button(CELL_LAYER_NAME,20,white,0,0,100,50,button_black,button_up_white,goToCellLayer)
        button(TREE_LAYER_NAME,20,white,110,0,100,50,button_black,button_up_white,goToTreeLayer)
        button(CAVE_LAYER_NAME,20,white,220,0,100,50,button_up_white,button_up_white,goToCaveLayer)

    def clear(self):
        self.setMouseEventUp(False)

# BlueGem reinforces cell_power according to its level
# if BlueGem clicked: Shopping window appears
#     if "Level Up" button clicked: Level up and blueStar increases
class BlueGem:
    def __init__(self):
        self.img = pygame.image.load(os.path.join('images','blueGem.png'))
        self.act_img = pygame.image.load(os.path.join('images','blueGemEffect_act.png'))
        self.inact_img = pygame.image.load(os.path.join('images','blueGemEffect_inact.png'))
        self.water_img = pygame.image.load(os.path.join('images','water.png'))

        self.star_img_list = []
        self.star_img_num = 3
        for i in range(self.star_img_num+1):
            self.star_img_list.append(pygame.image.load(os.path.join('images','blueStar_'+str(i)+'.png')))

        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = DISPLAY_WIDTH/2 - self.width/2
        self.y = DISPLAY_HEIGHT - self.height - 10
        self.effect_width = self.act_img.get_width()
        self.effect_height = self.act_img.get_height()
        self.effect_x = DISPLAY_WIDTH/2 - self.effect_width/2
        self.effect_y = DISPLAY_HEIGHT - self.effect_height

        # Level up cost
        self.cost =[10000, 50000, 100000]
        self.level = 0

        self.is_shopping = False
        self.is_generating = False

    def update(self):
        pass

    # if mouseover: act_img drawed
    #     else: inact_img drawed
    # Click out of blueGem: disappear shopping button
    def draw(self,mouseEventUp):
        mouse = pygame.mouse.get_pos()
        game_display.blit(self.img, (self.x, self.y))

        if self.x+self.width > mouse[0] > self.x and self.y+self.height > mouse[1] > self.y:
            if mouseEventUp == True:
                self.is_shopping = True
            game_display.blit(self.act_img, (self.effect_x, self.effect_y))
        else:
            if mouseEventUp == True:
                self.closeShop()
            game_display.blit(self.inact_img, (self.effect_x, self.effect_y))

        if self.is_shopping == True:
            if self.level < len(self.cost):
                self.shopping()
            else:
                textDisplay('Max level!',FONT,20,bright_red,DISPLAY_WIDTH/2,self.y-50)

        game_display.blit(self.water_img, (-5,DISPLAY_HEIGHT-86))
        game_display.blit(self.star_img_list[self.level], (0,0))


    def shopping(self):
        textDisplay('Cost: '+str(self.cost[self.level])+'Leaf',FONT,20,white,DISPLAY_WIDTH/2,self.y-90)
        button("Level Up",20,white,DISPLAY_WIDTH/2-50,self.y-70,100,50,button_black,button_up_white,self.genStar)

    def closeShop(self):
        self.is_shopping = False

    def genStar(self):
        global game_point
        global cave_power
        if(game_point >= self.cost[self.level]):
            game_point -= self.cost[self.level]
            self.level += 1

            if self.level == 1:
                cave_power = 11
            elif self.level == 2:
                cave_power = 111
            elif self.level == 3:
                cave_power = 11111

            self.closeShop()

        else:
            textDisplay('NO Leaf!',FONT,20,bright_red,DISPLAY_WIDTH/2,self.y-50)


gameInit()
gameQuit()
