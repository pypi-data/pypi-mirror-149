from io import TextIOWrapper
from functools import partial


class _FileTypePickable:
    """
    When pickling, if any class atributes as open files,
    close them and store a new function to open them again
    when the object is unpickled.
    """
    def __getstate__(self):
        state = self.__dict__.copy()
        for attribute, attr_value in state.items():
            assert not isinstance(attr_value, partial)
            if isinstance(attr_value, TextIOWrapper):
                attr_value.close()
                if 'w' in attr_value.mode:
                    raise RuntimeError('Attempting to write to a single '
                                       'file using multiple processes!')
                state[attribute] = partial(open, attr_value.name, mode=attr_value.mode)
        return state

    def __setstate__(self, state):
        for attribute, attr_value in state.items():
            if isinstance(attr_value, partial):
                state[attribute] = attr_value()
        self.__dict__.update(state)
