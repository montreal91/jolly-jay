
class CallStack:
    def __init__(self):
        # TODO: try to replace it with linked list in the future and compare
        #       results.
        self._records = []

    def push(self, ar):
        self._records.append(ar)

    def pop(self):
        return self._records.pop()

    def peek(self):
        return self._records[-1]

    def __len__(self):
        return len(self._records)

    def __str__(self):
        s = "\n".join(repr(ar) for ar in reversed(self._records))
        s = f"CALL STACK\n{s}\n"
        return s

    def __repr__(self):
        return self.__str__()
