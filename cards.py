import random
import pyxel
import constants
import math

CARD_MARKS = ["Hearts", "Diamonds", "Clubs", "Spades"]


class Card:
    """
    1枚のカード
    """

    def __init__(self, mark, number, is_joker=False):
        self.mark = mark
        self.number = number
        self.is_joker = is_joker
        self.is_dumped = False
        self.is_field = False
        self._constants = constants.Constants()

    @property
    def mark(self):
        return self.__mark

    @mark.setter
    def mark(self, mark):
        self.__mark = mark

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, number):
        if number < 1 or number > 13:
            raise ValueError("invalid number.")
        self.__number = number

    @property
    def is_joker(self):
        return self.__is_joker

    @is_joker.setter
    def is_joker(self, is_joker):
        self.__is_joker = is_joker

    @property
    def is_dumped(self):
        return self.__is_dumped

    @is_dumped.setter
    def is_dumped(self, value):
        self.__is_dumped = value

    @property
    def is_field(self):
        return self.__is_field

    @is_field.setter
    def is_field(self, value):
        self.__is_field = value

    def __str__(self):
        """
        カード情報を文字列で返す。
        """
        if self.is_joker:
            return "Joker"
        return f"{self.mark} {self.number}"

    def draw(self, x, y):
        """ """
        colkey = 0  # 背景色のキー
        back = self._constants.IMAGE_CARD_BACKGROUND[self.number - 1]
        mark = self._constants.IMAGE_MARKS[CARD_MARKS.index(self.mark)]
        number = self._constants.IMAGE_NUMBERS[self.number - 1]
        pyxel.blt(
            x,
            y,
            0,
            back[0],
            back[1],
            self._constants.IMAGE_CARD_W_H[0],
            self._constants.IMAGE_CARD_W_H[1],
            colkey,
        )  # back top
        pyxel.blt(
            x,
            y + 32,
            0,
            back[0],
            back[1],
            -self._constants.IMAGE_CARD_W_H[0],
            -self._constants.IMAGE_CARD_W_H[1],
            colkey,
        )  # back bottom
        pyxel.blt(
            x + 2,
            y + 2,
            0,
            number[0],
            number[1],
            self._constants.IMAGE_NUMBER_W_H[0],
            self._constants.IMAGE_NUMBER_W_H[1],
            colkey,
        )  # number top
        pyxel.blt(
            x + 1,
            y + 8,
            0,
            mark[0],
            mark[1],
            self._constants.IMAGE_MARK_W_H[0],
            self._constants.IMAGE_MARK_W_H[1],
            colkey,
        )  # mark top
        pyxel.blt(
            x + 33,
            y + 57,
            0,
            number[0],
            number[1],
            -self._constants.IMAGE_NUMBER_W_H[0],
            -self._constants.IMAGE_NUMBER_W_H[1],
            colkey,
        )  # number bottom
        pyxel.blt(
            x + 32,
            y + 50,
            0,
            mark[0],
            mark[1],
            -self._constants.IMAGE_MARK_W_H[0],
            -self._constants.IMAGE_MARK_W_H[1],
            colkey,
        )  # mark bottom

        self.draw_marks(x, y)

    def draw_marks(self, x, y):
        mark = self._constants.IMAGE_MARKS[CARD_MARKS.index(self.mark)]
        """
        カード内側のマーク描画
        """
        if self.number == 1:
            pyxel.blt(
                x + 17,
                y + 28,
                0,
                mark[0],
                mark[1],
                self._constants.IMAGE_MARK_W_H[0],
                self._constants.IMAGE_MARK_W_H[1],
                0,
                None,
                4.0,
            )
            return

        if self.number not in [1, 11, 12, 13]:
            self.draw_images(self.number, x, y, mark)
            return

    def draw_images(self, num_images: int, card_x, card_y, mark):
        # 画像のサイズ
        image_w = 7
        image_h = 7
        padding_x = 4  # 左右の余白
        padding_y = 0  # 上下の余白 (必要なら調整)

        # 描画領域
        area_w = 40 - (padding_x * 2)  # 左右 7px の余白を引いた描画エリア幅
        area_h = 64  # 縦は余白なし
        """
        指定された個数の 7x7 イメージを 40x64 領域の中央に等間隔で描画する
        左右の余白を固定し、適切な列数で整列する
        """
        if num_images < 2 or num_images > 10:
            return  # 2~10 の範囲外なら何もしない

        # 横の最大列数 (余白1pxを考慮)
        max_cols = (area_w + 1) // (image_w + 1) - 2  # 余白 1px 分を考慮
        cols = min(num_images, max_cols)  # 実際の列数
        rows = math.ceil(num_images / cols)  # 行数計算

        # 実際の描画範囲における中央基準
        total_width = cols * image_w + (cols - 1)  # 余白含む横幅
        total_height = rows * image_h + (rows - 1)  # 余白含む縦幅

        start_x = (
            card_x + padding_x + (area_w - total_width) // 2
        )  # 左右の固定余白 + 中央揃え
        start_y = card_y + (area_h - total_height) // 2  # 縦は均等に中央揃え

        # 描画処理
        index = 0
        for row in range(rows):
            for col in range(cols):
                if index >= num_images:
                    return
                x = start_x + col * (image_w + 1)
                y = start_y + row * (image_h + 1)
                pyxel.blt(x, y, 0, mark[0], mark[1], image_w, image_h, 0)
                index += 1


class Cards:
    """
    トランプ
    """

    def __init__(self, jokers=False):
        self.cards = []
        self.shuffle(jokers)

    def marks(self):
        return CARD_MARKS

    @property
    def cards(self):
        return self.__cards

    @cards.setter
    def cards(self, value):
        self.__cards = value

    def shuffle(self, jokers=False):
        """
        52枚のカードをシャッフル

        Args:
            jokers (boolean): ジョーカーを含むか
        """
        self.cards = []
        for mark in CARD_MARKS:
            for number in range(1, 14):
                self.cards.append(Card(mark, number))

        if jokers:
            self.cards.append(Card(None, None, is_joker=True))
            self.cards.append(Card(None, None, is_joker=True))

        random.shuffle(self.cards)

    def pop(self):
        """
        1枚取り出す

        Returns:
            Card: 取り出されたカード
        """
        if not self.cards:
            raise IndexError("No cards left in the deck.")
        return self.cards.pop()

    def rest(self):
        """
        残りの枚数を返す

        Returns:
            int: 残りの枚数
        """
        return len(self.cards)

    def reshuffle(self):
        """
        残りのカードのみをシャッフルする。
        """
        if len(self.cards) <= 1:
            print("Not enough cards to reshuffle.")
            return
        random.shuffle(self.cards)

    def group_and_sort(self):
        """
        残りのカードをマークごとに昇順に並び替え、4つの1次元配列を持つ2次元配列として返す。
        Jokerは含めない。
        """
        grouped = {mark: [None] * 13 for mark in CARD_MARKS}

        # 既存のカードを正しい位置に配置
        for card in self.cards:
            if not card.is_joker:
                grouped[card.mark][card.number - 1] = card

        return grouped

    def compare(self, card1, card2):
        """
        2枚のカードの mark, number を比較して、同じ番号か同じマークであれば true を返す
        それ以外は false を返す

        Args:
            card1 (Card): 比較対象のカード
            card2 (Card): 比較対象のカード

        Returns:
            bool: 同じ番号または同じマークの場合は True、それ以外は False
        """
        return card1.number == card2.number or card1.mark == card2.mark
