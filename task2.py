class Effect:
    pass

class Spell:
    def __init__(self):
        self.__effects = []

    def add_effect(self, effect: Effect):
        if not isinstance(effect, Effect):
            raise ValueError
        self.__effects.append(effect)

    def change_effect_magnitude(self, index:int, newmag:int):
        if newmag <= 0:
            raise ValueError
        if index > len(self.__effects) - 1:
            raise IndexError
        self.__effects[index].mag = newmag

    @property
    def value(self):
        summag = 0
        sumtext = []
        lensumtext = len(sumtext)
        for i in self.__effects:
            summag += i.mag
            if i.text not in sumtext:
                sumtext.append(i.text)
        cal = summag * lensumtext
        return lensumtext








