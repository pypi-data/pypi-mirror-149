


class Tree:
    def pre_order(self):
        if not self.__dict__:
            return []
        stack, results = [False, root], []
