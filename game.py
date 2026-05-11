import pyxel

from scenes import TitleScene, PlayScene, ClearScene
from entities import LuckyCats

class Game:
    def __init__(self):
        #pyxelの初期化
        pyxel.init(256, 256, title="Lucky Cats Matching Game")
        pyxel.mouse(True)
        # 外部からタイルマップを読み込む方法は後で調べる。←エディタで解決した。
        pyxel.load("assets/cats01.pyxres")
        #pyxel.save_pal("cats01.pyxpal")

        self.cats=[]
        self.generate_cats()

        # シーンを辞書型にまとめておく。この時、クラスの生成も行われている。
        self.scenes = {
            "title": TitleScene(self),
            "play": PlayScene(self),
            "clear": ClearScene(self),
        }
        self.scene_name = None
        self.stage = 1
        self.score = 0

        self.change_scene("title") # シーンをタイトル画面に変更する
        
        # ゲームの実行を開始する
        pyxel.run(self.update, self.draw)
    
    def generate_cats(self):
        for i in range(100):
            self.cats.append(LuckyCats(self))

    # シーンを変更する
    def change_scene(self, scene_name):
        self.scene_name = scene_name
        self.scenes[self.scene_name].start()

    # ゲームを更新する
    def update(self):
        self.scenes[self.scene_name].update()

    # ゲームを描画する
    def draw(self):
        # 現在のシーンを描画する
        self.scenes[self.scene_name].draw()
        
