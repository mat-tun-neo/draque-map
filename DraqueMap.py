# coding: utf-8
from pygame_functions import *
from random import randint
import random

BG_IMAGE_DIR = "bgimages/"                         # 背景画像　格納ディレクトリ
BG_IMAGE = ""                                      # 背景画像　ファイル相対パス

DESKTOP_X = 1920                                   # デスクトップ Xサイズ
DESKTOP_Y = 1080                                   # デスクトップ Yサイズ
PLAYER_IMAGE = "images/player3.png"                # プレイヤー 画像ファイル
PLAYER_ALLIMAGE = 16                               # プレイヤー アニメーション全コマ数
PLAYER_RULASPEED = 30000                           # プレイヤー ルーラの回転速度
BG_COLOR1 = "black"                                # 背景　黒色
BG_COLOR2 = "white"                                # 背景　白色
BG_SCROLLSPEED = 5                                 # 背景　スクロール速度
BG_BASE = DESKTOP_Y //10*9                         # 背景　基礎サイズ
BG_SCALE = [16, 10, 8, 5, 4, 2, 1]                 # 背景　スケール
MINI_MAP_SCALE = 10                                # ミニマップ　スケール
SOUND_BGM = ["sounds/bgm1.ogg",\
             "sounds/bgm2.ogg",\
             "sounds/bgm3.ogg"]                    # 効果音　BGM
SOUND_JUMON = makeSound("sounds/jumon.ogg")        # 効果音　魔法
SOUND_BUTTON = makeSound("sounds/pi.ogg")          # 効果音　ボタン
SOUND_WALL = makeSound("sounds/wall.ogg")          # 効果音　壁
SOUND_NEXT = makeSound("sounds/rula.ogg")          # 効果音　壁
SOUND_MESSAGE = makeSound("sounds/message.ogg")    # 効果音　メッセージ
FONT_SIZE = 32                                     # フォント　サイズ
FONT_COLOR = "black"                               # フォント　色
FONT_FILE = "fonts/DragonQuestFCIntact.ttf"        # フォント　ファイル
WAKU_BGCOLOR = "white"                             # メッセージ枠　背景色
WAKU_KADO_1 = "＆"                                 # メッセージ枠　角1
WAKU_KADO_2 = "’"                                   # メッセージ枠　角2
WAKU_KADO_3 = "）"                                  # メッセージ枠　角3
WAKU_KADO_4 = "（"                                  # メッセージ枠　角4
WAKU_YOKO_1 = "＃"                                 # メッセージ枠　横1
WAKU_YOKO_2 = "％"                                 # メッセージ枠　横2
WAKU_TATE_1 = "”"                                  # メッセージ枠　縦1
WAKU_TATE_2 = "＄"                                 # メッセージ枠　縦2
WAKU_SPACE = "　"                                   # メッセージ枠　スペース
WAKU_PERSON = "　てんのこえ　"                         # メッセージ枠　発声主
MESSAGE_KAKUDAI = ["　　　　　＜,もうヒントか　ほしいのか,,しかたないのぉ　おおきくしてやろう",\
                   "　　　　　　＜,ちょっと　むすかしいかのお,,もうすこし　からだを　おおきくしてやろう",\
                   ",たんきは　そんきと　いうじゃろう,　　　　　　　＜,じっくり　しらへて　みることじゃ",\
                   ",おぬしのからだを　おおきくしてやろう,＜　＜　　　　　　　　　　　　　　　＜,かんはって　こたえを　みつけるのじゃそ",\
                   "　　　＜　　　　＜,もうすく　こたえかわかるかも　しれんのぉ,　　　　＜　　　　＜　　　　＜,あきらめすに　すみすみを　さかすのじゃ"]           # メッセージ 拡大時
TRANE_TABLE = str.maketrans({"0":"０", "1":"１", "2":"２", "3":"３", "4":"４", "5":"５", "6":"６", "7":"７", "8":"８", "9":"９"})

screenSize(1,1)
setAutoUpdate(False)

# プレイヤークラス
class Player():
    # コンストラクタ
    def __init__(self, x, y):
        self.sprite = makeSprite(PLAYER_IMAGE, PLAYER_ALLIMAGE)
        self.width = self.sprite.image.get_rect().width
        self.height = self.sprite.image.get_rect().height
        self.timeOfNextFrame = clock()
        self.frame = 0
        self.bgWidth = x
        self.bgHeight = y
        self.centerx = x //2 - self.width //2
        self.centery = y //2 - self.height //2
        self.xpos = self.centerx
        self.ypos = self.centery
        changeSpriteImage(self.sprite, 1*PLAYER_ALLIMAGE //4 + 1)
        showSprite(self.sprite)
        moveSprite(self.sprite, self.xpos, self.ypos)
        self.scale_idx = 0
        self.scale = BG_SCALE[self.scale_idx]
        setBackgroundColour(BG_COLOR1)
        self.bg = setBackgroundImage(BG_IMAGE, self.bgWidth, self.bgHeight, self.scale)
        self.label_scale = None
        self.label_operation = Message("", "やじるし：　いどう,　＞,スヘース：　かくだい,,エンター：　こたえ", 10, 10, labelflg=True, size=24)
        self.updateScaleDisp()
        self.drawMiniMap()
        self.clearflg = False
    # 移動
    def move(self):
        if clock() > self.timeOfNextFrame:
            self.frame = (self.frame + 1) % (PLAYER_ALLIMAGE //4)
            self.timeOfNextFrame += 80
        # キー判定
        scrollable = False
        movable = True
        if keyPressed("right"):
            changeSpriteImage(self.sprite, 0*PLAYER_ALLIMAGE //4 + self.frame)
            if self.xpos == self.centerx:
                scrollable = scrollBackground(BG_SCROLLSPEED*(-1), 0)
            if not scrollable:
                self.xpos += BG_SCROLLSPEED
                if self.xpos > self.bgWidth - self.width:
                    self.xpos -= BG_SCROLLSPEED
                    movable = False
            self.label_operation.hide()
        elif keyPressed("down"):
            changeSpriteImage(self.sprite, 1*PLAYER_ALLIMAGE //4 + self.frame)
            if self.ypos == self.centery:
                scrollable = scrollBackground(0, BG_SCROLLSPEED*(-1))
            if not scrollable:
                self.ypos += BG_SCROLLSPEED
                if self.ypos > self.bgHeight - self.height:
                    self.ypos -= BG_SCROLLSPEED
                    movable = False
            self.label_operation.hide()
        elif keyPressed("left"):
            changeSpriteImage(self.sprite, 2*PLAYER_ALLIMAGE //4 + self.frame)
            if self.xpos == self.centerx:
                scrollable = scrollBackground(BG_SCROLLSPEED, 0)
            if not scrollable:
                self.xpos -= BG_SCROLLSPEED
                if self.xpos < 0:
                    self.xpos += BG_SCROLLSPEED
                    movable = False
            self.label_operation.hide()
        elif keyPressed("up"):
            changeSpriteImage(self.sprite, 3*PLAYER_ALLIMAGE //4 + self.frame)
            if self.ypos == self.centery:
                scrollable = scrollBackground(0, BG_SCROLLSPEED)
            if not scrollable:
                self.ypos -= BG_SCROLLSPEED
                if self.ypos < 0:
                    self.ypos += BG_SCROLLSPEED
                    movable = False
            self.label_operation.hide()
        else:
            changeSpriteImage(self.sprite, 1*PLAYER_ALLIMAGE //4 + 1)
            self.label_operation.show()
        # スプライト移動
        moveSprite(self.sprite, self.xpos, self.ypos)
        # 端に到達
        if not movable:
            playSound(SOUND_WALL)
        # エンターキー判定
        if keyPressed("return"):
            self.clearflg = True
            self.scale_idx = len(BG_SCALE) - 1
            self.changeScale(self.scale_idx)
        # スペースキー判定
        elif keyPressed("space"):
            if self.scale_idx < len(BG_SCALE) - 1:
                mes = Message(WAKU_PERSON, MESSAGE_KAKUDAI[randint(0, 4)],\
                              40, self.bgHeight - 250)
                playSound(SOUND_JUMON)
                for i in range(5):
                    setBackgroundColour(BG_COLOR1)
                    pause(60)
                    setBackgroundColour(BG_COLOR2)
                    pause(60)
                self.scale_idx += 1
                self.changeScale(self.scale_idx)
                self.xpos = self.centerx
                self.ypos = self.centery
                moveSprite(self.sprite, self.xpos, self.ypos)
            else:
                self.clearflg = True
        # ミニマップの表示
        self.drawMiniMap()
    # 拡大率の変更
    def changeScale(self, n):
        self.scale = BG_SCALE[n]
        self.bg = setBackgroundImage(BG_IMAGE, self.bgWidth, self.bgHeight, self.scale)
        self.updateScaleDisp()
    
    # 拡大率表示の更新
    def updateScaleDisp(self):
        if self.label_scale != None:
            self.label_scale.hide()
        tmptext = str(self.scale).translate(TRANE_TABLE)
        self.label_scale = Message("", "Ｘ" + "　"*(2-len(tmptext)) + tmptext,\
                                   self.bgWidth - 130, 10, labelflg=True, size=24)
    # ミニマップ更新
    def drawMiniMap(self):
        # 外枠（黒：画像のサイズ）
        out_width = self.bgWidth //MINI_MAP_SCALE
        out_height = self.bgHeight //MINI_MAP_SCALE
        out_x = self.bgWidth - out_width - 20
        out_y = self.bgHeight - out_height - 20
        drawRect(out_x, out_y, out_width, out_height, "white", 2)
        # 内枠（赤：画面のサイズ）
        in_width = self.bgWidth //10 //self.scale
        in_height = self.bgHeight //10 //self.scale
        in_x = out_width //2 - in_width //2 - int(self.bg.getScrollx() //self.scale //MINI_MAP_SCALE)
        in_y = out_height //2 - in_height //2 - int(self.bg.getScrolly() //self.scale //MINI_MAP_SCALE)
        drawRect(out_x + in_x, out_y + in_y, in_width, in_height, "red", 2)
        updateDisplay()
    # スプライトクリア
    def clear(self):
        killSprite(self.sprite)
        self.label_scale.hide()
        self.label_operation.hide()
    # ルーラ時
    def rula(self):
        playSound(SOUND_NEXT)
        n = 0
        while self.ypos > 0 - self.height:
            if n % PLAYER_RULASPEED == 0:
                changeSpriteImage(self.sprite, (n//PLAYER_RULASPEED%4)*PLAYER_ALLIMAGE //4 + self.frame)
                moveSprite(self.sprite, self.xpos, self.ypos)
                updateDisplay()
                self.ypos -= BG_SCROLLSPEED*2
            n += 1
        # キー判定無効
        pygame.event.clear()
    # クリア判定
    def isCleared(self):
        return self.clearflg
    # クリア判定をリセット
    def resetClear(self):
        self.clearflg = False
        
# メッセージ枠クラス
class Message():
    # コンストラクタ
    def __init__(self, person, str, x, y, yesnoflg=False, labelflg=False, hideflg=True, size=FONT_SIZE, color=FONT_COLOR, bgcolor=WAKU_BGCOLOR):
        self.str_array = str.split(',')
        self.waku_width = max([len(x) for x in self.str_array])
        if len(person) > 0: 
            self.message = WAKU_KADO_1 + person + WAKU_YOKO_1 * (self.waku_width - len(person) ) + WAKU_KADO_2 + "<br>"
        else:
            self.message = WAKU_KADO_1 + WAKU_YOKO_1 * self.waku_width + WAKU_KADO_2 + "<br>"
        for i in range(len(self.str_array)):
            self.message += WAKU_TATE_1
            self.message += self.str_array[i] + "　" * ( self.waku_width - len(self.str_array[i]) )
            self.message += WAKU_TATE_2 + "<br>"
        if yesnoflg:
            self.message += WAKU_TATE_1 + WAKU_SPACE * self.waku_width + WAKU_TATE_2 + "<br>"
            self.messageYes = self.message + WAKU_TATE_1 + "　　　　｝はい　　　いいえ" + WAKU_SPACE * (self.waku_width - 13) + WAKU_TATE_2 + "<br>"
            self.messageYes += WAKU_KADO_3 + WAKU_YOKO_2 * self.waku_width + WAKU_KADO_4
            self.messageNo  = self.message + WAKU_TATE_1 + "　　　　　はい　　｝いいえ" + WAKU_SPACE * (self.waku_width - 13) + WAKU_TATE_2 + "<br>"
            self.messageNo += WAKU_KADO_3 + WAKU_YOKO_2 * self.waku_width + WAKU_KADO_4
        elif not labelflg:
            self.message += WAKU_TATE_1 + WAKU_SPACE * (self.waku_width - 4) + "｛　　　" + WAKU_TATE_2 + "<br>"
        self.message += WAKU_KADO_3 + WAKU_YOKO_2 * self.waku_width + WAKU_KADO_4
        # YESNO表示の場合はキー判定
        if yesnoflg:
            playSound(SOUND_BUTTON)
            playSound(SOUND_MESSAGE)
            self.label = makeLabel(self.messageNo, size, x, y, fontColour=color, font=FONT_FILE, background=bgcolor)
            self.show()
            updateDisplay()
            # 左右キー／スペースキー判定
            while True:
                # キー入力待ち
                key = waitPress()
                if key == keydict["right"]:
                    self.hide()
                    self.label = makeLabel(self.messageNo, size, x, y, fontColour=color, font=FONT_FILE, background=bgcolor)
                    self.show()
                    self.answer = False
                    updateDisplay()
                if key == keydict["left"]:
                    self.hide()
                    self.label = makeLabel(self.messageYes, size, x, y, fontColour=color, font=FONT_FILE, background=bgcolor)
                    self.show()
                    self.answer = True
                    updateDisplay()
                if key == keydict["space"]:
                    break
                    playSound(SOUND_BUTTON)
                if key == keydict["esc"]:
                    pygame.quit()
                    sys.exit()
        else:
            self.label = makeLabel(self.message, size, x, y, fontColour=color, font=FONT_FILE, background=bgcolor)
            self.show()
            updateDisplay()
        # ラベル表示でなければ、音を鳴らしてキー判定
        if not labelflg:
            playSound(SOUND_BUTTON)
            if not yesnoflg:
                playSound(SOUND_MESSAGE)
                # スペースキー判定
                while True:
                    # キー入力待ち
                    key = waitPress()
                    if key == keydict["space"]:
                        break
                    if key == keydict["esc"]:
                        pygame.quit()
                        sys.exit()
            if hideflg:
                self.hide()
                updateDisplay()
    # 枠を表示する
    def show(self):
        showLabel(self.label)
    # 枠を消す
    def hide(self):
        hideLabel(self.label)
    # はい／いいえ
    def answer(self):
        return self.answer

p = None
bg_width = 0
bg_height = 0
bgm = None
bgimages = []
num = 0

# 背景画像の一覧をファイルから読み込む
for line in open("bgimages/files.txt", 'r'):
    if line != "":
        name, message = line[:-1].split('\t')
        bgimages.append([name, message])
# ランダムソート
bgimages = random.sample(bgimages, len(bgimages))

# リセット（背景画像を変更）
def reset():
    global p
    global bg_width
    global bg_height
    global bgm
    global BG_IMAGE
    
    # 背景画像サイズ取得
    BG_IMAGE = BG_IMAGE_DIR + bgimages[num % (len(bgimages) - 1)][0]
    bg = setBackgroundImage(BG_IMAGE)
    x = bg.getWidth()
    y = bg.getHeight()
    # ウインドウ作成
    if x > y:
        bg_width = BG_BASE
        bg_height = y * bg_width //x
    else:
        bg_height = BG_BASE
        bg_width = x * bg_height //y
    # ウインドウサイズ変更
    screenSize(bg_width, bg_height, (1920 - bg_width) //2, (1080 - bg_height) //2 - 50)
    # プレイヤー作成
    p = Player(bg_width, bg_height)
    # BGM再生
    bgm = makeSound(SOUND_BGM[randint(0, 2)])
    playSound(bgm, -1)

reset()
# メインループ
while True:
    p.move()
    # クリア判定
    if p.isCleared():
        mes = Message("　てんのこえ　", bgimages[num % (len(bgimages) - 1)][1]\
                       ,40, bg_height - 250)
        mes = Message("　てんのこえ　","　＜　　　　　＜　　　＜,つきの　ステーシに　とはしてやろう,　　＜,かくこは　よいかの？"\
                       ,40, bg_height - 280, yesnoflg = True)
        if mes.answer == True:
            num += 1
            p.rula()
            p.clear()
            stopSound(bgm)
            reset()
        else:
            p.resetClear()
        # キー入力待ち
        waitPress()
    updateDisplay()
    tick(120)

endWait()
