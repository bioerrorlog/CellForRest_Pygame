import pygame
import time
import random
import os
import math
from pygame.locals import *

pygame.init()

GAME_TITLE = 'CellForRest'
POINT_NAME = 'Leaf' # ゲーム内通貨
DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 800

# ゲーム内通貨の初期値
game_point = 1000000

# Cave power
cave_power = 1

# 各ゲームレイヤーの名前
CELL_LAYER_NAME = 'Cell'
TREE_LAYER_NAME = 'Forest'
CAVE_LAYER_NAME = 'Cave'

# 各ゲームレイヤー表示ON/OFFの初期設定
menu_on = False
cell_layer = True
tree_layer = False
cave_layer = False
intro = True

# 色の設定
black = (0, 0, 0)
white = (255, 255, 255)
up_white = (205, 198, 169)
red = (200, 0, 0)
bright_red = (255, 0, 0)

# ディスプレイを設定
game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

 # クロック設定
clock = pygame.time.Clock()

# 背景画像のロード
init_map = pygame.image.load(os.path.join('images', 'start.png')) # スタート画面
cell_map = pygame.image.load(os.path.join('images', 'cell_map.png')) # cellレイヤー背景画像
tree_map = pygame.image.load(os.path.join('images', 'tree_map.png')) # treeレイヤー背景画像
cave_map = pygame.image.load(os.path.join('images', 'cave_map.png')) # caveレイヤー背景画像
menu_background = pygame.image.load(os.path.join('images', 'menu_background.png')) # メニュー画面

# ボタン画像のロード
button_up_white = pygame.image.load(os.path.join('images', 'button_up_white.png')) # カーソルオーバー時に使用
button_white = pygame.image.load(os.path.join('images', 'button_white.png'))
button_black = pygame.image.load(os.path.join('images', 'button_black.png'))

# アイコン画像のロードと設定
icon_img = pygame.image.load(os.path.join('images', 'icon.png'))
pygame.display.set_icon(icon_img)

# フォントの設定
# http://font.cutegirl.jp/ から使用
FONT = 'JKG-L_3.ttf'

def gameInit():
    global intro
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # ×ボタンが押されたときにgameQuitする
                gameQuit()

        game_display.blit(init_map, (0,0))
        textDisplay(GAME_TITLE, FONT, 150, white, (DISPLAY_WIDTH/2), (DISPLAY_HEIGHT / 8)*3)

        button("Start",20,black,(DISPLAY_WIDTH/4),(DISPLAY_HEIGHT/4)*3,100,50,button_white,button_up_white, gameLoop) # Startが押されたらgameLoopを実行
        button("Quit", 20, black, (DISPLAY_WIDTH / 4)*3-50, (DISPLAY_HEIGHT / 4)*3, 100, 50, button_white, button_up_white, gameQuit) # Quitが押されたらgameQuitを実行

        # ディスプレイ更新
        pygame.display.update()
        clock.tick(60)

def gameLoop():
    global intro
    intro = False
    game_exit = False

    # レイヤを生成
    cellLayerManager = CellLayerManager()
    treeLayerManager = TreeLayerManager()
    caveLayerManager = CaveLayerManager()

    # ゲームループ
    while not game_exit:
        # マウスイベントの取得
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # ×ボタンが押されたときにgameQuitする
                gameQuit()
            elif event.type == pygame.KEYDOWN:  # mキーが押されて時にmenuを開く
                if event.key == pygame.K_m:
                    menu()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # 左クリックされたときに各レイヤに知らせる
                treeLayerManager.setMouseEventUp(True)
                caveLayerManager.setMouseEventUp(True)

        # レイヤを更新
        cellLayerManager.update()
        treeLayerManager.update()
        caveLayerManager.update()

        # どのレイヤーを描画するかを制御
        # マウスイベント処理もdraw()内に記述
        if cell_layer == True:
            cellLayerManager.draw()

        elif tree_layer == True:
            treeLayerManager.draw()

        elif cave_layer == True:
            caveLayerManager.draw()



        # ゲームdisplayの更新
        pygame.display.update()
        clock.tick(60)

        # クリア処理
        treeLayerManager.clear()
        caveLayerManager.clear()

# ゲームの終了
def gameQuit():
    pygame.quit()
    quit()

# メニュー画面を表示　
def menu():
    global menu_on
    menu_on = True

    game_display.blit(menu_background, (0, 0))
    textDisplay('PAUSE', FONT, 100, black, (DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2))
    while menu_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()

        button("Back", 20, white, (DISPLAY_WIDTH / 4), (DISPLAY_HEIGHT / 4)*3, 100, 50, button_black, button_up_white, unmenu) # Backボタンでunmenuを実行
        button("Quit", 20, white, (DISPLAY_WIDTH / 4)*3, (DISPLAY_HEIGHT / 4)*3, 100, 50, button_black, button_up_white, gameQuit) # QuitボタンでgameQuitを実行

        pygame.display.update()
        clock.tick(60)

# menuを終了
def unmenu():
    global menu_on
    menu_on = False

# ボタンを設置
# ボタンが押された時にはactionに指定されたメソッドを実行
# msgに指定された文字をボタンに描画
def button(msg, size, msg_color, x, y, w, h, ic, ac, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y: # マウスオーバーした時にはacを描画
        game_display.blit(ac,(x,y))
        if click[0] == 1 and action != None:
            action()
    else:
        game_display.blit(ic,(x,y)) # マウスオーバーしてないときにはicを描画

    textDisplay(msg, FONT, size, msg_color, (x+(w/2)), (y+(h/2)))

# テキストの表示 中央位置で指定する
def textDisplay(text, font, size, color, center_x, center_y):
    textFont = pygame.font.Font(font, size)
    TextSurf = textFont.render(text, True, color)
    TextRect = TextSurf.get_rect()
    TextRect.center = (center_x, center_y)
    game_display.blit(TextSurf, TextRect)

# cellレイヤーに切り替える
def goToCellLayer():
    global cell_layer
    global tree_layer
    global cave_layer
    cell_layer = True
    tree_layer = False
    cave_layer = False

# treeレイヤーに切り替える
def goToTreeLayer():
    global cell_layer
    global tree_layer
    global cave_layer
    cell_layer = False
    tree_layer = True
    cave_layer = False

# villaegレイヤーに切り替える
def goToCaveLayer():
    global cell_layer
    global tree_layer
    global cave_layer
    cell_layer = False
    tree_layer = False
    cave_layer = True

"""
cellレイヤーのインスタンス管理を行う
cellレイヤーにはGateのインスタンスが一つ、Cellのインスタンスが複数存在する
gate.is_generating == True のとき、cellの生成処理を行う"""
class CellLayerManager:
    def __init__(self):
        self.gate = Gate(DISPLAY_WIDTH/2-60, DISPLAY_HEIGHT/2-60) # gateを生成

    # cellレイヤの状態を更新
    def update(self):
        global game_point

        # gateの更新
        self.gate.update()

        # 出芽してないcellの更新
        for i in Cell.cell_list:
            i.update()
            if i.cell_age % i.divide_per == 0 and i.divide_limit > 0: # cellの複製
                self.genCell('SON',i.cell_x,i.cell_y,random.randrange(0, 8))
                i.divide_limit -= 1
            if i.cell_age > i.budding_time: # cellの発芽
                i.budding()
                Cell.bud_list.append(i)
                Cell.cell_list.remove(i)

        # 出芽したcellの更新
        for i in Cell.bud_list:
            if i.is_harvested == True: # 収穫されたかどうか
                Cell.bud_list.remove(i)
                game_point += i.cell_power * cave_power

    # cellレイヤを描画
    """
    TODO: cellが多いと描画がカクつく
          リストをforループで回すのではなく、イテレータを使った方が処理が早くなる...?
          Flyweightデザインパターンも要チェック"""
    def draw(self):
        game_display.blit(cell_map, (0, 0)) # cellレイヤ背景の描画

        # 各インスタンスの描画
        # イテレータにした方が処理速い？
        self.gate.draw()
        for i in Cell.cell_list:
            i.draw()
        for i in Cell.bud_list:
            i.draw()


        # gateがクリックされているとき、cellを生成する
        if self.gate.is_generating == True:
                self.cellgenerating()

        # game_pointの表示
        textDisplay(POINT_NAME+': '+str(math.floor(game_point)),FONT,30,black,DISPLAY_WIDTH/2,20)

        # 生成中のcellの描画
        game_display.blit(Cell.cell_gen_img_list[Cell.cell_gen_count], (self.gate.gate_x, self.gate.gate_y))

        # レイヤー切り替えボタンの描画
        button(CELL_LAYER_NAME,20,white,0,0,100,50,button_up_white,button_up_white,goToCellLayer)
        button(TREE_LAYER_NAME,20,white,110,0,100,50,button_black,button_up_white,goToTreeLayer)
        button(CAVE_LAYER_NAME,20,white,220,0,100,50,button_black,button_up_white,goToCaveLayer)

    # cellの生成を進める
    def cellgenerating(self):
        global game_point
        if game_point > 0:
            game_point -= 1
            if Cell.cell_gen_count < Cell.cell_gen_img_list_size:
                Cell.cell_gen_count += 1
            else:
                self.genCell('NEW',self.gate.gate_x+20,self.gate.gate_y+40,6)
                Cell.cell_gen_count = 0
        else: # game_pointの不足
            textDisplay('NO '+POINT_NAME+'!',FONT,20,red,self.gate.gate_x+self.gate.gate_width/2,self.gate.gate_y-20)

    # cellを生成、リストに加える
    def genCell(self,name,x,y,dir):
        cell = Cell(name,x,y,dir)
        Cell.cell_list.append(cell)

"""
Gateをクリックするとcellが生成される"""
class Gate:
    def __init__(self, x, y):
        # 画像のロード
        self.gate_act = pygame.image.load(os.path.join('images', 'gate_act.png')) # マウスオーバー中の画像
        self.gate_inact = pygame.image.load(os.path.join('images', 'gate_inact.png')) # マウスオーバーしてないときの画像

        # gateの大きさと座標
        self.gate_width = self.gate_act.get_width()
        self.gate_height = self.gate_act.get_height()
        self.gate_x = x
        self.gate_y = y

        # gateの状態
        self.is_generating = False # cellを生成中かどうか　生成の処理はcellLayerManagerで行う

    def update(self):
        self.is_generating = False

    # マウスオーバーを検知し、表示画像を切り替える
    # 押されている間を検知し、cell生成状態になる　cellの生成処理自体はcellLayerManagerが担う
    def draw(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.gate_x+self.gate_width > mouse[0] > self.gate_x and self.gate_y+self.gate_height > mouse[1] > self.gate_y:
            game_display.blit(self.gate_act, (self.gate_x, self.gate_y)) # マウスオーバー中の描画
            if click[0] == 1: # gateがクリックされている
                self.is_generating = True
        else:
            game_display.blit(self.gate_inact, (self.gate_x, self.gate_y)) # マウスオーバーしてないときの描画

"""
cellは動き回る
一定時間たつと分裂する
さらに一定時間たつと出芽する
出芽したcellをクリックすると採収できる"""
class Cell:
    # cell全体を格納するリスト
    cell_list = [] # cellインスタンスを格納
    bud_list = [] # 発芽後のcellインスタンスを格納

    # cell生成エフェクトの保持
    cell_gen_img_list = [] # cell生成エフェクトの画像を格納
    cell_gen_img_list_size = 74 # cell1生成エフェクト画像の総数
    cell_gen_count = 0 # 生成中のcellがどこまで生成されたかを保持

    # cell_gen_img_listにcell生成エフェクトの画像をロード
    for i in range(cell_gen_img_list_size+1):
        cell_gen_img_list.append(pygame.image.load(os.path.join('images', 'generate_' + str(i) + '.png')))

    def __init__(self,name,x,y,dir):
        # 各cell画像のロード
        self.cell_img_stay = pygame.image.load(os.path.join('images', 'cell_img_stay.png'))
        self.cell_img_left = pygame.image.load(os.path.join('images', 'cell_img_left.png'))
        self.cell_img_right = pygame.image.load(os.path.join('images', 'cell_img_right.png'))
        self.cell_img_down = pygame.image.load(os.path.join('images', 'cell_img_down.png'))
        self.cell_img_up = pygame.image.load(os.path.join('images', 'cell_img_up.png'))
        self.bud_img = pygame.image.load(os.path.join('images', 'bud.png'))
        self.bud_act_img = pygame.image.load(os.path.join('images', 'bud_act.png'))
        self.cell_img = self.cell_img_stay # 表示する画像を格納

        # cellの大きさと座標
        self.cell_width = self.cell_img.get_width()
        self.cell_height = self.cell_img.get_height()
        self.cell_x = x
        self.cell_y = y

        #cellの状態
        self.divide_limit = 1 # 分裂できる回数
        self.divide_per = 200 # 何フレームに一回分裂するか
        self.cell_age = 0 # 生まれてから何フレーム生きたか
        self.budding_time = 500 # 生まれてから何フレームで出芽するか
        self.cell_power = 40 # 収穫時にgame_pointに加算される値
        self.is_budded = False # 出芽したか
        self.is_harvested = False # 採収されたか

        self.is_moving = True # cellは移動中か
        self.move_count = 0 #移動を始めてから何フレーム経ったか
        self.cell_speed = 1 # cellの移動速度
        self.cell_dir = dir # 移動方向

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

    # cellの移動
    def move(self):
        if self.is_moving:
            # 壁に当たると止まる
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

            # 移動する
            else:
                if self.move_count > 100:
                    self.is_moving = False
                    self.cell_img = self.cell_img_stay
                    self.move_count = 0
                else: # 移動方向/速度を乱数で決める
                    if self.cell_dir == 0:# 右方向
                        self.cell_img = self.cell_img_right
                        self.cell_x += self.cell_speed
                    elif self.cell_dir == 1:# 左方向
                        self.cell_img = self.cell_img_left
                        self.cell_x -= self.cell_speed
                    elif self.cell_dir == 2:# 下方向
                        self.cell_img = self.cell_img_down
                        self.cell_y += self.cell_speed
                    elif self.cell_dir == 3:# 上方向
                        self.cell_img = self.cell_img_up
                        self.cell_y -= self.cell_speed
                    elif self.cell_dir == 4:# 右方向に速く
                        self.cell_img = self.cell_img_right
                        self.cell_x += self.cell_speed*2
                    elif self.cell_dir == 5:# 左方向に速く
                        self.cell_img = self.cell_img_left
                        self.cell_x -= self.cell_speed*2
                    elif self.cell_dir == 6:# 下方向に速く
                        self.cell_img = self.cell_img_down
                        self.cell_y += self.cell_speed*2
                    elif self.cell_dir == 7:# 上方向に速く
                        self.cell_img = self.cell_img_up
                        self.cell_y -= self.cell_speed*2
                    self.move_count +=1

        else: # 移動してないときの処理
            if self.move_count > 100:
                self.is_moving = True
                self.cell_dir = random.randrange(0, 8)
                self.move_count = 0
            else:
                self.cell_img = self.cell_img_stay
                self.move_count += 1

    # cellを出芽状態にする
    def budding(self):
        self.is_budded = True

"""
treeレイヤーのインスタンス管理を行う
treeレイヤーにはTreeのインスタンスが一つ、Humanのインスタンスが複数存在する"""
class TreeLayerManager:
    def __init__(self):
        self.tree = Tree()
        self.house = House()
        self.mouseEventUp = False

    # マウスイベントをゲームループから受け取る
    def setMouseEventUp(self,event):
        self.mouseEventUp = event

    def update(self):
        global game_point

        self.tree.update()
        self.house.update()
        for i in Human.human_list:
            i.update()

        # treeレベル*Human数に応じて自動的にgame_pointを増やす
        game_point += self.tree.tree_power[self.tree.tree_level] * (self.house.gen_count + 1)

    def draw(self):
        # treeレイヤー背景画像の描画
        game_display.blit(tree_map, (0, 0))

        # 各インスタンスの描画
        self.tree.draw(self.mouseEventUp)
        self.house.draw(self.mouseEventUp)
        for i in Human.human_list:
            i.draw()

        # Human 生成
        # if self.house.is_generating == True:
        #     self.genHuman('name',DISPLAY_WIDTH)
        #     self.house.is_generating = False

        # game_pointの描画
        textDisplay(POINT_NAME+': '+str(math.floor(game_point)),FONT,30,black,DISPLAY_WIDTH/2,20)

        # レイヤ切り替えボタンの描画
        button(CELL_LAYER_NAME,20,white,0,0,100,50,button_black,button_up_white,goToCellLayer)
        button(TREE_LAYER_NAME,20,white,110,0,100,50,button_up_white,button_up_white,goToTreeLayer)
        button(CAVE_LAYER_NAME,20,white,220,0,100,50,button_black,button_up_white,goToCaveLayer)

    # draw後に実行
    def clear(self):
        self.setMouseEventUp(False)


    # humanを生成、リストに加える
    # def genHuman(self,name,x):
    #     global game_point
    #     if(game_point >= self.house.cost[self.house.gen_count]):
    #         game_point -= self.house.cost[self.house.gen_count]
    #         human = Human(name,x)
    #         Human.human_list.append(human)
    #         self.house.gen_count += 1
    #     else:
    #         textDisplay('NO Leaf!',FONT,20,red,self.house.y-20,self.house.y-100)



class Human:
    human_list = []

    def __init__(self, name, x):
        # 画像のロード
        self.human_stay = pygame.image.load(os.path.join('images', 'human_stay.png'))
        self.human_left = pygame.image.load(os.path.join('images', 'human_left.png'))
        self.human_right = pygame.image.load(os.path.join('images', 'human_right.png'))
        self.human_img = self.human_left # 表示画像の保持

        # humanの大きさと座標
        self.human_width = self.human_img.get_width()
        self.human_height = self.human_img.get_height()
        self.human_x = x
        self.human_y = DISPLAY_HEIGHT - self.human_height

        # 移動パラメータ
        self.human_moving = True
        self.move_count = 0
        self.human_speed = 2
        self.human_dir = 2

        self.human_name = name

    def move(self):
        if self.human_moving:
            #Wall collision
            if self.human_x < 0:
                self.human_x = 0
                self.human_moving = False
            elif self.human_x > DISPLAY_WIDTH - self.human_width:
                self.human_x = DISPLAY_WIDTH - self.human_width
                self.human_moving = False
            #Move
            else:
                if self.move_count > 20:
                    self.human_moving = False
                    self.human_img = self.human_stay
                    self.move_count = 0
                else:
                    if self.human_dir == 0:#Go left
                        self.human_img = self.human_left
                        self.human_x -= self.human_speed
                    elif self.human_dir == 1:#Go Right
                        self.human_img = self.human_right
                        self.human_x += self.human_speed
                    elif self.human_dir == 2:#Go Left Long
                        self.human_img = self.human_left
                        self.human_x -= self.human_speed*2
                    elif self.human_dir == 3:#Go Right Long
                        self.human_img = self.human_right
                        self.human_x += self.human_speed*2
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

    def draw(self,mouseEventUp):
        mouse = pygame.mouse.get_pos()

        # マウスオーバー時には白く光る(ac画像を表示)
        # マウスオーバー時に左クリックすると、tree_shoppingボタンが出現する
        # treeとtree_shoppingボタン以外をクリックすると、tree_shoppingボタンは消える
        if self.tree_xy_list[self.tree_level][0]+self.tree_width_list[self.tree_level] > mouse[0] > self.tree_xy_list[self.tree_level][0] and self.tree_xy_list[self.tree_level][1]+self.tree_height_list[self.tree_level] > mouse[1] > self.tree_xy_list[self.tree_level][1]:
            if mouseEventUp == True:  #左クリック時
                self.tree_shop = True
            game_display.blit(self.tree_ac_img_list[self.tree_level],self.tree_xy_list[self.tree_level])
        else:
            if mouseEventUp == True:
                self.close_tree_window()
            game_display.blit(self.tree_img_list[self.tree_level],self.tree_xy_list[self.tree_level])

        if self.tree_shop == True:
            if self.tree_level < len(self.tree_img_list) - 1:
                self.tree_shopping()
            else:
                #TODO: treeが最高レベルの処理
                pass

    def tree_shopping(self):
        textDisplay('Cost: '+str(self.tree_cost[self.tree_level])+'Leaf',FONT,20,black,DISPLAY_WIDTH/2,self.tree_xy_list[self.tree_level][1]-70)
        button("Level UP",20,white,DISPLAY_WIDTH/2-50,self.tree_xy_list[self.tree_level][1]-50,100,50,button_black,button_up_white,self.tree_growth)

    def tree_growth(self):
        global game_point
        if game_point >= self.tree_cost[self.tree_level]:
            game_point -= self.tree_cost[self.tree_level]
            self.tree_level += 1
            self.close_tree_window()
        else:
            textDisplay('NO Leaf!',FONT,20,red,DISPLAY_WIDTH/2,self.tree_xy_list[self.tree_level][1]-100)

    def close_tree_window(self):
        self.tree_shop = False


class House:
    def __init__(self):
        self.act_img = pygame.image.load(os.path.join('images', 'house_act.png'))
        self.inact_img = pygame.image.load(os.path.join('images', 'house_inact.png'))

        # 大きさと座標
        self.width = self.act_img.get_width()
        self.height = self.act_img.get_height()
        self.x = DISPLAY_WIDTH - self.width
        self.y = DISPLAY_HEIGHT - self.height

        # Human生成コスト
        self.cost =[100, 500, 1000, 3000, 10000, 50000, 100000]

        # Human生成数
        self.gen_count = 0

        self.is_shopping = False
        self.is_generating = False

    def update(self):
        pass

    def draw(self,mouseEventUp):
        mouse = pygame.mouse.get_pos()

        # マウスオーバー時には白く光る(ac画像を表示)
        # マウスオーバー時に左クリックすると、house_shoppingボタンが出現する
        # houseとhouse_shoppingボタン以外をクリックすると、house_shoppingボタンは消える
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

class CaveLayerManager:
    def __init__(self):
        self.blueGem = BlueGem()
        self.mouseEventUp = False

    # マウスイベントをゲームループから受け取る
    def setMouseEventUp(self,event):
        self.mouseEventUp = event

    # caveレイヤの状態を更新
    def update(self):
        global game_point
        self.blueGem.update()

    # caveイヤを描画
    def draw(self):
        game_display.blit(cave_map, (0, 0)) # cellレイヤ背景の描画

        # 各インスタンスの描画
        self.blueGem.draw(self.mouseEventUp)


        # game_pointの描画
        textDisplay(POINT_NAME+': '+str(math.floor(game_point)),FONT,30,white,DISPLAY_WIDTH/2,20)

        button(CELL_LAYER_NAME,20,white,0,0,100,50,button_black,button_up_white,goToCellLayer)
        button(TREE_LAYER_NAME,20,white,110,0,100,50,button_black,button_up_white,goToTreeLayer)
        button(CAVE_LAYER_NAME,20,white,220,0,100,50,button_up_white,button_up_white,goToCaveLayer)

    # draw後に実行
    def clear(self):
        self.setMouseEventUp(False)

class BlueGem:
    def __init__(self):
        # Load images
        self.img = pygame.image.load(os.path.join('images','blueGem.png'))
        self.act_img = pygame.image.load(os.path.join('images','blueGemEffect_act.png'))
        self.inact_img = pygame.image.load(os.path.join('images','blueGemEffect_inact.png'))
        self.water_img = pygame.image.load(os.path.join('images','water.png'))

        self.star_img_list = []
        self.star_img_num = 3
        for i in range(self.star_img_num+1):
            self.star_img_list.append(pygame.image.load(os.path.join('images','blueStar_'+str(i)+'.png')))

        # Size and XY
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

        # Status
        self.is_shopping = False
        self.is_generating = False

    def update(self):
        pass

    # マウスオーバー時には白く光る(ac画像を表示)
    # マウスオーバー時に左クリックすると、house_shoppingボタンが出現する
    # houseとhouse_shoppingボタン以外をクリックすると、house_shoppingボタンは消える
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


# ゲームの開始と終了
gameInit()
gameQuit()
