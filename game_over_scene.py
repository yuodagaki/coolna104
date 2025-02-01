import pyxel


class Game_Over_Scene:
    """
    ゲームオーバーシーン
    """

    def is_replay(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_A):
            return True
