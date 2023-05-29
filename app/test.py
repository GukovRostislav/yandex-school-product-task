class A:
    def a(self):
        if type(self.__x) == int and type(self.__y) == int:
            print(self.__x)
        else:
            print('123')

    def __init__(self, x, y):
        self.__x = x
        self.__y = y


a = A

