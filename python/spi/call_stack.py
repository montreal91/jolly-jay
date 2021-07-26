
from spi.errors import RuntimeInterpreterError


class CallStack:
    def __init__(self):
        # TODO: try to replace it with linked list in the future and compare
        #       results.
        self._records = []

    def access_variable(self, var_name):
        var = self.peek().get(var_name)
        if var is not None:
            return var
        var = self._records[0].get(var_name)
        if var is not None:
            return var

        # After proper semantic check this should never happen
        raise RuntimeInterpreterError()

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
