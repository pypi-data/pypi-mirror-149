"""Maze class"""
import logging
import random
import networkx as nx


class HexagonGrid:
    """
    Base maze class which defines the area of the maze
    """

    def __init__(self, column_number, row_number, *name):
        self.columns = column_number
        self.rows = row_number
        # name of the maze
        self.name = name


class HexagonMaze(HexagonGrid):
    """
    Maze area for hexagonal platform

    Parameters
    ----------
    :param column_number: The number of rows of the hexagonal space
    :param row_number: The number of columns of the hexagonal space
    Returns
    ----------
    :return: Maze Network of the area of that is possible for the platforms to move around in
    """

    def __init__(self, column_number, row_number):
        super().__init__(column_number, row_number)
        # List of the object names of the robots that are present in the maze
        self.consecutive_positions = []
        self.robot_list = []
        self.non_moving_robot_list = None
        self.animal_list = []
        # move list of class
        self.valid_moves = None
        # animal goal
        self.goal = None
        # networkx grid
        self.movement_network = None
        self.temp_movement_network = None
        # keeps track of the choices the animal has been given to choose from
        self.choice_list = []
        # Creates hexgrid network
        self.set_network()

    def get_status(self):
        """Prints the status of the maze (the position of the animal, robots, maze and goal) for debugging"""
        direction_to_axis = {0: 'y', 1: 'z', 2: 'x', 3: 'y', 4: 'z', 5: 'x'}
        print('\n \n======== STATUS OF THE MAZE ========')
        print(f'Maze goal is: {self.goal}')
        print('Position of Robots:')
        for robot in self.robot_list:
            print(
                f'{robot.name} is in position {robot.position_vector}, with direction {direction_to_axis[robot.direction]} and its the {robot.is_animal_robot}')

        print('Position of Animals:')
        for animal in self.animal_list:
            print(f'{animal.name} is in position {animal.position_vector}')

        print('======= END OF STATUS UPDATE ======= \n \n ')

    def set_goal(self, goal):
        """
        The goal of that animal is trying to reach
        ------
        :parameter goal: The coordinates of the goal for the animal (x, y, x) is format
        """
        # Check the goal is in the correct format
        if type(goal) == tuple:
            self.goal = goal
        else:
            print('Type of goal was incorrect. Please format goal in (x, y, z)')

    def add_robot(self, robot):
        """
        Adds animals to the maze's list of robots, self.robot_list
        ------
        :parameter robot: The name fo the robot object that will be added to self.robot_list
        """
        self.robot_list.append(robot)

    def add_animal(self, animal):
        """
        Adds animals to the maze's list of animals, self.animal_list
        ------
        :parameter animal: The name of the animal object that will be added to self.animal_list
        """
        self.animal_list.append(animal)

    def generate_network(self, rows, columns):
        """
        Makes the correctly labeled grid in the correct coordinate system

        ------
        :param rows: Number of rows in the square grid space
        :param columns: Number of columsn in the square grid space

        :returns Network hexagonal grid on which the platforms move around. From the size of the actual space 2
        First is X dimension, second is Y dimension, where the X is the 'spikey' top surface and Y is the smooth side
        """

        def node_generation(row, col):

            def pairwise(iterable):
                "s -> (s0, s1), (s2, s3), (s4, s5), ..."
                a = iter(iterable)
                return zip(a, a)

            start = 0
            node_list = []
            # for every 2 rows in the network until you fun out of rows to iterate through:
            for x1, x2 in pairwise(list(range(row))):  # for every 2 elements in the list
                for y in list(range(start, col + start, 1)):  # for every y coordinate
                    node_list.append((x1, y, -(x1 + y)))
                    node_list.append((x2, y, -(x2 + y)))
                start = start - 1
                # y goes up however it starts back 1 every time it reaches the top

                # step back in the coordinate system 2
            return node_list

        def add_nodes(node_list, graph):
            for node in node_list:
                graph.add_node(node)
            # nx.draw_spring(graph, with_labels=True)
            return graph

        def consecutive_positions(node):
            # generate consecutive positions
            inner_ring_vectors = [(1, 0, -1), (1, -1, 0), (0, -1, 1), (-1, 0, 1), (-1, 1, 0),
                                  (0, 1, -1)]  # consecutive vectors
            inner_ring_nodes = []
            for inner_ring_vector in inner_ring_vectors:
                # add each vector to the node
                # print(node, inner_ring_vector)
                consecutive_node = [
                    a_i + b_i for a_i, b_i in zip(node, inner_ring_vector)]
                # print(consecutive_node)
                # add it to the list

                inner_ring_nodes.append(tuple(consecutive_node))

            return inner_ring_nodes

        def find_consecutive_nodes(node, graph):
            # if consecutive_nodes are in the node list, then add them to list of edges that need to be joined together
            edge_list = []  # list of edges that need to be joined

            inner_ring_nodes = consecutive_positions(node)  # list of positions consecutive to the nodes
            # print(inner_ring_nodes)
            # if consecutive nodes are in the list of nodes in the graph
            for inner_ring_node in inner_ring_nodes:
                if inner_ring_node in graph.nodes:
                    edge_list.append(inner_ring_node)  #
                # else:
                #     print(f'the node, {inner_ring_node} was not added as it is not in the {graph}')

            return edge_list

        def add_edges(edge_list, graph, node):
            # Add edges from edge list to the graph
            for edge in edge_list:
                graph.add_edge(node, edge)
            # nx.draw_spring(graph, with_labels=True)
            return graph

        I = nx.Graph()  # make graph

        def make_network(row, col, graph):
            # Join all the functions together

            # create coordinates
            node_list = node_generation(row, col)

            # add nodes to list
            add_nodes(node_list, graph)

            for node in graph.nodes:
                # for each node
                edge_list = find_consecutive_nodes(node,
                                                   graph)  # find the set of nodes that are consecutive and in the graph
                add_edges(edge_list, graph, node)

            return graph

        return make_network(rows, columns, I)

    def set_network(self):
        """
        Sets the network of points (in networkx) for which the robots can move around in
        """
        self.movement_network = self.generate_network(self.rows, self.columns)

    def get_animal_robot_class(self):
        """
        :returns the class of the animal robot (where there is only one animal robot)
        """
        for robot in self.robot_list:
            if robot.is_animal_robot == 'AR':
                return robot
            # else:
            #     print('ERROR: There is no animal robot in the maze')
            #     logging.error('ERROR: there is no animal robot in the maze')

    def get_non_animal_robot_class(self):
        """
        :return class of the robots in the robot list that are the non animal robot:
        """
        for robot in self.robot_list:
            if robot.is_animal_robot == 'NAR':
                return robot

    def get_non_non_animal_robot_class(self):
        """
        :return class of the robots in the robot list that are the non-non animal robot:
        """
        for robot in self.robot_list:
            if robot.is_animal_robot == 'NNAR':
                return robot

    def check_animal_at_goal(self):
        """Check if the animal position is at the position of the goal robot"""
        if self.get_animal_robot_class() == self.goal:
            return True
        elif self.get_animal_robot_class() != self.goal:
            return False

    def get_inner_ring_coordinates(self, position_vector):
        """
        Returns a list of all the consecutive positions around a particular position vector
        ------
        :param position_vector: the position vector that for which the inner ring will be found
        """
        inner_ring = [[1, 0, -1], [1, -1, 0], [0, -1, 1], [-1, 0, 1], [-1, 1, 0], [0, 1, -1]]
        consecutive_coordinate_list = []
        print(f' position vector', position_vector)
        logging.info(f' position vector', position_vector)
        x, y, z = list(position_vector)
        for i in range(len(inner_ring)):
            change_x = inner_ring[i][0]
            change_y = inner_ring[i][1]
            change_z = inner_ring[i][2]

            consecutive_coordinate_list.append([x + change_x, y + change_y, z + change_z])

        return consecutive_coordinate_list

    def get_outer_ring_coordinates(self, position_vector):
        """
        :returns outer_ring_coordinates: list of all the positions that are in the outer ring (ring of radius 2)
        list of all the positions that are in the outer ring (ring of radius 2)
        around a particular coordinate
        """
        outer_ring = [[2, 0, -2], [2, -1, -1],
                      [2, -2, 0], [1, -2, 1],
                      [0, -2, 2], [-1, -1, 2],
                      [-2, 0, 2], [-2, 1, 1],
                      [-2, 2, 0], [-1, 2, -1],
                      [0, 2, -2], [1, 1, -2]]
        outer_ring_coordinates = []
        x, y, z = position_vector
        for i in range(len(outer_ring)):
            change_x = outer_ring[i][0]
            change_y = outer_ring[i][1]
            change_z = outer_ring[i][2]

            outer_ring_coordinates.append([x + change_x, y + change_y, z + change_z])

        return outer_ring_coordinates

    def get_consecutive_positions(self, moving_robot_class):
        """
        From the robot positions, select the positions and consecutive positions of the non-moving robots
        from the network
        and
        returns a
        ------
        :param moving_robot_class: The class of the robot not moving
        :return formatted_consecutive_position_list: list of tuples that are consecutive to the robots in the network
        """
        # Non-moving robots position list
        robot_position_list = []
        for robot in self.robot_list:
            if robot != moving_robot_class:
                robot_position_list.append(robot.position_vector)
            else:
                pass

        # Non-moving robot position list
        consecutive_position_list = []
        for robot_position in robot_position_list:
            consecutive_coordinate_list = self.get_inner_ring_coordinates(robot_position)
            for c in consecutive_coordinate_list:
                consecutive_position_list.append(c)
        consecutive_position_list.sort()

        # define formatting functions
        def remove_duplicates(coordinate_list):
            new_coordinate_list = []
            for elem in coordinate_list:
                if elem not in new_coordinate_list:
                    new_coordinate_list.append(elem)
            return new_coordinate_list

        def list_to_tuples(coordinate_list):
            new_coordinate_list = []
            for c in coordinate_list:
                new_coordinate_list.append(tuple(c))
            return new_coordinate_list

        # run the formatting functions
        formatted_consecutive_position_list = remove_duplicates(consecutive_position_list)
        formatted_consecutive_position_list = list_to_tuples(formatted_consecutive_position_list)

        return formatted_consecutive_position_list

    def set_consecutive_positions(self, moving_robot_class):
        self.consecutive_positions = self.get_consecutive_positions(moving_robot_class)

    def make_temp_movement_network(self, moving_robot_class):
        """
        Generate the network that the robots will have to traverse
        """

        def remove_consecutive_positions(temp_movement_network, consecutive_positions):
            """Remove the positions that are consecutive to the robots and update self.temp_movement_network"""
            print('No of nodes of temp network', len(temp_movement_network.nodes))
            print(len(consecutive_positions))
            for position in consecutive_positions:
                if position in list(temp_movement_network.nodes):
                    temp_movement_network.remove_node(position)
                else:
                    print('ERROR: A node that is not in the network is trying to be removed')
            print('The positions consecutive to any other robot have been removed from the temp_movement_network')
            logging.info(
                'The positions consecutive to any other robot have been removed from the temp_movement_network')
            print('No of nodes of temp network', len(temp_movement_network.nodes))
            return temp_movement_network

        def add_edge_to_outer_ring(self, temp_movement_network):
            # get the corresponding move with no rotation to outer ring of network
            if moving_robot_class.is_animal_robot() == 'NNAR':
                # NAR if robot is NNAR
                stationary_robot = self.get_non_animal_robot_class()
            elif moving_robot_class.is_animal_robot() == 'NAR':
                # AR if robot is NAR
                stationary_robot = self.get_non_non_animal_robot_class()

            legal_position = moving_robot_class.move_to_robot_outer_ring(stationary_robot)
            temp_movement_network.add_edge(tuple(moving_robot_class.position_vector), legal_position)
            return temp_movement_network

        # Make temp movement network (this resets every time the function is called]
        self.temp_movement_network = self.movement_network.copy()
        # get consecutive positions of the robots that are not the moving robot class
        consecutive_positions = self.get_consecutive_positions(moving_robot_class)
        # remove consecutive positions from the temp_network
        temp_movement_network = remove_consecutive_positions(self.temp_movement_network, consecutive_positions)

        # add source and target
        # temp_movement_network = add_edge_to_outer_ring(self, temp_movement_network)

        return temp_movement_network

    def make_circular_movement_network(self, moving_robot_class):
        """
        Pathfinding function for circular robot platforms not hexagonal platforms
        ---
        :param moving_robot_class: the class of the robot that is going to move in the next move
        :return temp_movement_network: The movement network that is required for the pathfinding of the
        """
        # make copy of movement network
        self.temp_movement_network = self.movement_network.copy()
        # get inner ring positions of stationary robots
        consecutive_positions = self.get_consecutive_positions(moving_robot_class)
        # add positions of non-moving robot classes

        # make list of edges between nodes in (inner ring + AR.position_vector) then remove duplicates)

        # remove these edges from the network

        # find the shortest path
        pass

    def pathfinder(self, moving_robot_class):
        """
        Get the list of movements from the pathfinding start to the pathfinding end (using dijkstra pathfinding
        algorithm

        Parameters
        ----------
        :param moving_robot_class: the robot that is just about to move
        :return shortest_path: A list of tuples that is the shortest path between the pathfinding target and source
        """
        print(moving_robot_class.name)
        logging.debug(moving_robot_class.name)

        # getting the pathfinding target and start
        source = moving_robot_class.position_vector
        target = moving_robot_class.pathfinding_target_position

        temp_movement_network = self.make_temp_movement_network(moving_robot_class)

        logging.debug('\nPathfinding Source:', tuple(source), '\nPathfinding Target:', tuple(target))
        print('\nPathfinding Source:', tuple(source), '\nPathfinding Target:', tuple(target))

        return nx.shortest_path(temp_movement_network, source=tuple(source), target=tuple(target))

    def get_target_positions(self, sample_size=2):

        # get two target positions from the outer ring of the animal robot that are not occupied by other robots

        # for each robot's position vector, find the path length to each target position

        # the shortest path

        """
                Get a target position vector which is valid in the following ways:
                1. It must not be the current position of a robot
                2. It must be in the outer ring and a valid relative position
                3. It must not be in the current pathfinding target position of the other non animal robot
                """
        animal_robot = self.get_animal_robot_class()
        choices = self.get_inner_ring_coordinates(animal_robot.position_vector)
        # 1. It must not be the current position of a robot
        # remove positions of the animal coordinates
        for robot in self.robot_list:
            # remove the position of the robots from the 'choices' list
            if robot.position_vector in choices:
                choices.remove(robot.position_vector)
            else:
                print('INFO: Robot position vector not inside choice of target positions')
                logging.info('INFO: Robot position vector not inside choice of target positions')

            # remove the position of the other robot's target position

            if robot.target_position != None:
                if list(robot.target_position) in choices:
                    choices.remove(list(robot.target_position))
                else:
                    print(
                        f"INFO: The robot,{robot.name}'s target position was not in the list of choices. It was {robot.target_position}")

        print(choices)

        # make a list of tuples of length 'sample_size'
        sample_list = random.sample(choices, sample_size)

        def make_list_of_tuples(sample_list):
            tuple_list = []
            for position in sample_list:
                tuple_list.append(tuple(position))
            return tuple_list

        tuple_list = make_list_of_tuples(sample_list)

        # robot list without animal class created
        robot_list = self.robot_list.copy()
        robot_list.remove(animal_robot)
        print(robot_list)

        # length dictionary
        length_dict = {}
        length_list = []
        index = 0
        # for each robot:
        for robot in robot_list:
            # find the length of path to all targets
            for target_position in tuple_list:
                path_length = len(nx.shortest_path(self.make_temp_movement_network(robot), tuple(robot.position_vector),
                                                   target_position))
                # add to dictionary
                # length_dict[path_length] = target_position

                # add to list
                length_list[index].append(path_length)

            index += 1

        print(length_list)


def main():
    pass


if __name__ == '__main__':
    main()
