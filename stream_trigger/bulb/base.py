
class BaseBulb():

    def __return_not_implemented(self, func):
        raise NotImplementedError('subclasses must override {}'.format(func.__name__))

    def set_off(self):
        self.__return_not_implemented(self.set_off)

    def set_on(self):
        self.__return_not_implemented(self.set_on)

    def set_color(self, color):
        self.__return_not_implemented(self.set_color)
