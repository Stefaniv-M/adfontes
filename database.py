from rows import *
from slots import *


class Database:
    """
    Class representing a database.
    """
    def __init__(self, path):
        """
        Initialise by path to file.
        :param path: str
        """
        info = self._info_from_file(path)



    def clear(self):
        """
        Clear Database.
        :return: NoneType
        """
        self.rows = [Row(self.length) for i in range(self.rows_num)]

    @staticmethod
    def _info_from_file(path):
        """
        Get tuple containing input information from the file.

        Return tuple containing:
        - tuple with number of rows, length of each, number of unavailable
        slots, number of pools, and number of servers.
        - tuple with tuples with coordinates of unavailable slots
        - tuple with tuples of servers data (size and capacity)
        :param path: str
        :return: tuple
        """
        file = open(path, "r")
        lines = file.readlines()
        file.close()

        line = [int(num_str) for num_str in lines[0].split()]

        rows_num = line[0]
        row_len = line[1]
        unavailable_num = line[2]
        pools_num = line[3]
        servers_num = line[4]

        current_index = 1

        # Getting positions of unavailable slots:
        unavailable_pos_list = []
        for index in range(current_index, current_index + unavailable_num):
            unavailable_pos_list.append(tuple([int(num_str) for num_str
                                               in lines[index].split()]))
        current_index += unavailable_num

        # Getting tuples representing servers:
        servers_data_list = []
        for index in range(current_index, current_index + servers_num):
            servers_data_list.append(tuple([int(num_str) for num_str
                                            in lines[index].split()]))

        return tuple([tuple(line), tuple(unavailable_pos_list), tuple(servers_data_list)])
