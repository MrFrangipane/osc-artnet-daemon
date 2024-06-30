from oscartnetdaemon.python_extensions.singleton_metaclass import SingletonMetaclass


class ScribbleRepository(metaclass=SingletonMetaclass):

    def __init__(self):
        pass
