import pyxel
import cards
import field
import dump


class Game_Scene:
    """
    ゲームシーン
    """

    CARD_WIDTH = 40  # 各カードの幅
    CARD_HEIGHT = 64  # 各カードの高さ
    CARD_Y_POSITION = 80  # カードを描画するY座標
    SIDE_MARGIN = 10  # window左右の余白(片方分)

    __selected_field_card_index = -1  # フィールドにあるカードのうちどれを選択しているか

    def __init__(self):
        self.__cards = cards.Cards()
        self.__field = field.Field()
        self.dump = dump.Dump()
        self.start()

    @property
    def dump(self):
        return self.__dump

    @dump.setter
    def dump(self, value):
        self.__dump = value

    @property
    def field(self):
        return self.__field

    @field.setter
    def field(self, value):
        self.__field = value

    def draw(self):
        self.draw_count()
        self.draw_field()
        self.draw_dump()
        self.move_cursor()
        self.draw_cursor()
        self.select_card()
        self.draw_all_cards()
        self.draw_result_judge()

    def start(self):
        """
        ゲーム開始
        5枚のカードを場に配置
        """
        for i in range(0, 5):
            field_card = self.__cards.pop()
            field_card.is_field = True
            self.__field.put(field_card)
        self.jump_cursor()

    def jump_cursor(self):
        """
        現在の __selected_field_card_index から順番に
        配られている __field のカードのうち捨て場に pop することが
        可能なカードの位置にカーソルをジャンプする
        存在しない場合はカーソルを非表示にする
        """
        if self.__selected_field_card_index < 0:
            return

        dump_card = self.__dump.get_last()  # 捨て場の一番上のカードを取得
        field_cards = self.__field.field_cards  # フィールド上のカード

        # 現在のインデックスから順番にチェック
        for i in range(len(field_cards)):
            # サークル状に検索する
            index = (self.__selected_field_card_index + i) % len(field_cards)
            field_card = field_cards[index]

            # カードが捨て場に置ける場合
            if not dump_card or self.__cards.compare(dump_card, field_card):
                self.__selected_field_card_index = index
                return

        # 該当カードがない場合、カーソルを非表示に設定
        self.__selected_field_card_index = -1

    def draw_dump(self):
        """
        捨て場描画
        """
        if self.__dump.count() > 0:
            x_center = pyxel.width // 2 - self.CARD_WIDTH // 2
            y_position = (
                self.CARD_Y_POSITION - self.CARD_HEIGHT - 10
            )  # フィールド上部に描画
            self.__dump.draw_dump(x_center, y_position)

    def draw_field(self):
        """
        フィールド描画
        """
        screen_width = pyxel.width - (self.SIDE_MARGIN * 2)
        spacing = (screen_width - (self.CARD_WIDTH * 5)) // 4  # カード間のスペース
        start_x = self.SIDE_MARGIN  # 初期のX座標

        for i, card in enumerate(self.__field.field_cards):
            x_position = start_x + i * (self.CARD_WIDTH + spacing)

            card.draw(x_position, self.CARD_Y_POSITION)

    def compare_cards(self):
        """
        フィールドの __selected_field_card_index にあるカードと捨て場の一番上のカードを比較する
        同じマークあるいは同じ数字の場合のみ True を返す
        ただし、捨て場にカードがない場合も True を返す

        Returns:
            boolean: 同じ True , 違う False
        """
        dump_card = self.__dump.get_last()
        if not dump_card:
            return True

        field_card = self.__field.get(self.__selected_field_card_index)

        return self.__cards.compare(dump_card, field_card)

    def throw_to_dump(self, index):
        """
        フィールドで選択されたカードの index を利用して、Fieldインスタンスから該当のカードを pop
        popしたカードを捨て場(__dump)へ put
        合わせて所定の index の位置に 新しいカードを __cards から追加する

        Args:
            index (int): Fieldクラスが持つ5枚のカードのうち選択された index
        """
        # フィールドから指定されたカードを取り出す
        card_to_throw = self.__field.pop(index)

        # 捨て場にそのカードを置く
        self.__dump.put(card_to_throw)

        # 新しいカードをデッキから引く
        if self.__cards.rest() > 0:  # 残りカードがある場合のみ
            new_card = self.__cards.pop()

            # フィールドの指定された位置に新しいカードを挿入
            self.__field.insert(index, new_card)

    def move_cursor(self):
        """
        Fieldの5枚のカードのうち、いずれかの下部に任意の1枚を選択するカーソルの移動先の index を決定する
        """
        # 初期状態での選択位置を設定
        if self.__selected_field_card_index == -1:
            self.__selected_field_card_index = 0

        # 入力処理: 左右キーで選択カードを変更
        if pyxel.btnp(pyxel.KEY_LEFT):
            while True:
                self.__selected_field_card_index = (
                    self.__selected_field_card_index - 1
                ) % 5  # 循環するようになってる
                if self.compare_cards():
                    break
        if pyxel.btnp(pyxel.KEY_RIGHT):
            while True:
                self.__selected_field_card_index = (
                    self.__selected_field_card_index + 1
                ) % 5  # 循環するようになってる
                if self.compare_cards():
                    break

    def draw_cursor(self):
        """
        Fieldの5枚のカードのうち、いずれかの下部に任意の1枚を選択するカーソルを表示する
        初期値は __selected_field_card_index が 0 のカード(左端)を選択状態
        方向キーの左右が選択されたら、カーソルも移動する
        """

        if self.__selected_field_card_index < 0:
            return

        # カーソルの描画位置計算
        screen_width = pyxel.width - (self.SIDE_MARGIN * 2)
        spacing = (screen_width - (self.CARD_WIDTH * 5)) // 4  # カード間のスペース
        start_x = self.SIDE_MARGIN  # 初期のX座標
        cursor_x = start_x + self.__selected_field_card_index * (
            self.CARD_WIDTH + spacing
        )
        cursor_y = self.CARD_Y_POSITION + self.CARD_HEIGHT + 10  # カード下部

        # カーソルを描画 (三角形)
        pyxel.tri(
            cursor_x + self.CARD_WIDTH // 2 - 5,
            cursor_y,  # 左下
            cursor_x + self.CARD_WIDTH // 2 + 5,
            cursor_y,  # 右下
            cursor_x + self.CARD_WIDTH // 2,
            cursor_y - 5,  # 上部
            8,  # カーソル色
        )

    def select_card(self):
        """
        エンターキーを押下した際の __selected_field_card_index にある Field上のカードを捨て場(__dump)に追加し、新しいカードを補充
        """
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_A):
            if self.compare_cards():
                self.throw_to_dump(self.__selected_field_card_index)
                self.jump_cursor()

    def is_game_over(self):
        """
        捨て場( __dump )のカードと一致(mark or number)するカードがフィールド( __field )に1枚も存在しないことをチェック

        Returns:
            boolean: 存在しない True , 存在する False
        """
        # 捨て場の一番上のカードを取得
        dump_card = self.__dump.get_last()

        # 捨て場が空の場合はゲームオーバー条件ではない
        if not dump_card:
            return False

        # フィールドのカードをチェック
        for field_card in self.__field.field_cards:
            if self.__cards.compare(dump_card, field_card):
                return False  # 一致するカードが見つかった場合、ゲームオーバーではない

        return True  # 一致するカードが1枚もない場合、ゲームオーバー

    def draw_count(self):
        """
        捨て場カードの右側に現在捨て場( __dump )にあるカードの枚数を数字で表示
        捨て場にカードがない場合は 0 を表示
        """
        count = self.__dump.count()  # 捨て場にあるカードの枚数を取得

        # 捨て場カードの右側に表示する位置を計算
        x_center = pyxel.width // 2 - self.CARD_WIDTH // 2
        y_position = self.CARD_Y_POSITION - self.CARD_HEIGHT - 10
        count_x = x_center + self.CARD_WIDTH + 10  # 捨て場カードの右側
        count_y = y_position + self.CARD_HEIGHT // 2 - 4  # 縦方向でセンタリング

        # カード枚数を描画
        pyxel.text(count_x, count_y, str(count), 7)  # 白色で数字を描画

    def draw_all_cards(self):
        """
        self.__cards が持つ group_and_sort を利用して すべてのカード辞書を取得
        window の 下部に以下のように表示
        すでに捨て場に捨てたカードは空文字で何も表示しない
        また、横と縦が揃うように表示

        Hearts:   1 2 3 4   6 7 8 9 10 11 12 13
        Diamonds: 1 2 3 4 5 6   8 9 10 11 12 13
        Clubs:    1 2 3 4 5 6 7 8 9 10 11 12 13
        Spades:   1 2 3 4 5 6 7 8   10 11    13
        """
        grouped = self.__cards.group_and_sort()  # マークごとに並び替えたカードを取得

        # フィールドのカードも残カードに加える
        for card in self.__field.field_cards:
            grouped[card.mark][card.number - 1] = card

        # 描画（ウィンドウ下部に出力）
        y_offset = pyxel.height - 40  # 下部に表示するためのオフセット
        for mark, cards in grouped.items():
            index = self.__cards.marks().index(
                mark
            )  # 定数を他ファイルから import して呼び込む方法ってある?
            pyxel.text(10, y_offset + index * 8, '{:10} '.format(mark), 7)
            for j, card in enumerate(cards):
                if not card:
                    continue
                # フィールドのカードの場合は文字色を変更
                color = 5 if card.is_field else 7
                pyxel.text(
                    50 + j * 10,
                    y_offset + index * 8,
                    '{:2}'.format(str(card.number)) + " ",
                    color,
                )

    def draw_result_judge(self):
        """
        フィールド上の5枚のカードをポーカー役で判定
        """
        result = self.field.judge()
        exp = field.POKER_HANDS[result]['point']
        pyxel.text(200, 20, result, 7)
        pyxel.text(200, 30, str(exp), 7)
