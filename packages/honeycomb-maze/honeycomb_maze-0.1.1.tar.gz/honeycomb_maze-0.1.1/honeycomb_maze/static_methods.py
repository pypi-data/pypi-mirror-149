"""
Static Methods which are used in multiple places in the program
"""

def pause(bool = True):
    """
    Function to pause the code
    :param bool: True = will pause, False = Will not be used. Default value set to True
    :return: Will pause the code
    """
    if bool:
        pause = input('Would you like to continue?')
    else:
        pass

def flatten(t):
    """
    Remove that brackets from a list of lists
    :param t: list to be inputed
    :return flattened list:
    """
    return [item for sublist in t for item in sublist]


def common_elements(list1, list2):
    """
    Get the common elements from two lists
    :param list1:
    :param list2:
    :return result: the common elements from the two lists
    """
    result = []
    for element in list1:
        if element in list2:
            result.append(element)
    return result