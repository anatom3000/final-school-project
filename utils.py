class Stringable:
    # simple class that automatically generate a string representation
    # just subclass this class to add
    def __str__(self):
        return f"{self.__class__.__name__}({', '.join([f'{k}={repr(v)}' for k, v in vars(self).items()])})"

    def __repr__(self):
        return self.__str__()
