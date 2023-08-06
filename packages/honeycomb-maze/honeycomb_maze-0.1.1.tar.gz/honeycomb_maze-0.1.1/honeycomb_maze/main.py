# imports
from animal import *
from maze import *
from robot import *
from static_methods import *

# Start Logging
logging.basicConfig(filename='logs/maze.log', encoding='utf-8')

# INSTANTIATE OBJECTS
# Instantiate maze
hm = HexagonMaze(column_number=13, row_number=15)
# Instantiate robots
execute = False
robot1 = PlatformRobot(3, 5, -8, 3, '192.168.0.101', execute, 'robot1')
robot2 = PlatformRobot(2, 5, -7, 1, '192.168.0.103', execute, 'robot2')
robot3 = PlatformRobot(3, 4, -7, 4, '192.168.0.106', execute, 'robot3')

# robot4 = PlatformRobot(0, 0, 0, 0, '192.168.0.101', False, 'Robot4')

# Instantiate animal with its maze
mouse = Animal(hm, 'mouse')

# Set the maze (and add robots to maze class)
robot1.set_maze(hm)
robot2.set_maze(hm)
robot3.set_maze(hm)

mouse.set_maze(hm)
# Set initial animal robot - this should be automated
robot1.set_animal_robot(True)


def functional_main(execute=True, manual=False):
    hm.get_status()
    print('MOUSE CHOICE')
    # changes which animal is the correct animal class
    animal_choice_class = mouse.make_user_choice()  # animal makes choice
    print('Robot Selected:', animal_choice_class.name)
    # print(hm.get_animal_robot_class() == animal_choice_class)
    mouse.change_animal_class(animal_choice_class)  # animal moves to its choice

    hm.get_status()

    # set the animal position
    mouse.set_animal_position()  # change the position of the animal based on its movement

    hm.get_status()
    pause()

    # method for setting the target and pathfinding target

    print('GET THE CLASSES OF THE NON ANIMAL ROBOTS')
    nnar = hm.get_non_non_animal_robot_class()
    nar = hm.get_non_animal_robot_class()
    # print(nnar.name)
    # SETTING PATHFINDING TARGETS
    nnar.set_pathfinding_target_position(
        manual)  # pathfinding position must not be the pathfinding position of the other robot.
    print('\n\nnnar target position', nnar.target_position)

    nar.set_pathfinding_target_position(manual)
    print('\n\nnar target position', nar.target_position)

    hm.get_status()
    pause()

    print('NNAR step back from NAR')
    # NNAR step back from NAR
    nnar.step_back_from_NAR(execute)

    pause()
    # pathfinding method
    nnar.set_command_list()
    # tell robot to execute command
    nnar.execute_command_list(execute)

    hm.get_status()
    pause()

    print('NAR moves to outer ring of AR')
    # NAR moves to outer ring of AR
    # print('start', nar.position_vector)
    # print(hm.get_animal_robot_class())
    print(nar.move_to_animal_outer_ring())  # move the animal to the outer ring
    # print('end', nar.position_vector)
    # print(nar.pathfinding_target_position)
    nar.set_command_list()
    # print(nar.command_list)
    # robot executes command
    nar.execute_command_list(execute)

    hm.get_status()
    pause()

    # BOTH ARE IN THE OUTER RING IN CORRECT RELATIVE POSITION
    print('BOTH MOVE TO INNER RING')
    nar.move_to_inner_ring_animal()
    nnar.move_to_inner_ring_animal()

    nar.execute_command_list(execute)
    nnar.execute_command_list(execute)
    # EXECUTE COMMAND

    hm.get_status()
    pause()

    # nar_command_list =

    # hm.get_status()
    pass

    # print(mouse.animal_path)  # return the path of the animal


def test():
    robot2.is_animal_robot = 'NAR'
    robot3.is_animal_robot = 'NNAR'
    hm.get_status()

    robot3.step_back_from_NAR(True)

    hm.get_status()
    pass


def test_2():
    # robot1.ssh_connect(True, '192.168.0.101')
    print(robot1.position_vector)
    print(robot1.direction)
    command = robot1.make_command_list(
        [(3, 4, -7), (4, 5, -9), (5, 4, -9), (5, 3, -9), (5, 2, -7), (4, 2, -6), (3, 2, -5), (2, 3, -5)

         # (2,5,-7), (3, 5, -8), (2,6,-8), (3, 5, -8)
         ]
        )
    command_string = ' '.join(map(str, command))
    print(command_string)
    # robot1.execute_command(command_string)
    print(robot1.position_vector)
    print(robot1.direction)
    pass


def test_3():
    print(robot4.position_vector)
    robot4.change_position('y', -1)
    print(robot4.position_vector)

    pass


def run_program(run_no):
    run = 1
    while run <= run_no:
        print(f"START OF RUN {run}")
        functional_main()
        print(f"END OF RUN {run}")
        run = run + 1


if __name__ == '__main__':
    # run_program(1)
    # test()
    test_2()
    # test_3()
    pass
