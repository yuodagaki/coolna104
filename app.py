import pyxel
import game_scene
import game_over_scene
import game_report_scene


class App:
    """
    Main
    """

    TITLE_SCENE = "title"
    GAME_SCENE = "game"
    GAME_OVER_SCENE = "game over"
    __current_scene = GAME_SCENE

    def __init__(self):
        pyxel.init(240, 200, title="coolna 104")
        self.__scene = game_scene.Game_Scene()
        self.__report = game_report_scene.Game_Report_Scene()
        self.__is_replay = False
        pyxel.load("assets/coolna104.pyxres")

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if self.__current_scene == self.GAME_SCENE and self.__scene.is_game_over():
            # スコア登録
            self.__report.max = self.__scene.dump.count()
            self.__report.exp = self.__scene.dump.count()
            # シーン切り替え
            self.__current_scene = self.GAME_OVER_SCENE
            self.__scene = game_over_scene.Game_Over_Scene()
        if self.__current_scene == self.GAME_OVER_SCENE and self.__scene.is_replay():
            self.__current_scene = self.GAME_SCENE
            self.__scene = game_scene.Game_Scene()
            self.__is_replay = True  # GameOver -> Game へ切り替わるときのみのフラグ

    def draw(self):
        if self.__current_scene == self.TITLE_SCENE:
            pyxel.cls(1)
        if self.__current_scene == self.GAME_SCENE:
            if self.__is_replay:
                # GameOver から Game を再開(is_replay = True)するときの最初のフレームのみ
                # 余計な draw(ゲーム判定関連)をさせない
                self.__is_replay = False
                return
            pyxel.cls(1)
            self.__scene.draw()
        if self.__current_scene == self.GAME_OVER_SCENE:
            pyxel.cls(3)
            pyxel.text(10, 10, "Game Over", 0)
            pyxel.text(10, 30, "your max score is " + str(self.__report.max), 0)
            # pyxel.text(10, 40, "your max exp is " + str(self.__report.exp), 0)
        # pyxel.text(10, 20, self.__current_scene, 2)


App().run()
