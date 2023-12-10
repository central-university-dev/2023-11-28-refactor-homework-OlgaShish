class Test:

    def is_test(self):
        return True

    def is_prod(self):
        return False


def magic_function():
    test = Test()
    if test.is_test():
        return 42
    else:
        return 11


class Test1:
    value: int