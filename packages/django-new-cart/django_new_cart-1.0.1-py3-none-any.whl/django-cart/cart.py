from .multi import MultiCart

class SingleCart(MultiCart):
    def __init__(self, request):
        super().__init__(request)

