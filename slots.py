class AbstractSlot:
    """
    This is abstract of anything that is  in table.
    """
    pass


class UnavailableSlot(AbstractSlot):
    """
    Class representing unavailable slot.
    """
    def __init__(self):
        """
        I will need to create instances of it.
        """
        pass


class EmptySlot(AbstractSlot):
    """
    Class representing empty spot in database.
    """
    def __init__(self):
        pass


class AbstractServer(AbstractSlot):
    """
    Class representing slot filled by server.
    """
    def __init__(self, size, capacity, pool=0, parent=None):
        """
        Initialise abstract server.
        :param size: int size of server
        :param capacity: int capacity of server
        :param pool: int number of pool the server is part of
        :param parent: AbstractServer leftmost part of the server.
        This is a convenient way to work with separate slots with same
        server.
        """
        self.size = size
        self.capacity = capacity
        self.pool = pool
        self.parent = parent


class HeadServer(AbstractServer):
    """
    Represents leftmost (and main) part of the server.
    """
    def __init__(self, size, capacity, pool=0):
        super().__init__(size, capacity, pool, self)


class TailServer(AbstractServer):
    """
    Represents any part of the server which is not leftmost.
    """
    def __init__(self, head_server):
        """
        Initialisation is by main server because all the data
        must be copied from it.
        :param head_server: Abstract Server
        """
        super().__init__(head_server.parent.size,
                         head_server.parent.capacity,
                         head_server.parent.pool,
                         head_server.parent)


def slot_to_str(slot, max_capacity=0, max_pool=0):
    """
    Return string representation of slot.
    If slot is: , return something like:

    EmptySlot         " ------ "
    UnavailableSlot   " XXXXXX "
    HeadServer        "[{}]({})"
    TailServer        "<{}>({})"

    :param slot: AbstractFilledSlot or NoneType
    :return: str
    """
    # To avoid code duplication:
    def non_server_slot_helper(symbol, max_capacity, max_pool):
        """
        :param symbol: char
        :param max_capacity: int
        :param max_pool: int
        :return: str
        """
        return " " + (max_capacity + max_pool + 2) * symbol + " "

    def fit_num(num, spaces):
        """
        To fit string number into given number of spaces.
        :param num: int
        :param spaces: int
        :return: str
        """
        num_str = str(num)

        if len(num_str) > spaces:
            raise ValueError("Can't fit number " + num_str +
                             " into " + str(spaces) + " spaces!")

        # Calculating number of spaces before and behind the number:
        spaces_behind = (spaces - len(num_str)) // 2
        spaces_before = (spaces - len(num_str)) - spaces_behind

        # Result:
        return " " * spaces_before + num_str + " " * spaces_behind

    def server_slot_helper(server, max_capacity, max_pool):
        """
        Return string representation of server slot.
        :param server: HeadServer or TailServer
        :param max_capacity: int
        :param max_pool: int
        :return: str
        """
        brackets = ""

        if isinstance(server, HeadServer):
            brackets = "[]"
        elif isinstance(server, TailServer):
            brackets = "<>"
        else:
            raise ValueError("Non-Server argument was passed!")

        if len(str(server.capacity)) > max_capacity or \
           len(str(server.pool)) > max_pool:
            raise ValueError("Can't fit number into given amount of"
                             " spaces!")

        return "{}{}{}({})".format(brackets[0],
                                   fit_num(server.capacity, max_capacity),
                                   brackets[1],
                                   fit_num(server.pool, max_pool))

    # Main part:
    if isinstance(slot, EmptySlot):
        return non_server_slot_helper("-", max_capacity, max_pool)
    elif isinstance(slot, UnavailableSlot):
        return non_server_slot_helper("X", max_capacity, max_pool)
    elif isinstance(slot, AbstractServer):
        return server_slot_helper(slot, max_capacity, max_pool)
    else:
        raise ValueError("Function asked to print not a slot!")


def slot_copy(slot):
    """
    Return copy of the slot.
    :param slot: AbstractSlot
    :return: AbstractSlot
    """
    if isinstance(slot, EmptySlot):
        return EmptySlot()
    elif isinstance(slot, UnavailableSlot):
        return UnavailableSlot()
    elif isinstance(slot, HeadServer):
        return HeadServer(slot.size, slot.capacity, slot.pool)
    elif isinstance(slot, TailServer):
        head_server = slot_copy(slot.parent)
        return TailServer(head_server)
    else:
        raise ValueError("Can't create copy of this!")








