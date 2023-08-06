class Wrapper(dict):
    def __init__(self, model) -> None:
        self.__dict__ = model.__dict__
        if self.__dict__.keys().__contains__("_state"):
            del self.__dict__["_state"]
        super().__init__(model.__dict__)
