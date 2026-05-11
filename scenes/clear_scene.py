import pyxel

class ClearScene:
    def __init__(self, game):
        self.game = game
        self.dx = 0

    def start(self):
        self.dx = 0
        pyxel.stop()

    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.game.change_scene("title")

    def draw(self):
        # タイトルと同じスクロール背景
        pyxel.cls(0)
        pyxel.rect(1, 1, 255, 255, 7)

        self.dx += 1
        for i in range(10):
            self.dx = self.dx * -1
            for j in range(10):
                if self.dx > 0:
                    if j*24+self.dx+8 > 248:
                        self.game.cats[(i*10)+j].draw_face(j*24+self.dx+8-248, i*24+8)
                    else:
                        self.game.cats[(i*10)+j].draw_face(j*24+self.dx+8, i*24+8)
                if self.dx < 0:
                    if j*24+self.dx+8 < 8:
                        self.game.cats[(i*10)+j].draw_face(j*24+self.dx+8+248, i*24+8)
                    else:
                        self.game.cats[(i*10)+j].draw_face(j*24+self.dx+8, i*24+8)
        if abs(self.dx) >= 248:
            self.dx = 0

        pyxel.rect(0, 0, 28, 255, 7)
        pyxel.rect(224, 0, 32, 255, 7)

        # 半透明の暗幕
        pyxel.dither(0.5)
        pyxel.rect(0, 0, 256, 256, 0)
        pyxel.dither(1.0)

        # メッセージボックス
        pyxel.rect(32, 86, 192, 84, 7)
        pyxel.rectb(32, 86, 192, 84, 0)

        title = "ALL CLEAR!"
        pyxel.text(128 - len(title) * 2, 96, title, 8)

        time_str = f"TOTAL TIME : {self.game.score / 30:.1f}s"
        pyxel.text(128 - len(time_str) * 2, 110, time_str, 0)

        thanks = "THANK YOU FOR PLAYING!"
        pyxel.text(128 - len(thanks) * 2, 122, thanks, 11)

        # 点滅する入力促進テキスト
        if pyxel.frame_count % 60 < 40:
            prompt = "PRESS ENTER TO TITLE"
            pyxel.text(128 - len(prompt) * 2, 148, prompt, 5)
