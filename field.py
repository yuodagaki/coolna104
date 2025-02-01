from collections import Counter


class Field:
    """
    カードを5枚置いておく場
    """

    def __init__(self):
        self.field_cards = []

    @property
    def field_cards(self):
        return self.__field_cards

    @field_cards.setter
    def field_cards(self, value):
        self.__field_cards = value

    def put(self, card):
        """
        カードを１枚場に置く

        Args:
            card (Card): 選択されたカード
        """
        if len(self.field_cards) >= 5:
            raise ValueError("Field can only hold 5 cards.")
        self.field_cards.append(card)

    def pop(self, index):
        """
        カードを場から取り出す

        Args:
            index (int): カードの index
        Returns:
            Card: 取り出したカード
        """
        if index < 0 or index >= len(self.field_cards):
            raise IndexError("Invalid card index.")
        return self.field_cards.pop(index)

    def get(self, index):
        """
        場のカードを参照する

        Args:
            index (int): カードの index
        Returns:
            Card: 参照したカード
        """
        if index < 0 or index >= len(self.field_cards):
            raise IndexError("Invalid card index.")
        return self.field_cards[index]

    def judge(self):
        """
        場にある５枚のカードから役名を取得

        Returns:
            string: 役の名前
        """
        if len(self.field_cards) != 5:
            return "Not enough cards on the field."

        return PokerHandEvaluator.evaluate(self.field_cards)

    def insert(self, index, card):
        """
        指定された index の位置にカードを挿入

        Args:
            index (int): 挿入する index
            card (Card): 挿入するカード
        """
        self.field_cards.insert(index, card)


POKER_HANDS = {
    'Royal Straight Flush': {'name': 'Royal Straight Flush', 'point': 1000},
    'Straight Flush': {'name': 'Straight Flush', 'point': 200},
    'Four of a Kind': {'name': 'Four of a Kind', 'point': 100},
    'Full House': {'name': 'Full House', 'point': 70},
    'Flush': {'name': 'Flush', 'point': 50},
    'Straight': {'name': 'Straight', 'point': 20},
    'Three of a Kind': {'name': 'Three of a Kind', 'point': 10},
    'Two Pair': {'name': 'Two Pair', 'point': 5},
    'One Pair': {'name': 'One Pair', 'point': 0},
    'High Card': {'name': 'High Card', 'point': 0},
}


class PokerHandEvaluator:
    """
    ポーカーの役を判定するクラス
    """

    HANDS = [
        "High Card",
        "One Pair",
        "Two Pair",
        "Three of a Kind",
        "Straight",
        "Flush",
        "Full House",
        "Four of a Kind",
        "Straight Flush",
        "Royal Straight Flush",
    ]

    @staticmethod
    def evaluate(cards):
        """
        与えられたカードから役を判定する

        Args:
            cards (list[Card]): 5枚のカード

        Returns:
            string: 役の名前
        """
        numbers = [card.number for card in cards]
        marks = [card.mark for card in cards]

        # カードの数の頻度を数える
        num_count = Counter(numbers)

        # 同じカードの枚数の判定
        count_values = sorted(num_count.values(), reverse=True)

        # フラッシュ判定（全てのカードが同じマーク）
        is_flush = len(set(marks)) == 1

        # ストレート判定（数字が連続している）
        sorted_numbers = sorted(numbers)
        is_straight = sorted_numbers == list(
            range(min(numbers), max(numbers) + 1)
        ) or sorted_numbers == [
            1,
            10,
            11,
            12,
            13,
        ]  # 特殊なストレート

        # ロイヤルストレートフラッシュ判定
        if is_flush and sorted_numbers == [1, 10, 11, 12, 13]:
            return "Royal Straight Flush"

        # ストレートフラッシュ判定
        if is_flush and is_straight:
            return "Straight Flush"

        if count_values == [4, 1]:
            return "Four of a Kind"
        if count_values == [3, 2]:
            return "Full House"
        if is_flush:
            return "Flush"
        if is_straight:
            return "Straight"
        if count_values == [3, 1, 1]:
            return "Three of a Kind"
        if count_values == [2, 2, 1]:
            return "Two Pair"
        if count_values == [2, 1, 1, 1]:
            return "One Pair"

        return "High Card"
