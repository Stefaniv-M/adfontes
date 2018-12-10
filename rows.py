from slots import *


class Row:
    """
    Class representing a row.
    """
    def __init__(self, length):
        """
        Initialise an empty row of length.
        """
        self.length = length

        # Method clear sets empty slots.
        self.slots = None
        self.clear()

    def clear(self):
        """
        Clear a Row.
        :return: NoneType
        """
        self.slots = [EmptySlot for i in range(self.length)]

    def get_string(self, max_capacity_len, max_pool_len):
        """
        Get string representation of a Row. Arguments tell
        how much spaces to use for numbers (so that table
        alligns).
        :param max_capacity_len: int
        :param max_pool_len: int
        :return: None
        """
        result_str = "|"

        for i in range(self.length - 1):
            result_str = result_str + slot_to_str(self.slots[i],
                                                  max_capacity_len,
                                                  max_pool_len)

            # I want to separate different servers with "|",
            # and parts of same servers with spaces:
            if isinstance(self.slots[i], AbstractServer) and \
               isinstance(self.slots[i + 1], AbstractServer) and \
               self.slots[i].parent is self.slots[i + 1].parent:

                result_str = result_str + " "
            else:
                result_str = result_str + "|"

        result_str = result_str + slot_to_str(self.slots[-1],
                                              max_capacity_len,
                                              max_pool_len) + "|"

        return result_str

    def get_capacity(self, pool):
        """
        Get capacity of given pool in this Row.
        :param pool: int
        :return: int
        """
        total_capacity = 0

        for slot in self.slots:
            if isinstance(slot, HeadServer) and slot.pool == pool:
                total_capacity += slot.capacity

        return total_capacity

    def add_unavailable_slot(self, index):
        """
        Add unavailable slot to the Row.
        :param index: int
        :return: NoneType
        """
        # First, I will check if there are servers in Row
        # (adding unavailable slot can only be done when
        # there are no servers yet):
        for slot in self.slots:
            if isinstance(slot, AbstractServer):
                raise Exception("Attempt to add unavailable slot to "
                                "a Row after adding servers!")

        # Now, adding the slot (I won't check for anything because
        # it is not needed):
        # (if index is incorrect, list will take care of it)
        self.slots[index] = UnavailableSlot()

    def add_server(self, server_tuple, index):
        """
        Add server to the row.
        :param server_tuple: tuple with size, capacity, and pool
        :param index: int
        :return: NoneType
        """
        self.check_index(index)

        # Checking if server can fit there:
        if not self.check_if_fits(server_tuple, index):
            raise Exception("Server can't be inserted to that spot!")

        # Getting information from tuple:
        size = server_tuple[0]
        capacity = server_tuple[1]
        pool = server_tuple[2]

        # Now creating and adding server:
        head_server = HeadServer(size, capacity, pool)
        for i in range(index, index + size):
            if i == index:
                self.slots[i] = head_server
            else:
                self.slots[i] = TailServer(head_server)

    def check_if_fits(self, server_tuple, index):
        """
        Check if server fits into given spot in a Row.
        :param server_tuple: tuple with size, capacity, and pool
        :param index: int
        :return: bool
        """
        if not self.check_index(index):
            raise ValueError("Invalid index!")

        # Extracting data from tuple:
        size = server_tuple[0]

        # Checking each slot the server will fill:
        for i in range(index, index + size):
            if not self.check_index(index) or \
               not isinstance(self.slots[i], EmptySlot):
                return False

        return True

    def check_index(self, index):
        """
        Check if index is valid (here it can't be -1, for example)
        :param index: int
        :return: bool
        """
        if isinstance(index, int) and 0 <= index < len(self.slots):
            return True
        else:
            return False

    def get_slot_copy(self, index):
        """
        Get copy of thing in slot (to avoid encapsulation problems)
        :param index: int, here can be any for list
        :return: NoneType
        """
        return slot_copy(self.slots[index])

    def remove_server(self, index):
        """
        Remove server and return copy of the main one (head).
        :param index: int
        :return: HeadServer
        """
        slot = self.slots[index]

        if not isinstance(slot, AbstractServer):
            raise ValueError("No server to remove!")

        head_server = slot.parent

        # Erasing the server:
        for i in range(len(self.slots)):
            if isinstance(self.slots[i], AbstractServer) \
               and self.slots[i].parent is head_server:
                self.slots[i] = EmptySlot

        # Returning copy:
        return slot_copy(head_server)
