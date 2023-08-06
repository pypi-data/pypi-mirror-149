# imports
from honeycomb_maze.animal import *
from honeycomb_maze.maze import *
from honeycomb_maze.robot import *

# Start Logging
logging.basicConfig(filename='../logs/maze.log', encoding='utf-8')

# INSTANTIATE OBJECTS
# Instantiate maze
hm = HexagonMaze(column_number=13, row_number=15)
# Instantiate robots
execute = False
robot1 = PlatformRobot(0,0,0, 2, '192.168.0.101', execute, 'robot1')
robot2 = PlatformRobot(2, 5, -7, 1, '192.168.0.103', execute, 'robot2')
robot3 = PlatformRobot(3, 4, -7, 1, '192.168.0.106', execute, 'robot3')

# Instantiate animal with its maze
mouse = Animal(hm, 'mouse')

# Set the maze (and add robots to maze class)
robot1.set_maze(hm)
robot2.set_maze(hm)
robot3.set_maze(hm)

# Set initial animal robot - this should be automated
robot1.set_animal_robot(True)

mouse.set_maze(hm)


def main():
    # robot1.ssh_connect(True, '192.168.0.101')
    robot1.coordinate_callibration([0, 0, 0])

    # robot1.execute_command('1 1')
    # robot2.is_animal_robot = 'NAR'
    # print(robot1.direction)
    # robot1.step_back_from_NAR(True)
    # print(robot1.direction)
    pass


if __name__ == "__main__":
    main()
