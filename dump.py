import pyxel


class Dump:
    """
    カードを捨てる場所
    """

    __dump = []

    def __init__(self):
        self.__dump = []

    def put(self, card):
        """
        捨て場(__dump)にカードを加える

        Args:
            card (Card): カード
        """
        self.__dump.append(card)

    def draw_dump(self, x, y):
        """
        現時点で捨て場にストックされているカードのうち最後にストックされたカードを描画

        Args:
            x (int): カードを描画する x 座標
            y (int): カードを描画する y 座標
            width (int): カードの横幅
            height (int): カードの高さ
        """
        if self.__dump:
            last_card = self.__dump[-1]  # 最後にストックされたカード
            last_card.draw(x, y)

    def count(self):
        """
        捨て場にストックされたカード枚数を返す
        """
        return len(self.__dump)

    def get_last(self):
        """
        捨て場のカードの1番上(最後に追加したカード)を取得する

        Returns:
            Card: 最後に追加されたカード
        """
        if not self.__dump:
            return
        return self.__dump[-1]
