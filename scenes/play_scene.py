import pyxel
import random

from entities import LuckyCats

class PlayScene:
    STAGE_COLS = {1: 2, 2: 4, 3: 6}
    CARD_SIZE = 24
    SCREEN_SIZE = 256
    FLIP_DURATION = 12
    TITLE_BTN = (108, 245, 40, 9)  # x, y, w, h

    def __init__(self, game):
        self.game = game
        self.cards = []
        self.hit = 0
        self.rows = 2
        self.cols = 2
        self.offset_x = 104
        self.offset_y = 104
        self.face_up = []
        self.matched = []
        self.selected = []
        self.animating_cards = []
        self.anim_direction = 'to_face'
        self.anim_progress = 0
        self.wait_timer = 0
        self.clear_timer = 0
        self.moves = 0
        self.play_frames = 0  # 現在のステージの経過フレーム数

    def shuffle_cats(self):
        self.cols = self.STAGE_COLS[self.game.stage]
        self.rows = self.cols
        pairs = (self.cols * self.rows) // 2
        offset = (self.SCREEN_SIZE - self.cols * self.CARD_SIZE) // 2
        self.offset_x = offset
        self.offset_y = offset

        self.cards.clear()
        temp_cards = list(range(pairs)) * 2
        random.shuffle(temp_cards)
        self.cards = [temp_cards[i*self.cols:(i+1)*self.cols] for i in range(self.rows)]

        self.face_up = [[False] * self.cols for _ in range(self.rows)]
        self.matched = [[False] * self.cols for _ in range(self.rows)]
        self.selected = []
        self.animating_cards = []
        self.anim_direction = 'to_face'
        self.anim_progress = 0
        self.wait_timer = 0
        self.clear_timer = 0
        self.moves = 0
        self.play_frames = 0

    def start(self):
        self.shuffle_cats()
        pyxel.stop()
        pyxel.playm(0, loop=True)  # cats01.pyxres のmusicトラック0を再生

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.game.change_scene("title")
            return

        # クリア演出中以外はタイマーを進める
        if self.clear_timer == 0:
            self.play_frames += 1

        # TITLEボタンのクリックはいつでも有効
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self._on_title_button():
            self.game.change_scene("title")
            return

        if self.animating_cards:
            self.anim_progress += 1
            if self.anim_progress >= self.FLIP_DURATION:
                if self.anim_direction == 'to_face':
                    row, col = self.animating_cards[0]
                    self.face_up[row][col] = True
                    self.selected.append((row, col))
                    if len(self.selected) == 2:
                        self._check_match()
                else:
                    for row, col in self.animating_cards:
                        self.face_up[row][col] = False
                    self.selected = []
                self.animating_cards = []
                self.anim_progress = 0
            return

        if self.wait_timer > 0:
            self.wait_timer -= 1
            if self.wait_timer == 0:
                self._start_flip_back()
            return

        if self.clear_timer > 0:
            self.clear_timer -= 1
            if self.clear_timer == 0:
                self.clear_timer = -1
            return

        if self.clear_timer < 0:
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if self.game.stage < 3:
                    self.game.stage += 1
                    self.game.change_scene("play")
                else:
                    self.game.change_scene("clear")
            return

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            col = (pyxel.mouse_x - self.offset_x) // self.CARD_SIZE
            row = (pyxel.mouse_y - self.offset_y) // self.CARD_SIZE
            if 0 <= row < self.rows and 0 <= col < self.cols:
                if not self.face_up[row][col] and len(self.selected) < 2:
                    self.animating_cards = [(row, col)]
                    self.anim_direction = 'to_face'
                    self.anim_progress = 0
                    pyxel.play(3, 0)  # カードめくり音

    def _check_match(self):
        (r1, c1), (r2, c2) = self.selected
        self.moves += 1
        if self.cards[r1][c1] == self.cards[r2][c2]:
            self.matched[r1][c1] = True
            self.matched[r2][c2] = True
            self.selected = []
            if all(self.matched[i][j] for i in range(self.rows) for j in range(self.cols)):
                self.game.score += self.play_frames
                pyxel.stop()         # BGM停止
                pyxel.play(3, 3)     # ステージクリアファンファーレ
                self.clear_timer = 90
            else:
                pyxel.play(3, 1)     # マッチ成功音
        else:
            pyxel.play(3, 2)         # 不一致音
            self.wait_timer = 10

    def _start_flip_back(self):
        self.animating_cards = list(self.selected)
        self.anim_direction = 'to_back'
        self.anim_progress = 0

    def _on_title_button(self):
        bx, by, bw, bh = self.TITLE_BTN
        return bx <= pyxel.mouse_x < bx + bw and by <= pyxel.mouse_y < by + bh

    def _draw_clear_overlay(self):
        pyxel.dither(0.5)
        pyxel.rect(0, 0, 256, 256, 0)
        pyxel.dither(1.0)

        pyxel.rect(32, 86, 192, 90, 7)
        pyxel.rectb(32, 86, 192, 90, 0)

        header = f"STAGE {self.game.stage} CLEAR!"
        pyxel.text(128 - len(header) * 2, 96, header, 8)

        stage_time = f"STAGE TIME : {self.play_frames / 30:.1f}s"
        pyxel.text(128 - len(stage_time) * 2, 108, stage_time, 0)

        total_time = f"TOTAL TIME : {self.game.score / 30:.1f}s"
        pyxel.text(128 - len(total_time) * 2, 118, total_time, 0)

        moves_str = f"MOVES : {self.moves}"
        pyxel.text(128 - len(moves_str) * 2, 128, moves_str, 0)

        if self.clear_timer < 60:
            hint = "NEXT STAGE..." if self.game.stage < 3 else "CONGRATULATIONS!"
            pyxel.text(128 - len(hint) * 2, 142, hint, 11)

        if self.clear_timer < 0:
            prompt = "PRESS ENTER OR CLICK"
            pyxel.text(128 - len(prompt) * 2, 154, prompt, 5)

    def _draw_flip_anim(self, i, j, x, y):
        half = self.FLIP_DURATION // 2
        if self.anim_progress < half:
            visible_w = self.CARD_SIZE * (half - self.anim_progress) // half
            if self.anim_direction == 'to_face':
                self.game.cats[self.cards[i][j]].draw_back(x, y)
            else:
                self.game.cats[self.cards[i][j]].draw_face(x, y)
        else:
            visible_w = self.CARD_SIZE * (self.anim_progress - half + 1) // half
            if self.anim_direction == 'to_face':
                self.game.cats[self.cards[i][j]].draw_face(x, y)
            else:
                self.game.cats[self.cards[i][j]].draw_back(x, y)

        mask_w = (self.CARD_SIZE - visible_w) // 2
        if mask_w > 0:
            pyxel.rect(x, y, mask_w, self.CARD_SIZE, 7)
            pyxel.rect(x + self.CARD_SIZE - mask_w, y, mask_w, self.CARD_SIZE, 7)

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(1, 1, 255, 255, 7)

        time_str = f"TIME:{self.play_frames / 30:.1f}s"
        moves_str = f"MOVES:{self.moves}"
        pyxel.text(2, 1, moves_str, 0)
        pyxel.text(254 - len(time_str) * 4, 1, time_str, 0)

        for i in range(self.rows):
            for j in range(self.cols):
                x = j * self.CARD_SIZE + self.offset_x
                y = i * self.CARD_SIZE + self.offset_y
                if (i, j) in self.animating_cards:
                    self._draw_flip_anim(i, j, x, y)
                elif self.face_up[i][j]:
                    self.game.cats[self.cards[i][j]].draw_face(x, y)
                else:
                    self.game.cats[self.cards[i][j]].draw_back(x, y)

        if self.clear_timer != 0:
            self._draw_clear_overlay()

        bx, by, bw, bh = self.TITLE_BTN
        pyxel.rect(bx, by, bw, bh, 1)
        pyxel.text(bx + 10, by + 2, "TITLE", 7)
