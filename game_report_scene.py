class Game_Report_Scene:
    """
    ゲーム結果シーン
    """

    def __init__(self):
        self.__max = 0
        self.__exp = 0

    @property
    def max(self):
        return self.__max

    @max.setter
    def max(self, value):
        if self.max < value:
            self.__max = value

    @property
    def exp(self):
        return self.__exp

    @exp.setter
    def exp(self, value):
        self.__exp += value

    def reset_exp(self):
        self.__exp = 0
