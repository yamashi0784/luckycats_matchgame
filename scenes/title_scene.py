import pyxel

from entities import LuckyCats
import math

class TitleScene:
    def __init__(self, game):
        self.game = game  # ゲームクラス
        self.alpha = 0.0  # 画面の透明度(0.0:透明, 1.0:不透明)
        self.dx = 0
    
    def start(self):
        self.game.score = 0
        self.game.stage = 1
        self.dx = 0
        pyxel.stop()
        pyxel.playm(0, loop=True)

    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(
            pyxel.GAMEPAD1_BUTTON_B
        ) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):  # EnterキーまたはゲームパッドのBボタンが押された時
            # 画面の透明度を不透明にする
            #pyxel.dither(1.0)

            # プレイ画面に切り替える
            self.game.change_scene("play")

    def draw(self):
        # 画面をクリアする
        pyxel.cls(0)
        # タイトル画像の表示をここでやる。
        pyxel.rect(1,1,255,255,7)
        #pyxel.blt(66,104,1,0,0,24,24,colkey=0)#タイトルの代わりにとりあえず表示
        #self.game.cats[0].draw(66,104)
    
        self.dx += 1
        for i in range(10):
            self.dx = self.dx * -1
            for j in range(10):
                if self.dx > 0:
                    if j*24+self.dx+8 > 248:
                        self.game.cats[(i*10)+j].draw_face(j*24+self.dx+8-248,i*24+8)
                    else:
                        self.game.cats[(i*10)+j].draw_face(j*24+self.dx+8,i*24+8)
                if self.dx < 0:
                    if j*24+self.dx+8 < 8:
                        self.game.cats[(i*10)+j].draw_face(j*24+self.dx+8+248,i*24+8)
                    else:
                        self.game.cats[(i*10)+j].draw_face(j*24+self.dx+8,i*24+8)
        if abs(self.dx) >= 248:
            self.dx = 0
        
        pyxel.rect(0,0,28,255,7)
        pyxel.rect(224,0,32,255,7)
        pyxel.rect(98,127,62,8,7)
        pyxel.text(100, 129, "PRESS ENTER KEY", 16)