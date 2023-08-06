"""Animal Class"""
from random import choice


class Animal:
    def __init__(self, maze, *name):
        # Functions to set up the animal
        self.set_maze(maze)
        # self.set_animal_position()
        # Identifying the animal
        self.name = name
        self.position_vector = None
        # maze the animal is in
        self.maze = None
        # path that animal takes through maze
        self.animal_path = []  # this is a path of position vectors
        self.animal_choices = []

    def set_animal_position(self):
        """Get the position of the robot class with the animal in it"""
        print('animal position vector', self.maze.get_animal_robot_class().position_vector)
        self.position_vector = self.maze.get_animal_robot_class().position_vector

    def set_maze(self, maze):
        """Assigns the name for the animal object and the maze object to eachother"""
        self.maze = maze
        self.maze.add_animal(self)

    def make_random_movement_choice(self):
        """Makes random choice of platform to move to
        ---
        :return class of the selected robot platform:
        """
        robot_list = self.maze.robot_list.copy()  # create copy of robot list
        animal_robot_class = self.maze.get_animal_robot_class()

        robot_list.remove(animal_robot_class)  # remove the class of the robot on which the animal is on

        animal_choice = choice(robot_list)  # choose a platform for the robot to move to.

        self.animal_path.append(animal_choice.position_vector)  # append choice animal makes to list to keep track
        return animal_choice  # return position vector of the robot chosen

    def make_user_choice(self):
        """
        User can make choice of which platform the animal moves to.
        :return: User choice of platform for animal
        """
        robot_list = self.maze.robot_list.copy()  # create copy of robot list
        animal_robot_class = self.maze.get_animal_robot_class() # get the glass of the animal robot

        robot_list.remove(animal_robot_class)  # remove the class of the robot on which the animal is on
        # list of robots' names
        robot_name_list = []
        for robot in robot_list:
            robot_name_list.append(robot.name)

        # if self.check_robot_choices(robot_list) == False:
            # continue the rest of the code as if there is no duplicate choice
        while True:
            try:
                user_input = int(input(f'Which robot would you like to choose from the following list? \n{robot_name_list}'))
                break

            except ValueError:
                print('Invalid Input. Try entering a number.')

        # make sure the robot list
        selected_robot = robot_list[user_input - 1]
        self.animal_path.append(selected_robot.position_vector)

        return selected_robot

        # else:
        #     # reallocate potential choices for the animal to move to
        #     pass
    def record_robot_choices(self, robot_choice_list):
        """Add the choice that has been given to a list for records"""
        # get the position vectors of the robots that are a choice for the animal
        robot_position_vector_list = []
        for robot in robot_choice_list:
            robot_position_vector_list.append(robot.position_vector)
        # record it to a list
        self.animal_choices.append(robot_position_vector_list.sort()) # added sorted list

    def check_robot_choices(self, robot_choice_list):
        """
        Check if the choice the animal is presented with has already been given.
        :return True: this choice has already been given,
        False if this choice has not already been given.
        """
        # get the position vectors of the robots that are a choice for the animal
        robot_position_vector_list = []
        for robot in robot_choice_list:
            robot_position_vector_list.append(robot.position_vector)
        # ordered the list
        robot_position_vector_list.sort()
        # check if this list of position vectors are already the choices that have been presented to it
        for animal_choice in self.animal_choices:
            if animal_choice == robot_position_vector_list:
                return True
            elif animal_choice != robot_position_vector_list:
                return False


    def change_animal_class(self, new_animal_class):
        """
        Based on choice of the new_anima_class,
        the change the class of the animal robot and non-animal robot are changed
        ------
        :parameter new_animal_class: This must be a robot in the maze
        """

        # change class for robot list
        for robot in self.maze.robot_list:
            if robot.is_animal_robot == 'AR' and new_animal_class == robot:
                robot.is_animal_robot = 'AR'
            elif robot.is_animal_robot == 'AR' and new_animal_class != robot:
                robot.is_animal_robot = 'NAR'

            elif robot.is_animal_robot == 'NAR' and new_animal_class == robot:
                robot.is_animal_robot = 'AR'
            elif robot.is_animal_robot == 'NAR' and new_animal_class != robot:
                robot.is_animal_robot = 'NNAR'

            elif robot.is_animal_robot == 'NNAR' and new_animal_class == robot:
                robot.is_animal_robot = 'AR'
            elif robot.is_animal_robot == 'NNAR' and new_animal_class != robot:
                robot.is_animal_robot = 'NNAR'

    def output_animal_path(self, show_output=True):
        """
        Saves a file of the path the animal took through the maze.
        Default value for this will be the output be True so their will be an output
        """

        if show_output == True:
            with open(f'logs/animal_path_{self.name}.txt', 'w') as file:
                for path in self.animal_path:
                    file.write(str(path)) # path
                    file.write()
                    file.write('\n')
            file.close()
