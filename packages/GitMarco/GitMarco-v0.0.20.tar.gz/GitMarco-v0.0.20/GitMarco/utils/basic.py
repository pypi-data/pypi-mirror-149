def assertion_test(x, dtype, name: str = ''):
    assert isinstance(x, dtype), \
        f'Wrong data type for {name}. Required : {dtype} - Actual: {type(x)}'


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_fancy(txt: str,
                c=bcolors.HEADER):
    print(f'{c}{txt}{bcolors.ENDC}')


def clear():
    """
    :return: None

    Cleara python console with a system call
    """
    import os
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)
